#!/usr/bin/env python3
"""Resolve portable, user-overridable Zotero runtime settings."""

from __future__ import annotations

import ipaddress
import subprocess
import tomllib
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_PORT = 23119
DEFAULT_TIMEOUT_SECONDS = 5.0
VALID_MODES = {"auto", "native", "wsl"}
ENVIRONMENT_KEYS = {
    "mode": "GET_ZOTERO_MODE",
    "host": "GET_ZOTERO_HOST",
    "port": "GET_ZOTERO_PORT",
}


class ConfigError(ValueError):
    """Raised when get-zotero runtime settings are invalid or undiscoverable."""


@dataclass(frozen=True)
class PathMappingConfig:
    windows_prefix: str
    local_prefix: str


@dataclass(frozen=True)
class RuntimeConfig:
    mode: str
    host: str | None
    port: int
    timeout_seconds: float
    path_mappings: tuple[PathMappingConfig, ...]
    sources: dict[str, str]


@dataclass(frozen=True)
class Endpoint:
    url: str
    host_header: str
    source: str


def config_path(system: str, environ: Mapping[str, str], home: Path) -> Path:
    if system == "Windows":
        appdata = environ.get("APPDATA", "").strip()
        if not appdata:
            raise ConfigError("APPDATA is required to locate the Windows configuration")
        return Path(appdata) / "get-zotero" / "config.toml"
    return home / ".config" / "get-zotero" / "config.toml"


def is_wsl(system: str, release: str, proc_version: str) -> bool:
    if system != "Linux":
        return False
    markers = f"{release} {proc_version}".lower()
    return "microsoft" in markers or "wsl" in markers


def _load_document(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("rb") as stream:
            document = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"Invalid TOML configuration: {error}") from error
    if not isinstance(document, dict):
        raise ConfigError("Invalid TOML configuration root")
    return document


def _validate_document(document: dict[str, Any]) -> tuple[dict[str, Any], tuple[PathMappingConfig, ...]]:
    unknown_top = set(document) - {"version", "zotero", "attachments"}
    if unknown_top:
        raise ConfigError(f"Unknown top-level configuration keys: {sorted(unknown_top)}")
    if document and document.get("version") != 1:
        raise ConfigError("Configuration version must be 1")

    zotero = document.get("zotero", {})
    if not isinstance(zotero, dict):
        raise ConfigError("zotero must be a TOML table")
    unknown_zotero = set(zotero) - {"mode", "host", "port", "timeout_seconds"}
    if unknown_zotero:
        raise ConfigError(f"Unknown zotero configuration keys: {sorted(unknown_zotero)}")

    attachments = document.get("attachments", {})
    if not isinstance(attachments, dict):
        raise ConfigError("attachments must be a TOML table")
    unknown_attachments = set(attachments) - {"path_mappings"}
    if unknown_attachments:
        raise ConfigError(
            f"Unknown attachments configuration keys: {sorted(unknown_attachments)}"
        )
    raw_mappings = attachments.get("path_mappings", [])
    if not isinstance(raw_mappings, list):
        raise ConfigError("attachments.path_mappings must be an array of tables")
    mappings: list[PathMappingConfig] = []
    for index, raw_mapping in enumerate(raw_mappings):
        if not isinstance(raw_mapping, dict):
            raise ConfigError(f"path mapping {index} must be a table")
        unknown_mapping = set(raw_mapping) - {"windows_prefix", "local_prefix"}
        if unknown_mapping:
            raise ConfigError(f"Unknown path mapping keys: {sorted(unknown_mapping)}")
        for key in ("windows_prefix", "local_prefix"):
            if not isinstance(raw_mapping.get(key), str) or not raw_mapping[key].strip():
                raise ConfigError(f"path mapping {index} requires {key}")
        mappings.append(
            PathMappingConfig(
                windows_prefix=raw_mapping["windows_prefix"],
                local_prefix=raw_mapping["local_prefix"],
            )
        )
    return zotero, tuple(mappings)


