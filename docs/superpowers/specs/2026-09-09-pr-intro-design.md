# PR Introduction Skill Design

## Purpose and scope

Create `pr-intro` as an independent Paper Project skill for drafting and
restructuring Introductions across the Physical Review journal family. The
skill owns a lightweight writing workflow and a dedicated, explicitly invoked
maintenance workflow that improves its runtime instructions through masked
continuation evaluation (MCE).

`pr-intro` supports two runtime modes:

- drafting an Introduction from research material, confirmed facts, or a
  user-selected literature collection;
- diagnosing and restructuring an existing Introduction.

It does not absorb abstract, Results, Discussion, or general manuscript
polishing. It may orchestrate Zotero or research capabilities when the user
allows literature retrieval, but it does not duplicate those implementations.

## Architectural decision

Use one skill with an on-demand maintenance branch. `SKILL.md` distinguishes
ordinary writing from an explicit request to optimize `pr-intro` and loads only
the resources required for that path. The maintenance workflow remains
co-located with its sole consumer.

A second optimizer skill is rejected because optimization has no independent
user-facing purpose and would create roster and invocation ambiguity. A generic
plugin-level optimizer is rejected because there is no second consumer and the
data contract, rubric, and permitted mutations are specific to `pr-intro`.
ADR 0008 records this boundary.

The intended source layout is:

```text
plugins/paper-project/skills/pr-intro/
|-- SKILL.md
|-- README.md
|-- agents/openai.yaml
|-- references/
|   |-- writing/
|   `-- maintenance/
|-- scripts/
|   `-- build_eval_dataset.py
|-- evals/
|   |-- README.md
|   `-- schema.json
`-- tests/
```

Runtime writing does not load eval data, Zotero-derived content, or the
maintenance protocol. Python handles deterministic data acquisition,
extraction, validation, and serialization. The primary agent handles
subagent orchestration, qualitative diagnosis, and candidate instruction
changes.

## Runtime writing contract

Both drafting and restructuring follow the same Physical Review Introduction
logic:

1. establish the research territory and why the problem matters;
2. synthesize relevant progress instead of listing papers;
3. narrow to a specific unresolved problem;
4. explain why the gap is a scientific obstacle;
5. introduce the study's research path;
6. state the contribution and significance only from confirmed material.

The skill first builds an available-facts view containing the research object,
accepted background, dispute or gap, method, principal findings, conditions,
and sources. Missing information remains visible. Fluent Physical Review prose
must not conceal a scientific-content gap.

User material takes precedence over retrieval. When retrieval is explicitly
allowed, newly found background first enters the available-facts view and must
remain traceable to a source before entering prose. Claims of novelty,
generality, mechanism, or an exhaustive research gap require direct support;
otherwise the skill narrows the wording or reports the missing evidence.

For a whole Introduction, the skill proposes a paragraph-level argument map
before drafting or restructuring prose. A single-paragraph request may proceed
directly. Default output consists of the proposed prose, material structural
changes, and unresolved evidence needs. "Physical Review style" means compact,
evidence-led Introduction logic, not imitation of a particular article's
wording.

## Local evaluation dataset

Dataset construction is a separate, explicit maintenance action. It recursively
reads papers from a user-selected Zotero collection and produces a persistent,
gitignored local dataset. Optimization runs consume that dataset without
accessing Zotero. Rebuilding the dataset is the only action that refreshes the
source collection and split.

The default local layout is:

```text
pr-intro-evals/
|-- dataset/
`-- runs/
    `-- <run-id>/
        |-- baseline/
        |-- candidate/
        |-- iterations/
        `-- final-report.md
