# Matt Skills Merge Implementation Plan

> Execute inline with superpowers:executing-plans. The user approved merging all current skills before personal selection; no further design approval is pending.

**Goal:** Consolidate the current software skills into one personally maintained Codex plugin named `matt-skills`.

**Architecture:** Keep each skill and its resources together under the new plugin's `skills/` directory. Preserve all lifecycle states and invocation policies, unify qualified invocations, and replace obsolete dependency checks with direct sibling-skill references.

**Tech Stack:** Markdown, JSON, YAML, Python/pytest, Codex plugin validator.

**Spec:** Approved conversation on 2026-09-05: merge all 25 existing skills with their current states; personal selection and workflow redesign follow later.

## Global Constraints

- Preserve 11 published and 14 explicit-only skills, including their names and invocation policies.
- Keep prior user documentation edits; update their plugin descriptions and links.
- Record historical source-to-target mapping only in `docs/migrations/2026-09-04-plugin-consolidation.md`.
- Modify this source repository only; installation, publication and external marketplace changes are outside this execution.

## Task 1: Merge the publication unit and its consumers

**Files:** `plugins/matt-skills/`, `tests/test_repository_layout.py`, two calc-project-structure consumer documents, root `AGENTS.md`, `CONTEXT.md`, `README.md`, ADR 0002 and a superseding ADR, migration log.

**Interfaces:** One manifest with `name: matt-skills`, `skills: ./skills/`; explicit calls use `$matt-skills:<skill-name>`; one complete `skill-lifecycle.json`.

- [x] Move all skill files without losing supporting resources; combine the lifecycle registries and add a valid manifest and upstream license.
- [x] Rewrite the old qualified invocations and eliminate the two obsolete cross-plugin dependency documents and their pointers.
- [x] Update root/plugin navigation, provenance, consumer references, architecture decision and migration log.
- [x] Adapt repository tests for the merged roster, stale namespaces and resolvable sibling references.
- [x] Run `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py`.
- [x] Validate every moved skill and the plugin using the installed skill/plugin validators; validate a temporary archive extraction as a self-contained plugin.
- [x] Compare every lifecycle entry and invocation policy with the fixed pre-merge Git baseline, check links and `git diff --check`, and record results in the migration log.

Validation found pre-existing `argument-hint` frontmatter in `handoff` and `teach`; retain those input hints in the body so both skills pass the validator. Their lifecycle and invocation metadata remain unchanged.
