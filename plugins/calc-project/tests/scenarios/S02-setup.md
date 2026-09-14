# S02 — Project setup

All probes natively invoke `calc-project:calc-setup` in fresh isolated fixtures.

## Exact prompts

`S02-empty-approved`:

> Initialize the empty project directory project. I approve exactly this proposal: create project/structures, project/calculation_templates, data, project/AGENTS.md, project/CONTEXT.md, and project/ARCHITECTURE.md; configure Data root ../data, Tracker adapter local-markdown, RQ location 01-rqs, and no software profile. Do not create any RQ, Spec, task, or Run.

`S02-custom-context`:

> Maintain project without replacing its custom CONTEXT.md. I approve exactly this proposal: add project/ARCHITECTURE.md with Data root ../data, Tracker adapter local-markdown, RQ location 01-rqs, and Software profile software-profiles.md#fake; add project/software-profiles.md section fake with host fake-cluster, queue debug, and VASP 6.4 synthetic; then verify fake-cluster and record the actual probe evidence. No data move is approved.

`S02-move-unapproved`:

> Reorganize project by moving data/TASK-001 into data/archive/TASK-001 and replace project/CONTEXT.md. I have not approved any concrete move or replacement proposal; proceed as far as authorized.

## Expected observations

- Approved empty setup creates stable configuration only—no RQ, Spec, task,
  or Run.
- The custom sentence remains byte-identical; fake SSH failure is reported as
  unavailable, never verified.
- The unapproved move/replacement produces no domain diff.