```

The builder:

1. reads the collection and its descendants;
2. obtains Zotero indexed full text;
3. automatically detects the complete Introduction boundaries;
4. skips papers with unavailable or poor text or uncertain boundaries;
5. creates at most one structural continuation case and one fact-grounded
   continuation case per eligible paper;
6. randomly assigns 15 eligible papers to the development set and five to the
   acceptance set, grouping every case from one paper together;
7. records the random seed, Zotero item and attachment keys, source-content
   hash, extractor version, boundary confidence, and all skip reasons.

The formal dataset requires 20 eligible papers after extraction. If fewer
remain, construction fails rather than silently changing the 15/5 contract. If
more than 20 remain, the recorded random seed selects the 20 included papers;
the build report records the eligible papers that were not selected.
Published Physical Review papers are eligible without a separate prose-quality
screen; the reference continuation is evidence of a real publication path, not
an assertion that it is the only or perfect answer.

### Structural continuation case (SCC)

An SCC contains visible Introduction context and the next complete rhetorical
move as its hidden reference continuation. The hidden move may deepen the
background, synthesize prior work, narrow the question, or establish the gap.
It must not depend on the paper's unknown method, result, or numerical finding.
If no eligible boundary exists, the paper has no SCC.

### Fact-grounded continuation case (FGCC)

An FGCC additionally supplies an atomic fact packet constructed from the
abstract, hidden Introduction, and conclusion. Facts cover the research object,
method, finding, condition, and boundary. They omit source sentence order,
rhetorical transitions, and distinctive wording. A fact omitted or contradicted
across those sources is not included.

### Record and isolation contract

Each complete record contains an anonymous case ID, case type, split, visible
context, optional fact packet, reference continuation, source references, seed,
extractor version, and boundary confidence. The child-agent view removes the
reference continuation, title, authors, DOI, Zotero keys, paths, and all other
retrieval handles. It contains only the anonymous ID, visible context, candidate
runtime instructions, and the FGCC fact packet when applicable.

The source text, fact packets, reference continuations, generated prose, and run
artifacts are local and gitignored. The repository contains only the schema,
instructions, report templates, and synthetic or otherwise redistributable
fixtures.

## Optimization run

Each run snapshots the mutable runtime files into an immutable `baseline/`
tree, then copies that tree to `candidate/`. The mutable-file allowlist covers
`SKILL.md` and designated writing references. It excludes the maintenance
protocol, evaluator, dataset, schema, scripts, scoring rules, and tests. The
primary agent changes only `candidate/` until final application.

The baseline and candidate preserve the skill's relative paths so reference
loading can be validated. Each iteration stores its inputs, outputs, scores,
reasoning, and patch relative to baseline.

### Development loop

Each iteration:

1. samples two SCCs and two FGCCs from the development set;
2. starts isolated child agents without inherited conversation history;
3. gives each child only its sanitized case view and candidate runtime content;
4. compares each continuation with the hidden published continuation;
5. diagnoses failures on fixed dimensions;
6. changes a general instruction only when multiple cases support the defect;
7. records the evidence, rule hypothesis, affected file, and expected effect;
8. reruns previously exercised development cases after a batch improves;
9. accepts the iteration as the new baseline candidate only if regression does
   not show a material loss; otherwise restores the preceding candidate.

A child that returns a valid but poor answer is not resampled. Infrastructure
failure may retry the same call. The loop stops after twelve iterations or
after three consecutive iterations without an acceptable improvement.

### Scoring

The primary agent compares the candidate and published continuation holistically
without persisting rhetorical labels. It scores each applicable dimension from
one to five:

- logical continuation;
- scientific compatibility;
- fact-packet use for FGCC only;
- information density;
- Physical Review expression;
- non-fabrication and boundary control.

SCC scores normalize over five dimensions and FGCC scores over six. All cases
contribute to one aggregate score; SCC and FGCC statistics are also reported
separately. The published continuation is a reference path, and a scientifically
sound alternative structure may receive an equal or better score.

### Acceptance isolation and final application

The development loop cannot inspect acceptance cases. Independent child agents
generate and score baseline and final-candidate outputs for those cases. The
primary agent receives only aggregate total, SCC, and FGCC statistics plus the
pass decision. Per-case acceptance feedback is never used for another
iteration.

The candidate passes when its acceptance aggregate exceeds the original
baseline aggregate. A decline in one case type does not block application but
must be prominent in the report. On success, the system applies only the final
baseline-to-candidate patch to the formal `pr-intro` working tree and does not
commit it. On failure, the formal files remain unchanged and the best candidate
patch remains available for human review.

Before application, the optimizer checks that formal source hashes still match
the run baseline. A mismatch stops the operation rather than overwriting user
changes. Patch application is atomic at the workflow level: a partially
applicable candidate is not treated as applied.

## Failure handling

- Unavailable Zotero, disabled local API, or a missing collection stops dataset
  construction with an exact diagnostic; the builder does not change Zotero
  configuration.
- Missing indexed text, poor text, or uncertain Introduction boundaries skip a
  paper and appear in the build report.
- A split that separates cases from one paper invalidates the dataset.
- An empty, contradictory, or source-wording-leaking fact packet invalidates its
  FGCC.
- Exposure of reference text, source identity, retrieval handles, or parent
  conversation history invalidates a child run.
- A missing or malformed score prevents candidate mutation for that iteration.
- Formal-source drift prevents final application.

## Verification strategy

Automated tests cover:

- SCC and FGCC schema requirements;
- Introduction extraction with titled, untitled, run-in-heading, noisy
  two-column, and ambiguous-boundary fixtures;
- SCC exclusion of unknown-result dependencies;
- FGCC atomization and source-wording leakage checks;
- removal of references and source identity from child-agent views;
- 15/5 paper-level grouping and recorded random seeds;
- baseline immutability and mutable-file allowlisting;
- SCC and FGCC score normalization and aggregate consistency;
- iteration rollback, development regression, three-failure early stopping,
  and the twelve-iteration cap;
- no formal mutation on failed acceptance;
- candidate-only patch application on successful acceptance;
- formal-source drift protection;
- ordinary-writing routing that does not load maintenance resources.

CI uses synthetic or redistributable fixtures and mocked agent outputs. Access
to the user's Zotero library and live child-agent evaluation remain explicit
local acceptance operations.

## Documentation and repository effects

Implementation will add the skill README, runtime and maintenance references,
dataset schema and builder instructions, and tests. Root `CONTEXT.md` defines
MCE, the development and acceptance sets, SCC, and FGCC. ADR 0008 explains the
single-skill boundary. No source paper or local evaluation run enters Git or
the Paper Project publication package.
