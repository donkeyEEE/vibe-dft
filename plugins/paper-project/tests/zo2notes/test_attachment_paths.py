from pathlib import Path
import sys

import pytest


SCRIPTS = (
    Path(__file__).resolve().parents[2] / "skills" / "zo2notes" / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

from attachment_paths import (  # noqa: E402
    AttachmentPathError,
    redact_attachment_path,
    resolve_attachment_path,
)
from runtime_config import PathMappingConfig  # noqa: E402


def test_native_file_url_is_decoded_and_verified() -> None:
    resolved = resolve_attachment_path(
        "file:///tmp/My%20Paper.pdf", "native", (), exists=lambda path: True
    )
    assert resolved.path == Path("/tmp/My Paper.pdf")
    assert resolved.strategy == "native"


def test_wsl_standard_drive_maps_to_mnt() -> None:
    resolved = resolve_attachment_path(
        "file:///C:/Papers/a.pdf", "wsl", (), exists=lambda path: True
    )
    assert resolved.path == Path("/mnt/c/Papers/a.pdf")
    assert resolved.strategy == "wsl-drive"


def test_explicit_mapping_precedes_drive_mapping() -> None:
    mapping = PathMappingConfig(r"Z:\ZoteroStorage", "/data/papers")
    resolved = resolve_attachment_path(
        r"Z:\ZoteroStorage\topic\a.pdf",
        "wsl",
        (mapping,),
        exists=lambda path: True,
    )
    assert resolved.path == Path("/data/papers/topic/a.pdf")
    assert resolved.strategy == "configured-mapping"


def test_mapping_is_case_insensitive_and_requires_component_boundary() -> None:
    mappings = (
        PathMappingConfig(r"Z:\Papers", "/data/papers"),
        PathMappingConfig(r"Z:\PapersExtra", "/data/extra"),
    )
    resolved = resolve_attachment_path(
        r"z:\papersextra\a.pdf", "wsl", mappings, exists=lambda path: True
    )
    assert resolved.path == Path("/data/extra/a.pdf")


def test_mapping_declaration_order_is_authoritative() -> None:
    mappings = (
        PathMappingConfig(r"Z:\Papers", "/first"),
        PathMappingConfig(r"z:\papers", "/second"),
    )
    resolved = resolve_attachment_path(
        r"Z:\Papers\a.pdf", "wsl", mappings, exists=lambda path: True
    )
    assert resolved.path == Path("/first/a.pdf")


def test_unc_path_requires_explicit_mapping() -> None:
    with pytest.raises(AttachmentPathError, match="network or UNC"):
        resolve_attachment_path(
            r"\\server\share\paper.pdf", "wsl", (), exists=lambda path: True
        )


@pytest.mark.parametrize(
    "raw",
    [
        "https://example.test/paper.pdf",
        "relative/paper.pdf",
        "/tmp/../secret/paper.pdf",
        "/tmp/paper\x00.pdf",
    ],
)
def test_unsafe_or_nonlocal_paths_are_rejected(raw: str) -> None:
    with pytest.raises(AttachmentPathError):
        resolve_attachment_path(raw, "native", (), exists=lambda path: True)


def test_failure_message_does_not_reveal_full_path() -> None:
    with pytest.raises(AttachmentPathError) as error:
        resolve_attachment_path(
            r"C:\Secret\Topic\paper.pdf", "wsl", (), exists=lambda path: False
        )
    assert r"C:\Secret\Topic" not in str(error.value)
    assert "paper.pdf" in str(error.value)


def test_redaction_preserves_filename_without_parent_directories() -> None:
    redacted = redact_attachment_path(r"C:\Users\Ada\Secret\paper.pdf")
    assert redacted == "Windows attachment 'paper.pdf'"
    assert "Ada" not in redacted
