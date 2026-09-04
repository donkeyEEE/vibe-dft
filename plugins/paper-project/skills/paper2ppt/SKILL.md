---
name: paper2ppt
description: Use when turning a scientific paper, preprint, article, or reading notes into an evidence-led Chinese presentation through the bundled sibling PPT Master skill.
---

# Paper2PPT Router

`$paper2ppt` is the public paper-reading and interaction entry point. It owns
one serial workflow: [workflows/paper-to-deck.md](workflows/paper-to-deck.md).
It produces a small source-material directory and then invokes the bundled
sibling `$ppt-master`; it does not render slides itself.

## Required load order

1. Read [manifest.yaml](manifest.yaml).
2. Read `references/knowledge-source.yaml`, resolve its `path` relative to that
   file, and read the plugin-local knowledge directory's
   `CONSUMER_CONTRACT.md`, then `cards/INDEX.md` and the formal
   `cards/atoms/write-terminology-ledger.md`. On every new lookup read the
   current working tree; never read or search `candidates/`. If optional
   knowledge is unavailable or malformed, warn and continue without it rather
   than falling back to another location.
3. Read every skill-local file under `always_load` in manifest order.
4. Classify `paper_type` as `discovery`, `methods`, `resource`, `clinical`,
   `materials`, or `review`; use the user's framing first and `discovery` as
   the fallback.
5. Read only the matching paper-type fragment from `axes.paper_type.values`.
6. Execute [workflows/paper-to-deck.md](workflows/paper-to-deck.md) end to end.

Preserve the Terminology Ledger while preparing `brief.md` and `paper.md`.
Never invent results, numbers, methods, citations, or figure details. Once the
handoff begins, PPT Master owns every rendering choice and later interaction.
