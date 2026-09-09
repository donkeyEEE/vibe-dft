import json
import sys
import subprocess
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlsplit

import pytest


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "plugins/paper-project/skills/pr-intro/scripts"
sys.path.insert(0, str(SCRIPTS))

from build_eval_dataset import (  # noqa: E402
    BoundaryError,
    BuildError,
    FactPacketError,
    extract_introduction,
    validate_fact_packet,
    validate_output_root,
)


CONTEXT = (
    "The discovery of synthetic collective modes motivates a controlled study. "
    "Previous measurements establish a useful reference for the model."
)
HIDDEN = (
    "Whether this reference extends to disordered lattices remains unresolved. "
    "A comparison of independent probes would constrain the competing pictures."
)
PRL_UNTITLED_FIXTURE = (
    "Synthetic title\nA. Example\n(Dated: September 9, 2026)\n\n"
    "Abstract\nA synthetic abstract describes the work.\n\n"
    "DOI: 10.0000/example\n\n" + CONTEXT + "\n\n" + HIDDEN
    + "\n\nModel.—We define the Hamiltonian on a square lattice.\n"
)


def test_detects_untitled_prl_introduction():
    result = extract_introduction(PRL_UNTITLED_FIXTURE)
    assert result.text.startswith("The discovery")
    assert result.end_reason == "first-run-in-heading"
    assert "Abstract" not in result.text
    assert "Hamiltonian" not in result.text


def test_explicit_introduction_ends_before_numbered_section():
    result = extract_introduction(
        "Title\nAbstract\nSummary.\n\nI. INTRODUCTION\n" + CONTEXT
        + "\n\n" + HIDDEN + "\n\nII. METHODS\nThe apparatus..."
    )
    assert result.text == CONTEXT + "\n\n" + HIDDEN
    assert result.confidence >= 0.9


def test_ambiguous_boundary_is_rejected():
    with pytest.raises(BoundaryError, match="confidence"):
        extract_introduction("A title and author line.\nSome text without boundaries.")


@pytest.mark.parametrize("packet", [[HIDDEN], [HIDDEN.upper()], ["Fact: " + HIDDEN]])
def test_fact_packet_rejects_verbatim_sentence_leakage(packet):
    with pytest.raises(FactPacketError, match="source wording"):
        validate_fact_packet(packet, HIDDEN)


def test_builder_does_not_write_sources_inside_repository(tmp_path):
    with pytest.raises(BuildError, match="outside the repository"):
        validate_output_root(ROOT / "plugins/paper-project/pr-intro-evals", ROOT)
    link = tmp_path / "repository-link"
    link.symlink_to(ROOT, target_is_directory=True)
    with pytest.raises(BuildError, match="outside the repository"):
        validate_output_root(link / "private", ROOT)


def test_collection_resolution_walks_descendants_and_rejects_ambiguity():
    from build_eval_dataset import resolve_collection_tree

    collections = [
        {"key": "ROOT", "data": {"name": "PRL", "parentCollection": False}},
        {"key": "APS", "data": {"name": "APS论文素材库", "parentCollection": "ROOT"}},
        {"key": "CHILD", "data": {"name": "Nested", "parentCollection": "APS"}},
        {"key": "GRAND", "data": {"name": "More", "parentCollection": "CHILD"}},
        {"key": "OTHER", "data": {"name": "Elsewhere", "parentCollection": False}},
    ]
    assert resolve_collection_tree(collections, "PRL/APS论文素材库") == ("APS", "CHILD", "GRAND")
    collections.append({"key": "DUP", "data": {"name": "APS论文素材库", "parentCollection": "OTHER"}})
    with pytest.raises(BuildError, match="ambiguous"):
        resolve_collection_tree(collections, "APS论文素材库")
    with pytest.raises(BuildError, match="not found"):
        resolve_collection_tree(collections, "missing")


@contextmanager
def local_api(routes):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append((self.command, self.path, self.headers.get("Zotero-API-Version")))
            url = urlsplit(self.path)
            value = routes.get(url.path)
            if value is None:
                self.send_error(404)
                return
            if isinstance(value, list):
                query = parse_qs(url.query)
                start = int(query.get("start", ["0"])[0])
                limit = int(query.get("limit", ["100"])[0])
                value = value[start:start + limit]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(value).encode())

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield server.server_port, requests
    finally:
        server.shutdown()
        worker.join()
        server.server_close()


