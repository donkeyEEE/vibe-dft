# Workflow spine

The sole executable procedure is `../../workflows/paper-to-deck.md`. Its states
are, in order: `intake`, `output-directory-request`, `outline-confirmation`,
`asset-preparation`, `visual-confirmation`, `materialized`, `svg-authoring`,
`engineering-qa`, `scientific-qa`, `published`, and `revision`.

The output-directory request is required intake, not a confirmation gate. The
workflow has exactly two blocking chat confirmations: outline, then visual
identity. An explicit affirmative response is required at each; silence never
advances the run.

After materialization, author P01, pass the first-page quality gate, then author
P02 through Pnn continuously before final checks. Rendering and revisions use
the linked workflow contracts rather than direct slide authoring APIs.
