---
name: prl-shared
description: Internal developer support for paper-project knowledge cards. Do not invoke as a standalone user workflow. Long-term admission, promotion, and governance remain intentionally open.
---

# PRL Shared Knowledge Governance

This internal skill supports the plugin-local `paper-project/knowledge`
directory. It is not a standalone user workflow. Cangjie is currently a
developer-only workflow; its long-term write and governance model is open.

## Repository configuration

Before reading or writing paper knowledge during development:

1. Read `references/knowledge-source.yaml`.
2. Resolve its `path` relative to `references/knowledge-source.yaml`.
3. Read `references/consumer-contract.md`, then the repository's
   `CONSUMER_CONTRACT.md`.
4. For admission, also read `references/admission-contract.md`.
5. Read `cards/INDEX.md`.

If the repository or a formal resource is unavailable or malformed, warn and
continue the requesting task without plugin knowledge. Do not fall back to
another location and do not read or search `candidates/` during consumption.

## Governance responsibilities

For the current developer workflow, `prl-shared` preserves the existing paper
card schema, index checks, and validation. It does not settle the future
admission, promotion, or governance model and does not own consumer task
routing or output quality.

Cangjie development writes still require human confirmation, a card write, the
matching paper index update, and successful validation with:

```bash
python scripts/validate_knowledge_repository.py ../../../knowledge
```

Cangjie reports the plugin repository's Git revision and dirty state after a
development write but never commits automatically.

## Formal visibility

A resource is formal only when it exists under `cards/` and is registered by
the paper card index. Files under `candidates/`, or formal
files not yet indexed, are not consumable. `updated_at` records the latest
human-maintained knowledge change rather than mechanical formatting.