def test_acquisition_is_paginated_read_only_deduplicated_and_auditable():
    from build_eval_dataset import ZoteroClient, fetch_collection_papers

    paper = {"key": "P1", "data": {"itemType": "journalArticle", "abstractNote": "Summary"}}
    routes = {
        "/api/users/0/collections/A/items/top": [paper, {"key": "NOTE", "data": {"itemType": "note"}}, {"key": "P2", "data": {"itemType": "journalArticle"}}],
        "/api/users/0/collections/B/items/top": [paper],
        "/api/users/0/items/P1/children": [{"key": "ATT", "data": {"itemType": "attachment"}}],
        "/api/users/0/items/P2/children": [{"key": "NOINDEX", "data": {"itemType": "attachment"}}],
        "/api/users/0/items/ATT/fulltext": {"content": PRL_UNTITLED_FIXTURE},
    }
    with local_api(routes) as (port, requests):
        client = ZoteroClient(host="127.0.0.1", port=port, page_size=2)
        result = fetch_collection_papers(client, ["A", "B"])
    assert [(paper.item_key, paper.attachment_key) for paper in result.papers] == [("P1", "ATT")]
    assert {skip.reason for skip in result.skipped} == {"unsupported-item-type", "fulltext-http-404"}
    assert any("start=2" in path for _, path, _ in requests)
    assert all(method == "GET" and path.startswith("/api/users/0/") and version == "3" for method, path, version in requests)


def test_candidates_do_not_claim_semantic_selection_or_paraphrase_facts():
    from build_eval_dataset import choose_fgcc, choose_scc

    intro = extract_introduction(PRL_UNTITLED_FIXTURE)
    scc = choose_scc(intro)
    fgcc = choose_fgcc(intro, "Abstract facts.", "Conclusion facts.")
    assert len(scc) == len(fgcc) == 1
    assert scc[0].visible_context == CONTEXT
    assert scc[0].reference_continuation == HIDDEN
    assert scc[0].requires_semantic_review is True
    assert fgcc[0].requires_semantic_review is True
    assert not hasattr(fgcc[0], "fact_packet")


def synthetic_papers(count=23):
    from build_eval_dataset import SourcePaper
    return tuple(SourcePaper(f"P{i:02}", f"A{i:02}", PRL_UNTITLED_FIXTURE,
                             "Abstract details are available for agent review.")
                 for i in range(count))


def materialize(output):
    template_path = output / "review-template.json"
    records = json.loads(template_path.read_text())
    for paper in records["papers"]:
        paper["introduction_reviewed"] = True
        paper["cases"] = [{
            "case_type": "SCC", "visible_context": CONTEXT,
            "reference_continuation": HIDDEN, "fact_packet": [],
            "semantic_reviewed": True,
        }]
    # Add an independently paraphrased FGCC on each paper, without relying on
    # which seeded subset is selected.
    for paper in records["papers"]:
        paper["cases"].append({
            "case_type": "FGCC", "visible_context": CONTEXT,
            "reference_continuation": HIDDEN,
            "fact_packet": ["Open question: applicability under lattice disorder."],
            "semantic_reviewed": True,
        })
    review = output / "reviewed-cases.json"
    review.write_text(json.dumps(records))
    return review


def test_staged_builder_freezes_reproducible_dataset_and_prose_free_report(tmp_path):
    from build_eval_dataset import export_sources, finalize_dataset
    from eval_model import Dataset

    output = tmp_path / "snapshot"
    export_sources(synthetic_papers(), output, seed=17, repository_root=ROOT)
    assert not (output / "dataset.json").exists()
    review = materialize(output)
    dataset = finalize_dataset(output, review, repository_root=ROOT)
    stored = json.loads((output / "dataset.json").read_text())
    assert Dataset.from_record(stored) == dataset
    assert len(stored["development"]) == 15
    assert len(stored["acceptance"]) == 5
    report_text = (output / "build-report.json").read_text()
    report = json.loads(report_text)
    assert report["case_counts"] == {"SCC": 20, "FGCC": 20}
    assert len(report["selected_item_keys"]) == 20
    assert len(report["unselected_item_keys"]) == 3
    assert CONTEXT not in report_text and HIDDEN not in report_text
    assert "Abstract details" not in report_text
    other = tmp_path / "again"
    export_sources(tuple(reversed(synthetic_papers())), other, seed=17, repository_root=ROOT)
    finalize_dataset(other, materialize(other), repository_root=ROOT)
    assert (output / "dataset.json").read_bytes() == (other / "dataset.json").read_bytes()
    with pytest.raises(BuildError, match="already finalized"):
        finalize_dataset(output, review, repository_root=ROOT)


@pytest.mark.parametrize("mutation, message", [
    ("unreviewed", "semantic review"), ("provenance", "provenance"),
    ("wording", "source wording"), ("span", "Introduction span"),
    ("source_changed", "hash"),
])
def test_finalizer_rejects_unreviewed_leaking_or_unbound_records(tmp_path, mutation, message):
    from build_eval_dataset import export_sources, finalize_dataset

    output = tmp_path / "snapshot"
    export_sources(synthetic_papers(20), output, seed=17, repository_root=ROOT)
    review = materialize(output)
    records = json.loads(review.read_text())
    if mutation == "unreviewed":
        records["papers"][0]["cases"][0]["semantic_reviewed"] = False
    elif mutation == "provenance":
        records["papers"][0]["attachment_key"] = "WRONG"
    elif mutation == "wording":
        records["papers"][0]["cases"][1]["fact_packet"] = [HIDDEN]
    elif mutation == "span":
        records["papers"][0]["cases"][0]["reference_continuation"] = "Unrelated ending."
    elif mutation == "source_changed":
        source_path = output / "sources/P00.json"
        source = json.loads(source_path.read_text())
        source["fulltext"] += " Changed."
        source_path.write_text(json.dumps(source))
    review.write_text(json.dumps(records))
    with pytest.raises(BuildError, match=message):
        finalize_dataset(output, review, repository_root=ROOT)
    assert not (output / "dataset.json").exists()


