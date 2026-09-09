#!/usr/bin/env python3
"""Read-only Zotero acquisition and agent-reviewed dataset finalization.

Python proposes boundaries and validates records; it does not infer scientific
facts or make the semantic SCC/FGCC eligibility decision.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path
from random import Random
import re
import sys
from typing import Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

from eval_model import Dataset, EvalCase, split_papers


class BuildError(ValueError):
    """A safe-to-report build failure without article prose."""


class BoundaryError(BuildError):
    """No sufficiently clear automatic Introduction boundary."""


class FactPacketError(BuildError):
    """A fact packet violates the mechanical privacy checks."""


@dataclass(frozen=True)
class Introduction:
    text: str
    start: int
    end: int
    confidence: float
    start_reason: str
    end_reason: str


@dataclass(frozen=True)
class BoundaryCandidate:
    case_type: str
    visible_context: str
    reference_continuation: str
    requires_semantic_review: bool = True


@dataclass(frozen=True)
class SourcePaper:
    item_key: str
    attachment_key: str
    fulltext: str
    abstract: str = ""
    title: str = ""

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.fulltext.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SkipRecord:
    item_key: str
    attachment_key: str | None
    reason: str
    content_hash: str | None = None


@dataclass(frozen=True)
class FetchResult:
    papers: tuple[SourcePaper, ...]
    skipped: tuple[SkipRecord, ...]


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ZoteroClient:
    """GET-only local API client; never changes preferences or uses Connector."""

    def __init__(self, host: str = "127.0.0.1", port: int = 23119,
                 timeout: float = 30, page_size: int = 100):
        if not re.fullmatch(r"[A-Za-z0-9._-]+", host) or not 1 <= port <= 65535:
            raise BuildError("invalid Zotero host or port")
        if not 1 <= page_size <= 100:
            raise BuildError("page_size must be between 1 and 100")
        self.base = f"http://{host}:{port}/api/users/0/"
        self.timeout = timeout
        self.page_size = page_size
        self.opener = build_opener(_NoRedirect())

    def get(self, route: str, **params: object) -> object:
        if not re.fullmatch(r"[A-Za-z0-9_/-]+", route) or ".." in route:
            raise BuildError("invalid local API route")
        url = self.base + route
        if params:
            url += "?" + urlencode(params)
        request = Request(url, headers={"Zotero-API-Version": "3"}, method="GET")
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            raise BuildError(f"zotero-http-{exc.code}") from None
        except (URLError, TimeoutError, OSError):
            raise BuildError("zotero-connection-failed") from None
        except (ValueError, UnicodeError):
            raise BuildError("zotero-invalid-json") from None

    def list(self, route: str) -> tuple[Mapping[str, object], ...]:
        records = []
        start = 0
        while True:
            page = self.get(route, start=start, limit=self.page_size, format="json")
            if not isinstance(page, list) or any(not isinstance(row, dict) for row in page):
                raise BuildError("zotero-invalid-list-response")
            records.extend(page)
            if len(page) < self.page_size:
                return tuple(records)
            start += len(page)


def _key(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise BuildError("invalid-item-or-collection-key")
    return value


def resolve_collection_tree(collections: Sequence[Mapping[str, object]],
                            path: str) -> tuple[str, ...]:
    """Resolve a unique literal name or hierarchical path, then all descendants."""
    records = { _key(row["key"]): row["data"] for row in collections }
    matches = [key for key, data in records.items() if data.get("name") == path]
    if not matches:
        parents: set[str | bool] = {False}
        for component in path.strip("/").split("/"):
            parents = {
                key for key, data in records.items()
                if data.get("name") == component
                and (data.get("parentCollection") or False) in parents
            }
        matches = sorted(parents)
    if not matches:
        raise BuildError("collection not found")
    if len(matches) != 1:
        raise BuildError("ambiguous collection name or path")
    result: set[str] = set()
    pending = list(matches)
    while pending:
        key = pending.pop()
        if key in result:
            continue
        result.add(key)
        pending.extend(k for k, data in records.items() if data.get("parentCollection") == key)
    return tuple(sorted(result))


def fetch_collection_papers(client: ZoteroClient, keys: Sequence[str]) -> FetchResult:
    """Fetch every indexed attachment for deduplicated paper items."""
    items = {}
    for collection_key in sorted(set(keys)):
        for row in client.list(f"collections/{quote(_key(collection_key))}/items/top"):
            items[_key(row["key"])] = row["data"]
    papers = []
    skipped = []
    for item_key, data in sorted(items.items()):
        if data.get("itemType") not in {"journalArticle", "conferencePaper", "preprint"}:
            skipped.append(SkipRecord(item_key, None, "unsupported-item-type"))
            continue
        children = client.list(f"items/{item_key}/children")
        attachments = [row for row in children if row["data"].get("itemType") == "attachment"]
        if not attachments:
            skipped.append(SkipRecord(item_key, None, "no-attachments"))
        for attachment in sorted(attachments, key=lambda row: row["key"]):
            attachment_key = _key(attachment["key"])
            try:
                fulltext = client.get(f"items/{attachment_key}/fulltext")
            except BuildError as exc:
                if str(exc) != "zotero-http-404":
                    raise
                skipped.append(SkipRecord(item_key, attachment_key, "fulltext-http-404"))
                continue
            if not isinstance(fulltext, dict) or not isinstance(fulltext.get("content"), str):
                raise BuildError("zotero-invalid-fulltext-response")
            if not fulltext["content"].strip():
                skipped.append(SkipRecord(item_key, attachment_key, "empty-fulltext"))
                continue
            if any(
                isinstance(fulltext.get(total), (int, float))
                and isinstance(fulltext.get(indexed), (int, float))
                and fulltext[indexed] < fulltext[total]
                for indexed, total in (("indexedPages", "totalPages"), ("indexedChars", "totalChars"))
            ):
                skipped.append(SkipRecord(item_key, attachment_key, "partial-fulltext-index"))
                continue
            papers.append(SourcePaper(item_key, attachment_key, fulltext["content"],
                                      data.get("abstractNote", ""), data.get("title", "")))
    return FetchResult(tuple(papers), tuple(skipped))


def extract_introduction(fulltext: str) -> Introduction:
    """Propose conservative boundaries in indexed text; agent review is required.

    Untitled PRL starts require an end-of-front-matter marker (DOI or PACS)
    followed by a paragraph break. Layouts lacking this evidence are rejected.
    """
    explicit = re.search(
        r"(?im)^\s*(?:(?:[IVX]+|\d+)\.?\s+)?Introduction\s*(?:[.—–:]\s*)?$",
        fulltext,
    )
    if explicit:
        start = explicit.end()
        start_reason = "explicit-introduction-heading"
        confidence = 0.95
    else:
        marker = re.search(
            r"(?im)^(?:DOI\s*:|PACS(?:\s+numbers)?\s*:)[^\n]*\n\s*\n",
            fulltext,
        )
        if not marker:
            raise BoundaryError("low boundary confidence: no supported body start")
        start = marker.end()
        start_reason = "untitled-body-after-front-matter"
        confidence = 0.85
    while start < len(fulltext) and fulltext[start].isspace():
        start += 1
    tail = fulltext[start:]
    transitions = (
        (r"(?m)^[ \t]*[A-Z][A-Za-z /,&()-]{0,65}\.\s*[—–]", "first-run-in-heading"),
        (
            r"(?im)^[ \t]*(?:(?:[IVX]+|\d+)\.?[ \t]+)?"
            r"(?:Methods?|Models?|Results?(?: and discussion)?|Theory|"
            r"Experimental(?: setup| methods)?|Computational methods|"
            r"Theoretical model|Discussion|Conclusions?)\s*[.:]?\s*$",
            "section-heading",
        ),
    )
    endings = [
        (match.start(), reason)
        for pattern, reason in transitions
        if (match := re.search(pattern, tail)) is not None
    ]
    if not endings:
        raise BoundaryError("low boundary confidence: no supported Introduction end")
    offset, end_reason = min(endings)
    end = start + offset
    while end > start and fulltext[end - 1].isspace():
        end -= 1
    text = fulltext[start:end]
    if len(re.findall(r"\w+", text)) < 30:
        raise BoundaryError("low boundary confidence: insufficient Introduction text")
    return Introduction(text, start, end, confidence, start_reason, end_reason)


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"\w+", text.casefold()))


def _candidates(introduction: Introduction, case_type: str) -> tuple[BoundaryCandidate, ...]:
    return tuple(
        BoundaryCandidate(case_type, introduction.text[:match.start()].strip(),
                          introduction.text[match.end():].strip())
        for match in re.finditer(r"\n\s*\n", introduction.text)
        if introduction.text[:match.start()].strip()
        and introduction.text[match.end():].strip()
    )


def choose_scc(introduction: Introduction) -> tuple[BoundaryCandidate, ...]:
    """List paragraph split candidates; the primary agent must select SCCs."""
    return _candidates(introduction, "SCC")


def choose_fgcc(introduction: Introduction, abstract: str,
                conclusion: str) -> tuple[BoundaryCandidate, ...]:
    """List FGCC candidates without inventing or mechanically paraphrasing facts.

    Abstract and conclusion are reserved for the primary agent's support review.
    Supplying them here does not constitute that review.
    """
    return _candidates(introduction, "FGCC")


def validate_fact_packet(facts: Sequence[str], source_text: str) -> None:
    """Reject sentence copying and eight-token overlap, not certify paraphrases.

    This deliberately conservative lexical check cannot establish scientific
    support, atomicity, completeness or removal of rhetorical ordering.
    """
    if isinstance(facts, (str, bytes)) or not facts:
        raise FactPacketError("fact packet must be a non-empty array")
    source = _tokens(source_text)
    source_ngrams = {source[i:i + 8] for i in range(max(0, len(source) - 7))}
    sentences = [
        _tokens(sentence)
        for sentence in re.split(r"(?<=[.!?])\s+", source_text)
        if len(_tokens(sentence)) >= 3
    ]
    for fact in facts:
        if not isinstance(fact, str) or not fact.strip():
            raise FactPacketError("fact packet entries must be non-empty strings")
        words = _tokens(fact)
        if any(words[i:i + 8] in source_ngrams for i in range(max(0, len(words) - 7))):
            raise FactPacketError("fact packet contains source wording")
        if any(
            words[i:i + len(sentence)] == sentence
            for sentence in sentences
            for i in range(max(0, len(words) - len(sentence) + 1))
        ):
            raise FactPacketError("fact packet contains source wording")


def validate_output_root(output: Path, repository_root: Path) -> Path:
    """Resolve symlinks and refuse private output within the source repository."""
    resolved = Path(output).expanduser().resolve()
    repository = Path(repository_root).resolve()
    if resolved.is_relative_to(repository):
        raise BuildError("dataset output must be outside the repository")
    if any((ancestor / ".git").exists() for ancestor in (resolved, *resolved.parents)):
        raise BuildError("dataset output must be outside the repository")
    # A checkout nested in .worktrees must not permit writing into its parent repo.
    for ancestor in repository.parents:
        if (ancestor / ".git").exists() and resolved.is_relative_to(ancestor):
            raise BuildError("dataset output must be outside the repository")
    return resolved


@dataclass(frozen=True)
class AgentCase:
    case_type: str
    visible_context: str
    reference_continuation: str
    fact_packet: tuple[str, ...]
    semantic_reviewed: bool

    def __post_init__(self) -> None:
        if isinstance(self.fact_packet, (str, bytes)):
            raise BuildError("fact_packet must be an array")
        object.__setattr__(self, "fact_packet", tuple(self.fact_packet))


@dataclass(frozen=True)
class ReviewedPaper:
    source: SourcePaper
    introduction_reviewed: bool
    cases: tuple[AgentCase, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "cases", tuple(self.cases))


def _validate_review(paper: ReviewedPaper) -> None:
    if not paper.cases:
        return
    if paper.introduction_reviewed is not True:
        raise BuildError("Introduction boundary requires agent semantic review")
    introduction = extract_introduction(paper.source.fulltext)
    seen = set()
    for case in paper.cases:
        if case.semantic_reviewed is not True:
            raise BuildError("case requires agent semantic review")
        if case.case_type not in {"SCC", "FGCC"} or case.case_type in seen:
            raise BuildError("paper requires at most one SCC and one FGCC")
        seen.add(case.case_type)
        if not all(isinstance(value, str) and value.strip()
                   for value in (case.visible_context, case.reference_continuation)):
            raise BuildError("case requires non-empty Introduction spans")
        # Context is a prefix and the hidden continuation the remaining suffix;
        # only whitespace between the two spans may be omitted.
        visible = case.visible_context
        hidden = case.reference_continuation
        if (not introduction.text.startswith(visible)
                or not introduction.text.endswith(hidden)
                or len(visible) + len(hidden) > len(introduction.text)
                or introduction.text[len(visible):len(introduction.text) - len(hidden)].strip()):
            raise BuildError("case does not match a contiguous Introduction span")
        if case.case_type == "SCC" and case.fact_packet:
            raise BuildError("SCC cannot contain a fact packet")
        if case.case_type == "FGCC":
            validate_fact_packet(case.fact_packet,
                                 paper.source.fulltext + "\n\n" + paper.source.abstract)
            if len(set(case.fact_packet)) != len(case.fact_packet):
                raise BuildError("duplicate fact packet entries")


def build_dataset(papers: Sequence[ReviewedPaper], seed: int) -> Dataset:
    """Validate agent-materialized records, select 20, and freeze a 15/5 split."""
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise BuildError("seed must be an integer")
    keys = [paper.source.item_key for paper in papers]
    if len(keys) != len(set(keys)):
        raise BuildError("duplicate paper records")
    for paper in papers:
        _validate_review(paper)
    eligible = {paper.source.item_key: paper for paper in papers if paper.cases}
    if len(eligible) < 20:
        raise BuildError("exactly 20 eligible papers required; fewer than 20 reviewed papers")
    selected = sorted(Random(seed).sample(sorted(eligible), 20))
    splits = split_papers(selected, seed)
    split_by_key = {key: split for split, keys in splits.items() for key in keys}
    cases = []
    for index, key in enumerate(selected, 1):
        paper = eligible[key]
        for case in paper.cases:
            cases.append(EvalCase(
                case_id=f"case-{index:04d}-{case.case_type}", case_type=case.case_type,
                split=split_by_key[key], visible_context=case.visible_context,
                fact_packet=case.fact_packet, reference_continuation=case.reference_continuation,
                item_key=key, attachment_key=paper.source.attachment_key,
                content_hash=paper.source.content_hash,
            ))
    return Dataset(cases, seed)


def _private_path(root: Path, relative: str, repository_root: Path) -> Path:
    path = validate_output_root(root / relative, repository_root)
    if not path.is_relative_to(root):
        raise BuildError("private artifact path escapes output directory")
    return path


def _write_json(path: Path, value: object, *, replace: bool = False) -> None:
    flags = os.O_WRONLY | os.O_CREAT | (os.O_TRUNC if replace else os.O_EXCL)
    with os.fdopen(os.open(path, flags, 0o600), "w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def _load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as stream:
            record = json.load(stream)
    except (OSError, ValueError, UnicodeError):
        raise BuildError("private artifact is missing or invalid JSON") from None
    if not isinstance(record, dict):
        raise BuildError("private artifact must be a JSON object")
    return record


def _record_hash(record: Mapping[str, object]) -> str:
    encoded = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def export_sources(papers: Sequence[SourcePaper], output: Path, seed: int,
                   repository_root: Path, skipped: Sequence[SkipRecord] = ()) -> dict:
    """Write private source packets and a blank agent-review form, never a Dataset."""
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise BuildError("seed must be an integer")
    output = validate_output_root(output, repository_root)
    if output.exists() and any(output.iterdir()):
        raise BuildError("export requires a new or empty output directory")
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    (output / "sources").mkdir(mode=0o700)
    sources = []
    reviews = []
    exclusions = [asdict(skip) for skip in skipped]
    seen = set()
    for paper in sorted(papers, key=lambda paper: (paper.item_key, paper.attachment_key)):
        _key(paper.item_key)
        _key(paper.attachment_key)
        if paper.item_key in seen:
            exclusions.append(asdict(SkipRecord(paper.item_key, paper.attachment_key,
                                                 "alternative-attachment", paper.content_hash)))
            continue
        try:
            intro = extract_introduction(paper.fulltext)
        except BoundaryError as exc:
            exclusions.append(asdict(SkipRecord(paper.item_key, paper.attachment_key,
                                                 str(exc), paper.content_hash)))
            continue
        scc = choose_scc(intro)
        if not scc:
            exclusions.append(asdict(SkipRecord(paper.item_key, paper.attachment_key,
                                                 "no-paragraph-split-candidate", paper.content_hash)))
            continue
        seen.add(paper.item_key)
        metadata = {
            "item_key": paper.item_key, "attachment_key": paper.attachment_key,
            "content_hash": paper.content_hash, "boundary_confidence": intro.confidence,
            "start_reason": intro.start_reason, "end_reason": intro.end_reason,
        }
        # Keep all source text here so the agent can locate and verify conclusion
        # evidence without trusting a second automatic section extraction.
        packet = {**asdict(paper), "content_hash": paper.content_hash,
                  "introduction": asdict(intro),
                  "candidates": [asdict(candidate) for candidate in
                                 (*scc, *choose_fgcc(intro, paper.abstract, ""))]}
        metadata["source_packet_hash"] = _record_hash(packet)
        sources.append(metadata)
        _write_json(_private_path(output, f"sources/{paper.item_key}.json", repository_root), packet)
        reviews.append({"item_key": paper.item_key, "attachment_key": paper.attachment_key,
                        "content_hash": paper.content_hash, "introduction_reviewed": False,
                        "cases": []})
    all_keys = {paper.item_key for paper in papers} | {skip.item_key for skip in skipped}
    report = {
        "status": "awaiting-agent-review" if len(seen) >= 20 else "insufficient-candidates",
        "seed": seed, "selected_item_keys": [], "unselected_item_keys": sorted(all_keys),
        "sources": sources, "skipped": exclusions, "case_counts": {"SCC": 0, "FGCC": 0},
    }
    _write_json(output / "review-template.json", {"papers": reviews})
    _write_json(output / "build-report.json", report)
    if len(seen) < 20:
        raise BuildError("exactly 20 eligible papers required; fewer than 20 boundary candidates")
    return report


def finalize_dataset(output: Path, cases_path: Path, repository_root: Path) -> Dataset:
    """Validate private reviewed records against their export; no Zotero access."""
    output = validate_output_root(output, repository_root)
    dataset_path = _private_path(output, "dataset.json", repository_root)
    if dataset_path.exists():
        raise BuildError("snapshot already finalized; explicitly rebuild in a new directory")
    report_path = _private_path(output, "build-report.json", repository_root)
    report = _load_json(report_path)
    records = _load_json(validate_output_root(cases_path, repository_root))
    if set(records) != {"papers"} or not isinstance(records["papers"], list):
        raise BuildError("review file must contain a papers array")
    sources = {row["item_key"]: row for row in report["sources"]}
    reviewed = []
    try:
        for record in records["papers"]:
            if set(record) != {"item_key", "attachment_key", "content_hash", "introduction_reviewed", "cases"}:
                raise BuildError("invalid reviewed paper fields")
            item_key = _key(record["item_key"])
            if item_key not in sources:
                raise BuildError("review provenance does not match exported sources")
            metadata = sources[item_key]
            if any(record[key] != metadata[key] for key in ("attachment_key", "content_hash")):
                raise BuildError("review provenance does not match exported sources")
            packet = _load_json(_private_path(output, f"sources/{item_key}.json", repository_root))
            if _record_hash(packet) != metadata["source_packet_hash"]:
                raise BuildError("source packet hash mismatch")
            source = SourcePaper(**{key: packet[key] for key in
                                   ("item_key", "attachment_key", "fulltext", "abstract", "title")})
            if source.content_hash != metadata["content_hash"] or packet["content_hash"] != source.content_hash:
                raise BuildError("source content hash mismatch")
            if source.item_key != item_key or source.attachment_key != record["attachment_key"]:
                raise BuildError("source provenance mismatch")
            if not isinstance(record["cases"], list):
                raise BuildError("reviewed cases must be an array")
            reviewed.append(ReviewedPaper(source, record["introduction_reviewed"],
                                          tuple(AgentCase(**case) for case in record["cases"])))
        if {paper.source.item_key for paper in reviewed} != set(sources):
            raise BuildError("review must account for every exported paper; use empty cases for exclusions")
        # Validate before treating empty cases as exclusions, then record that
        # distinction even if too few scientifically eligible papers remain.
        for paper in reviewed:
            _validate_review(paper)
        report["skipped"] = [skip for skip in report["skipped"]
                             if skip["reason"] not in {"agent-no-eligible-case", "seeded-selection-not-chosen"}]
        if sum(bool(paper.cases) for paper in reviewed) < 20:
            report["status"] = "insufficient-reviewed-papers"
            report["skipped"].extend(asdict(SkipRecord(paper.source.item_key,
                                                     paper.source.attachment_key,
                                                     "agent-no-eligible-case"))
                                     for paper in reviewed if not paper.cases)
            _write_json(report_path, report, replace=True)
            raise BuildError("exactly 20 eligible papers required; fewer than 20 reviewed papers")
        dataset = build_dataset(reviewed, report["seed"])
    except (KeyError, TypeError, AttributeError):
        raise BuildError("invalid source or agent-materialized record") from None
    selected = {case.item_key for case in dataset.cases}
    report["status"] = "finalized"
    report["selected_item_keys"] = sorted(selected)
    report["unselected_item_keys"] = sorted(set(report["unselected_item_keys"]) - selected)
    report["case_counts"] = {kind: sum(case.case_type == kind for case in dataset.cases)
                             for kind in ("SCC", "FGCC")}
    report["skipped"].extend(
        asdict(SkipRecord(paper.source.item_key, paper.source.attachment_key,
                         "seeded-selection-not-chosen" if paper.cases else "agent-no-eligible-case"))
        for paper in reviewed if paper.source.item_key not in selected
    )
    _write_json(dataset_path, dataset.to_record())
    _write_json(report_path, report, replace=True)
    return dataset


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    stage = argv.pop(0) if argv and argv[0] in {"export", "finalize"} else "export"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    if stage == "export":
        parser.add_argument("--collection", default="PRL/APS论文素材库")
        parser.add_argument("--seed", required=True, type=int)
        parser.add_argument("--host", default="127.0.0.1")
        parser.add_argument("--port", default=23119, type=int)
    else:
        parser.add_argument("--cases", required=True, type=Path)
    args = parser.parse_args(argv)
    repository_root = Path(__file__).resolve().parents[5]
    try:
        output = validate_output_root(args.output, repository_root)
        if stage == "export":
            client = ZoteroClient(args.host, args.port)
            keys = resolve_collection_tree(client.list("collections"), args.collection)
            fetched = fetch_collection_papers(client, keys)
            report = export_sources(fetched.papers, output, args.seed, repository_root, fetched.skipped)
            print(json.dumps({"status": report["status"], "candidate_papers": len(report["sources"])}))
        else:
            dataset = finalize_dataset(output, args.cases, repository_root)
            print(json.dumps({"status": "finalized", "papers": 20, "cases": len(dataset.cases)}))
        return 0
    except BuildError as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        # Never echo arbitrary source/agent values, HTTP bodies, or private prose.
        print("Build failed: invalid input, API response, or filesystem operation", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
