"""Read-only Zotero Desktop Windows-to-WSL bridge used by Zo2Notes."""

from __future__ import annotations

import ipaddress
import json
import subprocess
from typing import Any
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


ZOTERO_PORT = 23119
ZOTERO_API_PREFIX = "/api"


def default_gateway(route_output: str) -> str:
    """Return the non-loopback IPv4 address from an ``ip route`` default route."""
    for line in route_output.splitlines():
        fields = line.split()
        if len(fields) < 3 or fields[0] != "default" or fields[1] != "via":
            continue
        try:
            gateway = ipaddress.IPv4Address(fields[2])
        except ipaddress.AddressValueError:
            continue
        if gateway.is_loopback or gateway.is_unspecified or gateway.is_multicast:
            continue
        return str(gateway)
    raise ValueError("no usable IPv4 default gateway found")


def wsl_default_gateway() -> str:
    """Read the current WSL default gateway without invoking a shell."""
    completed = subprocess.run(
        ["ip", "route"],
        check=True,
        capture_output=True,
        text=True,
    )
    return default_gateway(completed.stdout)


def bridge_headers() -> dict[str, str]:
    """Return exactly the headers required by the restricted Zotero bridge."""
    return {
        "Host": "127.0.0.1:23119",
        "Zotero-API-Version": "3",
    }


def build_request_url(gateway: str, path: str) -> str:
    """Build a URL confined to the local Zotero API namespace."""
    try:
        address = ipaddress.IPv4Address(gateway)
    except ipaddress.AddressValueError as error:
        raise ValueError("gateway must be an IPv4 address") from error
    if address.is_loopback or address.is_unspecified or address.is_multicast:
        raise ValueError("gateway must not be a loopback, unspecified, or multicast address")

    parsed = urlsplit(path)
    decoded_path = unquote(parsed.path)
    if (
        not path.startswith("/")
        or parsed.scheme
        or parsed.netloc
        or parsed.fragment
        or parsed.path.startswith(f"{ZOTERO_API_PREFIX}/")
        or parsed.path == ZOTERO_API_PREFIX
        or any(segment in {".", ".."} for segment in decoded_path.split("/"))
    ):
        raise ValueError("path must be a relative Zotero API path without a fragment")
    return f"http://{address}:{ZOTERO_PORT}{ZOTERO_API_PREFIX}{path}"


def get_json(gateway: str, path: str, *, timeout: float = 10.0) -> Any:
    """Issue one read-only GET request and decode its JSON response."""
    request = Request(
        build_request_url(gateway, path),
        headers=bridge_headers(),
        method="GET",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))
