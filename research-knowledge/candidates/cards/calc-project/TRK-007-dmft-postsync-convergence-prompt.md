---
name: TRK-007-dmft-postsync-convergence-prompt
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-007: Opt-in DMFT convergence diagnostic after completed sync

## Problem

After a completed DFT+DMFT result pull, the sync workflow did not consistently
ask whether the user wanted the approved convergence plotting script deployed
and the convergence assessed.

## Targeted evidence

- `skills/calc-sync/SKILL.md`
- `skills/dmft-workflow/SKILL.md`
- `tracks/INDEX.md`

## Proposed affected skills and assets

- `calc-sync`: prompt for an optional, user-confirmed convergence diagnostic
  only after a verified completed DFT+DMFT pull with relevant lightweight
  outputs.
- `dmft-workflow`: advise on observables, identify the plotting script, and
  verify only lightweight outputs are produced.
- `script-management`: handle the approved plotting-script deployment after
  the user opts in, under the standard deployment contract.
- `scripts/sync/sync_calc_data.py`: remains transfer-only; no plotting-script
  upload is automated.

## Requested rule

For a verified completed DFT+DMFT task with synchronized `conv_imp*.dat` or
`observables_imp*.dat` results, ask the user whether to upload or deploy the
project-approved convergence plotting script and prepare a diagnostic. Do not
upload, deploy, or run that script without the user's confirmation. Keep HDF5
on the server; only lightweight plots or text data may be pulled.

## Status

Resolved. Implemented in `calc-sync` (post-pull opt-in prompt), `dmft-workflow`
(convergence diagnostic guidance), and routed through `script-management`
(standard deployment contract). The sync script remains transfer-only.

## Versions

- First recorded: `0.1.0+codex.20260724072220`
- Last verified: implemented in dev (not yet released)
