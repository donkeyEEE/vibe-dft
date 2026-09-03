---
name: calc-skill-distillation
description: Use when user-selected formal or calc candidate cards need reviewable change proposals and user-confirmed Calc Project skill maintenance.
---

# Calc Skill Distillation

Turn user-selected knowledge cards into narrowly scoped, reviewable Calc
Project skill changes. Cangjie owns evidence intake, candidate-card writes, and
formal knowledge admission; this skill only maintains calc plugin behavior from
cards the user selects.

1. Read [knowledge-source.yaml](references/knowledge-source.yaml), then the
   external consumer contract and [proposal contract](references/proposal-contract.md).
2. Read only the formal cards or
   `candidates/cards/calc-project/` cards explicitly selected by the user. This
   candidate access is a governance exception for this skill; do not scan the
   candidate directory, conversation archives, or unrelated plugin sources.
3. Read the exact target skill or reference. Check the card's evidence,
   conditions, limits, conflicts, suggested ownership, and whether the target
   already implements the knowledge.
4. Create one complete `PRP-NNN` proposal with a user-visible diff for one
   exact target file. Never combine target files in one proposal.
5. Present each proposal and wait for an explicit decision.
   Do not implement or modify a target file before the user explicitly accepts
   that proposal.
6. Implement only accepted proposals, run the stated targeted test and plugin
   validator, and report the result. Do not edit candidate or formal cards;
   route knowledge changes back to Cangjie.

Do not update a cachebuster, reinstall or publish the plugin, scan sources
automatically, operate on remote jobs, or modify task data without separate
user approval. Never generalize a task-specific parameter beyond the selected
card's evidence and conditions.
