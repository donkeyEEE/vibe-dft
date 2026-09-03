---
name: TRK-012-calculation-note-scope-boundary
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-012: Calculation-note scope boundary

## Problem

When calculation notes have already fixed the problem to solve, its diagnostic
purpose, and the stopping condition, later review can still drift into proposing
additional comparisons or calculations that answer a broader question. This can
turn an already completed diagnostic into an open-ended campaign and conflict
with the calculation notes as the project authority.

## Targeted evidence

- User-provided instruction in the 2026-08-11 FGET/FGAT DMFT discussion:
  “在计算笔记已经敲定需要解决某个问题时，不要随意扩展计算问题。”
- `01DFT+DMFT/03-计算笔记/beta116-FM符号诊断-实施计划.md` states that
  the density-basis threshold branch is complete, is diagnostic rather than a
  formal physical comparison, and must not automatically create or submit
  follow-up jobs.
- `01DFT+DMFT/04-问题排查/beta116-FM符号问题与后续测试方案.md` records the
  completed `0.01/0.02/0.05` diagnostic and limits the conclusion to numerical
  sign-problem relief.

## Proposed affected skills and assets

- `calc-workflows`: should evaluate a general scope-control rule when routing
  work from an existing calculation note.
- Method workflow skills (`vasp-workflow`, `dmft-workflow`,
  `magnetic-workflow`, and `namd-workflow`): should evaluate the same boundary
  when interpreting method-specific notes and troubleshooting records.
- `calc-project-structure`: should evaluate whether the calculation-note
  convention needs an explicit problem boundary and stopping-condition field.

## Requested candidate rule

Before recommending new calculations from an existing calculation campaign,
identify the problem, decision criterion, and stopping condition already fixed
by the authoritative calculation notes. If that problem has been answered under
the recorded criterion, stop at consolidation and reporting. Do not make a
broader mechanism question, production-quality validation, parameter campaign,
or new comparison a required next step unless the notes already require it or
the user explicitly confirms the expanded scope.

New contradictory evidence or a prerequisite strictly necessary to answer the
same recorded problem may be raised, but it must be labelled as such and must
not silently redefine the project question.

## Status

Resolved. `calc-workflows` now stops after a settled note criterion rather than
expanding the question, and method workflows preserve that boundary. The
calculation-note template records optional problem, criterion, and stopping
condition fields.

## Versions

- First recorded: `0.1.0+codex.20260807073201`
- Last verified: plugin references and focused regression tests on 2026-08-11

## Distilled experience

### EXP-001: respect-settled-note-scope

#### Observation

After the beta116 FM threshold diagnostic had met its recorded purpose, a review
incorrectly promoted optional physical-validation comparisons into an immediate
next step.

#### Evidence

The user explicitly corrected the scope and stated: “在计算笔记已经敲定需要解决某个问题时，
不要随意扩展计算问题。” The two targeted project notes above show that the
threshold branch was already complete and diagnostic-only.

#### Conditions and limits

This applies when authoritative calculation notes clearly define the problem and
its completion boundary. It does not prohibit reporting contradictory evidence,
performing validation already required by the notes, or discussing an expanded
question after explicit user confirmation.

#### Candidate knowledge

Treat the settled calculation-note problem boundary as the default scope for
analysis and recommendations; once its recorded criterion is met, consolidate
rather than inventing mandatory follow-up calculations.

#### Suggested ownership

`calc-workflows`, with corresponding review by `calc-project-structure` and the
method workflow skills.

#### Proposal status

Implemented in `calc-workflows`, the four method workflows, and the
calculation-note template; verified by `test_workflow_handoff.py` and
`test_template_copy_preflight.py`.
