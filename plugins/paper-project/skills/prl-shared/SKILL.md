---
name: prl-shared
description: Internal governance for formal research-knowledge cards and templates. Do not invoke as a standalone user workflow. Cangjie uses it for admission, validation, index maintenance, and formal writes to the configured external repository.
---

# PRL Shared Knowledge Governance

This internal skill governs the external `research-knowledge` content
repository. It is not the content library and is not a standalone user
workflow. Cangjie is the supported formal promotion workflow.

## Repository configuration

Before reading or writing shared content:

1. Read `references/knowledge-source.yaml`.
2. Resolve its fixed repository path (`/home/donk/plugins/research-knowledge`).
3. Read `references/consumer-contract.md`, then the repository's
   `CONSUMER_CONTRACT.md`.
4. For admission, also read `references/admission-contract.md`.
5. Read `cards/INDEX.md`; for physics cards also read
   `cards/physics/PHYSICS_INDEX.md`; for calculation templates read
   `templates/INDEX.md`.

If the repository or a formal resource is unavailable or malformed, warn and
continue the requesting task without shared knowledge. Do not use a bundled
legacy copy and do not read or search `candidates/` during consumption.

## Governance responsibilities

`prl-shared` owns schemas, admission and evolution rules, index rules,
validation, and formal-write boundaries. It does not own consumer task routing
or output quality.

Only Cangjie may promote a candidate into formal content. Promotion requires
human confirmation, a formal file write, the matching formal index update, and
successful validation with:

```bash
python scripts/validate_knowledge_repository.py /home/donk/plugins/research-knowledge
```

Calculation templates additionally require recorded `calc-project`
acceptance. Cangjie reports the knowledge repository's Git revision and dirty
state after a formal write but never commits automatically.

## Formal visibility

A resource is formal only when it exists under `cards/` or `templates/` and is
registered by the relevant formal index. Files under `candidates/`, or formal
files not yet indexed, are not consumable. `updated_at` records the latest
human-maintained knowledge change rather than mechanical formatting.
