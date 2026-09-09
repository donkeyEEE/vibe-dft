import json
import subprocess
import sys
from copy import deepcopy
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOT = ROOT / "plugins/paper-project/skills/pr-intro"
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from eval_model import (  # noqa: E402
    FGCC_DIMENSIONS,
    SCC_DIMENSIONS,
    Dataset,
    EvalCase,
    normalized_score,
    sanitized_case_view,
    split_papers,
)

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None


SYSTEM_PYTHON = Path("/usr/bin/python3")
SYSTEM_HAS_JSONSCHEMA = (
    Draft202012Validator is None
    and SYSTEM_PYTHON.is_file()
    and subprocess.run(
        [str(SYSTEM_PYTHON), "-c", "import jsonschema"],
        capture_output=True,
        check=False,
    ).returncode
    == 0
)


def make_case(item_key, split, case_type="SCC", case_id=None):
    return EvalCase(
        case_id=case_id or f"{item_key}-{case_type}",
        case_type=case_type,
        split=split,
        visible_context="Known context.",
        fact_packet=("method: DFT",) if case_type == "FGCC" else (),
        reference_continuation="Hidden answer.",
        item_key=item_key,
        attachment_key=f"ATT-{item_key}",
        content_hash=f"hash-{item_key}",
    )


def valid_cases():
    cases = [
        make_case(f"I{i:02d}", "development" if i < 15 else "acceptance")
        for i in range(20)
    ]
    cases.insert(1, make_case("I00", "development", "FGCC"))
    return tuple(cases)


def balanced_cases():
    return tuple(
        make_case(
            f"I{i:02d}",
            "development" if i < 15 else "acceptance",
            case_type,
        )
        for i in range(20)
        for case_type in ("SCC", "FGCC")
    )


def serialized_dataset():
    return Dataset(cases=valid_cases(), seed=17).to_record()