def _select_value(
    name: str,
    cli: Mapping[str, object],
    environ: Mapping[str, str],
    configured: Mapping[str, Any],
    default: object,
) -> tuple[object, str]:
    if cli.get(name) is not None:
        return cli[name], "cli"
    env_key = ENVIRONMENT_KEYS.get(name)
    if env_key and env_key in environ:
        return environ[env_key], "environment"
    if name in configured:
        return configured[name], "config"
    return default, "default"


def _validated_mode(value: object) -> str:
    if not isinstance(value, str) or value not in VALID_MODES:
        raise ConfigError(f"zotero mode must be one of {sorted(VALID_MODES)}")
    return value


def _validated_host(value: object) -> str | None:
    if not isinstance(value, str):
        raise ConfigError("zotero host must be a string")
    return value.strip() or None


def _validated_port(value: object) -> int:
    if isinstance(value, bool):
        raise ConfigError("zotero port must be an integer from 1 to 65535")
    try:
        port = int(value)
    except (TypeError, ValueError) as error:
        raise ConfigError("zotero port must be an integer from 1 to 65535") from error
    if str(port) != str(value).strip() or not 1 <= port <= 65535:
        raise ConfigError("zotero port must be an integer from 1 to 65535")
    return port


def _validated_timeout(value: object) -> float:
    if isinstance(value, bool):
        raise ConfigError("zotero timeout_seconds must be positive")
    try:
        timeout = float(value)
    except (TypeError, ValueError) as error:
        raise ConfigError("zotero timeout_seconds must be positive") from error
    if timeout <= 0:
        raise ConfigError("zotero timeout_seconds must be positive")
    return timeout


def load_runtime_config(
    cli: Mapping[str, object],
    environ: Mapping[str, str],
    system: str,
    release: str,
    proc_version: str,
    home: Path,
) -> RuntimeConfig:
    path = config_path(system, environ, home)
    configured, mappings = _validate_document(_load_document(path))

    raw_mode, mode_source = _select_value("mode", cli, environ, configured, "auto")
    raw_host, host_source = _select_value("host", cli, environ, configured, "")
    raw_port, port_source = _select_value("port", cli, environ, configured, DEFAULT_PORT)
    raw_timeout, timeout_source = _select_value(
        "timeout_seconds", cli, environ, configured, DEFAULT_TIMEOUT_SECONDS
    )

    mode = _validated_mode(raw_mode)
    if mode == "auto":
        mode = "wsl" if is_wsl(system, release, proc_version) else "native"
        mode_source = "automatic"

    return RuntimeConfig(
        mode=mode,
        host=_validated_host(raw_host),
        port=_validated_port(raw_port),
        timeout_seconds=_validated_timeout(raw_timeout),
        path_mappings=mappings,
        sources={
            "mode": mode_source,
            "host": host_source,
            "port": port_source,
            "timeout_seconds": timeout_source,
        },
    )


def default_gateway(route_output: str) -> str:
    for line in route_output.splitlines():
        fields = line.split()
        if len(fields) < 3 or fields[:2] != ["default", "via"]:
            continue
        try:
            gateway = ipaddress.IPv4Address(fields[2])
        except ipaddress.AddressValueError:
            continue
        if gateway.is_loopback or gateway.is_unspecified or gateway.is_multicast:
            continue
        return str(gateway)
    raise ConfigError("No usable WSL IPv4 default gateway was found")


def wsl_default_gateway(
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> str:
    try:
        completed = run(
            ["ip", "route"], check=True, capture_output=True, text=True
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise ConfigError(f"Could not inspect the WSL gateway: {error}") from error
    return default_gateway(completed.stdout)


def candidate_endpoints(
    config: RuntimeConfig, gateway: str | None
) -> tuple[Endpoint, ...]:
    host_header = f"127.0.0.1:{config.port}"
    if config.host:
        hosts = [(config.host, "explicit-host")]
    elif config.mode == "wsl":
        hosts = [("127.0.0.1", "automatic-loopback")]
        if gateway and gateway != "127.0.0.1":
            hosts.append((gateway, "automatic-wsl-gateway"))
    else:
        hosts = [("127.0.0.1", "automatic-loopback")]
    return tuple(
        Endpoint(
            url=f"http://{host}:{config.port}",
            host_header=host_header,
            source=source,
        )
        for host, source in hosts
    )
