# `paper2ppt` Skill

[中文说明](README.md)

`paper2ppt` is an academic adapter from a paper to PPT Master source material. It reads the paper, organizes an evidence-led story, confirms emphasis with the user, selects and verifies scientific figures, builds a minimal material directory, and invokes the bundled sibling `$ppt-master` normal Generate workflow.

## Workflow

1. Ask for the output location every time.
2. Normalize the paper through `paper-project:liteparse`.
3. Confirm the academic story, emphasis, and key figures.
4. Confirm visual intent without locking a template or page layout.
5. Produce `brief.md`, `paper.md`, `original/`, and optional `images/`.
6. Give the whole directory to PPT Master as ordinary source material.

Paper2ppt itself contains no PPT Master runtime and creates no page-level contract, design specification, SVG, notes file, QA report, or PPTX. The sibling PPT Master remains free to choose page count, template, varied page layouts, SVG implementation, speaker notes, QA, and final PPTX.

## Delivery constraints

`brief.md` records the central message, audience, emphasis, limits, and image provenance. It is editorial guidance, not a machine-readable page plan. Speaker notes are requested by default; animations, transitions, audio, and video are prohibited. Every selected image records `Source` and `Preserve`.

Return to paper2ppt when the paper emphasis or figure selection changes. Use PPT Master for template, page, layout, notes, QA, or PPTX revisions. The bundled skills retain separate ownership and do not share a runtime or automated merge protocol.
