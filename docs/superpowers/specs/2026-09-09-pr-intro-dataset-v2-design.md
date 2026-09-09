# PR Introduction dataset v2 and calibrated baseline

Date: 2026-09-09
Status: approved in conversation; pending written-spec review

## Objective

Replace the calibration-failed Introduction dataset with a balanced snapshot
built from every paper in the Zotero collection `PRL/APS论文素材库`, establish a
credible generated baseline no higher than 80, and use retained development
evidence from prior runs to begin the next optimization round.

The workflow uses `gpt-5.6-sol` with `reasoning_effort="low"` for every primary,
child, generator, scorer, coordinator, reviewer, and fixer role. Only an
explicit later user instruction may override that policy.

## Dataset composition

Use all 20 papers in the selected Zotero collection. Materialize exactly two
cases per paper:

- one Structural Continuation Case (SCC), whose continuation can be written
  without an undisclosed research result;
- one Fact-Grounded Continuation Case (FGCC), supplied with a minimal atomic
  fact packet stripped of source wording and rhetorical order.

The snapshot therefore contains 40 cases: 20 SCC and 20 FGCC. Split by paper,
not by case, into 15 development papers and 5 acceptance papers. This gives 30
development cases and 10 acceptance cases, balanced within each split. A paper
and both of its cases remain in exactly one split.

Do not reject, replace, or down-rank a paper because its case appears easy.
Semantic review selects valid Introduction boundaries and case types; it does
not perform a difficulty-admission test.

Write the new immutable snapshot outside Git at
`/home/donk/pr-intro-evals/dataset-v2`. Retain source provenance, extractor
version, exact source hashes, reviewed boundaries, fact packets, split seed,
and case construction records as private artifacts.

## Baseline generation invariant

The published continuation is never a baseline output. For every case, a fresh
isolated Sol-low generator receives only:

- the baseline `pr-intro` runtime;
- `visible_context`;
- `fact_packet` for FGCC;
- the fixed continuation instruction.

It produces a new `baseline_output`. The hidden `reference_continuation`, paper
identity, source text, retrieval handles, and other cases remain inaccessible.
The generator is isolated from network and retrieval tools. Public locators in
the visible material are replaced with `[SOURCE_IDENTIFIER_REDACTED]`; private
item, attachment, or explicitly recorded handles fail closed.

Persist the generated output once. A valid poor answer is not regenerated.
Reject an output as invalid when it reproduces a suspiciously long source span;
record the overlap evidence and infrastructure status. An invalid run may be
retried only with the identical prompt and settings after the isolation defect
is corrected.

Candidate generation later uses the same cases, instruction, model, reasoning
effort, isolation, and output validation. The tested runtime is the only
intentional difference.

## Single-scorer calibration

Use one fresh, fixed Sol-low scorer for the whole baseline annotation pass. The
scorer receives the visible context, hidden reference, generated output, fact
packet when applicable, and the fixed rubric. It never generates the candidate
continuation.

Revise the annotation guidance before freezing the v2 rubric so that:

- score 5 means reference-level argument quality with no identifiable defect;
- generally correct and fluent prose with a real precision, placement,
  completeness, or progression defect receives 3 or 4;
- recap without advancement, generic questions, missing necessary facts, fact
  dumping, misplaced argument endpoints, unsupported extensions, and avoidable
  verbosity receive explicit deductions;
- non-fabrication cannot raise unrelated dimensions;
- every dimension score cites concrete correspondence to the visible context,
  fact packet, and reference argument step.

The final system reports one score set only. After the first blind annotation
pass, compute aggregate, SCC, FGCC, distribution, and dimension frequencies. A
baseline aggregate above 80 is a failed calibration, not a valid frozen result.
Inspect the scorer's high-score rationales, strengthen ambiguous annotation
guidance, and rescore the same fixed outputs from scratch with the same Sol-low
scorer configuration. Never directly decrement labels or transform the scale
to hit the threshold. Freeze the first rubric and score set whose aggregate is
at most 80. Preserve prior calibration attempts privately for audit.

## Prior-run evidence

Mark the v1 dataset and its scores as calibration-failed. Before removal,
distill development-only evidence into v2 provenance:

- preserving the epistemic status of supplied facts improved the first
  development batch but failed one-shot acceptance, so it remains an unproven
  hypothesis rather than an inherited rule;
- forcing continuation to avoid recap caused FGCC regression in the second
  development batch, so that candidate wording is rejected;
- the observed score saturation and cross-run variance motivate the v2 balance
  and annotation calibration.

Do not inspect, transfer, or infer old acceptance case content or per-case
feedback. Old acceptance aggregates may remain in historical run reports but
cannot guide v2 case construction or optimization.

## Next optimization round

After v2 and its baseline are frozen, start optimization in another fresh
Sol-low context that did not construct or score the dataset. Use the retained
development evidence to form a new hypothesis without copying either rejected
candidate rule. Evaluate the candidate on development cases against the fixed
generated baseline and rubric. Run acceptance exactly once only after a
development improvement passes regression checks. Acceptance returns aggregate,
SCC, and FGCC statistics only; it supplies no iterative feedback.

Apply a candidate to the formal runtime only after strict acceptance
improvement, source/dataset/hash verification, and Sol-low review.

## Old-data retirement

After `dataset-v2` and its baseline artifacts pass validation and the retained
development findings are recorded, permanently remove only:

`/home/donk/pr-intro-evals/dataset`

Preserve all old run directories. Mark them historical and non-replayable after
the source snapshot is removed. Do not delete `/home/donk/pr-intro-evals/runs`,
`dataset-v2`, or any repository content.

## Verification

Before reporting completion, verify:

- exactly 20 source papers and 40 cases;
- 20 SCC and 20 FGCC overall;
- development has 15 papers, 15 SCC, and 15 FGCC;
- acceptance has 5 papers, 5 SCC, and 5 FGCC;
- every baseline output was generated and differs from the stored reference;
- no suspicious long reference span or retrieval handle entered a generator;
- one scorer configuration produced the final single score set;
- the frozen aggregate baseline is at most 80;
- v2 provenance contains only development findings from old runs;
- old acceptance content remained isolated;
- deletion targets only the old dataset path after all preceding gates pass;
- repository tests, plugin validation, private permissions, hashes, and the
  formal-runtime apply boundary pass.
