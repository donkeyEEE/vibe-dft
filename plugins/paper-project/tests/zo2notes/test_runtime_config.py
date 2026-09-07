from pathlib import Path, PureWindowsPath
import subprocess
import sys

import pytest


SCRIPTS = (
    Path(__file__).resolve().parents[2] / "skills" / "zo2notes" / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

from runtime_config import (  # noqa: E402
    ConfigError,
    RuntimeConfig,
    candidate_endpoints,
    config_path,
    default_gateway,
    is_wsl,
    load_runtime_config,
    wsl_default_gateway,
)


def test_is_wsl_uses_kernel_markers() -> None:
    assert is_wsl("Linux", "5.15.90.1-microsoft-standard-WSL2", "")
    assert is_wsl("Linux", "6.1.0", "Linux version Microsoft WSL2")
    assert not is_wsl("Linux", "6.8.0-generic", "Linux version 6.8")
    assert not is_wsl("Windows", "microsoft", "Microsoft")


def test_config_path_uses_platform_conventions(tmp_path: Path) -> None:
    windows = config_path(
        "Windows", {"APPDATA": r"C:\Users\Ada\AppData\Roaming"}, tmp_path
    )
    assert PureWindowsPath(str(windows)) == PureWindowsPath(
        r"C:\Users\Ada\AppData\Roaming\zo2notes\config.toml"
    )
    assert config_path("Linux", {}, tmp_path) == (
        tmp_path / ".config" / "zo2notes" / "config.toml"
    )


def test_windows_config_path_requires_appdata(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="APPDATA"):
        config_path("Windows", {}, tmp_path)


def test_precedence_is_cli_then_env_then_toml_then_default(tmp_path: Path) -> None:
    path = tmp_path / ".config" / "zo2notes" / "config.toml"
    path.parent.mkdir(parents=True)
    path.write_text(
        'version = 1\n[zotero]\nmode="native"\nhost="toml-host"\nport=24000\n',
        encoding="utf-8",
    )

    config = load_runtime_config(
        {"host": "cli-host", "port": None, "mode": None, "timeout_seconds": None},
        {"ZO2NOTES_ZOTERO_HOST": "env-host", "ZO2NOTES_ZOTERO_PORT": "25000"},
        "Linux",
        "6.8",
        "Linux",
        tmp_path,
    )

    assert (config.host, config.port, config.mode) == ("cli-host", 25000, "native")
    assert config.sources == {
        "mode": "config",
        "host": "cli",
        "port": "environment",
        "timeout_seconds": "default",
    }


def test_auto_mode_resolves_to_detected_environment(tmp_path: Path) -> None:
    config = load_runtime_config(
        {}, {}, "Linux", "5.15-microsoft-standard-WSL2", "", tmp_path
    )
    assert config.mode == "wsl"
    assert config.sources["mode"] == "automatic"


def test_invalid_configuration_fails_without_fallback(tmp_path: Path) -> None:
    invalid_cases = [
        ("not valid toml = [", "Invalid TOML"),
        ("version = 2\n", "version"),
        ('version = 1\n[zotero]\nmode = "remote"\n', "mode"),
        ("version = 1\n[zotero]\nport = true\n", "port"),
        ("version = 1\n[zotero]\nport = 0\n", "port"),
        ("version = 1\n[zotero]\ntimeout_seconds = 0\n", "timeout"),
        ("version = 1\n[unknown]\nvalue = 1\n", "Unknown"),
        ("version = 1\n[zotero]\nporrt = 1\n", "Unknown"),
        (
            'version = 1\n[[attachments.path_mappings]]\nwindows_prefix = "C:\\\\Papers"\n',
            "local_prefix",
        ),
    ]
    path = tmp_path / ".config" / "zo2notes" / "config.toml"
    path.parent.mkdir(parents=True)
    for content, message in invalid_cases:
        path.write_text(content, encoding="utf-8")
        with pytest.raises(ConfigError, match=message):
            load_runtime_config({}, {}, "Linux", "6.8", "Linux", tmp_path)


def runtime(*, mode: str, host: str | None, port: int = 23119) -> RuntimeConfig:
    return RuntimeConfig(
        mode=mode,
        host=host,
        port=port,
        timeout_seconds=5.0,
        path_mappings=(),
        sources={
            "mode": "test",
            "host": "test",
            "port": "test",
            "timeout_seconds": "test",
        },
    )


def test_wsl_candidates_try_loopback_then_gateway() -> None:
    endpoints = candidate_endpoints(runtime(mode="wsl", host=None), "172.20.0.1")
    assert [endpoint.url for endpoint in endpoints] == [
        "http://127.0.0.1:23119",
        "http://172.20.0.1:23119",
    ]
    assert [endpoint.source for endpoint in endpoints] == [
        "automatic-loopback",
        "automatic-wsl-gateway",
    ]


def test_explicit_host_has_no_fallback_and_uses_configured_port() -> None:
    endpoints = candidate_endpoints(
        runtime(mode="wsl", host="192.0.2.10", port=24000), "172.20.0.1"
    )
    assert [endpoint.url for endpoint in endpoints] == ["http://192.0.2.10:24000"]
    assert endpoints[0].host_header == "127.0.0.1:24000"
    assert endpoints[0].source == "explicit-host"


def test_native_mode_has_only_loopback_default() -> None:
    endpoints = candidate_endpoints(runtime(mode="native", host=None), "172.20.0.1")
    assert [endpoint.url for endpoint in endpoints] == ["http://127.0.0.1:23119"]


def test_default_gateway_rejects_unusable_routes() -> None:
    unusable_routes = [
        "",
        "default via 127.0.0.1 dev eth0",
        "default via 0.0.0.0 dev eth0",
        "default via 224.0.0.1 dev eth0",
        "default via not-an-ip dev eth0",
    ]
    for route_output in unusable_routes:
        with pytest.raises(ConfigError, match="gateway"):
            default_gateway(route_output)


def test_wsl_default_gateway_invokes_ip_without_shell() -> None:
    calls: list[tuple[object, object]] = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, "default via 172.19.0.1 dev eth0\n", "")

    assert wsl_default_gateway(run) == "172.19.0.1"
    assert calls == [
        (
            ["ip", "route"],
            {"check": True, "capture_output": True, "text": True},
        )
    ]
