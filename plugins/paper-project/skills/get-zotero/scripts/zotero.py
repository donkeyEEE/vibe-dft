#!/usr/bin/env python3
"""Read Zotero Desktop data through a portable local API client."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

from attachment_paths import AttachmentPathError, resolve_attachment_path
from runtime_config import (
    ConfigError,
    Endpoint,
    RuntimeConfig,
    candidate_endpoints,
    config_path,
    load_runtime_config,
    wsl_default_gateway,
)


LOCAL_USER = "/api/users/0"
API_VERSION_HEADERS = {"Zotero-API-Version": "3"}
CONNECTOR_HEADERS = {"X-Zotero-Connector-API-Version": "3"}
TEXT_LIMIT = 300
API_PAGE_LIMIT = 100


@dataclass(frozen=True)
class Response:
    status: int | None
    headers: dict[str, str]
    text: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300

    @property
    def content_type(self) -> str:
        return self.headers.get("Content-Type", "")


class ZoteroConnectionError(ConnectionError):
    """Raised when none of the permitted Zotero endpoints is reachable."""


class ZoteroClient:
    """GET-only client for the Zotero Desktop local API."""

    def __init__(
        self,
        config: RuntimeConfig,
        endpoints: Sequence[Endpoint],
        opener: Callable[..., Any] = urllib.request.urlopen,
        gateway_error: str | None = None,
    ) -> None:
        self.config = config
        self.endpoints = tuple(endpoints)
        self.opener = opener
        self.gateway_error = gateway_error
        self.selected_endpoint: Endpoint | None = None

    def _request_at(
        self, endpoint: Endpoint, path: str, timeout: float | None = None
    ) -> Response:
        headers = {
            "Host": endpoint.host_header,
            "Zotero-API-Version": "3",
        }
        try:
            request = urllib.request.Request(
                endpoint.url.rstrip("/") + path,
                method="GET",
                headers=headers,
            )
            with self.opener(
                request,
                timeout=self.config.timeout_seconds if timeout is None else timeout,
            ) as response:
                return Response(
                    status=response.status,
                    headers=dict(response.headers.items()),
                    text=response.read().decode("utf-8", errors="replace"),
                )
        except urllib.error.HTTPError as error:
            return Response(
                status=error.code,
                headers=dict(error.headers.items()),
                text=error.read().decode("utf-8", errors="replace"),
                error=str(error),
            )
        except Exception as error:
            return Response(status=None, headers={}, text="", error=str(error))

    def select_endpoint(self) -> Endpoint:
        if self.selected_endpoint is not None:
            return self.selected_endpoint
        attempts: list[Response] = []
        for endpoint in self.endpoints:
            response = self._request_at(endpoint, "/api/")
            attempts.append(response)
            if response.ok:
                self.selected_endpoint = endpoint
                return endpoint
        target = "explicit host" if self.config.host else "automatic Zotero endpoints"
        detail = attempts[-1].error if attempts else "no candidate endpoints"
        raise ZoteroConnectionError(f"Could not reach {target}: {detail}")

    def request(self, path: str, timeout: float | None = None) -> Response:
        endpoint = self.select_endpoint()
        return self._request_at(endpoint, path, timeout)

    def selected_target(self) -> Response:
        """Read the Zotero UI selection through its non-mutating Connector route."""
        endpoint = self.select_endpoint()
        headers = {
            "Host": endpoint.host_header,
            "Content-Type": "application/json",
            **CONNECTOR_HEADERS,
        }
        try:
            request = urllib.request.Request(
                endpoint.url.rstrip("/") + "/connector/getSelectedCollection",
                data=b"{}",
                method="POST",
                headers=headers,
            )
            with self.opener(
                request, timeout=self.config.timeout_seconds
            ) as response:
                return Response(
                    status=response.status,
                    headers=dict(response.headers.items()),
                    text=response.read().decode("utf-8", errors="replace"),
                )
        except Exception as error:
            return Response(status=None, headers={}, text="", error=str(error))


def dump_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=False))


def exit_with(message: str) -> None:
    raise SystemExit(message)


def parse_body(response: Response) -> Any:
    if "json" not in response.content_type.lower():
        return response.text
    try:
        return json.loads(response.text or "null")
    except json.JSONDecodeError:
        return response.text


def require_ok(response: Response, action: str) -> Response:
    if response.ok:
        return response
    detail = response.error or response.text[:TEXT_LIMIT] or "no response body"
    exit_with(f"{action} failed: status={response.status} detail={detail}")
    raise AssertionError("unreachable")


def api_response(client: ZoteroClient, path: str) -> Response:
    api_path = path if path.startswith("/api") else "/api" + path
    return require_ok(client.request(api_path), f"GET {api_path}")


def api_get(client: ZoteroClient, path: str) -> Any:
    return parse_body(api_response(client, path))


def runtime_endpoints(
    config: RuntimeConfig,
    gateway_loader: Callable[[], str] = wsl_default_gateway,
) -> tuple[tuple[Endpoint, ...], str | None]:
    gateway = None
    gateway_error = None
    if config.mode == "wsl" and not config.host:
        try:
            gateway = gateway_loader()
        except ConfigError as error:
            gateway_error = str(error)
    return candidate_endpoints(config, gateway), gateway_error


def query(params: dict[str, str | int | bool | None]) -> str:
    clean = {key: value for key, value in params.items() if value is not None}
    return urllib.parse.urlencode(clean)


def creators_from_item(data: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for creator in data.get("creators", []) or []:
        name = creator.get("name") or " ".join(
            part for part in [creator.get("firstName"), creator.get("lastName")] if part
        )
        if name:
            names.append(name)
    return names


def year_from_date(raw: str | None) -> str | None:
    if not raw:
        return None
    match = re.search(r"(\d{4})", raw)
    return match.group(1) if match else None


def summarize_item(item: dict[str, Any]) -> dict[str, Any]:
    data = item.get("data", item)
    return {
        "key": item.get("key") or data.get("key"),
        "itemType": data.get("itemType"),
        "title": data.get("title"),
        "creators": creators_from_item(data),
        "year": year_from_date(data.get("date")),
    }


def artifact_metadata(item: dict[str, Any]) -> dict[str, Any]:
    """Return stable bibliographic metadata for the content artifact contract."""
    data = item.get("data", item)
    return {
        "title": data.get("title"),
        "authors": creators_from_item(data),
        "year": year_from_date(data.get("date")),
        "publication": data.get("publicationTitle"),
        "doi": data.get("DOI"),
        "url": data.get("url"),
        "abstract": data.get("abstractNote"),
        "collections": list(data.get("collections") or []),
    }


def _pdf_attachment(children: list[dict[str, Any]]) -> dict[str, Any] | None:
    for child in children:
        data = child.get("data", child)
        if (
            data.get("itemType") == "attachment"
            and data.get("contentType") == "application/pdf"
        ):
            return child
    return None


def _artifact_manifest(
    item_key: str, metadata: dict[str, Any], content: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "item_key": item_key,
        "metadata": metadata,
        "content": content,
    }


def build_content_artifact(
    client: ZoteroClient, item_key: str, mode: str, out_dir: Path
) -> dict[str, Any]:
    """Fetch one parent item and expose its content as a file artifact."""
    if mode not in {"auto", "indexed-text", "pdf"}:
        raise ValueError(f"Unsupported content mode: {mode}")

    quoted_item_key = urllib.parse.quote(item_key)
    item = api_get(client, f"{LOCAL_USER}/items/{quoted_item_key}")
    metadata = artifact_metadata(item)
    children = api_get(client, f"{LOCAL_USER}/items/{quoted_item_key}/children")
    attachment = _pdf_attachment(children if isinstance(children, list) else [])
    if attachment is None:
        if mode != "auto":
            return _artifact_manifest(
                item_key,
                metadata,
                {
                    "kind": "error",
                    "code": "pdf-attachment-not-found",
                    "next_step": (
                        "Attach a local PDF in Zotero or request auto mode for "
                        "metadata-only evidence."
                    ),
                },
            )
        return _artifact_manifest(
            item_key,
            metadata,
            {"kind": "metadata-only", "source": "metadata-abstract-only"},
        )

    attachment_data = attachment.get("data", attachment)
    attachment_key = attachment.get("key") or attachment_data.get("key")
    if not attachment_key:
        return _artifact_manifest(
            item_key,
            metadata,
            {
                "kind": "error",
                "code": "attachment-key-missing",
                "next_step": "Select a PDF attachment with a valid Zotero key.",
            },
        )
    quoted_attachment_key = urllib.parse.quote(str(attachment_key))

    if mode in {"auto", "indexed-text"}:
        response = client.request(
            f"{LOCAL_USER}/items/{quoted_attachment_key}/fulltext"
        )
        if response.ok:
            fulltext = parse_body(response)
            content = fulltext.get("content", "") if isinstance(fulltext, dict) else ""
            if content:
                out_dir = out_dir.expanduser().resolve()
                out_dir.mkdir(parents=True, exist_ok=True)
                path = out_dir / f"{attachment_key}.txt"
                path.write_text(content, encoding="utf-8")
                return _artifact_manifest(
                    item_key,
                    metadata,
                    {
                        "kind": "text-file",
                        "path": str(path),
                        "source": "zotero-indexed-fulltext",
                        "attachment_key": attachment_key,
                        "indexed_pages": fulltext.get("indexedPages"),
                        "total_pages": fulltext.get("totalPages"),
                    },
                )
        if mode == "indexed-text":
            return _artifact_manifest(
                item_key,
                metadata,
                {
                    "kind": "error",
                    "code": "indexed-text-unavailable",
                    "attachment_key": attachment_key,
                    "next_step": "Request PDF mode or use metadata-only evidence.",
                },
            )

    response = client.request(
        f"{LOCAL_USER}/items/{quoted_attachment_key}/file/view/url"
    )
    if response.ok:
        try:
            raw = parse_body(response)
            resolved = resolve_attachment_path(
                str(raw), client.config.mode, client.config.path_mappings
            )
            return _artifact_manifest(
                item_key,
                metadata,
                {
                    "kind": "pdf-file",
                    "path": str(resolved.path.resolve()),
                    "source": "local-pdf",
                    "attachment_key": attachment_key,
                },
            )
        except AttachmentPathError as error:
            detail = str(error)
    else:
        detail = response.error or f"HTTP {response.status}"
    return _artifact_manifest(
        item_key,
        metadata,
        {
            "kind": "error",
            "code": "pdf-unavailable",
            "attachment_key": attachment_key,
            "next_step": detail,
        },
    )


def summarize_collection(collection: dict[str, Any]) -> dict[str, Any]:
    data = collection.get("data", collection)
    return {
        "key": collection.get("key") or data.get("key"),
        "name": data.get("name"),
        "parentCollection": data.get("parentCollection"),
        "version": collection.get("version"),
    }


def summarize_tag(tag: dict[str, Any]) -> dict[str, Any]:
    return {"tag": tag.get("tag"), "numItems": (tag.get("meta") or {}).get("numItems")}


def summarize_group(group: dict[str, Any]) -> dict[str, Any]:
    data = group.get("data", group)
    return {
        "id": group.get("id") or data.get("id"),
        "name": data.get("name"),
        "type": data.get("type"),
    }


def print_items(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        creators = ", ".join(row.get("creators") or [])
        print(
            f"{row.get('key') or '':10} "
            f"{row.get('itemType') or '':14} "
            f"{row.get('year') or '':4} "
            f"{row.get('title') or ''} | {creators}"
        )


def extract_bibtex_keys(text: str) -> list[str]:
    return re.findall(r"@\w+\s*\{\s*([^,\s]+)", text)


def count_bibtex_entries(text: str) -> int:
    return len(extract_bibtex_keys(text))


def total_results(response: Response) -> int | None:
    raw = response.headers.get("Total-Results")
    return int(raw) if raw and raw.isdigit() else None


def export_bibtex(
    client: ZoteroClient,
    item_key: str | None = None,
    *,
    include_children: bool = False,
) -> str:
    if item_key:
        params = query({"itemKey": item_key, "format": "bibtex", "limit": API_PAGE_LIMIT})
        return api_response(client, f"{LOCAL_USER}/items?{params}").text

    endpoint = "items" if include_children else "items/top"
    start = 0
    chunks: list[str] = []
    while True:
        params = query(
            {
                "format": "bibtex",
                "sort": "title",
                "direction": "asc",
                "limit": API_PAGE_LIMIT,
                "start": start,
            }
        )
        response = api_response(client, f"{LOCAL_USER}/{endpoint}?{params}")
        if response.text.strip():
            chunks.append(response.text.strip())

        total = total_results(response)
        start += API_PAGE_LIMIT
        if total is not None and start >= total:
            break
        if total is None and count_bibtex_entries(response.text) < API_PAGE_LIMIT:
            break

    text = "\n\n".join(chunks)
    return text + "\n" if text else ""


def write_text_output(text: str, out: str | None) -> None:
    if out is None:
        print(text, end="" if text.endswith("\n") else "\n")
        return

    path = Path(out).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    dump_json(
        {
            "path": str(path),
            "bytes": len(text.encode("utf-8")),
            "bibtex_entries": count_bibtex_entries(text),
        }
    )


def find_item(
    client: ZoteroClient, *, item_key: str | None, query_text: str | None
) -> dict[str, Any]:
    if item_key:
        return api_get(client, f"{LOCAL_USER}/items/{urllib.parse.quote(item_key)}")
    if not query_text:
        exit_with("Provide --item-key or --query")

    params = query({"q": query_text})
    matches = api_get(client, f"{LOCAL_USER}/items/top?{params}")
    if not matches:
        exit_with(f"No top-level Zotero items matched query: {query_text}")
    if len(matches) > 1:
        print(
            f"warning: {len(matches)} matches; using first result {matches[0].get('key')}",
            file=sys.stderr,
        )
    return matches[0]


def doctor_payload(
    config: RuntimeConfig,
    endpoints: Sequence[Endpoint],
    client: ZoteroClient,
    *,
    config_exists: bool,
) -> dict[str, Any]:
    try:
        selected = client.select_endpoint()
        root = client.request("/api/")
        api = {
            "running": root.ok,
            "status": root.status,
            "error_code": None if root.ok else "local-api-unavailable",
            "next_step": None
            if root.ok
            else "Enable the local API in the Zotero interface, then run doctor again.",
            "zotero_version": root.headers.get("X-Zotero-Version"),
            "api_version": root.headers.get("Zotero-API-Version"),
            "selected_endpoint_source": selected.source,
        }
    except ZoteroConnectionError:
        explicit = config.host is not None
        gateway_failed = client.gateway_error is not None
        api = {
            "running": False,
            "status": None,
            "error_code": "explicit-host-unreachable"
            if explicit
            else "wsl-gateway-unavailable"
            if gateway_failed
            else "zotero-unreachable",
            "next_step": "Check the configured host and port, then run doctor again."
            if explicit
            else "Provide the current Windows host address, then run doctor again."
            if gateway_failed
            else "Start Zotero and enable its local API in the Zotero interface.",
            "zotero_version": None,
            "api_version": None,
            "selected_endpoint_source": None,
        }
    return {
        "platform": platform.system(),
        "config_exists": config_exists,
        "runtime": {
            key: {"value": getattr(config, key), "source": config.sources[key]}
            for key in ("mode", "host", "port", "timeout_seconds")
        },
        "candidate_sources": [endpoint.source for endpoint in endpoints],
        "api": api,
    }


def cmd_doctor(args: argparse.Namespace, client: ZoteroClient) -> None:
    payload = doctor_payload(
        client.config,
        client.endpoints,
        client,
        config_exists=args.config_exists,
    )
    if args.json:
        dump_json(payload)
        return
    print(f"Mode: {payload['runtime']['mode']['value']}")
    print(f"Config file present: {payload['config_exists']}")
    print(f"API running: {payload['api']['running']} status={payload['api']['status']}")
    if payload["api"]["next_step"]:
        print(f"Next step: {payload['api']['next_step']}")


def cmd_probe(args: argparse.Namespace, client: ZoteroClient) -> None:
    endpoints = [
        ("root", "/api/"),
        ("schema", "/api/schema"),
        ("itemTypes", "/api/itemTypes"),
        ("itemFields", "/api/itemFields"),
        ("creatorFields", "/api/creatorFields"),
        ("collections", f"{LOCAL_USER}/collections"),
        ("topCollections", f"{LOCAL_USER}/collections/top"),
        ("topItems", f"{LOCAL_USER}/items/top"),
        ("tags", f"{LOCAL_USER}/tags"),
        ("searches", f"{LOCAL_USER}/searches"),
        ("groups", f"{LOCAL_USER}/groups"),
        ("fulltextVersions", f"{LOCAL_USER}/fulltext?since=0"),
    ]
    rows: list[dict[str, Any]] = []
    for label, path in endpoints:
        response = client.request(path)
        parsed = parse_body(response)
        if isinstance(parsed, list):
            summary: Any = {"type": "array", "len": len(parsed)}
        elif isinstance(parsed, dict):
            summary = {"type": "object", "keys": list(parsed)[:8]}
        else:
            summary = str(parsed)[:160]
        rows.append(
            {
                "label": label,
                "path": path,
                "status": response.status,
                "content_type": response.content_type,
                "total": response.headers.get("Total-Results"),
                "summary": summary,
            }
        )

    if args.json:
        dump_json(rows)
        return
    for row in rows:
        print(
            f"{row['status'] or 'ERR':>3} {row['label']:18} {row['path']:45} total={row['total']} {row['summary']}"
        )


def cmd_inventory(args: argparse.Namespace, client: ZoteroClient) -> None:
    endpoint = "items" if args.include_children else "items/top"
    if args.collection_key:
        collection_key = urllib.parse.quote(args.collection_key, safe="")
        endpoint = f"collections/{collection_key}/{endpoint}"
    params = query({"sort": "title", "direction": "asc"})
    rows = [summarize_item(item) for item in api_get(client, f"{LOCAL_USER}/{endpoint}?{params}")]
    dump_json(rows) if args.json else print_items(rows)


def cmd_collections(args: argparse.Namespace, client: ZoteroClient) -> None:
    rows = [summarize_collection(collection) for collection in api_get(client, f"{LOCAL_USER}/collections")]
    if args.json:
        dump_json(rows)
        return
    for row in rows:
        parent = f" parent={row['parentCollection']}" if row.get("parentCollection") else ""
        print(f"{row.get('key') or '':10} {row.get('name') or ''}{parent}")


def cmd_tags(args: argparse.Namespace, client: ZoteroClient) -> None:
    rows = [summarize_tag(tag) for tag in api_get(client, f"{LOCAL_USER}/tags")]
    if args.json:
        dump_json(rows)
        return
    for row in rows:
        print(f"{row.get('tag') or ''} ({row.get('numItems') or 0})")


def cmd_groups(args: argparse.Namespace, client: ZoteroClient) -> None:
    rows = [summarize_group(group) for group in api_get(client, f"{LOCAL_USER}/groups")]
    if args.json:
        dump_json(rows)
        return
    for row in rows:
        print(f"{row.get('id') or '':>10} {row.get('type') or '':12} {row.get('name') or ''}")


def cmd_search(args: argparse.Namespace, client: ZoteroClient) -> None:
    params = query({"q": args.query})
    rows = [summarize_item(item) for item in api_get(client, f"{LOCAL_USER}/items/top?{params}")]
    if args.with_bibtex_keys:
        for row in rows:
            bibtex = export_bibtex(client, row.get("key")) if row.get("key") else ""
            keys = extract_bibtex_keys(bibtex)
            row["bibtexKey"] = keys[0] if keys else None
    dump_json(rows) if args.json else print_items(rows)


def cmd_export_bibtex(args: argparse.Namespace, client: ZoteroClient) -> None:
    write_text_output(
        export_bibtex(client, args.item_key, include_children=args.include_children), args.out
    )


def cmd_citations(args: argparse.Namespace, client: ZoteroClient) -> None:
    params = query({"include": "data,citation", "style": args.style})
    rows: list[dict[str, Any]] = []
    for item in api_get(client, f"{LOCAL_USER}/items/top?{params}"):
        row = summarize_item(item)
        row["citation"] = item.get("citation")
        rows.append(row)
    if args.json:
        dump_json(rows)
        return
    for row in rows:
        print(f"{row.get('key')} {row.get('citation')}")


def cmd_children(args: argparse.Namespace, client: ZoteroClient) -> None:
    data = api_get(client, f"{LOCAL_USER}/items/{urllib.parse.quote(args.item_key)}/children")
    rows = [summarize_item(item) for item in data]
    dump_json(rows) if args.json else print_items(rows)


def cmd_fulltext(args: argparse.Namespace, client: ZoteroClient) -> None:
    data = api_get(client, f"{LOCAL_USER}/items/{urllib.parse.quote(args.attachment_key)}/fulltext")
    content = data.get("content", "") if isinstance(data, dict) else str(data)
    if args.out is None:
        print(content)
        return
    path = Path(args.out).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    dump_json(
        {
            "path": str(path),
            "chars": len(content),
            "indexedPages": data.get("indexedPages") if isinstance(data, dict) else None,
            "totalPages": data.get("totalPages") if isinstance(data, dict) else None,
        }
    )


def cmd_file_url(args: argparse.Namespace, client: ZoteroClient) -> None:
    raw = api_get(client, f"{LOCAL_USER}/items/{urllib.parse.quote(args.attachment_key)}/file/view/url")
    if args.resolve:
        resolved = resolve_attachment_path(
            str(raw), client.config.mode, client.config.path_mappings
        )
        print(resolved.path)
    else:
        print(raw)


def cmd_selected_target(args: argparse.Namespace, client: ZoteroClient) -> None:
    response = require_ok(
        client.selected_target(), "Read selected Zotero library/collection"
    )
    payload = parse_body(response)
    print(json.dumps(payload, indent=2) if args.json else payload)


def cmd_content(args: argparse.Namespace, client: ZoteroClient) -> None:
    dump_json(
        build_content_artifact(
            client,
            args.item_key,
            args.content_mode,
            Path(args.out_dir),
        )
    )


def add_json_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--json", action="store_true", help="Print JSON instead of a compact text summary"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read Zotero Desktop through its local API."
    )
    parser.add_argument("--mode", choices=("auto", "native", "wsl"))
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    parser.add_argument("--timeout-seconds", type=float)
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor = subcommands.add_parser("doctor", help="Diagnose read-only Zotero access")
    add_json_flag(doctor)
    doctor.set_defaults(func=cmd_doctor)

    status = subcommands.add_parser("status", help="Compatibility alias for doctor")
    add_json_flag(status)
    status.set_defaults(func=cmd_doctor)

    probe = subcommands.add_parser("probe", help="Probe common safe local API routes")
    add_json_flag(probe)
    probe.set_defaults(func=cmd_probe)

    inventory = subcommands.add_parser("inventory", help="List Zotero items")
    inventory.add_argument(
        "--include-children", action="store_true", help="Include child notes and attachments"
    )
    inventory.add_argument(
        "--collection-key",
        help="List items in one user-selected Zotero collection",
    )
    inventory.add_argument(
        "--all", action="store_true", dest="include_children", help=argparse.SUPPRESS
    )
    add_json_flag(inventory)
    inventory.set_defaults(func=cmd_inventory)

    collections = subcommands.add_parser("collections", help="List collections")
    add_json_flag(collections)
    collections.set_defaults(func=cmd_collections)

    tags = subcommands.add_parser("tags", help="List tags")
    add_json_flag(tags)
    tags.set_defaults(func=cmd_tags)

    groups = subcommands.add_parser("groups", help="List synced group libraries visible locally")
    add_json_flag(groups)
    groups.set_defaults(func=cmd_groups)

    search = subcommands.add_parser("search", help="Search top-level Zotero items")
    search.add_argument("query")
    search.add_argument("--with-bibtex-keys", action="store_true")
    add_json_flag(search)
    search.set_defaults(func=cmd_search)

    export = subcommands.add_parser("export-bibtex", help="Export Zotero items as BibTeX")
    export.add_argument("--item-key")
    export.add_argument("--include-children", action="store_true")
    export.add_argument(
        "--all", action="store_true", dest="include_children", help=argparse.SUPPRESS
    )
    export.add_argument("--out")
    export.set_defaults(func=cmd_export_bibtex)

    citations = subcommands.add_parser("citations", help="Render formatted citations")
    citations.add_argument("--style", default="apa")
    add_json_flag(citations)
    citations.set_defaults(func=cmd_citations)

    children = subcommands.add_parser("children", help="List child notes/attachments for an item")
    children.add_argument("item_key")
    add_json_flag(children)
    children.set_defaults(func=cmd_children)

    fulltext = subcommands.add_parser(
        "fulltext", help="Print or save indexed full text for an attachment"
    )
    fulltext.add_argument("attachment_key")
    fulltext.add_argument("--out")
    fulltext.set_defaults(func=cmd_fulltext)

    file_url = subcommands.add_parser(
        "file-url", help="Print Zotero's local file URL for an attachment"
    )
    file_url.add_argument("attachment_key")
    file_url.add_argument(
        "--resolve", action="store_true", help="Resolve and verify the local platform path"
    )
    file_url.set_defaults(func=cmd_file_url)

    selected = subcommands.add_parser(
        "selected-target", help="Show the currently selected Zotero library/collection"
    )
    add_json_flag(selected)
    selected.set_defaults(func=cmd_selected_target)

    content = subcommands.add_parser(
        "content", help="Expose metadata, indexed text, or a PDF as a content artifact"
    )
    content.add_argument("item_key")
    content.add_argument(
        "--mode",
        dest="content_mode",
        choices=("auto", "indexed-text", "pdf"),
        default="auto",
    )
    content.add_argument("--out-dir", required=True)
    content.set_defaults(func=cmd_content)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    system = platform.system()
    release = platform.release()
    try:
        proc_version = Path("/proc/version").read_text(encoding="utf-8", errors="replace")
    except OSError:
        proc_version = ""
    cli = {
        "mode": args.mode,
        "host": args.host,
        "port": args.port,
        "timeout_seconds": args.timeout_seconds,
    }
    try:
        config = load_runtime_config(
            cli, os.environ, system, release, proc_version, Path.home()
        )
        endpoints, gateway_error = runtime_endpoints(config)
        args.config_exists = config_path(system, os.environ, Path.home()).exists()
        args.func(
            args,
            ZoteroClient(config, endpoints, gateway_error=gateway_error),
        )
    except (ConfigError, ZoteroConnectionError) as error:
        exit_with(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
