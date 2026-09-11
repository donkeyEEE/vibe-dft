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
`plugins/calc-project/knowledge/candidates/cards/calc-project/` and its
`INDEX.md`. Use candidate frontmatter with `name`,
`type: calc-experience-candidate`, `source_plugin: calc-project`,
`status: candidate`, and `updated_at`. Candidate frontmatter is not the formal
ATOM CARD schema.

Candidate writes require human confirmation of the proposed record. They do
not update `cards/INDEX.md` and do not make the record available to ordinary
consumers.

## Future admission

Formal admission is not defined while calc-project knowledge management remains
experimental. Re-evaluate the knowledge object, evidence, atomicity,
applicability, conflicts, type, and tags, then deliver a reviewable proposal.
Do not turn a candidate into a formal card or update a formal index.
