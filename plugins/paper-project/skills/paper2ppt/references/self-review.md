# Handoff self-review

Before invoking PPT Master, verify only paper2ppt-owned artifacts:

- `brief.md` states one defensible central message, audience, emphasis, source
  gaps, and limitations without inventing claims or numbers;
- terminology is consistent with the paper and the Terminology Ledger;
- `paper.md` is readable UTF-8 normalized source text;
- every original source is present under `original/`;
- every selected image is readable, scientifically complete, and documented
  in the brief with non-empty Source and Preserve fields;
- the brief requests speaker notes and forbids animations, transitions, audio,
  and video;
- no page count, template, layout, SVG, QA, or PPTX implementation has leaked
  into the handoff.

Run the builder and retain its digest as the preparation receipt. Presentation
self-review belongs to PPT Master after handoff.
