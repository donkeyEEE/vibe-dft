"""Fixed, reviewable local API write plans. Codex grants are shared outside project data."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
import urllib.error
import urllib.parse
import urllib.request
from copy import deepcopy
from pathlib import Path
from typing import Any

import write_auth

KEY = re.compile(r"^[23456789ABCDEFGHIJKLMNPQRSTUVWXYZ]{8}$")
RESOURCES = {"items", "collections", "searches"}
ACTIONS = {"update", "create", "trash", "delete", "upload", "fulltext"}


class WriteError(ValueError):
    pass


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode()
    ).hexdigest()


def key(value: str) -> str:
    if not isinstance(value, str) or not KEY.fullmatch(value):
        raise WriteError(f"Invalid Zotero object key: {value!r}")
    return value


def generated_key() -> str:
    return "".join(
        secrets.choice("23456789ABCDEFGHIJKLMNPQRSTUVWXYZ") for _ in range(8)
    )


class LocalWrites:
    def __init__(self, client):
        self.client = client
        self.endpoint = client.select_endpoint()
        root = client.request("/api/")
        server = next(
            (v for k, v in root.headers.items() if k.lower() == "zotero-server-id"),
            None,
        )
        if not root.ok or not server:
            raise WriteError(
                "Local writes require Zotero 10+ with Zotero-Server-ID; read access remains available."
            )
        self.server: str = str(server)
        self.api_key = write_auth.load(self.server, self.endpoint.url)
        self.remember = bool(self.api_key)
        self.last_write_version = None

    def request(self, method, path, data=None, headers=None, *, timeout=None):
        raw = (
            data
            if isinstance(data, bytes)
            else (json.dumps(data).encode() if data is not None else None)
        )
        request = urllib.request.Request(
            self.endpoint.url.rstrip("/") + path,
            data=raw,
            method=method,
            headers={
                "Host": self.endpoint.host_header,
                "Zotero-API-Version": "3",
                "Zotero-Server-ID": self.server,
                "Content-Type": "application/json",
                **(headers or {}),
            },
        )
        try:
            with self.client.opener(
                request, timeout=timeout or self.client.config.timeout_seconds
            ) as response:
                body = response.read().decode("utf-8", errors="replace")
                try:
                    body = json.loads(body) if body else None
                except json.JSONDecodeError:
                    pass
                return response.status, dict(response.headers.items()), body
        except urllib.error.HTTPError as error:
            # Do not echo request headers or authorization response bodies.
            error_text = error.read().decode("utf-8", errors="replace")
            return error.code, dict(error.headers.items()), error_text[:500]
        except (OSError, TimeoutError) as error:
            raise WriteError(
                "Transport failure; outcome may be unknown. Reconcile before retrying."
            ) from error

    def get(self, path, *, missing=False):
        status, headers, body = self.request("GET", path)
        if status == 404 and missing:
            return None, headers
        if status != 200:
            raise WriteError(f"GET {path}: HTTP {status}")
        return body, headers

    def authorize(self):
        status, _, body = self.request(
            "POST", "/api/local/authorize", {"appName": "Codex"}, timeout=300
        )
        if status != 200 or not isinstance(body, dict) or not body.get("key"):
            raise WriteError(
                f"Zotero write authorization not granted (HTTP {status}); no automatic prompt loop."
            )
        self.api_key = body["key"]
        self.remember = bool(body.get("remember"))
        if self.remember:
            write_auth.save(self.server, self.endpoint.url, self.api_key)

    def write(self, method, path, data=None, headers=None):
        if not self.api_key:
            self.authorize()
        result = self.request(
            method, path, data, {**(headers or {}), "Zotero-API-Key": self.api_key}
        )
        if result[0] == 401:
            write_auth.forget(self.server)
            self.api_key = None
            self.authorize()
            result = self.request(
                method, path, data, {**(headers or {}), "Zotero-API-Key": self.api_key}
            )
        if not self.remember:
            self.api_key = None
        if 200 <= result[0] < 300:
            self.last_write_version = next(
                (
                    v
                    for k, v in result[1].items()
                    if k.lower() == "last-modified-version"
                ),
                None,
            )
        return result


def object_data(obj):
    return deepcopy(obj.get("data", obj))


def version(obj):
    return obj.get("version", obj.get("data", {}).get("version"))


def library_path(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"/api/(users/0|groups/[1-9][0-9]*)", value
    ):
        raise WriteError("library must be /api/users/0 or /api/groups/<numeric-id>")
    return value


def select_targets(api, library, selection):
    """Resolve selection exactly once. Only top-level items enter batch changes."""
    if set(selection) - {"item_keys", "collection_key", "query", "recursive"}:
        raise WriteError("Unknown selection property")
    modes = [
        name for name in ("item_keys", "collection_key", "query") if name in selection
    ]
    if len(modes) != 1:
        raise WriteError(
            "Choose exactly one selection: item_keys, collection_key, query"
        )
    if modes[0] == "item_keys":
        return list(dict.fromkeys(key(k) for k in selection["item_keys"]))
    if selection.get("recursive") and modes[0] != "collection_key":
        raise WriteError("recursive requires collection_key")
    if modes[0] == "query":
        rows, _ = api.get(
            library + "/items/top?" + urllib.parse.urlencode({"q": selection["query"]})
        )
    else:
        collections = [key(selection["collection_key"])]
        if selection.get("recursive"):
            all_collections, _ = api.get(library + "/collections")
            for parent in collections:
                for row in all_collections:
                    data = object_data(row)
                    if (
                        data.get("parentCollection") == parent
                        and data["key"] not in collections
                    ):
                        collections.append(data["key"])
        rows = []
        for collection in collections:
            members, _ = api.get(library + "/collections/" + collection + "/items/top")
            rows.extend(members)
    return list(
        dict.fromkeys(key(row.get("key") or row["data"]["key"]) for row in rows)
    )


def changed_values(before, operation):
    changes = deepcopy(operation.get("set", {}))
    if not isinstance(changes, dict) or set(changes) & {
        "key",
        "version",
        "dateAdded",
        "dateModified",
        "md5",
        "mtime",
    }:
        raise WriteError(
            "set must contain editable fields, not object identity or timestamps"
        )
    for field, add, remove in [
        ("tags", "add_tags", "remove_tags"),
        ("collections", "add_collections", "remove_collections"),
    ]:
        if add not in operation and remove not in operation:
            continue
        if field in changes:
            raise WriteError(f"Use either set.{field} or {add}/{remove}")
        removed = operation.get(remove, [])
        values = deepcopy(before.get(field, []))
        if field == "tags":
            values = [v for v in values if v["tag"] not in removed]
            for tag in operation.get(add, []):
                if not isinstance(tag, str) or not tag:
                    raise WriteError("Tags must be nonempty strings")
                if tag not in [v["tag"] for v in values]:
                    values.append({"tag": tag})
        else:
            removed = [key(v) for v in removed]
            values = [v for v in values if v not in removed]
            for collection in operation.get(add, []):
                if key(collection) not in values:
                    values.append(collection)
        changes[field] = values
    return changes


def item_template(api, item_type, link_mode=None):
    params = {"itemType": item_type}
    if link_mode:
        params["linkMode"] = link_mode
    template, _ = api.get(
        "/api/items/new?" + urllib.parse.urlencode(params), missing=True
    )
    if template is not None:
        return template
    fields, _ = api.get(
        "/api/itemTypeFields?" + urllib.parse.urlencode({"itemType": item_type})
    )
    template = {
        "itemType": item_type,
        "tags": [],
        "relations": {},
        **{f["field"]: "" for f in fields},
    }
    if item_type in {"note", "attachment"}:
        template.update(note="", parentItem=False)
    else:
        template.update(creators=[], collections=[])
    if item_type == "attachment":
        template.update(
            linkMode=link_mode or "imported_file",
            contentType="",
            charset="",
            filename="",
        )
    return template


def prepare(api, request):
    library = library_path(request.get("library", "/api/users/0"))
    operations = deepcopy(request.get("operations", []))
    if request.get("selection"):
        template = request.get("change", {})
        if template.get("resource", "items") != "items" or template.get(
            "action"
        ) not in {"update", "trash"}:
            raise WriteError(
                "Batch selection supports item update/trash; list other operations explicitly"
            )
        operations.extend(
            {**template, "resource": "items", "key": k}
            for k in select_targets(api, library, request["selection"])
        )
    if not operations:
        raise WriteError("No operations selected")
    prepared = []
    targets = set()
    for op in operations:
        action, resource = op.get("action"), op.get("resource", "items")
        if action not in ACTIONS or resource not in RESOURCES:
            raise WriteError("Unsupported action/resource")
        if action in {"trash", "upload", "fulltext"} and resource != "items":
            raise WriteError(f"{action} requires items")
        object_key = (
            key(op.get("key") or generated_key())
            if action == "create"
            else key(op.get("key"))
        )
        path = f"{library}/{resource}/{object_key}"
        if path in targets:
            raise WriteError(
                "One operation per object per plan; prepare a new plan after each step"
            )
        targets.add(path)
        obj, _ = api.get(path, missing=action == "create")
        before = object_data(obj) if obj else None
        if action == "create" and obj:
            raise WriteError("Creation key already exists")
        entry = {
            "action": action,
            "resource": resource,
            "key": object_key,
            "before": before,
            "version": version(obj) if obj else None,
            "evidence": op.get("evidence"),
            "destructive": action in {"trash", "delete", "upload"}
            or bool(op.get("set", {}).get("deleted")),
        }
        if obj and entry["version"] is None:
            raise WriteError("Object version missing")
        if action == "create":
            after = deepcopy(op.get("data", {}))
            if not isinstance(after, dict) or set(after) & {"key", "version"}:
                raise WriteError("Creation data must exclude key/version")
            if resource == "items":
                item_type = after.get("itemType")
                template = item_template(api, item_type, after.get("linkMode"))
                after = {**template, **after}
            after["key"] = object_key
            entry["after"] = after
        elif action in {"update", "trash"}:
            assert before is not None
            changes = (
                {"deleted": 1} if action == "trash" else changed_values(before, op)
            )
            after = {**before, **changes}
            if changes.get("itemType", before.get("itemType")) != before.get(
                "itemType"
            ):
                template = item_template(api, changes["itemType"])
                allowed = set(template) | {
                    "key",
                    "version",
                    "dateAdded",
                    "dateModified",
                    "deleted",
                }
                lost = {
                    name: value
                    for name, value in after.items()
                    if name not in allowed and value not in ("", [], {}, None)
                }
                after = {
                    name: value for name, value in after.items() if name in allowed
                }
                entry["cleared_fields"] = lost
                entry["type_conversion"] = True
            entry["after"] = after
        elif action == "delete":
            entry["after"] = None
            entry["impact"] = (
                "Permanent removal of this object. Item children are also removed; collection descendants and memberships are removed, library items remain."
            )
            # Deletion can affect children/members. Freeze the whole library revision.
            _, headers = api.get(library + "/items?limit=1")
            entry["library_version"] = next(
                (v for k, v in headers.items() if k.lower() == "last-modified-version"),
                None,
            )
            if entry["library_version"] is None:
                raise WriteError(
                    "Cannot freeze deletion impact without library version"
                )
            if resource == "items":
                entry["affected"], _ = api.get(path + "/children")
            elif resource == "collections":
                entry["affected"], _ = api.get(path + "/items")
                entry["subcollections"], _ = api.get(library + "/collections")
        elif action == "fulltext":
            data = op.get("data", {})
            allowed = {
                "content",
                "indexedPages",
                "totalPages",
                "indexedChars",
                "totalChars",
            }
            if (
                not isinstance(data, dict)
                or set(data) - allowed
                or not isinstance(data.get("content"), str)
            ):
                raise WriteError(
                    "Full-text data requires content and supported count fields only; identity fields are forbidden"
                )
            if any(
                type(value) is not int or value < 0
                for name, value in data.items()
                if name != "content"
            ):
                raise WriteError("Full-text counts must be nonnegative integers")
            entry["after"] = deepcopy(data)
            entry["fulltext_before"], _ = api.get(path + "/fulltext", missing=True)
            _, headers = api.get(library + "/items?limit=1")
            entry["library_version"] = next(
                (v for k, v in headers.items() if k.lower() == "last-modified-version"),
                None,
            )
            if entry["library_version"] is None:
                raise WriteError("Full-text write requires library version")
        else:
            assert before is not None
            if before.get("itemType") != "attachment" or before.get("linkMode") not in {
                "imported_file",
                "imported_url",
            }:
                raise WriteError(
                    "Upload requires an existing stored-file attachment; create it first"
                )
            source = Path(op["file"]).expanduser().resolve(strict=True)
            if not source.is_file() or source.stat().st_size >= 4 * 1024**3:
                raise WriteError("File must be regular and under 4 GB")
            raw = source.read_bytes()
            entry["file"] = str(source)
            entry["file_sha256"] = hashlib.sha256(raw).hexdigest()
            entry["after"] = {
                "md5": hashlib.md5(raw).hexdigest(),
                "filename": source.name,
                "filesize": len(raw),
                "mtime": int(source.stat().st_mtime * 1000),
            }
        prepared.append(entry)
    result = {
        "schema_version": 1,
        "server_id": api.server,
        "library": library,
        "operations": prepared,
    }
    result["digest"] = digest(result)
    return result


def same_fields(actual, expected):
    return all(
        (
            actual.get(k) == v
            or (
                k not in actual and (v == "" or v is False or k == "deleted" and v == 0)
            )
        )
        for k, v in expected.items()
        if k not in {"key", "version", "dateAdded", "dateModified"}
    )


def upload(api, path, op):
    source = Path(op["file"])
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != op["file_sha256"]:
        raise WriteError("Upload source changed; new authorization required")
    old_md5 = op["before"].get("md5")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        **({"If-Match": old_md5} if old_md5 else {"If-None-Match": "*"}),
    }
    data = urllib.parse.urlencode(op["after"]).encode()
    status, _, body = api.write("POST", path + "/file", data, headers)
    if status != 200:
        raise WriteError(f"Upload registration HTTP {status}")
    if not body.get("exists"):
        url = urllib.parse.urlsplit(body["url"])
        expected = urllib.parse.urlsplit(api.endpoint.url)
        if (url.scheme, url.netloc) != (
            expected.scheme,
            expected.netloc,
        ) or not re.fullmatch(r"/api/local/uploads/[A-Za-z0-9]+", url.path):
            raise WriteError("Unexpected upload destination; refusing to send file")
        status, _, _ = api.request(
            "POST",
            url.path,
            raw,
            {"Content-Type": body.get("contentType", "application/octet-stream")},
        )
        if status != 201:
            raise WriteError(f"Upload bytes HTTP {status}")
        status, _, _ = api.write(
            "POST",
            path + "/file",
            urllib.parse.urlencode({"upload": body["uploadKey"]}).encode(),
            headers,
        )
        if status != 204:
            raise WriteError(f"Upload commit HTTP {status}")
    obj, _ = api.get(path)
    return object_data(obj).get("md5") == op["after"]["md5"]


def operation_delta(op):
    return {k: v for k, v in op["after"].items() if op["before"].get(k) != v}


def execute(api, plan, approval, destructive_approval=None):
    unsigned = {k: v for k, v in plan.items() if k != "digest"}
    if (
        plan.get("schema_version") != 1
        or digest(unsigned) != plan.get("digest")
        or approval != plan["digest"]
    ):
        raise WriteError(
            "Plan digest does not match approval; regenerate and obtain authorization"
        )
    if plan["server_id"] != api.server:
        raise WriteError("Zotero instance changed; new plan required")
    if (
        any(op["destructive"] for op in plan["operations"])
        and destructive_approval != plan["digest"]
    ):
        raise WriteError(
            "Deletion/file overwrite requires separate --approve-destructive <digest>"
        )
    library = library_path(plan["library"])
    results = []
    initial_library_version = None
    if any("library_version" in op for op in plan["operations"]):
        _, h = api.get(library + "/items?limit=1")
        initial_library_version = next(
            (v for k, v in h.items() if k.lower() == "last-modified-version"), None
        )
    current_library_version = initial_library_version
    api.last_write_version = None
    for op in plan["operations"]:
        path = f"{library}/{op['resource']}/{key(op['key'])}"
        result = {"key": op["key"], "action": op["action"]}
        body: Any
        try:
            obj, _ = api.get(path, missing=True)
            current = object_data(obj) if obj else None
            if op["action"] == "create" and obj:
                if same_fields(current, op["after"]):
                    result["status"] = "already-applied"
                else:
                    raise WriteError("Creation key exists with different data")
            elif op["action"] == "delete" and obj is None:
                result["status"] = "already-applied"
            elif (
                obj
                and op["action"] in {"update", "trash"}
                and same_fields(
                    current,
                    operation_delta(op),
                )
            ):
                result["status"] = "already-applied"
            else:
                if current != op["before"]:
                    # Unrelated changes may proceed only when target fields are unchanged.
                    target_fields = (
                        set(op.get("after") or {})
                        if op["action"] != "update"
                        else {
                            k
                            for k in set(op["before"]) | set(op["after"])
                            if op["before"].get(k) != op["after"].get(k)
                        }
                    )
                    if (
                        op["action"] != "update"
                        or op.get("type_conversion")
                        or not current
                        or any(
                            current.get(k) != op["before"].get(k) for k in target_fields
                        )
                    ):
                        raise WriteError(
                            "Target changed since preview; new authorization required"
                        )
                headers = (
                    {"If-Unmodified-Since-Version": str(version(obj))}
                    if obj
                    else {
                        "Zotero-Write-Token": digest(
                            {"plan": plan["digest"], "key": op["key"]}
                        )[:32]
                    }
                )
                action = op["action"]
                if action == "upload":
                    verified = upload(api, path, op)
                else:
                    if action == "create":
                        method, target, body = (
                            "POST",
                            f"{library}/{op['resource']}",
                            [{**op["after"], "version": 0}],
                        )
                    elif action == "delete":
                        _, h = api.get(library + "/items?limit=1")
                        revision = next(
                            (
                                v
                                for k, v in h.items()
                                if k.lower() == "last-modified-version"
                            ),
                            None,
                        )
                        if str(initial_library_version) != str(
                            op["library_version"]
                        ) or str(revision) != str(current_library_version):
                            raise WriteError(
                                "Deletion impact may have changed; new plan required"
                            )
                        headers = {
                            "If-Unmodified-Since-Version": str(current_library_version)
                        }
                        parameter = {
                            "items": "itemKey",
                            "collections": "collectionKey",
                            "searches": "searchKey",
                        }[op["resource"]]
                        method, target, body = (
                            "DELETE",
                            f"{library}/{op['resource']}?{parameter}={op['key']}",
                            None,
                        )
                    elif action == "fulltext":
                        existing, _ = api.get(path + "/fulltext", missing=True)
                        if existing != op["fulltext_before"]:
                            raise WriteError(
                                "Full-text index changed; new authorization required"
                            )
                        method, target, body = (
                            "POST",
                            library + "/fulltext",
                            [{**op["after"], "key": op["key"]}],
                        )
                        if str(initial_library_version) != str(op["library_version"]):
                            raise WriteError(
                                "Library changed since full-text preview; new plan required"
                            )
                        headers = {
                            "If-Unmodified-Since-Version": str(current_library_version)
                        }
                    elif op["resource"] != "items":
                        fields = operation_delta(op)
                        method, target, body = (
                            "POST",
                            f"{library}/{op['resource']}",
                            [{"key": op["key"], "version": version(obj), **fields}],
                        )
                        headers = {}
                    elif op.get("type_conversion"):
                        method, target, body = "PUT", path, op["after"]
                    else:
                        method, target, body = (
                            "PATCH",
                            path,
                            operation_delta(op),
                        )
                    status, _, response = api.write(method, target, body, headers)
                    if status not in {200, 201, 204}:
                        raise WriteError(
                            f'Write HTTP {status}: {response if isinstance(response, str) else "request rejected"}; no blind retries'
                        )
                    if isinstance(response, dict) and response.get("failed"):
                        failure = next(iter(response["failed"].values()))
                        raise WriteError(
                            f"API object failure {failure.get('code')}: {failure.get('message', 'write rejected')}"
                        )
                    if action == "fulltext":
                        readback, _ = api.get(path + "/fulltext")
                        verified = same_fields(readback, op["after"])
                    else:
                        readback, _ = api.get(path, missing=action == "delete")
                        expected = op["after"]
                        if action == "update" and not op.get("type_conversion"):
                            expected = operation_delta(op)
                        verified = (
                            readback is None
                            if action == "delete"
                            else readback is not None
                            and same_fields(object_data(readback), expected)
                        )
                result["status"] = "verified" if verified else "verification-failed"
        except (WriteError, OSError, KeyError, TypeError) as error:
            result.update(status="failed", message=str(error))
        if (
            result["status"] in {"verified", "verification-failed"}
            and api.last_write_version is not None
        ):
            current_library_version = api.last_write_version
        results.append(result)
    return {
        "schema_version": 1,
        "plan_digest": plan["digest"],
        "results": results,
        "ok": all(r["status"] in {"verified", "already-applied"} for r in results),
    }


def cmd_plan(args, client):
    plan = prepare(
        LocalWrites(client), json.loads(Path(args.request).read_text(encoding="utf-8"))
    )
    Path(args.out).write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(plan, indent=2, ensure_ascii=False))


def cmd_apply(args, client):
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    report = execute(LocalWrites(client), plan, args.approve, args.approve_destructive)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["ok"]:
        raise SystemExit(1)


def add_commands(subcommands):
    preview = subcommands.add_parser(
        "write-plan", help="Read-only preview of fixed, versioned writes"
    )
    preview.add_argument("request")
    preview.add_argument("--out", required=True)
    preview.set_defaults(func=cmd_plan)
    apply = subcommands.add_parser(
        "write-apply",
        help="Execute an explicitly authorized plan and verify each result",
    )
    apply.add_argument("plan")
    apply.add_argument("--approve", required=True)
    apply.add_argument("--approve-destructive")
    apply.set_defaults(func=cmd_apply)