def test_insufficient_candidates_leave_auditable_failure_without_dataset(tmp_path):
    from build_eval_dataset import export_sources

    output = tmp_path / "snapshot"
    with pytest.raises(BuildError, match="20"):
        export_sources(synthetic_papers(19), output, seed=17, repository_root=ROOT)
    assert not (output / "dataset.json").exists()
    assert json.loads((output / "build-report.json").read_text())["status"] == "insufficient-candidates"


def test_default_cli_exports_then_finalize_completes_offline(tmp_path):
    routes = {"/api/users/0/collections": [{"key": "COLL", "data": {"name": "PRL/APS论文素材库", "parentCollection": False}}]}
    routes["/api/users/0/collections/COLL/items/top"] = [
        {"key": f"P{i:02}", "data": {"itemType": "journalArticle"}} for i in range(20)
    ]
    for i in range(20):
        routes[f"/api/users/0/items/P{i:02}/children"] = [{"key": f"A{i:02}", "data": {"itemType": "attachment"}}]
        routes[f"/api/users/0/items/A{i:02}/fulltext"] = {"content": PRL_UNTITLED_FIXTURE}
    output = tmp_path / "snapshot"
    with local_api(routes) as (port, requests):
        result = subprocess.run([sys.executable, str(SCRIPTS / "build_eval_dataset.py"),
                                 "--collection", "PRL/APS论文素材库", "--output", str(output),
                                 "--seed", "17", "--port", str(port)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "awaiting-agent-review" in result.stdout
    review = materialize(output)
    result = subprocess.run([sys.executable, str(SCRIPTS / "build_eval_dataset.py"),
                             "finalize", "--output", str(output), "--cases", str(review)],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (output / "dataset.json").exists()


def test_fact_packet_rejects_short_copied_sentence():
    with pytest.raises(FactPacketError, match="source wording"):
        validate_fact_packet(["We observe superconductivity."], "We observe superconductivity.")


def test_output_refuses_any_git_checkout_not_only_builder_repository(tmp_path):
    other_repo = tmp_path / "other-repository"
    other_repo.mkdir()
    (other_repo / ".git").mkdir()
    with pytest.raises(BuildError, match="outside the repository"):
        validate_output_root(other_repo / "private", ROOT)


def test_finalizer_detects_changed_abstract_as_source_tampering(tmp_path):
    from build_eval_dataset import export_sources, finalize_dataset

    output = tmp_path / "snapshot"
    export_sources(synthetic_papers(20), output, seed=17, repository_root=ROOT)
    review = materialize(output)
    source_path = output / "sources/P00.json"
    source = json.loads(source_path.read_text())
    source["abstract"] = "Changed fact support after export."
    source_path.write_text(json.dumps(source))
    with pytest.raises(BuildError, match="hash"):
        finalize_dataset(output, review, repository_root=ROOT)


def test_semantic_exclusions_cannot_silently_shrink_dataset(tmp_path):
    from build_eval_dataset import export_sources, finalize_dataset

    output = tmp_path / "snapshot"
    export_sources(synthetic_papers(20), output, seed=17, repository_root=ROOT)
    review = materialize(output)
    records = json.loads(review.read_text())
    records["papers"][0]["cases"] = []
    review.write_text(json.dumps(records))
    with pytest.raises(BuildError, match="20"):
        finalize_dataset(output, review, repository_root=ROOT)
    assert not (output / "dataset.json").exists()
    report = json.loads((output / "build-report.json").read_text())
    assert report["status"] == "insufficient-reviewed-papers"
    assert any(skip["reason"] == "agent-no-eligible-case" and skip["item_key"] == "P00"
               for skip in report["skipped"])


def test_rejected_boundary_report_retains_attachment_hash_without_prose(tmp_path):
    from build_eval_dataset import SourcePaper, export_sources

    rejected = SourcePaper("BAD", "BADATT", "Private synthetic text with no clear boundaries.")
    output = tmp_path / "snapshot"
    report = export_sources((*synthetic_papers(20), rejected), output, seed=17, repository_root=ROOT)
    skip = next(skip for skip in report["skipped"] if skip["item_key"] == "BAD")
    assert skip["content_hash"] == rejected.content_hash
    assert skip["attachment_key"] == "BADATT"
    assert rejected.fulltext not in json.dumps(report)
