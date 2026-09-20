# PR Introduction

`pr-intro` drafts or restructures evidence-grounded Introductions for the
Physical Review journal family. It always uses `SKILL.md` and the three
references under `references/writing/`.

The skill accepts a user draft or research material. It may retrieve literature
only with the user's explicit permission. Whole-Introduction work produces an
argument map before grounded prose; single-paragraph work may proceed directly.

For multi-paragraph input, the skill first presents a numbered `P1`, `P2`, ...
revision map. After confirmation, it reviews one paragraph at a time with the
complete original and selectable `C1`, `C2`, ... changes containing `Before`,
`After`, and `Why`. Each paragraph may be accepted, revised, kept verbatim, or
skipped before final consolidation. An explicit one-shot request bypasses the
intermediate decisions. Before generated prose is shown, a selective embedded
`$humanizer:humanizer` pass removes AI-writing patterns without changing its
supported scientific content; user originals and locked paragraphs are never
sent to that pass.
