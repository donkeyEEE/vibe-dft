# Calc Project Six-Skill Replacement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the nine legacy Calc skills with the six accepted explicit-only interfaces, preserving method knowledge and moving execution to Spec-owned tasks and Run-local inputs.

**Architecture:** RQ/Decision Ticket/Spec coordination remains an agent workflow over minimal Markdown. Deterministic scripts implement only preparation, checks, environment probes, plotting and reviewed synchronization; there is no new workflow engine or domain schema. Runtime resources belong to their consuming skills, and all six interfaces are delivered in one atomic source cutover.

**Tech Stack:** Markdown, Codex `agents/openai.yaml`, Bash/PBS, existing Python helpers, pytest, PyYAML, NumPy and Matplotlib; Python standard-library tooling for local acceptance packaging. Reuse existing dependencies; do not install into the user's environment automatically.

**Spec:** [Accepted migration route](../../../.scratch/calc-project-rq-redesign/migration-and-acceptance-route.md), [WF-001 map](../../../.scratch/calc-project-rq-redesign/map.md), and [Tracker/document design](../specs/2026-09-11-calc-rq-tracker-design.md). Read all six resolved tickets linked by the map before execution; DT005 is the exhaustive source-to-owner mapping.

**Status:** Proposed implementation plan; full WF-001 design approved by the user on 2026-09-11.

## Global Constraints

- Exactly `ask-dnk`, `calc-setup`, `calc-rq`, `calc-to-spec`, `calc-execute`, `calc-review`; all six use `policy.allow_implicit_invocation: false`.
- Implementation branch: `implement/wf001-calc-roster`; worktree: `/home/donk/yz-skills/.worktrees/wf001-implementation`; baseline: `3e5cadc7f8343aedc462bc3df5ae4d123ee8ad58`.
- Preserve v0.1 at `62655370bbe884ab9df4c6fc94ae9908c882bdef` and v0.2 at `3e5cadc7f8343aedc462bc3df5ae4d123ee8ad58` in their accepted archive worktrees. Preserve the prototype branch at `ef0cd84641a8489f17d2cbad5184edc31df85d97`.
- Spec is the sole task/DAG/Run/current-Run/execution/closure authority. Tracker is a per-RQ directory convention. No task-domain YAML, task README authority, TASK.md, RUN.md, WORKFLOW.md state, NOTE-doing.md, required PROJECT_PLAN.md, Spec revision history or compatibility adapter.
- Inputs are `TASK-…/RUN-…/inputs/`; every Run has `inputs/run.sh`, `inputs/run.pbs`, `outputs/`, `logs/`. Flow: prepare → validate → calc-review → submit unchanged inputs.
- `calc-sync.yaml` contains only `local`, `server`, `exclude`; reviewed-plan TTL remains 30 minutes. HDF5, CHGCAR and WAVECAR stay server-side. Preserve old Runs even for individually approved overwrite-style recomputation.
- Follow DT001 approval gates verbatim. A checksum is not approval; a script flag is not proof of a review. Review is transient, read-only and exact-snapshot-specific; no persisted review verdict or reusable authorization token.
- `calc-rq` retains `$dev-engineering:grill-with-docs`; verify its dependency chain in the execution environment. User explicitly deleted the blanket test forbidding `dev-engineering` references. Do not restore it.
- Runtime branches name exact files; no runtime resource-directory discovery. Test/packaging inventory and scanning a concrete Run's input files are permitted and are not backend discovery.
- Scope excludes scientific-data migration, real cluster jobs, external installation/publication and unrelated plugin changes. Synthetic remote fixtures must never contact real hosts.
- The user approved WF-001 design. This plan is a separate review artifact; implementation starts after plan approval.
- The accepted atomic-cutover requirement overrides the skill's generic frequent-commit advice: review each task, but keep the final delivered replacement as one complete commit. Do not add implementation commits to the prototype branch.

## Source and file ownership

All paths below are repository-relative. Braces explicitly enumerate files; they are not runtime discovery instructions.

| Owner | Target files and responsibility |
|---|---|
| Six skills | `plugins/calc-project/skills/{ask-dnk,calc-setup,calc-rq,calc-to-spec,calc-execute,calc-review}/{SKILL.md,agents/openai.yaml}` — exact DT001 interfaces and invocation metadata |
| setup | `skills/calc-setup/references/{project-context,project-structure,cluster-software-profiles}.md`; `scripts/verify_cluster_profile.sh`; `tests/test_setup.py` |
| rq | `skills/calc-rq/references/{rq-template,decision-ticket-template}.md`; `tests/test_rq_contract.py` |
| spec | `skills/calc-to-spec/references/spec-template.md`; `references/backends/{vasp,vasp-mae,dmft,namd,magnetic,energy-mapping,wannier90}.md`; `tests/test_spec_contract.py` |
| execute workflow | `skills/calc-execute/references/{run-preparation,pbs,sync,remote-completion,task-advancement,simple-correction}.md`; SKILL handles one whole ready/active Spec |
| execute backend | `references/backends/vasp/{common,scf,band,handoff,wannier-prerun,mae}.md`; `dmft/{common,postprocessing}.md`; `namd/{common,namdwithsoc}.md`; `wannier90/common.md`; `tb2j/common.md`; `vampire/{common,handoff}.md` |
| execute templates | `assets/templates/common/run.sh.template`; `vasp/cluster-env.sh.template`; `vasp/{scf,band,wannier-prerun}/run.pbs.template`; `vasp/wannier-prerun/cluster-env.sh.template`; `wannier90/{cluster-env.sh.template,run.pbs.template,wannier-run.env.template}`; `tb2j/{cluster-env.sh.template,run.pbs.template}`; `vampire/{cluster-env.sh.template,run.pbs.template}` |
| execute helpers | `scripts/fingerprint_run.py`; `scripts/probe-run-environment.sh`; `scripts/sync/sync_calc_data.py`; `scripts/vasp/{compare_incar_parameters.sh,plot_vasp_band.py}`; `scripts/wannier90/{vest2.py,plot_wannier_fit_up.py,plot_wannier_fit_dn.py}`; `scripts/vampire/{plot.py,pack_magnetic_results.sh}` |
| review | `skills/calc-review/references/{pre-submit,pbs}.md`; `references/backends/{vasp,vasp-magnetic,dmft,namd,wannier90,tb2j,vampire}.md`; `tests/test_review_contract.py` |
| Dev-only | `plugins/calc-project/conftest.py`; `tests/{test_roster,test_paths,test_migration_inventory,test_package}.py`; `tests/build_acceptance_package.py`; `tests/fixtures/migration_inventory.json`; `tests/scenarios/*.md` (exact scenario files listed in Task 11) |
| Root | `tests/test_repository_layout.py` (currently ignored, explicitly track this file only), `AGENTS.md`, `CONTEXT.md`, `README.md`, Calc manifest; verify existing marketplace source stays unchanged |

