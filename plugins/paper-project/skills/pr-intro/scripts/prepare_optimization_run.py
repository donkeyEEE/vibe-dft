#!/usr/bin/env python3
"""Isolate mutable PR Introduction rules and apply a reviewed candidate safely."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from typing import Iterator, Sequence
from urllib.parse import unquote, urlsplit

from eval_model import Dataset, sanitized_case_view


MUTABLE_PATTERNS = ("SKILL.md", "references/writing/*.md")
IMMUTABLE_PREFIXES = ("references/maintenance/", "evals/", "scripts/", "tests/")


class WorkspaceError(ValueError):
    """An isolation, integrity, or candidate-validation boundary was violated."""


class SourceDriftError(WorkspaceError):
    """Formal mutable files changed after baseline capture."""


class RecoveryError(WorkspaceError):
    """An interrupted rollback requires recovery from the retained staging tree."""


@dataclass(frozen=True)
class RunWorkspace:
    root: Path
    formal_skill: Path
    dataset_root: Path

    @property
    def baseline(self) -> Path:
        return self.root / "baseline"

    @property
    def candidate(self) -> Path:
        return self.root / "candidate"


def _mutable(name: str) -> bool:
    path = PurePosixPath(name)
    return name == "SKILL.md" or (
        path.parent == PurePosixPath("references/writing")
        and path.suffix == ".md"
    )


def _files(root: Path, *, isolated: bool = False) -> dict[str, bytes]:
    if root.is_symlink() or not root.is_dir():
        raise WorkspaceError(f"expected a real directory: {root}")
    result = {}
    if isolated:
        paths = list(root.rglob("*"))
    else:
        for parent in (root / "references", root / "references/writing"):
            if parent.is_symlink():
                raise WorkspaceError(f"symlink in mutable source: {parent}")
        paths = [root / "SKILL.md", *root.glob("references/writing/*.md")]
    for path in paths:
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise WorkspaceError(f"symlinks are not allowed: {name}")
        if path.is_dir():
            if isolated and name not in {"references", "references/writing"}:
                raise WorkspaceError(f"directory outside mutable allowlist: {name}")
            continue
        if not path.is_file() or not _mutable(name):
            raise WorkspaceError(f"file outside mutable allowlist: {name}")
        content = path.read_bytes()
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise WorkspaceError(f"runtime Markdown must be UTF-8: {name}") from exc
        result[name] = content
    if "SKILL.md" not in result:
        raise WorkspaceError("SKILL.md must remain present")
    return dict(sorted(result.items()))


def _hashes(files: dict[str, bytes]) -> dict[str, str]:
    return {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}


def _write_json(path: Path, record: object) -> None:
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _overlap(left: Path, right: Path) -> bool:
    return left.is_relative_to(right) or right.is_relative_to(left)


def _outside_repository(path: Path) -> None:
    for parent in (path, *path.parents):
        if (parent / ".git").exists():
            raise WorkspaceError("datasets and runs must be outside a Git repository")


def prepare_run(
    skill_root: str | Path, dataset_root: str | Path,
    runs_root: str | Path, run_id: str,
) -> RunWorkspace:
    """Capture source hashes, then create private baseline/candidate snapshots.

    Dataset contents remain in their persistent location. Only sanitized
    development cases are copied into prompts; acceptance stays evaluator-only.
    """
    if not isinstance(run_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", run_id):
        raise WorkspaceError("run_id must be a single alphanumeric-led path component")
    formal = Path(skill_root).resolve(strict=True)
    dataset_root = Path(dataset_root).resolve(strict=True)
    root = Path(runs_root).resolve() / run_id
    if any(_overlap(a, b) for a, b in ((formal, root), (dataset_root, root), (formal, dataset_root))):
        raise WorkspaceError("formal skill, dataset, and run must not overlap")
    _outside_repository(root)
    _outside_repository(dataset_root)
    source = _files(formal)
    dataset_bytes = (dataset_root / "dataset.json").read_bytes()
    dataset = Dataset.from_record(json.loads(dataset_bytes))
    if root.exists():
        raise WorkspaceError(f"run already exists: {root}")
    root.parent.mkdir(parents=True, exist_ok=True)
    root.mkdir(mode=0o700)
    workspace = RunWorkspace(root, formal, dataset_root)
    try:
        # Persist hashes before creating either copied tree.
        _write_json(root / "workspace.json", {
            "version": 1, "formal_skill": str(formal), "dataset_root": str(dataset_root),
            "source_hashes": _hashes(source),
            "dataset_hash": hashlib.sha256(dataset_bytes).hexdigest(),
        })
        for destination in (workspace.baseline, workspace.candidate):
            destination.mkdir()
            for name, content in source.items():
                path = destination / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                path.chmod(0o444 if destination == workspace.baseline else 0o644)
        # Detect edits during preparation rather than silently using mixed input.
        if _hashes(_files(formal)) != _hashes(source):
            raise SourceDriftError("formal source changed during preparation")
        (root / "iterations.jsonl").touch(mode=0o600)
        prompts = root / "prompts/development"
        prompts.mkdir(parents=True)
        for index, case in enumerate(c for c in dataset.cases if c.split == "development"):
            _write_json(prompts / f"{index:03d}.json", sanitized_case_view(case))
        _write_json(root / "run-state.json", {"status": "prepared"})
    except BaseException:
        shutil.rmtree(root)
        raise
    return workspace


def _manifest(workspace: RunWorkspace) -> dict:
    record = json.loads((workspace.root / "workspace.json").read_text(encoding="utf-8"))
    if record.get("version") != 1:
        raise WorkspaceError("unsupported workspace version")
    if record["formal_skill"] != str(workspace.formal_skill) or record["dataset_root"] != str(workspace.dataset_root):
        raise WorkspaceError("workspace locations differ from the captured manifest")
    return record


def _snapshots(workspace: RunWorkspace) -> tuple[dict[str, bytes], dict[str, bytes]]:
    baseline = _files(workspace.baseline, isolated=True)
    if _hashes(baseline) != _manifest(workspace)["source_hashes"]:
        raise WorkspaceError("baseline integrity check failed")
    return baseline, _files(workspace.candidate, isolated=True)


def candidate_patch(workspace: RunWorkspace) -> str:
    """Return an allowlisted unified diff; baseline is always the fixed source."""
    baseline, candidate = _snapshots(workspace)
    return _diff(baseline, candidate)


def _diff(baseline: dict[str, bytes], candidate: dict[str, bytes]) -> str:
    output = []
    for name in sorted(baseline.keys() | candidate.keys()):
        if baseline.get(name) == candidate.get(name):
            continue
        output.append(f"diff --git a/{name} b/{name}\n")
        if name not in baseline:
            output.append("new file mode 100644\n")
        elif name not in candidate:
            output.append("deleted file mode 100644\n")
        lines = difflib.unified_diff(
            baseline.get(name, b"").decode("utf-8").splitlines(keepends=True),
            candidate.get(name, b"").decode("utf-8").splitlines(keepends=True),
            fromfile=f"a/{name}" if name in baseline else "/dev/null",
            tofile=f"b/{name}" if name in candidate else "/dev/null",
        )
        for line in lines:
            output.append(line)
            if not line.endswith("\n"):
                output.append("\n\\ No newline at end of file\n")
    return "".join(output)


def _link_targets(content: str) -> list[str]:
    # Inline links, reference-style definitions, and the repo's backtick paths.
    targets = re.findall(r"\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", content)
    targets += re.findall(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", content, re.MULTILINE)
    targets += [s for s in re.findall(r"`([^`\n]+)`", content)
                if s.endswith(".md") and ("/" in s or s == "SKILL.md")]
    return [s.strip("<>") for s in targets]


def _validate_links(workspace: RunWorkspace, candidate: dict[str, bytes]) -> None:
    formal = workspace.formal_skill
    for name, content in candidate.items():
        for target in _link_targets(content.decode("utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            relative = unquote(parsed.path)
            if Path(relative).is_absolute():
                raise WorkspaceError(f"absolute local link in {name}: {target}")
            destination = (formal / name).parent.joinpath(relative).resolve()
            if not destination.is_relative_to(formal):
                raise WorkspaceError(f"link escapes skill root in {name}: {target}")
            link_name = destination.relative_to(formal).as_posix()
            if _mutable(link_name):
                exists = link_name in candidate
            else:
                exists = destination.is_file()
            if not exists:
                raise WorkspaceError(f"broken relative link in {name}: {target}")


def _check_source(workspace: RunWorkspace, hashes: dict[str, str]) -> None:
    try:
        actual = _hashes(_files(workspace.formal_skill))
    except (OSError, WorkspaceError) as exc:
        raise SourceDriftError("formal source was removed or replaced") from exc
    if actual != hashes:
        raise SourceDriftError("formal mutable source differs from the captured baseline")


@contextmanager
def _staging(formal: Path) -> Iterator[Path]:
    stage = Path(tempfile.mkdtemp(prefix=f".{formal.name}.apply-", dir=formal.parent))
    preserve = False
    try:
        yield stage
    except RecoveryError:
        preserve = True
        raise
    finally:
        if not preserve:
            shutil.rmtree(stage)


def apply_candidate(workspace: RunWorkspace) -> Sequence[Path]:
    """Stage every replacement and backup before writes; roll back on failure.

    This is workflow-level atomicity for cooperating writers and caught errors,
    not a filesystem-wide transaction or protection against power loss.
    """
    manifest = _manifest(workspace)
    _check_source(workspace, manifest["source_hashes"])
    dataset_hash = hashlib.sha256((workspace.dataset_root / "dataset.json").read_bytes()).hexdigest()
    if dataset_hash != manifest["dataset_hash"]:
        raise WorkspaceError("dataset changed after preparation; start a fresh run")
    baseline, candidate = _snapshots(workspace)
    _validate_links(workspace, candidate)
    changed = sorted(name for name in baseline.keys() | candidate.keys()
                     if baseline.get(name) != candidate.get(name))
    if not changed:
        return []
    # A sibling lock serializes this workflow without changing formal resources.
    lock = workspace.formal_skill.parent / f".{workspace.formal_skill.name}.optimization.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise WorkspaceError(f"another apply holds the lock: {lock}") from exc
    try:
        with _staging(workspace.formal_skill) as stage:
            for kind, files in (("replacement", candidate), ("backup", baseline)):
                for name in changed:
                    if name in files:
                        path = stage / kind / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(files[name])
                        original = workspace.formal_skill / name
                        path.chmod(original.stat().st_mode & 0o777 if original.exists() else 0o644)
            _check_source(workspace, manifest["source_hashes"])
            (workspace.root / "candidate.patch").write_text(_diff(baseline, candidate), encoding="utf-8")
            applied = []
            created_directories = []
            try:
                for name in changed:
                    target = workspace.formal_skill / name
                    if name in candidate:
                        missing = []
                        parent = target.parent
                        while not parent.exists():
                            missing.append(parent)
                            parent = parent.parent
                        for directory in reversed(missing):
                            directory.mkdir()
                            created_directories.append(directory)
                        os.replace(stage / "replacement" / name, target)
                    else:
                        target.unlink()
                    applied.append(name)
                _write_json(workspace.root / "run-state.json", {"status": "applied", "changed": changed})
            except BaseException as failure:
                recovery_failures = []
                for name in reversed(applied):
                    target = workspace.formal_skill / name
                    try:
                        if name in baseline:
                            os.replace(stage / "backup" / name, target)
                        else:
                            target.unlink()
                    except OSError:
                        recovery_failures.append(name)
                for directory in reversed(created_directories):
                    try:
                        directory.rmdir()
                    except OSError:
                        recovery_failures.append(str(directory))
                if recovery_failures:
                    raise RecoveryError(
                        f"apply failed and recovery is needed for {recovery_failures}; "
                        f"retained backups: {stage}"
                    ) from failure
                raise
    finally:
        lock.rmdir()
    return [workspace.formal_skill / name for name in changed]


def load_workspace(root: str | Path) -> RunWorkspace:
    root = Path(root).resolve(strict=True)
    record = json.loads((root / "workspace.json").read_text(encoding="utf-8"))
    workspace = RunWorkspace(root, Path(record["formal_skill"]), Path(record["dataset_root"]))
    _manifest(workspace)
    return workspace


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="create a fresh private optimization run")
    for name in ("skill-root", "dataset-root", "runs-root", "run-id"):
        prepare.add_argument(f"--{name}", required=True)
    for name in ("patch", "apply"):
        commands.add_parser(name).add_argument("workspace", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            run = prepare_run(args.skill_root, args.dataset_root, args.runs_root, args.run_id)
            print(run.root)
        elif args.command == "patch":
            print(candidate_patch(load_workspace(args.workspace)), end="")
        else:
            print(json.dumps([str(path) for path in apply_candidate(load_workspace(args.workspace))]))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
