# Hefei-NAMD execution

Load this reference for every Hefei-NAMD or NAMDwithSOC Run. It stages the exact
approved VASP snapshots, validates their interface evidence, renders the Run,
and checks declared products. The approved Spec owns implementation/version,
representation, snapshot set, band window, initial-condition meaning,
observables, and production acceptance. `$calc-review` owns the independent
read-only check of one prepared snapshot.

## Prepare the exact Run

1. Read the Spec, installed implementation/version evidence, its exact current
   source Runs, representative source records, and the maintained software
   profile. Missing representation/window knowledge or competing diagnoses
   stops here and returns to `$calc-to-spec`; never guess a patch from an error
   message.
2. Select the approved source instructions for input and PBS rendering named by
   the Spec. There is no universal NAMD backend template. Render concrete
   `inputs/run.pbs` from those approved source instructions, the exact snapshot
   set, and the configured executable.
3. Render [the common Run
   template](../../../assets/templates/common/run.sh.template) as
   `inputs/run.sh`. Replace `__FINGERPRINT_SOURCE__` with the exact
   server-visible owner path, and replace `__PREPARE_BODY__` and
   `__VALIDATE_BODY__` once each.
4. In `__PREPARE_BODY__`, stage every declared file separately on the server
   with `copy_immutable SOURCE DESTINATION || return 1`. Substitute shell-quoted
   exact paths below this Run's `inputs/`; do not use a wildcard or derive a
   source Run. WAVECAR and CHGCAR remain server-only and excluded from local
   synchronization.
5. Preserve every source VASP Run and treat its files as read-only by convention.
   Preparation may copy declared source bytes into the new
   immutable Run snapshot; it never moves, renames, edits, or deletes source
   `WAVECAR`, `CHGCAR`, or `POTCAR`. Record/check the targeted source identity
   during preparation and recheck it immediately before submission.

In `__VALIDATE_BODY__`, every command ends in `|| return 1` and checks all of
the following for every snapshot, not merely a representative frame:

- every declared source directory and required VASP file is nonempty;
- `OUTCAR` evidence includes effective `ISPIN`, `NKPTS`, `NBANDS`, `LSORBIT`,
  and `LNONCOLLINEAR`;
- `EIGENVAL` includes the band indices and occupations needed to prove the
  approved window and initial band across every frame;
- `RUNDIR`, the staged directory names, representation fields, band fields, and
  `INICON` column count agree with the Spec.

An absent field, out-of-window initial condition, source-identity change, or
inconsistent snapshot blocks validation before review. Representation or band
window changes return to `$calc-to-spec`.

## Render PBS and evaluate evidence

The concrete `inputs/run.pbs` retains the approved source's exact input syntax,
invocation, and operation order while adopting the Run contract from [PBS
execution](../../pbs.md): resolve `PBS_O_WORKDIR`, bind `inputs/`, `outputs/`,
and `logs/`, source the rendered environment, refuse nonempty outputs, stage
only named immutable inputs, execute in `outputs/`, preserve command/failure
logs in `logs/`, and require every Spec-named product. Use the exact Hefei-NAMD
or NAMDwithSOC environment probe from that reference before review and again
immediately before submission.

An interface smoke test establishes only the tested file/representation
contract. It is not production-trajectory validation and cannot replace the
Spec's production observables, acceptance criteria, or submission approval.
Keep failed logs and staged evidence; deletion requires its own explicit user
authorization.
