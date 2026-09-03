# Calculation track to candidate card

Use this route when the user supplies a calculation-maintenance track,
calculation directory, focused run evidence, or an existing `TRK-NNN` candidate
that should be preserved as reusable calculation experience.

## Input boundary

Use only user-provided conversation text, files, or calculation directories.
Use targeted searches and short extracts; never scan conversation history or
read long logs in full. Preserve the source track ID and filename when one
exists. Allocate the next unused `TRK-NNN` identity only for a new candidate.

## Candidate record

Distill each reusable item into these evidence roles:

- **Observation**: what happened, without turning it into a general rule;
- **Evidence**: a short quote or targeted path and what it supports;
- **Conditions and limits**: task context, uncertainty, exceptions, and known
  boundaries;
- **Candidate knowledge**: the smallest reusable implication;
- **Suggested ownership**: the calc skill, reference, script, or template that
  could later apply the knowledge;
- **Proposal status**: whether calc-skill-distillation has proposed or applied
  a user-confirmed skill change.

Merge duplicate evidence into the same candidate. Preserve every substantive
conflict and its limits rather than synthesizing an unsupported rule.

## Candidate write

Write or update only
`/home/donk/plugins/research-knowledge/candidates/cards/calc-project/` and its
`INDEX.md`. Use candidate frontmatter with `name`,
`type: calc-experience-candidate`, `source_plugin: calc-project`,
`status: candidate`, and `updated_at`. Candidate frontmatter is not the formal
ATOM CARD schema.

Candidate writes require human confirmation of the proposed record. They do
not update `cards/INDEX.md` and do not make the record available to ordinary
consumers.

## Formal admission

When the user asks to preserve the distilled result as shared knowledge, start
the normal Cangjie admission flow. Re-evaluate the knowledge object, evidence,
atomicity, applicability, conflicts, type, and tags. Show the proposed formal
card and obtain human confirmation. Only then write a formal card and formal
index entry through `prl-shared` governance. Do not rename a candidate into a
formal card mechanically and do not auto-commit either repository.

