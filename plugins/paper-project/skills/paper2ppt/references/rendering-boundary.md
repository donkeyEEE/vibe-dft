# Rendering boundary

Paper2ppt owns paper interpretation, terminology, evidence selection, two chat
confirmation gates, and the minimal handoff directory. It must not choose or
copy a template, dictate page count or layouts, author slide SVG, generate
speaker-note files, perform presentation QA, or export PPTX.

The bundled sibling `$ppt-master` receives the directory as ordinary
source material through its normal Generate workflow. PPT Master owns all
rendering decisions and all later interaction. The brief expresses intent, not
a machine-readable page contract.

Speaker notes are requested. Animations, transitions, auto-advance, narration
audio, and video are forbidden. These constraints travel as prose in
`brief.md`; paper2ppt does not enforce them by embedding a renderer.
