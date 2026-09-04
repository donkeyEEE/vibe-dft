import argparse
import json
from pathlib import Path
import sys

import pytest


SCRIPTS = (
    Path(__file__).resolve().parents[2] / "skills" / "zo2notes" / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

import zotero  # noqa: E402
from runtime_config import Endpoint, RuntimeConfig  # noqa: E402


def subcommand_names(parser: argparse.ArgumentParser) -> set[str]:
    action = next(
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    )
    return set(action.choices)


def test_command_surface_is_read_only() -> None:
    commands = subcommand_names(zotero.build_parser())
    assert {"enable", "disable", "restart", "import-bibtex", "import-ris"}.isdisjoint(
        commands
    )
    assert "doctor" in commands
    assert "selected-target" in commands


def test_global_connection_overrides_parse() -> None:
    args = zotero.build_parser().parse_args(
        [
            "--mode",
            "wsl",
            "--host",
            "192.0.2.10",
            "--port",
            "24000",
            "--timeout-seconds",
            "2.5",
            "doctor",
            "--json",
        ]
    )
    assert (args.mode, args.host, args.port, args.timeout_seconds) == (
        "wsl",
        "192.0.2.10",
        24000,
        2.5,
    )


def runtime(*, mode: str = "wsl", host: str | None = None) -> RuntimeConfig:
    return RuntimeConfig(
        mode=mode,
        host=host,
        port=24000,
        timeout_seconds=2.5,
        path_mappings=(),
        sources={
            "mode": "automatic",
            "host": "default",
            "port": "config",
            "timeout_seconds": "default",
        },
    )


class FakeHTTPResponse:
    def __init__(self, status: int = 200, body: bytes = b"{}") -> None:
        self.status = status
        self.headers = {
            "Content-Type": "application/json",
            "X-Zotero-Version": "8.0",
            "Zotero-API-Version": "3",
        }
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self) -> bytes:
        return self.body


def test_client_selects_first_healthy_endpoint_and_builds_required_headers() -> None:
    requests = []

    def opener(request, timeout):
        requests.append((request, timeout))
        if request.full_url.startswith("http://127.0.0.1"):
            raise OSError("loopback unavailable")
        return FakeHTTPResponse()

    endpoints = (
        Endpoint("http://127.0.0.1:24000", "127.0.0.1:24000", "automatic-loopback"),
        Endpoint("http://172.20.0.1:24000", "127.0.0.1:24000", "automatic-wsl-gateway"),
    )
    client = zotero.ZoteroClient(runtime(), endpoints, opener=opener)

    selected = client.select_endpoint()

    assert selected == endpoints[1]
    assert [request.full_url for request, _ in requests] == [
        "http://127.0.0.1:24000/api/",
        "http://172.20.0.1:24000/api/",
    ]
    assert requests[1][0].get_header("Host") == "127.0.0.1:24000"
    assert requests[1][0].get_header("Zotero-api-version") == "3"
    assert requests[1][0].method == "GET"
    assert requests[1][1] == 2.5


def test_explicit_host_failure_has_one_attempt() -> None:
    attempts = []

    def opener(request, timeout):
        attempts.append(request.full_url)
        raise OSError("unreachable")

    endpoint = Endpoint(
        "http://192.0.2.10:24000", "127.0.0.1:24000", "explicit-host"
    )
    client = zotero.ZoteroClient(runtime(host="192.0.2.10"), (endpoint,), opener=opener)

    with pytest.raises(zotero.ZoteroConnectionError, match="explicit host"):
        client.select_endpoint()
    assert attempts == ["http://192.0.2.10:24000/api/"]


def test_doctor_reports_sources_without_local_paths() -> None:
    endpoint = Endpoint(
        "http://127.0.0.1:24000", "127.0.0.1:24000", "automatic-loopback"
    )
    client = zotero.ZoteroClient(
        runtime(), (endpoint,), opener=lambda request, timeout: FakeHTTPResponse()
    )

    payload = zotero.doctor_payload(runtime(), (endpoint,), client, config_exists=False)

    assert payload["runtime"]["mode"] == {"value": "wsl", "source": "automatic"}
    assert payload["runtime"]["port"] == {"value": 24000, "source": "config"}
    assert payload["api"]["running"] is True
    serialized = json.dumps(payload)
    assert "/Users/" not in serialized
    assert r"C:\Users" not in serialized


def test_doctor_distinguishes_unreachable_api() -> None:
    endpoint = Endpoint(
        "http://192.0.2.10:24000", "127.0.0.1:24000", "explicit-host"
    )
    client = zotero.ZoteroClient(
        runtime(host="192.0.2.10"),
        (endpoint,),
        opener=lambda request, timeout: (_ for _ in ()).throw(OSError("offline")),
    )

    payload = zotero.doctor_payload(
        runtime(host="192.0.2.10"), (endpoint,), client, config_exists=True
    )

    assert payload["api"]["running"] is False
    assert payload["api"]["error_code"] == "explicit-host-unreachable"
    assert "configured host" in payload["api"]["next_step"]


def test_cite_still_writes_project_files_after_client_refactor(
    tmp_path: Path, capsys
) -> None:
    def opener(request, timeout):
        if request.full_url.endswith("/api/"):
            return FakeHTTPResponse()
        if "/items/ABCD1234" in request.full_url:
            return FakeHTTPResponse(
                body=b'{"key":"ABCD1234","data":{"title":"Example"}}'
            )
        if "format=bibtex" in request.full_url:
            return FakeHTTPResponse(
                body=b"@article{Example2026,\n  title={Example}\n}\n"
            )
        raise AssertionError(request.full_url)

    endpoint = Endpoint(
        "http://127.0.0.1:24000", "127.0.0.1:24000", "automatic-loopback"
    )
    client = zotero.ZoteroClient(runtime(), (endpoint,), opener=opener)
    manuscript = tmp_path / "paper.md"
    bibliography = tmp_path / "references.bib"
    args = argparse.Namespace(
        item_key="ABCD1234",
        query=None,
        bib=str(bibliography),
        tex=None,
        markdown=str(manuscript),
        marker=None,
    )

    zotero.cmd_cite(args, client)

    assert manuscript.read_text(encoding="utf-8") == "[@Example2026]\n"
    assert "@article{Example2026" in bibliography.read_text(encoding="utf-8")
    assert json.loads(capsys.readouterr().out)["inserted"] == "[@Example2026]"
