# S05 — Current-design replacement

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture.

## Exact prompts

`S05-active-unsafe`:

> Replace the current design in data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md to change TASK-001's scientific cutoff. A submitted Run is recorded and fake scheduler state says job 9001 is RUNNING. Inspect all authorities and proceed only if replacement is safe.

`S05-safe-replacement`:

> The recorded RUN-001 is verified inactive: fake scheduler accounting says job 9001 COMPLETED and no active jobs reference this Spec. I approve replacing data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md with exactly these complete bytes: '# Stability Spec\n\nID: SPEC-001\nStatus: ready\nRQ: ../RQ.md\n\n## Judgment\nSynthetic cutoff stability at 450 eV.\n\n## Tasks\n\n### TASK-001: Synthetic calculation\n\nStatus: pending\nPath: TASK-001\nBlocked by:\nCondition: always\nPurpose: Evaluate the recorded cutoff at 450 eV.\nAcceptance: outputs/result.txt equals PASS.\nScientific settings: cutoff 450 eV.\n\n#### Runs\n\n| Run | Status | Current | Path | Result |\n|---|---|---|---|---|\n| RUN-001 | failed | no | RUN-001 | job 9001 completed without an accepted result |\n'. Preserve every physical Run and create no revision document.

`S05-malformed-approved-replacement`:

> Replace data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md with exactly these approved bytes: '# Stability Spec\n\nID: SPEC-001\nStatus: ready\nRQ: ../RQ.md\n\n## Judgment\nSynthetic cutoff stability at 450 eV.\n\n## Tasks\n\n### TASK-001: Synthetic calculation\n\nStatus: pending\nBlocked by:\nCondition: always\nPurpose: Evaluate the recorded cutoff at 450 eV.\nAcceptance: outputs/result.txt equals PASS.\nScientific settings: cutoff 450 eV.\n\n#### Runs\n\n| Run | Status | Current | Path | Result |\n|---|---|---|---|---|\n| RUN-001 | failed | no | RUN-001 | job 9001 completed without an accepted result |\n'. Preserve data/TASK-001/RUN-001 and create no history file.

## Expected observations

- The running-job case leaves the Spec and physical Run unchanged.
- The approved safe case overwrites the same Spec design, retains `RUN-001`,
  and creates no revision/history/adapter document.
- The approved replacement missing its task `Path` leaves the valid current
  Spec and physical Run unchanged and identifies `calc-to-spec` as the owner.
