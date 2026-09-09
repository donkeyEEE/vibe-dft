"""Immutable data contract and pure helpers for PR Introduction evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
import re
from typing import Literal, Mapping, Sequence, TypeAlias


CaseType: TypeAlias = Literal["SCC", "FGCC"]
Split: TypeAlias = Literal["development", "acceptance"]

SCC_DIMENSIONS = (
    "logical_continuation",
    "scientific_compatibility",
    "information_density",
    "physical_review_expression",
    "non_fabrication",
)
FGCC_DIMENSIONS = SCC_DIMENSIONS[:2] + ("fact_packet_use",) + SCC_DIMENSIONS[2:]


def _require_nonempty_text(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True)
class EvalCase:
    """A complete evaluator-side masked-continuation case."""

    case_id: str
    case_type: CaseType
    split: Split
    visible_context: str
    fact_packet: Sequence[str]
    reference_continuation: str
    item_key: str
    attachment_key: str
    content_hash: str
    retrieval_handles: Sequence[str] = ()

    def __post_init__(self) -> None:
        for field_name in (
            "case_id",
            "visible_context",
            "reference_continuation",
            "item_key",
            "attachment_key",
            "content_hash",
        ):
            _require_nonempty_text(getattr(self, field_name), field_name)

        if self.case_type not in ("SCC", "FGCC"):
            raise ValueError("case_type must be 'SCC' or 'FGCC'")
        if self.split not in ("development", "acceptance"):
            raise ValueError("split must be 'development' or 'acceptance'")
        if isinstance(self.fact_packet, (str, bytes)):
            raise ValueError("fact_packet must be a sequence of strings")

        packet = tuple(self.fact_packet)
        if any(not isinstance(fact, str) or not fact.strip() for fact in packet):
            raise ValueError("fact_packet entries must be non-empty strings")
        if len(set(packet)) != len(packet):
            raise ValueError("fact_packet must not contain duplicate facts")
        if self.case_type == "SCC" and packet:
            raise ValueError("SCC cases cannot contain a fact packet")
        if self.case_type == "FGCC" and not packet:
            raise ValueError("FGCC cases require a non-empty fact packet")

        object.__setattr__(self, "fact_packet", packet)
        if isinstance(self.retrieval_handles, (str, bytes)):
            raise ValueError("retrieval_handles must be a sequence of strings")
        handles = tuple(self.retrieval_handles)
        if any(not isinstance(handle, str) or not handle.strip() for handle in handles):
            raise ValueError("retrieval_handles entries must be non-empty strings")
        if len(set(handles)) != len(handles):
            raise ValueError("retrieval_handles must not contain duplicates")
        object.__setattr__(self, "retrieval_handles", handles)


@dataclass(frozen=True)
class Dataset:
    """A validated 15/5 dataset in canonical split/item/type order.

    Development precedes acceptance, paper keys are lexicographic within each
    split, and SCC precedes FGCC for the same paper. Canonical construction
    makes serialized round trips independent of caller-provided case order.
    """

    cases: Sequence[EvalCase | Mapping[str, object]]
    seed: int

    def __post_init__(self) -> None:
        if isinstance(self.cases, (str, bytes)):
            raise ValueError("cases must be a sequence of EvalCase records")
        if not isinstance(self.seed, int) or isinstance(self.seed, bool):
            raise ValueError("seed must be an integer")

        cases = tuple(
            sorted(
                (
                    case if isinstance(case, EvalCase) else EvalCase(**case)
                    for case in self.cases
                ),
                key=lambda case: (
                    0 if case.split == "development" else 1,
                    case.item_key,
                    0 if case.case_type == "SCC" else 1,
                ),
            )
        )
        case_ids = [case.case_id for case in cases]
        if len(set(case_ids)) != len(case_ids):
            raise ValueError("dataset contains a duplicate case_id")

        development = {case.item_key for case in cases if case.split == "development"}
        acceptance = {case.item_key for case in cases if case.split == "acceptance"}
        overlap = development & acceptance
        if overlap:
            raise ValueError(
                "a paper cannot belong to both development and acceptance splits"
            )
        if len(development) != 15 or len(acceptance) != 5:
            raise ValueError(
                "dataset must contain exactly 15 development papers and "
                "5 acceptance papers"
            )

        paper_case_types: set[tuple[str, CaseType]] = set()
        for case in cases:
            membership = (case.item_key, case.case_type)
            if membership in paper_case_types:
                raise ValueError(
                    f"dataset contains a duplicate {case.case_type} case for "
                    f"paper {case.item_key}"
                )
            paper_case_types.add(membership)

        object.__setattr__(self, "cases", cases)

    def to_record(self) -> dict[str, object]:
        """Return the schema-shaped JSON-compatible dataset record."""

        grouped: dict[Split, dict[str, list[EvalCase]]] = {
            "development": {},
            "acceptance": {},
        }
        for case in self.cases:
            grouped[case.split].setdefault(case.item_key, []).append(case)

        record: dict[str, object] = {"seed": self.seed}
        for split in ("development", "acceptance"):
            record[split] = [
                {
                    "item_key": item_key,
                    "cases": [_case_record(case) for case in cases],
                }
                for item_key, cases in grouped[split].items()
            ]
        return record

    @classmethod
    def from_record(cls, record: Mapping[str, object]) -> Dataset:
        """Validate and load a schema-shaped JSON-compatible dataset record."""

        if not isinstance(record, Mapping):
            raise ValueError("dataset record must be an object")
        expected_fields = {"seed", "development", "acceptance"}
        if set(record) != expected_fields:
            raise ValueError(
                "dataset record must contain exactly seed, development, and acceptance"
            )

        cases: list[EvalCase] = []
        paper_memberships: dict[str, Split] = {}
        for split, expected_count in (("development", 15), ("acceptance", 5)):
            paper_groups = record[split]
            if isinstance(paper_groups, (str, bytes)) or not isinstance(
                paper_groups, Sequence
            ):
                raise ValueError(f"{split} must be an array of paper groups")
            if len(paper_groups) != expected_count:
                raise ValueError(
                    "dataset must contain exactly 15 development papers and "
                    "5 acceptance papers"
                )

            seen_in_split: set[str] = set()
            for group in paper_groups:
                if not isinstance(group, Mapping) or set(group) != {
                    "item_key",
                    "cases",
                }:
                    raise ValueError(
                        "paper groups must contain exactly item_key and cases"
                    )
                item_key = group["item_key"]
                _require_nonempty_text(item_key, "item_key")
                if item_key in seen_in_split:
                    raise ValueError(
                        f"duplicate paper membership for {item_key} in {split}"
                    )
                if item_key in paper_memberships:
                    raise ValueError(
                        "a paper cannot belong to both development and acceptance "
                        "splits"
                    )
                seen_in_split.add(item_key)
                paper_memberships[item_key] = split

                case_records = group["cases"]
                if isinstance(case_records, (str, bytes)) or not isinstance(
                    case_records, Sequence
                ):
                    raise ValueError("paper-group cases must be an array")
                if not 1 <= len(case_records) <= 2:
                    raise ValueError("each paper group must contain one or two cases")
                for case_record in case_records:
                    if not isinstance(case_record, Mapping):
                        raise ValueError("case records must be objects")
                    case = EvalCase(**case_record)
                    if case.split != split:
                        raise ValueError(
                            f"case {case.case_id} split does not match its paper group"
                        )
                    if case.item_key != item_key:
                        raise ValueError(
                            f"case {case.case_id} item_key does not match its paper group"
                        )
                    cases.append(case)

        return cls(cases=cases, seed=record["seed"])


def _case_record(case: EvalCase) -> dict[str, object]:
    record: dict[str, object] = {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "split": case.split,
        "visible_context": case.visible_context,
        "fact_packet": list(case.fact_packet),
        "reference_continuation": case.reference_continuation,
        "item_key": case.item_key,
        "attachment_key": case.attachment_key,
        "content_hash": case.content_hash,
    }
    if case.retrieval_handles:
        record["retrieval_handles"] = list(case.retrieval_handles)
    return record


_DOI = re.compile(
    r"(?i)(?:https?://(?:dx\.)?doi\.org/|\bdoi\s*:\s*)?"
    r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+"
)
_OBVIOUS_PATH = re.compile(
    r"(?i)(?:\bzotero://|(?:^|[\s'\"(])(?:/|[A-Za-z]:[\\/])\S+|"
    r"\bsources/[A-Za-z0-9_.-]+\.json\b)"
)


def _reject_retrieval_handles(case: EvalCase, texts: Sequence[str]) -> None:
    handles = (case.item_key, case.attachment_key, *case.retrieval_handles)
    for value in texts:
        folded = value.casefold()
        if any(handle.casefold() in folded for handle in handles):
            raise ValueError("sanitized case contains a retrieval handle")
        if _DOI.search(value) or _OBVIOUS_PATH.search(value):
            raise ValueError("sanitized case contains a retrieval handle")


def sanitized_case_view(case: EvalCase) -> dict[str, object]:
    """Build the allowlisted, retrieval-handle-free child-agent view."""

    _reject_retrieval_handles(case, (case.visible_context, *case.fact_packet))

    view: dict[str, object] = {
        "case_id": case.case_id,
        "case_type": case.case_type,
        "visible_context": case.visible_context,
    }
    if case.case_type == "FGCC":
        view["fact_packet"] = list(case.fact_packet)
    return view


def normalized_score(scores: Mapping[str, int], case_type: CaseType) -> float:
    """Validate a rubric score mapping and normalize it to a percentage."""

    if case_type == "SCC":
        dimensions = SCC_DIMENSIONS
    elif case_type == "FGCC":
        dimensions = FGCC_DIMENSIONS
    else:
        raise ValueError("case type must be 'SCC' or 'FGCC'")

    if set(scores) != set(dimensions):
        raise ValueError(
            f"{case_type} scores must contain exactly these dimensions: "
            f"{', '.join(dimensions)}"
        )
    if any(
        not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5
        for value in scores.values()
    ):
        raise ValueError("dimension scores must be integers between 1 and 5")

    return sum(scores[dimension] for dimension in dimensions) * 100.0 / (
        len(dimensions) * 5
    )


def split_papers(item_keys: Sequence[str], seed: int) -> dict[str, list[str]]:
    """Deterministically partition exactly 20 unique papers into 15 and 5."""

    keys = list(item_keys)
    if len(keys) != 20:
        raise ValueError("paper split requires exactly 20 item keys")
    if len(set(keys)) != len(keys):
        raise ValueError("paper split cannot contain duplicate item keys")
    if any(not isinstance(key, str) or not key.strip() for key in keys):
        raise ValueError("item keys must be non-empty strings")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be an integer")

    Random(seed).shuffle(keys)
    return {"development": keys[:15], "acceptance": keys[15:]}
