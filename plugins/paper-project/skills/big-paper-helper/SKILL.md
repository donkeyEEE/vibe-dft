---
name: big-paper-helper
description: Use when a user asks to plan, outline, draft, rewrite, integrate, or audit a Chinese 博士论文、大论文或学位论文 in 材料计算, computational materials, first-principles, or DFT/DFT+U/AIMD/DMFT/Wannier/NEGF work. Do not use for journal-only polishing, citation validation, calculation input preparation, or standalone university-format lookup.
---

# Big Paper Helper

## Core principle

Build the dissertation around a traceable chain from 科学问题 (scientific question) to chapter role, direct evidence, mechanism, contribution, and boundary. Treat length as a consequence of complete reasoning, not as a goal.

## Start from the user's scope

Classify the request as one of four modes:

| Mode | Required output |
| --- | --- |
| Plan | Thesis spine, chapter roles, evidence allocation, unresolved decisions |
| Draft | Continuous Chinese academic prose for the requested section |
| Revise | Revised text, material change notes, remaining scientific uncertainty |
| Audit | Findings by severity with location, consequence, and repair direction |

Identify whether the target is the whole thesis, one chapter, one section, or a paragraph. Ask only for missing information that would materially change the scientific structure; otherwise proceed and mark the gap.

## Establish the evidence contract

Before drafting, record the available scientific question, systems, control variables, methods, direct observables, comparisons, controls, numerical results, model boundaries, and intended contribution. Preserve the user's terminology and reported values.

不得编造计算结果、机制、引文、实验验证或学校要求。Missing support is a **证据缺口**, not permission to create a bridge claim. If current university formatting or degree rules matter, require a supplied rule or verify it separately; never infer them from exemplar theses.

Keep these evidence levels distinct:

1. **直接结果** — output actually calculated or observed;
2. **机制解释** — interpretation supported by observables or controls;
3. **应用潜力** — implication that remains conditional on model and validation boundaries;
4. **实验实现** — use only when independent experimental evidence exists.

## Route the knowledge cards

Read [references/INDEX.md](references/INDEX.md) before opening any atom. Select the **最小** relevant tag set:

- whole-thesis structure: `stage/thesis-architecture`;
- abstract: `section/abstract`;
- introduction or literature synthesis: `section/introduction`;
- methods or reproducibility: `section/methods`;
- results, figures, controls, or chapter transitions: `section/research-chapter`;
- conclusion, innovation, terminology, or outlook: `section/conclusion`;
- dynamics, machine-learning potentials, or ballistic transport: add the matching `method/*` tag only when applicable.

Do not load all cards merely because the request concerns a dissertation. Whole-thesis work may read several routes sequentially after the chapter map identifies a concrete need.

The `References` section in each card records how the writing rule was distilled. It is provenance, not a citation recommendation for the user's dissertation; never insert those theses into the bibliography unless the user independently supplies and uses them as sources.

## Workflows

### Whole thesis

1. Build a scientific-question—chapter—evidence—innovation map.
2. State what each chapter inherits and uniquely adds.
3. Check that methods escalate only when a scale, environment, or model boundary requires them.
4. Create chapter-opening contracts and chapter-closing bridges.
5. Audit shared metrics, assumptions, terminology, and claim strength across chapters.

Do not draft a full thesis until its chapter map exposes no orphan chapter, unsupported innovation, or essential evidence with no destination.

### Chapter or section

1. State the section's reader question and its role in the thesis.
2. Select the relevant cards from the index.
3. Arrange supplied evidence in the order required by those cards.
4. Draft coherent paragraphs rather than a bullet-point manuscript.
5. End at the strongest claim the evidence supports, then state the boundary or next dependency.

### Revision or audit

Check scientific function before sentence style. Prioritize broken thesis logic, unsupported claims, incomparable results, missing controls, reproducibility gaps, and result–mechanism–application conflation. Polish wording only after those defects are repaired or reported.

## Handoffs

Use a literature-retrieval or Zotero skill when sources must be found or verified. Use citation validation when checking whether references support claims. Use calculation workflow skills for input preparation or simulation diagnosis. Return here after those tasks to integrate verified evidence into the dissertation.
