# Output and quality contract

Paper2ppt publishes exactly one minimal source-material directory:

```text
paper2ppt_handoff/
├── brief.md
├── paper.md
├── original/
└── images/        # optional
```

`brief.md` captures the central message, audience, emphasis, exclusions,
selected-image provenance, speaker-notes request, and the prohibition on
animations, transitions, audio, and video. `paper.md` is normalized source
text. `original/` preserves at least one untouched input. `images/` contains
only confirmed selected assets with Source and Preserve entries in the brief.

The builder rejects symlinks, undocumented images, duplicate destination
names, and non-empty destinations. It returns a deterministic content digest.
Paper2ppt must not add a page plan, design files, slide source, notes files, QA
reports, or presentation exports. PPT Master owns page count, template, layout,
SVG, speaker notes, QA, and the final PPTX after handoff.
