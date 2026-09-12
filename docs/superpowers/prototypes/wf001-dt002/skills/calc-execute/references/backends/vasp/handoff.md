# SCF to band handoff

The band frontier requires an accepted current SCF Run and its non-empty
`CHGCAR`. `CHGCAR` is not a template asset and must not enter Git or local data
sync. After the user confirms its server-side source, the preparation script
copies it into the exact prepared band Run without overwriting an existing
file. If the upstream current Run changes or becomes invalid, the band task is
removed from the frontier and any dependent accepted result needs review.