def validate_structural_schema(payload):
    """Use jsonschema when present; otherwise exercise the repository parser."""

    schema_path = SKILL_ROOT / "evals/schema.json"
    if Draft202012Validator is not None:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.check_schema(schema)
        errors = list(validator.iter_errors(payload))
        if errors:
            raise ValueError(errors[0].message)
        return
    if SYSTEM_HAS_JSONSCHEMA:
        script = """
import json
import sys
from jsonschema import Draft202012Validator

schema = json.loads(open(sys.argv[1], encoding="utf-8").read())
payload = json.loads(sys.stdin.read())
validator = Draft202012Validator(schema)
validator.check_schema(schema)
errors = list(validator.iter_errors(payload))
if errors:
    print(errors[0].message, file=sys.stderr)
    raise SystemExit(1)
"""
        result = subprocess.run(
            [str(SYSTEM_PYTHON), "-c", script, str(schema_path)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise ValueError(result.stderr.strip())
        return
    Dataset.from_record(payload)


def test_sanitized_view_removes_reference_and_source():
    case = make_case("ITEM1234", "development", "FGCC", "case-1")

    assert sanitized_case_view(case) == {
        "case_id": "case-1",
        "case_type": "FGCC",
        "visible_context": "Known context.",
        "fact_packet": ["method: DFT"],
    }


def test_sanitized_scc_view_omits_inapplicable_fact_packet():
    case = make_case("ITEM1234", "development", case_id="case-1")

    assert sanitized_case_view(case) == {
        "case_id": "case-1",
        "case_type": "SCC",
        "visible_context": "Known context.",
    }


def test_sanitized_view_is_a_fresh_copy():
    case = make_case("ITEM1234", "development", "FGCC", "case-1")

    view = sanitized_case_view(case)
    view["fact_packet"].append("finding: changed")

    assert case.fact_packet == ("method: DFT",)


@pytest.mark.parametrize(
    "leak",
    [
        "doi:10.1103/PhysRevLett.130.123456",
        "10.1103/PhysRevLett.130.123456",
        "https://arxiv.org/abs/2609.01234",
        "arXiv:2609.01234v2",
        "file:///private/sources/paper.pdf",
        r"\\server\share\paper.pdf",
        "~/papers/source.pdf",
        "/private/pr-intro-evals/sources/public-paper.json",
        "zotero://select/library/items/OTHERKEY",
        "file://[2001:db8::1]/share/paper.pdf",
        "file:///home/me/a_(b).pdf",
        "zotero://select/library/items/(OTHERKEY)",
        "http://[2001:db8::1]/paper",
        "https://example.org/a_(b)",
        "(/private/data/paper.pdf)",
        '"C:\\papers\\paper.pdf"',
        "'~/papers/study.pdf'",
        r"(\\server\share\paper.pdf)",
    ],
)
def test_sanitized_view_redacts_public_retrieval_handles(leak):
    case = EvalCase(
        case_id="case-1",
        case_type="FGCC",
        split="development",
        visible_context=f"Scientific context with {leak}",
        fact_packet=("method: DFT",),
        reference_continuation="Hidden answer.",
        item_key="ITEM1234",
        attachment_key="ATT-ITEM1234",
        content_hash="hash-ITEM1234",
        retrieval_handles=(),
    )

    view = sanitized_case_view(case)

    assert leak not in view["visible_context"]
    assert "[SOURCE_IDENTIFIER_REDACTED]" in view["visible_context"]


@pytest.mark.parametrize("leak", ["ITEM1234", "ATT-ITEM1234"])
def test_sanitized_view_rejects_internal_retrieval_handles(leak):
    case = EvalCase(
        case_id="case-1",
        case_type="SCC",
        split="development",
        visible_context=f"Scientific context with {leak}",
        fact_packet=(),
        reference_continuation="Hidden answer.",
        item_key="ITEM1234",
        attachment_key="ATT-ITEM1234",
        content_hash="hash-ITEM1234",
    )

    with pytest.raises(ValueError, match="retrieval handle"):
        sanitized_case_view(case)


def test_url_redaction_consumes_balanced_url_delimiters_but_preserves_prose_punctuation():
    case = EvalCase(
        case_id="case-1", case_type="SCC", split="development",
        visible_context="See (https://example.org/a_(b)), then continue.",
        fact_packet=(), reference_continuation="Hidden answer.",
        item_key="ITEM1234", attachment_key="ATT-ITEM1234", content_hash="hash",
    )

    assert sanitized_case_view(case)["visible_context"] == (
        "See ([SOURCE_IDENTIFIER_REDACTED]), then continue."
    )


def test_sanitized_view_rejects_explicit_nonstandard_retrieval_handle():
    case = EvalCase(
        case_id="case-1",
        case_type="SCC",
        split="development",
        visible_context="Located by library-record:alpha-7.",
        fact_packet=(),
        reference_continuation="Hidden answer.",
        item_key="ITEM1234",
        attachment_key="ATT-ITEM1234",
        content_hash="hash-ITEM1234",
        retrieval_handles=("library-record:alpha-7",),
    )

    with pytest.raises(ValueError, match="retrieval handle"):
        sanitized_case_view(case)


def test_dataset_round_trip_preserves_explicit_retrieval_handles():
    cases = list(valid_cases())
    original = cases[0]
    cases[0] = EvalCase(
        **{
            **original.__dict__,
            "retrieval_handles": ("https://doi.org/10.1103/example", "sources/I00.json"),
        }
    )

    loaded = Dataset.from_record(Dataset(cases=cases, seed=17).to_record())

    assert loaded.cases[0].retrieval_handles == (
        "https://doi.org/10.1103/example",
        "sources/I00.json",
    )


def test_split_groups_exactly_fifteen_and_five_papers():
    item_keys = [f"I{i:02d}" for i in range(20)]

    split = split_papers(item_keys, seed=17)

    assert len(split["development"]) == 15
    assert len(split["acceptance"]) == 5
    assert set(split["development"]).isdisjoint(split["acceptance"])
    assert set(split["development"] + split["acceptance"]) == set(item_keys)
    assert item_keys == [f"I{i:02d}" for i in range(20)]
    assert split == split_papers(item_keys, seed=17)


@pytest.mark.parametrize(
    ("item_keys", "message"),
    [
        ([f"I{i:02d}" for i in range(19)], "exactly 20"),
        ([f"I{i:02d}" for i in range(21)], "exactly 20"),
        ([f"I{i:02d}" for i in range(19)] + ["I00"], "duplicate"),
    ],
)
def test_split_rejects_invalid_paper_membership(item_keys, message):
    with pytest.raises(ValueError, match=message):
        split_papers(item_keys, seed=17)


def test_scores_normalize_five_or_six_dimensions():
    assert normalized_score({key: 5 for key in SCC_DIMENSIONS}, "SCC") == 100.0
    assert normalized_score({key: 5 for key in FGCC_DIMENSIONS}, "FGCC") == 100.0
    assert normalized_score({key: 1 for key in SCC_DIMENSIONS}, "SCC") == 20.0


@pytest.mark.parametrize(
    ("scores", "case_type", "message"),
    [
        ({key: 5 for key in SCC_DIMENSIONS[:-1]}, "SCC", "dimensions"),
        (
            {**{key: 5 for key in SCC_DIMENSIONS}, "fact_packet_use": 5},
            "SCC",
            "dimensions",
        ),
        ({key: 0 for key in SCC_DIMENSIONS}, "SCC", "between 1 and 5"),
        ({key: 6 for key in SCC_DIMENSIONS}, "SCC", "between 1 and 5"),
        ({key: True for key in SCC_DIMENSIONS}, "SCC", "between 1 and 5"),
        ({key: 5 for key in SCC_DIMENSIONS}, "unknown", "case type"),
    ],
)
def test_score_rejects_malformed_rubrics(scores, case_type, message):
    with pytest.raises(ValueError, match=message):
        normalized_score(scores, case_type)


def test_eval_case_is_deeply_immutable_and_rejects_scc_fact_packets():
    case = make_case("ITEM1234", "development", "FGCC")

    assert case.fact_packet == ("method: DFT",)
    with pytest.raises(FrozenInstanceError):
        case.visible_context = "Changed"
    with pytest.raises(ValueError, match="SCC.*fact packet"):
        EvalCase(
            case_id="case-1",
            case_type="SCC",
            split="development",
            visible_context="Known context.",
            fact_packet=("method: DFT",),
            reference_continuation="Hidden answer.",
            item_key="ITEM1234",
            attachment_key="ATTACH12",
            content_hash="abc",
        )


def test_eval_case_rejects_empty_fgcc_fact_packet():
    with pytest.raises(ValueError, match="FGCC.*fact packet"):
        EvalCase(
            case_id="case-1",
            case_type="FGCC",
            split="development",
            visible_context="Known context.",
            fact_packet=(),
            reference_continuation="Hidden answer.",
            item_key="ITEM1234",
            attachment_key="ATTACH12",
            content_hash="abc",
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "case_id",
        "visible_context",
        "reference_continuation",
        "item_key",
        "attachment_key",
        "content_hash",
    ),
)
def test_eval_case_rejects_whitespace_only_text_fields(field_name):
    values = {
        "case_id": "case-1",
        "case_type": "SCC",
        "split": "development",
        "visible_context": "Known context.",
        "fact_packet": (),
        "reference_continuation": "Hidden answer.",
        "item_key": "ITEM1234",
        "attachment_key": "ATTACH12",
        "content_hash": "abc",
    }
    values[field_name] = " \t\n"

    with pytest.raises(ValueError, match=field_name):
        EvalCase(**values)


def test_eval_case_rejects_whitespace_only_fact():
    with pytest.raises(ValueError, match="fact_packet entries"):
        EvalCase(
            case_id="case-1",
            case_type="FGCC",
            split="development",
            visible_context="Known context.",
            fact_packet=(" \t",),
            reference_continuation="Hidden answer.",
            item_key="ITEM1234",
            attachment_key="ATTACH12",
            content_hash="abc",
        )


def test_eval_case_rejects_missing_and_invalid_fields():
    with pytest.raises(TypeError):
        EvalCase(
            case_id="case-1",
            case_type="SCC",
            split="development",
            visible_context="Known context.",
            fact_packet=(),
            reference_continuation="Hidden answer.",
            item_key="ITEM1234",
            attachment_key="ATTACH12",
        )
    with pytest.raises(ValueError, match="case_type"):
        make_case("ITEM1234", "development", case_type="unknown")
    with pytest.raises(ValueError, match="split"):
        make_case("ITEM1234", "unknown")


def test_dataset_accepts_json_records_and_freezes_cases():
    records = [
        {
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
        for case in valid_cases()
    ]

    dataset = Dataset(cases=records, seed=17)

    assert isinstance(dataset.cases, tuple)
    assert all(isinstance(case, EvalCase) for case in dataset.cases)
    assert dataset.seed == 17
    with pytest.raises(FrozenInstanceError):
        dataset.seed = 18


def test_dataset_serializes_as_exact_paper_group_arrays_and_round_trips():
    dataset = Dataset(cases=valid_cases(), seed=17)

    record = dataset.to_record()

    assert set(record) == {"seed", "development", "acceptance"}
    assert len(record["development"]) == 15
    assert len(record["acceptance"]) == 5
    assert all(set(group) == {"item_key", "cases"} for group in record["development"])
    assert Dataset.from_record(record) == dataset


def test_dataset_canonicalizes_non_adjacent_cases_before_round_trip():
    cases = list(valid_cases())
    i00_fgcc = cases.pop(1)
    cases.append(i00_fgcc)

    dataset = Dataset(cases=cases, seed=17)

    assert [case.case_id for case in dataset.cases[:3]] == [
        "I00-SCC",
        "I00-FGCC",
        "I01-SCC",
    ]
    assert Dataset.from_record(dataset.to_record()) == dataset


def test_dataset_requires_a_recorded_seed():
    with pytest.raises(TypeError):
        Dataset(cases=valid_cases())


def test_dataset_rejects_wrong_split_counts_and_cross_split_membership():
    with pytest.raises(ValueError, match="15 development.*5 acceptance"):
        Dataset(cases=valid_cases()[:-1], seed=17)

    cases = list(valid_cases())
    cases[-1] = make_case("I00", "acceptance", case_id="cross-split")
    with pytest.raises(ValueError, match="both development and acceptance"):
        Dataset(cases=cases, seed=17)


def test_dataset_rejects_duplicate_case_ids():
    cases = list(valid_cases())
    cases[-1] = make_case("I19", "acceptance", case_id=cases[0].case_id)

    with pytest.raises(ValueError, match="duplicate case_id"):
        Dataset(cases=cases, seed=17)


def test_dataset_rejects_duplicate_case_type_for_one_paper():
    cases = list(valid_cases())
    cases.append(make_case("I00", "development", case_id="duplicate-scc"))

    with pytest.raises(ValueError, match="duplicate SCC case.*I00"):
        Dataset(cases=cases, seed=17)


def test_v2_dataset_requires_one_scc_and_one_fgcc_for_every_paper():
    cases = list(balanced_cases())
    cases.pop(1)

    with pytest.raises(ValueError, match="v2.*one SCC and one FGCC"):
        Dataset(cases=cases, seed=17, version=2)

    cases = list(balanced_cases())
    cases[1] = make_case("I00", "development", "SCC", case_id="duplicate-scc")
    with pytest.raises(ValueError, match="duplicate SCC case.*I00"):
        Dataset(cases=cases, seed=17, version=2)


def test_v2_dataset_has_balanced_case_counts_in_each_paper_split():
    dataset = Dataset(cases=balanced_cases(), seed=17, version=2)

    assert dataset.version == 2
    assert sum(
        case.split == "development" and case.case_type == "SCC"
        for case in dataset.cases
    ) == 15
    assert sum(
        case.split == "development" and case.case_type == "FGCC"
        for case in dataset.cases
    ) == 15
    assert sum(
        case.split == "acceptance" and case.case_type == "SCC"
        for case in dataset.cases
    ) == 5
    assert sum(
        case.split == "acceptance" and case.case_type == "FGCC"
        for case in dataset.cases
    ) == 5
    assert Dataset.from_record(dataset.to_record()) == dataset


def test_dataset_reads_v1_records_without_a_version_field():
    payload = serialized_dataset()

    loaded = Dataset.from_record(payload)

    assert loaded.version == 1


def test_serialized_dataset_rejects_duplicate_and_cross_split_membership():
    duplicate = serialized_dataset()
    duplicate["development"][1]["item_key"] = duplicate["development"][0][
        "item_key"
    ]
    with pytest.raises(ValueError, match="duplicate paper membership"):
        Dataset.from_record(duplicate)

    cross_split = serialized_dataset()
    cross_split["acceptance"][0]["item_key"] = cross_split["development"][0][
        "item_key"
    ]
    with pytest.raises(ValueError, match="both development and acceptance"):
        Dataset.from_record(cross_split)


def test_serialized_dataset_rejects_duplicate_case_ids():
    payload = serialized_dataset()
    payload["acceptance"][0]["cases"][0]["case_id"] = payload["development"][0][
        "cases"
    ][0]["case_id"]

    with pytest.raises(ValueError, match="duplicate case_id"):
        Dataset.from_record(payload)


def test_serialized_dataset_rejects_case_item_key_mismatching_group():
    payload = serialized_dataset()
    payload["development"][0]["cases"][0]["item_key"] = "OTHER"

    with pytest.raises(ValueError, match="item_key does not match"):
        Dataset.from_record(payload)


def test_serialized_schema_contract_accepts_valid_payload():
    validate_structural_schema(serialized_dataset())


@pytest.mark.parametrize("development_count", (0, 20))
def test_serialized_schema_contract_rejects_wrong_development_count(
    development_count,
):
    payload = serialized_dataset()
    groups = payload["development"] + payload["acceptance"]
    payload["development"] = groups[:development_count]
    payload["acceptance"] = groups[development_count:]

    with pytest.raises(ValueError):
        validate_structural_schema(payload)


def test_serialized_schema_contract_rejects_empty_fgcc_packet():
    payload = serialized_dataset()
    fgcc = deepcopy(payload["development"][0]["cases"][0])
    fgcc["case_id"] = "fgcc-empty"
    fgcc["case_type"] = "FGCC"
    fgcc["fact_packet"] = []
    payload["development"][0]["cases"] = [fgcc]

    with pytest.raises(ValueError):
        validate_structural_schema(payload)


def test_serialized_schema_contract_rejects_whitespace_only_values():
    payload = serialized_dataset()
    payload["development"][0]["cases"][0]["visible_context"] = " \t"

    with pytest.raises(ValueError):
        validate_structural_schema(payload)


def test_serialized_schema_contract_rejects_whitespace_only_group_key():
    payload = serialized_dataset()
    payload["development"][0]["item_key"] = " \n"

    with pytest.raises(ValueError):
        validate_structural_schema(payload)


def test_schema_requires_the_python_case_fields_and_closes_records():
    schema = json.loads((SKILL_ROOT / "evals/schema.json").read_text(encoding="utf-8"))
    case_schema = schema["$defs"]["evalCase"]
    expected_fields = {
        "case_id",
        "case_type",
        "split",
        "visible_context",
        "fact_packet",
        "reference_continuation",
        "item_key",
        "attachment_key",
        "content_hash",
    }

    assert set(schema["required"]) == {"development", "acceptance", "seed"}
    assert schema["properties"]["version"] == {"type": "integer", "enum": [1, 2]}
    assert schema["properties"]["development"]["minItems"] == 15
    assert schema["properties"]["development"]["maxItems"] == 15
    assert schema["properties"]["acceptance"]["minItems"] == 5
    assert schema["properties"]["acceptance"]["maxItems"] == 5
    assert set(case_schema["required"]) == expected_fields
    assert set(case_schema["properties"]) == expected_fields | {"retrieval_handles"}
    assert case_schema["additionalProperties"] is False
    assert schema["$defs"]["nonBlankString"] == {
        "type": "string",
        "pattern": "\\S",
    }
    for field_name in expected_fields - {"case_type", "split", "fact_packet"}:
        assert case_schema["properties"][field_name] == {
            "$ref": "#/$defs/nonBlankString"
        }
    assert case_schema["properties"]["fact_packet"]["items"] == {
        "$ref": "#/$defs/nonBlankString"
    }
    assert schema["x-semantic-invariants"]
    assert "not enforced by JSON Schema" in schema["$comment"]
