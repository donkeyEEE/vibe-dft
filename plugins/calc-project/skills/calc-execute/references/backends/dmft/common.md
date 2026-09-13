# DMFT input and runtime execution

Load this reference for a DMFT input-and-run task. It executes the scientific
commitments already fixed by the approved Spec. `$calc-to-spec` owns the
correlated subspace, PLO/local-orbital basis and orbital order, projection
window, `U`/`J`, double counting, interaction convention, solver settings,
PM/magnetic and one-shot/CSC scope, requested observables, and decisive
criteria. `$calc-review` independently checks one exact prepared snapshot.

## Prepare the exact Run

1. Read the approved Spec, its named DMFT parameter/PLO/troubleshooting records,
   the current upstream Runs, and the maintained software profile. A missing or
   conflicting scientific commitment returns to `$calc-to-spec`; a missing
   executable/profile entry returns to `$calc-setup`.
2. Select the approved source instructions named by the Spec for the program
   invocation and rendering mechanics. The Spec is the sole scientific parameter authority;
   source instructions supply rendering mechanics only and never override or add a missing scientific parameter.
   A conflict with the Spec or a missing commitment stops and returns to
   `$calc-to-spec`. There is no universal DMFT backend template: render concrete
   `inputs/run.pbs` from the approved source instructions and exact Spec
   commitments.
3. Render [the common Run
   template](../../../assets/templates/common/run.sh.template) as
   `inputs/run.sh`. Replace `__FINGERPRINT_SOURCE__` with the exact
   server-visible owner path. Replace `__PREPARE_BODY__` and
   `__VALIDATE_BODY__` once each with the stage-specific commands below.
4. In `__PREPARE_BODY__`, name every approved input source and Run-local
   destination separately. The integration form is
   `copy_immutable SOURCE DESTINATION || return 1`; substitute shell-quoted
   exact paths, including the destination below this Run's `inputs/`. Use the
   same server-only handoff for a Spec-declared HDF5 input. It stays on the
   server and never enters the local project, Git, or synchronization.
5. In `__VALIDATE_BODY__`, use explicit `test`, comparison, or approved
   validation commands for every named input, its expected nonempty state, and
   the committed subspace/basis/order/window/interaction/solver settings. Every
   injected command ends in `|| return 1`. A generic default, filename glob, or
   similarity to an earlier task cannot fill a missing value.

The concrete `inputs/run.pbs` keeps the approved source's program invocation
and method-specific ordering while adopting the Run contract from
[PBS execution](../../pbs.md): resolve `PBS_O_WORKDIR`, bind the Run's
`inputs/`, `outputs/`, and `logs/`, source the exact rendered environment,
refuse nonempty outputs, stage only named inputs, run in `outputs/`, route the
program log to `logs/`, and require the Spec-named products before success.
Do not invent a common solid_dmft command line, scientific solver value, input
filename, or output list. Environment initialization and scheduler resources
may be filled from the maintained software profile or another deterministic
execution source and must be recorded in the Run inputs.

Before review, run `inputs/run.sh prepare` and `inputs/run.sh validate` on the
server and run the exact DMFT environment probe from [PBS
execution](../../pbs.md). HDF5 source identity is rechecked with the upstream
current Run immediately before submission. Any change restarts validation and
review.

## Runtime evidence and acceptance

Keep the full calculation and its HDF5 on the server. Inspect long logs only
with targeted commands and bring back only the exact lightweight text or plot
evidence declared by the Spec. When convergence is in scope, use the Spec-named
`conv_imp<N>.dat`, `observables_imp<N>.dat`, and requested self-energy evidence;
name concrete files for the Run rather than discovering them with a wildcard.

Apply the approved Spec's decisive criteria to that evidence. A clear result
may satisfy or fail the declared criterion. Any ambiguous or conflicting evidence,
or any need to change a physical commitment, stops execution and returns the
evidence to `$calc-to-spec`; it does not justify a guessed threshold, a fake
convergence claim, or a runtime patch.
