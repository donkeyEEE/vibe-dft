---
name: prl-polishing
description: Polish, restructure, or translate scientific prose using compact PRL-style claim, evidence, boundary, and consequence logic. Use for Physical Review Letters manuscripts and for general physics writing that needs evidence-led compression, calibrated claims, model assumptions, controls, quantitative criteria, or main-text/supplement allocation. Also supports publication-quality English and Chinese-to-English polishing without inventing scientific content.
metadata:
  version: 6.3.0
  author: Yuan1z skill, refactored into static/dynamic layers
---

# PRL Scientific Polishing — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (PRL argument logic, core principles, the interactive review protocol, paper-type playbooks, per-section guidance, language-specific rules, and per-journal constraints).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads only the fragments needed for the current job.

Do not try to apply the polishing logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`paper_type`, `section`, `language`, `journal`), the allowed values, and the file paths each value maps to.

Read every file listed under `always_load`. For PRL work, load each applicable
evidence reference declared under `references.on_demand`; those entries name
the exact skill-owned or plugin-shared file. The local
`static/core/prl-argument-logic.md` integrates the reusable workflow, while the
references retain the evidence and caveats for each rule.

Read shared resources from the current plugin tree on each invocation. If an
optional shared resource is unavailable or malformed, warn and continue the
polishing task without substituting another resource source. A missing
skill-owned reference is a plugin packaging defect.

For a managed manuscript or section revision, the always-loaded writing-workspace protocol is a readiness gate: use the managed draft, ensure `zo2notes` has built the user-selected material library, and search relevant material plus active user habits before proposing each paragraph.

### 2. Detect the axis values for this request

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input. Use the shared `write-paper-type-taxonomy` card for the `paper_type` decision:

- `paper_type` — research / methods / hypothesis / algorithmic / review. Default: research.
- `section` — abstract / intro / results / discussion / conclusion / title / methods. May be multiple. Ask the user if it is ambiguous and matters for the polish.
- `language` — en or zh-to-en. Detect from the draft itself.
- `journal` — prl / nature / nat-comms / generic. Default: prl. If the user names a Nature subjournal, treat it as `nature`.

State the detected axis values in one short line to the user before proceeding, so they can correct you cheaply.

### 3. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section` axis only if the user has supplied free-floating prose with no section context.

Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Polish using the loaded material

Apply the loaded fragments in this priority order, matching the `paper type -> central inference -> evidence dependency -> paragraph logic -> claim/evidence/boundary -> sentence polish` rule from `core/failure-modes.md`:

1. PRL argument logic (claim, decisive evidence, boundary, consequence).
2. Paper-type playbook (architecture, writing order).
3. Section-specific job and failure modes.
4. Journal-specific framing and constraints.
5. Language-specific sentence and paragraph rules (apply last).
6. Core stance and ethics throughout.

If a paragraph's structural problem cannot be fixed without inventing content, flag it instead of papering over it.

### 5. Run the interaction protocol

Follow `static/core/interaction-protocol.md` for every prose-polishing job. For
multi-paragraph or section-level input, default to interactive review unless
the user explicitly asks for a one-shot final version. First return a numbered
revision map without rewriting the full draft. After the user confirms the map,
review exactly one paragraph per turn with `Original`, `Proposed`, and `Why
changed`, then wait for a paragraph decision.

Always offer these decisions: accept, revise, keep original, or skip for now.
Treat **keep original** as a locked decision: preserve that paragraph verbatim
in the consolidated text and do not silently normalize it during later edits.
Reopen it only if the user explicitly asks. If the user dislikes the proposed
rewrite and says to retain the original, record that decision and continue to
the next unresolved paragraph.

For a single paragraph, skip the revision-map turn and start with the
side-by-side paragraph review. For explicit one-shot requests, use the direct
output contract in `static/core/output-format.md`.

### 6. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest, for example when the user explicitly asks for phrasebank-style alternatives or a stricter style audit.

**Layout/typesetting (排版) requests are different.** If the user asks to fix
*placement* rather than wording — loose/sparse pages, stranded headings, figures
that don't fill the page or split across pages, "Float too large", multi-panel
arrangement, sparse Supplementary Information — skip the prose axes (paper_type,
section, language, journal) and load `references/latex-layout.md` directly. That
file is self-contained: it carries the diagnosis workflow (render → contact-sheet →
read the log), the float-glue and `[H]`/`\clearpage`/`placeins` patterns, and the
"regenerate wide figures taller at the source" rule. Always compile and visually
inspect rendered pages before and after — never judge layout from the `.tex` alone.

## Why this split

- The static layer is versioned and reviewable. Adding a new journal style or paper type is one new file plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft enter context, instead of the full 1000-line monolith.
- The router itself is short on purpose. Update fragments, not this file, when adding scope.
