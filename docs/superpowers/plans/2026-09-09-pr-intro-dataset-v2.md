# PR Introduction Dataset v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a private 20-paper, 40-case balanced Introduction dataset and a genuinely generated, single-scorer Sol-low baseline with aggregate score at most 80 for user inspection.

**Architecture:** Repository code owns deterministic validation, sanitization, scoring arithmetic, and the frozen annotation contract. A fresh dataset coordinator owns semantic case construction from Zotero-derived sources; a separate fresh baseline coordinator owns isolated generation and one-scorer calibration. Private artifacts remain outside Git, and the old dataset is removed only after v2 verification succeeds.

**Tech Stack:** Python 3.11, pytest, JSON Schema, Codex CLI, bubblewrap, Zotero local API through read-only `curl.exe` transport.

**Spec:** `docs/superpowers/specs/2026-09-09-pr-intro-dataset-v2-design.md`

## Global Constraints

- Every agent role uses `gpt-5.6-sol` with `reasoning_effort="low"`.
- Use all 20 papers from Zotero collection `PRL/APS论文素材库`.
- Produce one SCC and one FGCC per paper; split by paper into 15 development and 5 acceptance papers.
- Hidden published continuations are evaluator-only and never generated baseline outputs.
- Use one scorer for the complete final annotation pass and report one score set.
- Baseline aggregate above 80 is calibration failure; never transform or directly decrement labels.
- Do not expose old or new acceptance case content to the optimizing controller.
- Delete only `/home/donk/pr-intro-evals/dataset`, after v2 and baseline verification.

---

### Task 1: Encode balanced-v2 contracts

**Files:**
- Modify: `plugins/paper-project/skills/pr-intro/scripts/eval_model.py`
- Modify: `plugins/paper-project/skills/pr-intro/scripts/build_eval_dataset.py`
- Modify: `plugins/paper-project/skills/pr-intro/evals/schema.json`
- Modify: `plugins/paper-project/skills/pr-intro/evals/README.md`
- Test: `plugins/paper-project/tests/pr_intro/test_eval_model.py`
- Test: `plugins/paper-project/tests/pr_intro/test_dataset_builder.py`

**Interfaces:**
- Consumes: `Dataset`, `EvalCase`, `build_dataset`, and `sanitized_case_view`.
- Produces: a strict v2 mode requiring 20 papers with one SCC and one FGCC each and balanced 15/5 paper splits.

- [ ] Write failing tests that reject missing/duplicate types and assert 15/15 development plus 5/5 acceptance counts.
- [ ] Run `pytest plugins/paper-project/tests/pr_intro/test_eval_model.py plugins/paper-project/tests/pr_intro/test_dataset_builder.py -q` and verify RED.
- [ ] Implement the minimum opt-in v2 validation and record the invariant in the build report while preserving v1 reading compatibility.
- [ ] Run `pytest plugins/paper-project/tests/pr_intro -q` and verify GREEN.
- [ ] Commit with `git commit -m "feat: validate balanced pr-intro datasets"`.

### Task 2: Calibrate the single-scorer annotation contract

**Files:**
- Modify: `plugins/paper-project/skills/pr-intro/references/maintenance/scoring-rubric.md`
- Modify: `plugins/paper-project/skills/pr-intro/references/maintenance/optimization-protocol.md`
- Test: `plugins/paper-project/tests/pr_intro/test_skill_contract.py`

**Interfaces:**
- Consumes: the existing dimension identifiers and `normalized_score` arithmetic.
- Produces: one-scorer ceiling discipline and the `aggregate <= 80` calibration gate.

- [ ] Write a failing contract test for rare score-5 use, mandatory deductions, dimension independence, concrete evidence, one scorer, and prohibition on score transformation.
- [ ] Run the focused test and verify RED.
- [ ] Add concise annotation rules without changing dimensions or normalization.
- [ ] Run `pytest plugins/paper-project/tests/pr_intro -q` and verify GREEN.
- [ ] Commit with `git commit -m "docs: calibrate pr-intro baseline scoring"`.

### Task 3: Build and freeze dataset-v2

**Files:**
- Create privately: `/home/donk/pr-intro-evals/dataset-v2/`
- Create privately: `/home/donk/pr-intro-evals/dataset-v2/prior-development-findings.json`
- Preserve until Task 5: `/home/donk/pr-intro-evals/dataset/`

**Interfaces:**
- Consumes: the exact Zotero collection, current extractor, and strict v2 finalizer.
- Produces: immutable `dataset.json`, source/review artifacts, build report, hashes, and development-only historical findings.

- [ ] Start a fresh Sol-low dataset coordinator with no inherited context; any children must also be Sol-low.
- [ ] Export all 20 collection papers read-only into the new private directory.
- [ ] Materialize one reviewed SCC and one reviewed FGCC per paper, with minimal paraphrased facts and exact source boundaries.
- [ ] Finalize with a new recorded seed and verify 20 papers, 40 cases, 20/20 type balance, and 15/5 balanced paper splits.
- [ ] Persist only old development findings: epistemic-status hypothesis unproven after acceptance, recap rule rejected after FGCC regression, and score saturation/cross-run variance.
- [ ] Obtain a fresh Sol-low review of hashes, permissions, provenance, contiguity, leakage, and counts without exposing acceptance content to this controller.

### Task 4: Generate, score, and calibrate baseline

**Files:**
- Create privately: `/home/donk/pr-intro-evals/baselines/dataset-v2-sol-low/`
- Read: `/home/donk/pr-intro-evals/dataset-v2/dataset.json`
- Read: `plugins/paper-project/skills/pr-intro/`

**Interfaces:**
- Consumes: frozen v2 cases, formal runtime, fixed generation instruction, and calibrated rubric.
- Produces: 40 generated outputs, isolation records, one score set, distribution report, calibration audit, and frozen hashes.

- [ ] Freeze runtime, dataset, `gpt-5.6-sol`, `reasoning_effort="low"`, prompt, and rubric hashes.
- [ ] Generate one baseline output per case in fresh OS isolation; each generator sees one sanitized case and runtime, never its reference.
- [ ] Reject exact reference equality or suspicious long-span overlap and preserve evidence without returning acceptance text.
- [ ] Have one fresh Sol-low scorer annotate all fixed outputs with raw dimensions and concrete evidence.
- [ ] If aggregate exceeds 80, preserve the failed pass, clarify only annotation guidance, and rescore the same outputs; never regenerate or transform scores.
- [ ] Freeze the first valid score set at or below 80 and report development, acceptance, overall, SCC, FGCC, distributions, model audit, overlap audit, and hashes. Return acceptance aggregates only.

### Task 5: Retire v1 and verify handoff

**Files:**
- Delete after gates: `/home/donk/pr-intro-evals/dataset/`
- Preserve: `/home/donk/pr-intro-evals/runs/`
- Mark privately: old runs historical and non-replayable.

**Interfaces:**
- Consumes: verified v2 and frozen baseline.
- Produces: one unambiguous active dataset/baseline pair for inspection.

- [ ] Mechanically verify every count, model setting, hash, output/reference inequality, overlap threshold, score record, aggregate threshold, and permission.
- [ ] Run `pytest plugins/paper-project/tests -q`.
- [ ] Run `python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/paper-project`.
- [ ] Run `python3 -m compileall -q plugins/paper-project/skills/pr-intro/scripts` and `git diff --check`.
- [ ] Inventory and hash the exact old dataset, then remove only `/home/donk/pr-intro-evals/dataset` after all prior gates pass.
- [ ] Confirm v2/baseline remain readable, old runs remain and are marked non-replayable, and request final Sol-low review.