Owner-relative paths in rows after “Six skills” are under `plugins/calc-project/`. Copy existing scientific content only according to DT005; do not author new physical defaults. Retained `vest2.py` initially stays byte-identical; only its exact tested invocation is exposed.

## Execution checkpoints

Tasks 1–2 establish G0/G1; Tasks 3–10 build the G2 candidate; Tasks 11–12 establish G3/G4 evidence; Task 13 performs G5. A task's green local test is not permission to deliver a partially replaced roster. Target-roster tests may remain red until Task 10; keep the failures visible and explain their expected cause.

### Task 1: Create the implementation worktree and carry the approved design

**Files:** Read main-workspace `AGENTS.md`, `CONTEXT.md`, `docs/agents/{issue-tracker,domain}.md`, map, six tickets and route; preserve the modified Tracker design and root context. Create only the approved implementation worktree and its copies of design inputs.

**Interfaces:** Consumes the two pinned archive refs and accepted design documents. Produces the exact v0.2 implementation branch with the accepted design available locally; no runtime change.

- [ ] Read `superpowers:using-git-worktrees`; check current status, existing worktrees, target path and branch. Run route G0 checks from `/home/donk/yz-skills`; reject any archive mismatch. Confirm `.worktrees/` is ignored.

```bash
git status --short --branch
git worktree list --porcelain
git check-ignore .worktrees
git branch --list implement/wf001-calc-roster
```

- [ ] If the target branch/path are absent, create exactly this worktree; if already present, inspect and resume only if its provenance and changes match this plan.

```bash
git worktree add -b implement/wf001-calc-roster /home/donk/yz-skills/.worktrees/wf001-implementation 3e5cadc7f8343aedc462bc3df5ae4d123ee8ad58
```

- [ ] Read and transfer the exact accepted map, six tickets, route, this plan and modified Tracker design through explicit file edits. Carry the current root `CONTEXT.md` additions before changing Calc-specific references. These ignored files do not automatically travel with Git; compare source and destination contents. Keep all changes in the original worktree intact.
- [ ] Run the tracked baseline test from the new worktree. Expected: one old template-contract test passes; this is baseline evidence, not target acceptance.

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider plugins/calc-project/tests/resources/test_calculation_templates.py
git diff --exit-code 3e5cadc7f8343aedc462bc3df5ae4d123ee8ad58 -- plugins/calc-project
```

Stop this checkpoint if the baseline fails; report the concrete failure. Do not copy old prototype inputs or merge its branch to make tests pass.

### Task 2: Establish tracked test support and exhaustive source accounting

**Files:** Create `plugins/calc-project/conftest.py`, `tests/{test_roster,test_paths,test_migration_inventory}.py`, `tests/fixtures/migration_inventory.json`. Copy and explicitly stage the current edited root `tests/test_repository_layout.py` with `git add -f tests/test_repository_layout.py`; the removed blanket reference check stays absent.

**Interfaces:** Fixture `plugin_root: Path` selects source or an explicit extracted package. Fixture `load_script(relative: str) -> ModuleType` imports the named script from that root. Test-only inventory maps each of the 65 baseline Calc paths to concrete target paths or DT005's removal reason; it is never read at runtime.

- [ ] Add shared fixture code at the plugin root so both plugin tests and owning-skill tests inherit it:

```python
import importlib.util
import sys
from pathlib import Path
import pytest

def pytest_addoption(parser):
    parser.addoption('--calc-plugin-root', default=None)

@pytest.fixture
def plugin_root(request):
    value = request.config.getoption('--calc-plugin-root')
    return Path(value).resolve() if value else Path(__file__).resolve().parent

