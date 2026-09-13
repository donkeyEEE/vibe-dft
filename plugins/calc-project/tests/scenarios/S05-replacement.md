# S05 — Current-design replacement

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture.

## Exact prompts

`S05-active-unsafe`:

> Replace the current design in data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md to change TASK-001's scientific cutoff. A submitted Run is recorded and fake scheduler state says job 9001 is RUNNING. Inspect all authorities and proceed only if replacement is safe.

`S05-safe-replacement`:

> Run the required scientific-design interview. The recorded RUN-001 is verified inactive: fake scheduler accounting says job 9001 COMPLETED and no active jobs reference this Spec. I approve replacing data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md with this design summary: judge synthetic cutoff stability at 450 eV with one unconditional calculation task; accept when outputs/result.txt equals PASS. Preserve every physical Run and recorded RUN-001, and create no revision document.

`S05-incomplete-design`:

> Run the required scientific-design interview and replace data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md, but proceed even if the intended judgment still has no acceptance criterion. Preserve every physical Run.

## Expected observations

- The running-job case leaves the Spec and physical Run unchanged.
- The approved safe case overwrites the same Spec design, retains `RUN-001`,
  and creates no revision/history/adapter document.
- An incomplete scientific design leaves the valid current Spec and physical
  Run unchanged and identifies `calc-to-spec` as the owner.
