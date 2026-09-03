# Paper-to-material handoff workflow

Run these states serially. Paper2ppt owns interaction only until it hands the
material directory to the bundled sibling PPT Master.

## 1. Intake and output location

For every new run, ask the user for an explicit destination with this marker:

`REQUEST_OUTPUT_DIRECTORY`

Do not infer or reuse a destination. Record it as `<output_dir>`; the handoff
will be `<output_dir>/paper2ppt_handoff`.

## 2. First reading and outline confirmation

Use `paper-project:liteparse` to normalize the supplied PDF, Office document,
image, or other source. Retain the untouched source file. Read metadata,
abstract, headings, figure legends, and table captions first. Classify the
paper type, build the Terminology Ledger, and propose an evidence-led story.

Present the paper type, narrative arc, likely claims, key evidence, selected
figures, and known source gaps. This is guidance rather than a fixed slide or
page plan. Stop with exactly:

`⛔ CONFIRM_OUTLINE`

Proceed only after explicit confirmation. Apply requested changes and repeat
this same gate when necessary.

## 3. Focused reading and optional figure preparation

Read the results, methods, validation, and limitations needed by the confirmed
story. Prefer original scientific figures. When a dense figure needs a crop,
use `scripts/figure_assets.py`, visually inspect the crop, and preserve panel
labels, axes, legends, scale bars, and method labels. Each selected image must
be documented in `brief.md` as one list item:

```markdown
- `figure-name.png`
  - Source: Figure/panel and page in the supplied paper.
  - Preserve: panel labels, axes, legends, and essential annotations.
```

## 4. Visual intent confirmation

Present one concise visual direction: audience, tone, density, desired visual
character, and any user-supplied constraints. Do not choose a template or
freeze layouts here; PPT Master needs freedom to interpret the paper. Stop:

`⛔ CONFIRM_VISUAL`

Proceed only after explicit confirmation. Repeat the same gate after edits.

## 5. Build the minimal handoff

Write:

- `brief.md`: central message, audience, emphasis, exclusions, selected-image
  provenance, and delivery constraints;
- `paper.md`: the normalized paper text from `paper-project:liteparse`;
- the untouched source file(s);
- only the selected confirmed images, when any.

The brief must contain `## Central Message`, `## Delivery`, `Include speaker
notes`, and `No animations, transitions, audio, or video`. Build atomically:

```bash
python3 <skill_root>/scripts/build_material_handoff.py \
  --brief <brief_source> \
  --paper-md <normalized_paper_md> \
  --original <original_source> \
  --image <selected_image> \
  <output_dir>/paper2ppt_handoff
```

Repeat `--original` and `--image` as needed; omit `--image` when none is
selected. The resulting directory contains only `brief.md`, `paper.md`,
`original/`, and optional `images/`.

## 6. Invoke PPT Master

Invoke the bundled sibling `$ppt-master` with the handoff directory as
ordinary input to its normal Generate workflow. Do not translate the brief
into a page schema or prescribe implementation details. PPT Master owns page
count, template, layout, SVG authoring, speaker notes, QA, export, and the final
PPTX, as well as every subsequent rendering interaction.

For revisions, follow `revise-deck.md`. For failures before handoff, follow
`failure-recovery.md`; failures after handoff belong to PPT Master.
