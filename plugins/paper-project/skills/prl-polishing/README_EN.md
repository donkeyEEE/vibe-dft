# `prl-polishing` skill

[中文说明](README.md)

`prl-polishing` polishes, restructures, or translates physics manuscripts using compact PRL argument logic while preserving the author's facts, evidence boundaries, and citation intent.

## Core logic

The skill reconstructs the inference before editing sentences:

`condition or question -> central claim -> decisive evidence -> boundary -> physical consequence`

It checks whether predictions are distinguished from observations, mechanism claims have discriminating controls, quantitative claims retain their operational definitions and uncertainty, model assumptions remain visible, and the main text contains every indispensable logical link.

## Outputs

- A numbered revision map before editing multi-paragraph input.
- One-paragraph-at-a-time `Original` / `Proposed` / `Why changed` review.
- Explicit accept, revise, keep-original, and skip decisions for every paragraph.
- Consolidated prose only after paragraph decisions, plus unresolved evidence boundaries.
- Direct polished prose and revision notes when the user explicitly requests one-shot mode.

## Boundaries

The skill does not invent data, mechanisms, statistics, citations, or novelty. Corpus-derived patterns are writing defaults rather than APS mandates; current official APS guidance controls submission requirements.
