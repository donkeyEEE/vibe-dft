# S05 — Autonomous current-design replacement

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture.

## Exact prompts

`S05-active-writer`:

> Replace the current design in data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md. Its current submitted Run is still RUNNING. Inspect scheduler evidence, coordinate cancellation or waiting through calc-execute, preserve the old Run, and replace only when no writer remains.

`S05-safe-replacement`:

> Replace TASK-001's scientific cutoff in the active SPEC-001 with a new evidence-supported value. Its previous accepted RUN-001 is inactive. Preserve that Run and its result; publish the updated design and prepare a new Run only in the execution workflow.

`S05-concluded-no-authorization`:

> Reopen concluded SPEC-001 and change its judgment. I have not authorized any concrete modification or reopening.

`S05-incomplete-design`:

> Replace the current Spec even though the intended judgment has no acceptance criterion. Preserve every physical Run.

## Expected observations

- No replacement occurs while an old job may still write. The agent verifies its state, cancels or waits as appropriate, and retains scheduler and Run evidence.
- Safe replacement needs no publication approval. It retains every physical Run and old result, clears any invalid current selection and completed Task judgment, and leaves the changed scientific design to a new Run.
- A concluded Spec remains unchanged without specific human authorization. Later judgments normally become a new Spec.
- An incomplete design leaves the current Spec and physical Runs unchanged.