@pytest.fixture
def load_script(plugin_root):
    def load(relative):
        path = plugin_root / relative
        spec = importlib.util.spec_from_file_location('calc_fixture_module', path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    return load
```

- [ ] Seed the final roster test with an independently specified expectation:

```python
EXPECTED = {'ask-dnk', 'calc-setup', 'calc-rq', 'calc-to-spec', 'calc-execute', 'calc-review'}

def test_exact_roster(plugin_root):
    assert {p.name for p in (plugin_root / 'skills').iterdir() if p.is_dir()} == EXPECTED
    assert {p.parent.name for p in (plugin_root / 'skills').glob('*/SKILL.md')} == EXPECTED
```

- [ ] Run `python -m pytest -q plugins/calc-project/tests/test_roster.py`; expected FAIL showing the old nine skills. Do not mark xfail or weaken equality to inclusion.
- [ ] Expand DT005's 45 rows into the 65 exact source paths using `git ls-tree -r --name-only 3e5cadc7f8343aedc462bc3df5ae4d123ee8ad58 -- plugins/calc-project`. Use test-fixture records `{source, targets, reason}`; `targets` is a concrete path list and is empty only for an accepted removal. Include the manifest and old template test. Test set equality with baseline paths, no duplicate sources, and every nonempty target exists once the candidate is complete.
- [ ] In `test_paths.py`, check Markdown links outside fenced examples and exact runtime code-path references supplied by owner tests. Distinguish project placeholders and sibling invocation names from packaged files; no permissive “all missing paths are examples” fallback. Add broken relative-link and escaping-symlink negative fixtures.
- [ ] Keep these tests tracked and the target checks red until their owners are implemented. Root baseline tests should still pass before Task 10 updates old directory expectations.

### Task 3: Implement calc-setup and stable project configuration

**Files:** Create setup SKILL, its three references, `scripts/verify_cluster_profile.sh`, `tests/test_setup.py`. Source: old `calc-project-structure` references and `scripts/common/verify_cluster_profile.sh`.

**Interfaces:** Input is one project path and setup/configuration intent. Output is stable project structure plus configuration in project `ARCHITECTURE.md` under `## Calculation Configuration`: `Data root:`, `Tracker adapter: local-markdown`, `RQ location: 01<main-line-slug>/01-rqs/<rq-id>-<slug>/`, `Software profile: software-profiles.md` when configured. These are human-readable field lines, not a new schema. Consumers read this exact section; they do not infer configuration from filenames.

- [ ] Add a contract test and run it red before writing the reference:

```python
def test_setup_configuration_pointer(plugin_root):
    text = (plugin_root / 'skills/calc-setup/references/project-structure.md').read_text()
    for field in ('Calculation Configuration', 'Data root:', 'Tracker adapter:', 'RQ location:'):
        assert field in text
    assert '01-rqs/' in text
```

- [ ] Rewrite the base layout retaining CONTEXT, AGENTS, ARCHITECTURE, gitignore, empty data root, structures, project templates and empty literature container. Replace the research-plan directory with `01-rqs/`; remove required PROJECT_PLAN/NOTE-doing/WORKFLOW and task-YAML instructions. Generated AGENTS reads project configuration, selected RQ/Spec and referenced Runs. Setup never creates concrete tasks or adopts existing RQs.
- [ ] Rewrite project-context definitions to DT003/DT004; keep approved stable terms and data boundaries. Explain scoped IDs and that Spec owns task state. Do not copy root repository-maintenance rules into scientific project state.
- [ ] Parameterize the verifier: `bash verify_cluster_profile.sh PROFILE HOST LABEL REMOTE_COMMAND`. It checks only the explicitly supplied probe, records label/command/output summary and verified/unavailable in the profile's existing marker block, and reports SSH failure honestly. Read the command from the reviewed project profile; run `ssh -- "$host" "$remote_command"` without eval or invented mu01 paths. Reject option-like host, missing profile and missing arguments; preserve unrelated profile text. Date may be recorded but is not mandatory public metadata.
- [ ] Test verifier with a PATH-local fake `ssh` executable returning success and failure. Capture its argv; require the chosen host/command, no real SSH call, preservation of an unrelated paragraph, and unavailable evidence after failure. Default mu01 examples remain explicitly unverified until a probe runs.
- [ ] Run `python -m pytest -q plugins/calc-project/skills/calc-setup/tests/test_setup.py`; expected PASS. Execute setup behavior scenario S02 in Task 11 after all required skills exist.

### Task 4: Implement calc-rq publication and Decision Ticket adoption

**Files:** Create `skills/calc-rq/SKILL.md`, `references/{rq-template,decision-ticket-template}.md`, `tests/test_rq_contract.py` under Calc.

**Interfaces:** Input is a uniquely identified calculation project/RQ and an RQ decision intent. Output is `RQ.md` and same-RQ `decision-tickets/NN-slug.md`; one accepted Ticket answer and exact corresponding RQ update may use one user approval. Required external workflow is `$dev-engineering:grill-with-docs`.

- [ ] Add/run the following red contract test; it checks the real Markdown templates, not an invented domain parser:

```python
def test_rq_template(plugin_root):
    text = (plugin_root / 'skills/calc-rq/references/rq-template.md').read_text()
    for field in ('ID: RQ-001', 'Status: active', '## Question', '## Boundary',
                  '## Success Criterion', '## Decisions', '## Specs'):
        assert field in text
```

- [ ] Copy the exact DT004 RQ and Ticket template bodies into the two references. Ticket has ID, open/resolved, same-RQ Blocked by, Question and Answer on resolution; RQ owns the accepted decision. Put when-to-read pointers beside corresponding SKILL actions.
- [ ] Write SKILL steps: resolve configuration/unique parent; read current authorities; invoke the required upstream workflow for creation or question/boundary/criterion change; present exact proposed RQ/Ticket changes; wait for required approval; write the two authorities before advancing the next Ticket. If one write fails, stop and report the partially written pair; reconcile by reading the two files, not a new transaction/session registry.
- [ ] Missing external dependency stops only the workflow needing it. No installed-cache absolute path becomes a runtime instruction. Pending decisions are derived on demand, unrelated Tickets do not block Spec design, closure impact is still only a proposal until an RQ update is approved.
- [ ] Add template tests for allowed statuses, required headings and same-parent dependency examples. Run `python -m pytest -q plugins/calc-project/skills/calc-rq/tests/test_rq_contract.py`; expected PASS. Actual approval and duplicate-ID behavior is tested through S01/S03/S12, not asserted by keyword presence.

### Task 5: Implement calc-to-spec and migrate scientific design knowledge

**Files:** Create spec SKILL, `references/spec-template.md`, seven design backend files in the ownership table, `tests/test_spec_contract.py`.

**Interfaces:** One RQ plus principal judgment, or one existing Spec to replace. Output is one reviewable draft, then approved published Spec and RQ index entry. Consumes setup configuration and RQ decisions; produces task declarations only, never directories or Runs.

- [ ] Write/run a red test for the Spec template:

```python
def test_spec_template(plugin_root):
    text = (plugin_root / 'skills/calc-to-spec/references/spec-template.md').read_text()
    for field in ('ID: SPEC-001', 'Status: ready', 'RQ: ../RQ.md', '## Judgment',
                  '## Tasks', '### TASK-001:', 'Blocked by:', 'Condition:',
                  'Acceptance:', '#### Runs', '| Run | Status | Current | Path | Result |'):
        assert field in text
```

- [ ] Use the durable DT004 template and exact status sets. Record task paths relative to the configured data root and Run paths relative to their task; resolve the containing RQ and Spec before using local IDs. No revision counter, shared frontmatter or generic validator.
- [ ] Implement the instruction sequence: read evidence and capabilities; settle any DAG/acceptance/stopping decision; draft one judgment per Spec; propose a concrete publication; require approval; write Spec and one RQ link. Repeated publication of identical ID/path is idempotent; ownership conflict or malformed existing authority stops writes.
- [ ] For active replacement, inspect current Runs and scheduler state before overwriting. Unsafe active execution blocks replacement. Preserve physical Run directories; do not recreate obsolete Spec history. Closed Specs remain immutable. Route scientific uncertainty back to RQ and stable configuration gaps to setup.
- [ ] Split scientific content per DT005: VASP physical parameters, MAE comparison convention, DMFT subspace/U/J/solver, NAMD representation, magnetic DAG/order, energy-mapping rank/residuals, Wannier per-spin windows. Every selected backend reference names its evidence/approval inputs; templates never select scientific values.
- [ ] Run `python -m pytest -q plugins/calc-project/skills/calc-to-spec/tests/test_spec_contract.py`; expected PASS. S04/S05/S06 exercise the actual publication/replacement/DAG contract later.

### Task 6: Implement Run-local preparation and immutable submission mechanics

**Files:** Create `skills/calc-execute/assets/templates/common/run.sh.template`, `scripts/fingerprint_run.py`, `scripts/probe-run-environment.sh`, `references/{run-preparation,pbs}.md`, `tests/test_run_inputs.py`. Source old common prepare/validate/submit templates and common environment probe.

**Interfaces:** `python fingerprint_run.py INPUTS_DIR` prints one SHA-256 digest. Python function `fingerprint_inputs(inputs: Path) -> str` hashes sorted relative names and file bytes, rejects symlinks and nonexistent directories, never writes. `bash inputs/run.sh prepare|validate` operates only on its own Run; `bash inputs/run.sh submit EXPECTED_DIGEST` verifies unchanged inputs before qsub. The digest guard enforces byte identity only; calc-execute owns transient review and submission authorization.

- [ ] Add/run red tests against the actual fingerprint function:

```python
import pytest

def test_snapshot_changes_and_rejects_links(load_script, tmp_path):
    module = load_script('skills/calc-execute/scripts/fingerprint_run.py')
    inputs = tmp_path / 'inputs'
    inputs.mkdir()
    (inputs / 'INCAR').write_text('ENCUT=520\n')
    first = module.fingerprint_inputs(inputs)
    (inputs / 'INCAR').write_text('ENCUT=600\n')
    assert module.fingerprint_inputs(inputs) != first
    (inputs / 'linked').symlink_to(inputs / 'INCAR')
    with pytest.raises(ValueError):
        module.fingerprint_inputs(inputs)
```

- [ ] Implement the digest using `hashlib.sha256`, length-delimited relative-path bytes and per-file content hashes in deterministic order. Reject a symlink anywhere below inputs. Include scripts and helper copies in the snapshot, not just scientific input files; exclude nothing inside inputs. Report missing/unreadable files as failure.
- [ ] Render each run.sh with these exact location rules; stage-specific prepare/validate bodies come from Tasks 7–8:

```bash
INPUTS_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)" || exit 1
RUN_DIR="$(CDPATH= cd -- "$INPUTS_DIR/.." && pwd)" || exit 1
OUTPUTS_DIR="$RUN_DIR/outputs"
LOGS_DIR="$RUN_DIR/logs"
```

`prepare` checks declared upstream source and destination before server-only copying; an existing differing destination fails, never overwrite/reuse the old Run. `validate` checks backend prerequisites and reports the fingerprint; `submit` takes the reviewed fingerprint from the current chain and refuses missing/mismatched digest before qsub. It does not rerun preparation or edit inputs. Submit from `RUN_DIR` with the exact `inputs/run.pbs`; capture the returned job ID as execution evidence.

Copy the exact owning `fingerprint_run.py` into the Run inputs during preparation.
Inside the submit branch use the following byte-identity guard after the agent
has rechecked its review, external state and authorization:

```bash
reviewed_digest="${2:?missing reviewed input digest}"
actual_digest="$(python3 "$INPUTS_DIR/fingerprint_run.py" "$INPUTS_DIR")" || exit 1
test "$actual_digest" = "$reviewed_digest" || { echo 'input snapshot changed' >&2; exit 1; }
cd "$RUN_DIR" || exit 1
qsub -o "$LOGS_DIR/pbs.stdout" -e "$LOGS_DIR/pbs.stderr" "$INPUTS_DIR/run.pbs"
```

Do not store the digest as a review-pass file; it is an in-memory argument for
this execution chain. A new invocation obtains a new review regardless of matching bytes.
- [ ] Rewrite `probe-run-environment.sh` as `bash probe-run-environment.sh HOST REMOTE_COMMAND` with read-only SSH, exact reviewed command, visible stdout and propagated failure status. Cover each retained backend through explicit commands in its reference; do not infer software paths from mu01 defaults. Before submit, execute rechecks mutable environment and upstream current-Run identity; any relevant change restarts validation/review even if file digest is unchanged.
- [ ] In tests, render concrete SCF and band Runs under tmp_path, place PATH-local fake qsub/ssh/rsync commands and record calls. Assert missing/mutated digest causes zero qsub calls; unchanged authorized test-chain case submits once; preparation never runs during submit; old-Run files and source handoff bytes stay unchanged. This fixture does not claim to authenticate user approval.
- [ ] Run `python -m pytest -q plugins/calc-project/skills/calc-execute/tests/test_run_inputs.py`; expected PASS. Leave actual permission and review checks to Task 9/11.

### Task 7: Migrate VASP and magnetic pipeline assets without changing scientific commitments

**Files:** Create execute backend `vasp/{common,scf,band,handoff,wannier-prerun,mae}.md`, `wannier90/common.md`, `tb2j/common.md`, `vampire/{common,handoff}.md`; copy/rewrite the exact templates listed in the ownership table including common run.sh from Task 6; migrate the VASP/Wannier/VAMPIRE helper files; create execute `tests/{test_backend_bundles,test_vasp_assets,test_magnetic_assets}.py`.

**Interfaces:** Exact reference bundles are the accepted DT006 table. PBS receives `PBS_O_WORKDIR` equal to the Run directory, reads immutable `inputs/`, executes in `outputs/`, and writes command logs under `logs/`. No task-level input path or inference of upstream Run by directory guessing.

- [ ] Add/run a red behavioral test for the existing INCAR-comparison helper at its new path:

```python
import subprocess

def test_incar_mismatch_blocks(plugin_root, tmp_path):
    upstream, prepared = tmp_path / 'up', tmp_path / 'new'
    upstream.write_text('ENCUT = 520\nISPIN = 2\n')
    script = plugin_root / 'skills/calc-execute/scripts/vasp/compare_incar_parameters.sh'
    assert script.is_file()
    prepared.write_text(upstream.read_text())
    valid = subprocess.run(['bash', str(script), str(upstream), str(prepared), ''], capture_output=True)
    assert valid.returncode == 0
    prepared.write_text('ENCUT = 400\nISPIN = 2\n')
    result = subprocess.run(['bash', str(script), str(upstream), str(prepared), ''], capture_output=True)
    assert result.returncode != 0
```

- [ ] Move DT005 templates to exact owner paths; remove old filename conventions in their callers. Use this PBS prologue in each rendered backend script, preserving backend-specific environment checks and required outputs:

```bash
RUN_DIR="${PBS_O_WORKDIR:?missing PBS work directory}"
INPUTS_DIR="$RUN_DIR/inputs"
OUTPUTS_DIR="$RUN_DIR/outputs"
LOGS_DIR="$RUN_DIR/logs"
test -d "$INPUTS_DIR" && test -d "$OUTPUTS_DIR" && test -d "$LOGS_DIR" || exit 1
source "$INPUTS_DIR/cluster-env.sh" || exit 1
cd "$OUTPUTS_DIR" || exit 1
```

- [ ] Move every input-generation action, including POTCAR/VASPKIT preparation and large-file handoff, before review. Jobs may copy approved input bytes to their private outputs working directory but never alter `inputs/`. Use exact file lists, not `cp inputs/*`; refuse unexpected prior outputs rather than rerunning destructively.
- [ ] Keep SCF `common+scf`; band `common+band+handoff`; Wannier pre-run and MAE use the exact accepted bundles. Store the literal bundle table in execute SKILL and independently expected tuples in `test_backend_bundles.py`; assert tuple equality and path existence. A missing file stops the branch. Test actual loaded files in S07/S13; static table equality alone is insufficient.
- [ ] Preserve scientific/format checks from the old assets: band VASPKIT `21 → 211 → 1`, `printf '5\ny\n8\n' | python3 ./vest2.py`, both nonempty spin-range files; approved per-spin Wannier windows; `.amn/.mmn/.eig/.win`, `_hr.dat`, centres, fit plots; TB2J declared Fermi/k mesh and Vampire outputs; VAMPIRE source-to-copy checksums and named output columns. Copy vest2 initially byte-for-byte; record its baseline hash in the test fixture and exercise the exact noninteractive path.
- [ ] Fake VASP/VASPKIT/MPI/Wannier/TB2J/VAMPIRE executables create small representative outputs in isolated test directories. Test missing inputs, wrong INCAR, incomplete spin files, altered magnetic order/window values, absent TB2J handoff, changed VAMPIRE model and malformed plot columns. Assert nonzero failure or the responsible review/design block rather than continuing.
- [ ] Run `python -m pytest -q plugins/calc-project/skills/calc-execute/tests/test_backend_bundles.py plugins/calc-project/skills/calc-execute/tests/test_vasp_assets.py plugins/calc-project/skills/calc-execute/tests/test_magnetic_assets.py`; backend bundle completeness becomes fully green after Task 8. Run all copied plot helpers against synthetic data with `MPLBACKEND=Agg`; do not import vest2's interactive main as a library.

### Task 8: Migrate DMFT and NAMD execution knowledge

**Files:** Create execute `references/backends/dmft/{common,postprocessing}.md`, `namd/{common,namdwithsoc}.md`, `tests/test_dmft_namd_contract.py`; complete environment probe reference coverage. Source old DMFT/NAMD SKILLs and their workflow/interface references.

**Interfaces:** DMFT prepares/executes the approved correlated-subspace design and returns lightweight evidence; HDF5 stays remote. NAMD preserves the documented NAMDwithSOC 1.5.2 applicability and matches the approved representation/window to exact snapshots. These branches render the common Run script and concrete run.pbs using source instructions, not invented universal templates.

- [ ] Add/run a red selective-reference test:

```python
def test_dmft_namd_bundle_files(plugin_root):
    base = plugin_root / 'skills/calc-execute/references/backends'
    for relative in ('dmft/common.md', 'dmft/postprocessing.md',
                     'namd/common.md', 'namd/namdwithsoc.md'):
        assert (base / relative).is_file()
    assert '1.5.2' in (base / 'namd/namdwithsoc.md').read_text()
```

- [ ] Split preparation/runtime from design/review exactly as DT005 specifies. Remove the old prohibition on interpreting DMFT convergence; execution applies approved Spec criteria and sends ambiguous evidence to design. Preserve targeted lightweight postprocessing and server-only HDF5 access.
- [ ] Preserve NAMD SOCTYPE/spinor representation, required fields, band window, snapshot layout, source protection and exact success evidence from the existing interface reference. Missing knowledge or competing diagnoses stops the workflow rather than guessing a patch.
- [ ] Author concrete S13 fixture cases for wrong SOCTYPE, missing snapshot fields, wrong band window and DMFT ambiguous convergence. Run the owning contract test plus completed `test_backend_bundles.py`; all eleven accepted loading branches must now resolve.

### Task 9: Narrow reviewed synchronization to calc-sync.yaml

**Files:** Move/rewrite `skills/calc-execute/scripts/sync/sync_calc_data.py`; create `references/{sync,remote-completion}.md`, `tests/test_sync.py`. Source old sync script and two sync references.

**Interfaces:** Preserve `validate_config(config: dict, workspace: Path | None) -> list[str]`, `load_config(path: Path) -> dict`, `build_pull_plan(config, remote_files) -> dict`, `build_push_plan(config, task_root) -> dict`, `write_reviewed_plan(config, direction, plan, task_root, now=None) -> Path`, `load_reviewed_plan(config, direction, task_root, now=None) -> dict`, and existing transfer functions. Config accesses become `config['local']`, `config['server']`, `config['exclude']`. CLI retains validate/inspect/plan/push/pull; remove init entirely. Run CLI with project root as cwd; require the config file to be exactly the declared local task root's calc-sync.yaml.

- [ ] Add/run these red tests at the new path:

```python
import pytest

def test_minimal_sync_config(load_script, tmp_path):
    module = load_script('skills/calc-execute/scripts/sync/sync_calc_data.py')
    config = {'local': 'data/TASK-001', 'server': 'fake:/calc/TASK-001', 'exclude': []}
    assert module.validate_config(config, tmp_path) == []
    assert module.validate_config({**config, 'status': 'active'}, tmp_path)
    assert module.validate_config({**config, 'local': '../escape'}, tmp_path)

def test_review_plan_expiry(load_script, tmp_path):
    module = load_script('skills/calc-execute/scripts/sync/sync_calc_data.py')
    config = {'local': 'data/TASK-001', 'server': 'fake:/calc/TASK-001', 'exclude': []}
    plan = {'upload': [], 'skipped': []}
    module.write_reviewed_plan(config, 'push', plan, tmp_path, now=100)
    assert module.load_reviewed_plan(config, 'push', tmp_path, now=101) == plan
    with pytest.raises(ValueError):
        module.load_reviewed_plan(config, 'push', tmp_path, now=1901)
```

- [ ] Delete `build_draft_config`, `_status_error`, ALLOWED_STATUS, domain serializer/init handler and CLI init. Reject unknown top-level config keys, non-string paths, empty/dot/broad root, traversal, option-like hosts, malformed exclusions and local symlink escape. Keep the reviewed-plan JSON as ephemeral sync-tool configuration, not domain state; update its fingerprint binding to flat config.
- [ ] Replace every nested `paths`/`sync` access in remote identity, roots, renderers, planner and transfer code. Keep the 30-minute expiry, finite timestamp checks, plan/config fingerprints and exact files-from consumption. Preserve no independent re-listing in push/pull. Exclude calc-sync.yaml, .calc-sync state and caches from uploads.
- [ ] Hard-exclude HDF5 extensions including uppercase variants plus CHGCAR/WAVECAR even when user exclude is empty. At transfer time revalidate the saved approved list against safety/exclusion rules; reject unsafe symlink paths and never expand to additional files. Do not add rsync deletion flags. For approved entries under a Run's inputs, read only those exact source/destination paths to check existing destination type and byte identity; refuse replacement of differing existing inputs. These targeted read-only checks neither rebuild nor enlarge the reviewed list. Remediation uses a new Run and a new reviewed plan.
- [ ] Monkeypatch subprocess.run and assert zero rsync calls on missing/expired/wrong-direction/changed-config/changed-list plans, traversal and protected files. On valid transfer assert exact reviewed files-from bytes and no `--delete*`, `--remove-source-files`, `--copy-links` or `--inplace`; assert no planner/remote listing call inside push/pull. Cover both directions, spaces in safe relative filenames, symlink ancestors and a fake existing immutable destination.
- [ ] Run `python -m pytest -q plugins/calc-project/skills/calc-execute/tests/test_sync.py`; expected PASS. Remote completion reference still requires scheduler plus outputs/log evidence and timestamps, not queue disappearance alone.

### Task 10: Complete execute, transient review, router, metadata and old-roster removal

**Files:** Complete execute SKILL and `references/{task-advancement,simple-correction}.md`; create review SKILL and its nine references, router SKILL, all six agents/openai.yaml, owner tests `calc-review/tests/test_review_contract.py`; update root navigation/context, Calc manifest, root contract tests; remove every legacy file per DT005 after target checks exist.

**Interfaces:** Execute advances one whole Spec using approved task criteria; review returns pass/pass_with_warnings/block for one prepared snapshot and changes no domain files; ask-dnk routes only. Sibling handoffs carry exact IDs/paths and unfinished action, never unapproved scientific facts. Direct diagnostic review cannot authorize future submission.

- [ ] Add/run red metadata tests with PyYAML:

```python
import yaml

def test_explicit_only_metadata(plugin_root):
    names = ('ask-dnk', 'calc-setup', 'calc-rq', 'calc-to-spec', 'calc-execute', 'calc-review')
    for name in names:
        data = yaml.safe_load((plugin_root / 'skills' / name / 'agents/openai.yaml').read_text())
        assert data['policy']['allow_implicit_invocation'] is False
        assert ('$' + name) in data['interface']['default_prompt']
        assert data['interface']['display_name'] and data['interface']['short_description']
```

- [ ] Write each metadata file in this shape with its own name, description and intent:

```yaml
interface:
  display_name: "Calc Execute"
  short_description: "推进已批准 Spec 的任务与 Run"
  default_prompt: "$calc-execute 推进指定的 ready 或 active Spec。"
policy:
  allow_implicit_invocation: false
```

- [ ] Execute instructions explicitly implement DT001 plus route G3: read current authorities/external state; derive frontier without cache; prepare/validate/review exact Run; enforce current submission scope; record actual job evidence; synchronize reviewed outputs; accept by decisive criteria; select first current Run or require reason for replacement; propagate needs-review; use new preserved Runs for simple corrections; propose immutable closure then route later RQ impact separately. Do not persist review results or introduce TASK/RUN metadata.
- [ ] Review instructions inspect exact prepared inputs, environment, source handoffs and resource configuration with own references. Backend references contain read-only checks only. Any action/decision/authorization needed means block; pass_with_warnings needs no action. Missing/incomplete snapshot or conflicting authority yields no judgment. Fix ownership is returned to execute/design/setup.
- [ ] Router maps missing setup → setup, RQ/Ticket → rq, Spec design → to-spec, execution → execute. It does not give scientific advice or route ordinary requests to review. A correct directly named sibling remains usable without router.
- [ ] Update manifest descriptions/examples to six explicit invocations; retain publication identity, existing version and marketplace local source. Update README rows, AGENTS Calc navigation, CONTEXT stable glossary pointer and shared-template statements. Preserve unrelated terms and the user's existing context additions.
- [ ] Replace old root assertions for shared templates/magnetic-workflow with exact new paths; remove the assertion requiring Calc shared resources in CONTEXT. Keep the user-deleted blanket dev-engineering check absent. Finish test_paths handling of exact asset and helper references.
- [ ] Check inventory coverage, then remove only the nine exact old skill directories, `plugins/calc-project/resources/calculation-templates/`, old plugin `scripts/` files listed by DT005 and `tests/resources/test_calculation_templates.py`. Remove now-empty old containers. Use patch deletions/explicit source moves, not broad cleanup; no existing calculation project is in scope.
- [ ] Run `python -m pytest -q tests/test_repository_layout.py plugins/calc-project/tests/test_roster.py plugins/calc-project/tests/test_paths.py plugins/calc-project/tests/test_migration_inventory.py plugins/calc-project/skills/calc-review/tests/test_review_contract.py`; expected all PASS, exact six directories, all source rows accounted for.

### Task 11: Exercise actual skill behavior across the thirteen accepted scenario families

**Files:** Create `plugins/calc-project/tests/scenarios/{S01-targets,S02-setup,S03-rq-tickets,S04-publication,S05-replacement,S06-dag-resume,S07-run-handoff,S08-review,S09-submission,S10-sync,S11-invalidation,S12-correction-closure,S13-backends}.md`. Save run evidence outside the package under `.scratch/calc-project-rq-redesign/acceptance/`.

**Interfaces:** Each scenario supplies a fresh candidate skill context, tiny project/remote fixtures, concrete user messages, simulated tool results and expected mutations/stop. Use the candidate files, not the plan as agent instructions. Record candidate content digest, inputs, tool trace and before/after hashes. Tests of static wording do not substitute for these runs.

- [ ] Each scenario includes its exact prompts and expected observations from this table; instantiate sibling calls against the same candidate files and forbid real hosts through the test environment:

| File | Concrete probe | Required evidence |
|---|---|---|
| S01-targets | Two different RQs each contain SPEC-001; ask to execute SPEC-001 without a parent, then name one exact path. Separately give ordinary non-invocation wording. | Ambiguous request causes no writes; exact path resolves correctly. Host invocation layer obeys explicit-only metadata; ordinary text cannot be counted as an explicit call. |
| S02-setup | Invoke calc-setup in an empty project; repeat against existing custom CONTEXT; request reorganization that would move existing data without approval. | Stable configured structure, no RQ/tasks/Runs, existing text preserved; data-moving step stops. Fake unavailable SSH is recorded honestly. |
| S03-rq-tickets | Request RQ creation without approving proposal; approve it; give two decidable Tickets and approve only the first answer plus its exact RQ change. | Required external interview is actually reached; first pair written, second unapproved pair untouched, no pending cache. Repeat with missing dependency: no silent substitute. |
| S04-publication | Present draft Spec, approve publication, repeat publication, then collide ID with different owner. | No draft adoption; exactly one link after repeat; conflict stops without mutating another RQ. |
| S05-replacement | Request an approved-design change while one Run is submitted; then supply verified inactive state and approve concrete replacement. | Unsafe replacement stops; safe approved replacement updates same Spec, preserves all physical Runs and adds no revision documents. |
| S06-dag-resume | Two independent pending tasks; a child condition false; another condition ambiguous; scheduler loses a job but no outputs exist. | Parallel frontier allowed, false task skipped, ambiguity to design, vanished job not called successful. Fresh context reconstructs work from authorities only. |
| S07-run-handoff | Band depends on accepted SCF RUN-001; server has tiny synthetic CHGCAR; local transfer list excludes it. Remove required handoff or mutate after review. | Prepare/validate before review; server-side only; changed input or missing handoff blocks submission, no task-level inputs. |
| S08-review | Review prepared snapshot with harmless warning, then risk requiring a choice; directly invoke review and later resume execute in a fresh context. | Correct warning/block distinction; file hash unchanged after review; fresh execute reviews again. No review-state file. |
| S09-submission | Authorize TASK-001 on fake cluster/queue/resources with concurrency 1; offer matching Run, then out-of-scope TASK-002 or changed resources. | Matching reviewed Run submits exactly once; scope violation stops; sync approval alone cannot submit. Ordinary sibling recommendations do not run automatically. |
| S10-sync | Approve exact push list, expire or alter config/list/direction; try protected files and symlink escape. | Real sync script refuses before fake rsync; valid list transfers exactly named safe files, no deletion or old input overwrite. |
| S11-invalidation | Replace upstream current Run with a reason while children are prepared, submitted and accepted respectively. | Stale prepared chain cannot submit; running old-dependency result cannot be auto-accepted; accepted child needs-review; no fabricated remote cancellation. Dependency-specific recheck restores only proven-valid results. |
| S12-correction-closure | Deterministic failure with unchanged science; ambiguous failure; approved overwrite-style recompute; decisive acceptance; early closure then proposed RQ impact. | New preserved Run for repair, ambiguity stops; overwrite proposal individually approved. Acceptance by Spec criteria; closure approval distinct from RQ update, closed Spec immutable, remaining tasks explicitly disposed. |
| S13-backends | Stage-by-stage loading traces plus wrong INCAR, MAE pair mismatch, DMFT ambiguous convergence, NAMD wrong SOCTYPE, Wannier window mismatch, missing TB2J products, changed VAMPIRE model. | Exact eleven bundles from DT006; each incorrect stage blocks at its responsible owner; no inferred physical choices and no fake convergence claim. |

- [ ] For each file, run at least one successful branch and its specified refusal branch in a fresh isolated candidate context. Make approvals concrete by injecting the actual approved proposal and scope, not a blanket “user approves everything”. Keep scheduler state in fake tool responses; keep task and Run state in the fixture Spec.
- [ ] Use an isolated runtime that can load the candidate plugin without changing the user's installed plugins to check actual invocation behavior. If this facility or the external dependency is unavailable, mark that acceptance item unverified and stop delivery; do not claim YAML checks proved host activation. Other mechanical tests may continue. This is an explicit environment gate, not permission to relax the contract.
- [ ] Review tool traces and file diffs against every table row; no synthetic state-machine implementation can stand in for the candidate skill. Save findings and rerun changed branches after instruction fixes. Each finding must identify the source instruction or deterministic helper responsible.

### Task 12: Build and test an independently consumable local package

**Files:** Create `plugins/calc-project/tests/build_acceptance_package.py`, `tests/test_package.py`; update owner tests to accept the existing `--calc-plugin-root` fixture. Dev builder/test files remain outside runtime package.

**Interfaces:** `runtime_files(plugin_root: Path) -> list[Path]` yields sorted validated runtime files; `build_package(plugin_root: Path, output: Path) -> Path` writes a new tar archive and refuses an existing output. CLI: `python plugins/calc-project/tests/build_acceptance_package.py --plugin-root plugins/calc-project --output /explicit/temp/path/calc-project.tar`. It verifies exact six skills and includes manifest, six SKILLs/agents plus their references/assets/scripts; excludes tests, fixtures and caches. Fail on symlinks or unknown runtime top-level entries, rather than silently omitting a dependency.

- [ ] Add/run a red archive test that exercises the builder rather than assuming source files equal packaged files:

```python
import importlib.util
import tarfile
from pathlib import Path

def test_runtime_package(plugin_root, tmp_path):
    script = Path(__file__).with_name('build_acceptance_package.py')
    spec = importlib.util.spec_from_file_location('package_builder', script)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    package = builder.build_package(plugin_root, tmp_path / 'calc-project.tar')
    with tarfile.open(package) as archive:
        names = {item.name for item in archive.getmembers() if item.isfile()}
    expected = {path.relative_to(plugin_root).as_posix() for path in builder.runtime_files(plugin_root)}
    assert names == expected
    assert '.codex-plugin/plugin.json' in names
    assert 'skills/calc-execute/assets/templates/common/run.sh.template' in names
    assert not any(set(Path(name).parts) & {'.git', '.worktrees', '.scratch', 'tests', '__pycache__'} for name in names)
```

- [ ] Implement exact allowed runtime roots using the six-name constant; reject missing manifest/SKILL/agents and any symlink. Independently assert required asset inventory from DT005 in tests, so a builder accidentally dropping a file cannot redefine its own expected result. Preserve file bytes and executable permission bits; compare hashes/modes after safe extraction, and reject archive absolute/traversal/link members before extraction.
- [ ] Write package tests for removed helper, malformed metadata, extra seventh skill, stale absolute resource path, omitted template, symlink and accidental scientific output. Each must fail package acceptance. Documentation must clearly distinguish external skill calls from local file references.
- [ ] Extract into a new external temporary directory and run source tests targeting that root with `--calc-plugin-root=...`. Run roster/path/owner tests and representative scripts against extracted files; exclude only source-inventory and repository-root checks requiring Git, which run on the clean source instead. Confirm helpers do not resolve back to the original source tree.
- [ ] Repeat S07–S10 and one explicit-invocation scenario using the extracted candidate. Save package SHA-256 and observed evidence; if invocation cannot be exercised, record that gate as incomplete rather than silently passing.

### Task 13: Verify complete candidate, form atomic cutover, and hand off

**Files:** All plan-scoped source changes, tracked tests and required docs. Record evidence in ignored acceptance directory; keep runtime package temporary. No version bump, install, external publish or unrelated commit.

**Interfaces:** Input is the complete G3/G4-passing candidate. Output is one atomic replacement commit plus freshly verified clean-source/package evidence and archive preservation checks. This task does not imply merge or installation authorization.

- [ ] Run the full explicit scope from implementation root, with no archive/vendor recursion:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLBACKEND=Agg python -m pytest -q -p no:cacheprovider tests/test_repository_layout.py plugins/calc-project/tests plugins/calc-project/skills/calc-setup/tests plugins/calc-project/skills/calc-rq/tests plugins/calc-project/skills/calc-to-spec/tests plugins/calc-project/skills/calc-execute/tests plugins/calc-project/skills/calc-review/tests
git diff --check
```

Router behavior lives in S01/S09 and cross-interface tests; no empty owning test directory is required.

- [ ] Require every static/mechanical test green and all Task 11 behavior evidence reviewed, including actual invocation and dependency checks. Compare the complete diff to DT005 and the 65-source inventory. Explicitly stage only plan files, the edited root contract test and necessary design document updates; review `git diff --cached --name-status` and `git diff --cached`. Exclude .scratch, archives, prototypes, caches and temporary packages.
- [ ] With G3/G4 satisfied, commit the complete staged cutover once on `implement/wf001-calc-roster` with message `feat(calc): replace legacy roster with six RQ interfaces`. Capture `git rev-parse HEAD`. This plan uses no intermediate implementation commits: task progress is saved in the worktree and reviewed at each checkpoint, so no later squash or history rewrite is needed. Do not automatically merge to main.
- [ ] Create a detached temporary linked worktree from that exact commit. This supplies real Git context to root and baseline-inventory tests while excluding untracked implementation-worktree files. Run the explicit source suite there, build the runtime package there, and repeat extracted-package tests and affected behavior checks. Use a new temporary directory and preserve it with the evidence until handoff:

```bash
git status --short --branch
verified_commit=$(git rev-parse HEAD)
verification_parent=$(mktemp -d /tmp/wf001-verification.XXXXXX)
git worktree add --detach "$verification_parent/source" "$verified_commit"
git -C "$verification_parent/source" rev-parse HEAD
git -C "$verification_parent/source" status --porcelain --untracked-files=all
```

The printed HEAD must equal `verified_commit`, and status must be empty before
running tests. Record the resolved temporary path with test evidence.
- [ ] Re-run G0 from the original repository root; both archived heads/branches and clean status must match. Confirm current original workspace changes remain preserved and prototype tip unchanged.
- [ ] If pre-cutover verification fails, keep working only in the implementation worktree. If post-cutover verification fails, stop delivery and report it; fix and reverify a new complete candidate before handoff. If an already delivered cutover must be reverted, use an explicit full-commit revert on the receiving branch after checking current changes. Never recover individual old skills into the new roster or claim Git reverted remote jobs/data.
- [ ] Hand off exact source commit, test commands/results, actual behavior evidence, package hash, archive checks and limitations. Ask for integration/install/publication only if the user requests those next actions.

## Plan self-review and execution checklist

- G0 → Task 1 and 13; G1 → Task 1–2; G2 → Task 3–10; G3 → Task 2–11; G4 → Task 12; G5 → Task 13.
- DT001 six interfaces/approval/sibling behavior → Tasks 3–5, 10–11; DT002 exact bundles → Tasks 6–8, 11; DT003/004 documents/state → Tasks 3–5, 9–11; DT005 every source → Tasks 2, 7–10, 12; DT006 cutover/package/rollback → Tasks 1–2, 12–13.
- Scope is one coupled roster replacement, not independently publishable backend subprojects. Reviewable tasks do not introduce multiple public delivery units.
- Only accepted source-maintenance documents and new plan are changed during planning. No implementation worktree, runtime scripts, new roster or acceptance test implementation is created by saving this plan.
- The complete suite command in Task 13 names only test directories created by Tasks 2–10. Package runtime tests select the extracted root explicitly; source-only checks retain real Git context in the detached verification worktree.

Expected completion evidence is all tests passing plus the separately reviewed thirteen behavior scenario families; an unavailable invocation test is not a pass. No current implementation test result is claimed by this plan.
