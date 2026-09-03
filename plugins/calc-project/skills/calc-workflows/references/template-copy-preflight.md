# Template Copy and Conversation Preflight

Use this shared contract before preparing a new task copy. Template files are
declared inputs, submission/PBS scripts, and approved helper scripts; their only
permitted copy sources are external `research-knowledge templates/computation/` and project
`calculation_templates/`. Existing task directories, historical reference
cases, completed-run outputs, logs, job identifiers, caches, and remote paths
are not template sources. Template files must not include outputs, logs,
scheduler state, caches, or remote absolute paths.

Large upstream files are HDF5 files, `CHGCAR`, and `WAVECAR`. They are not
template assets: a user explicitly confirms an existing task or remote-result
path, then the submission script copies them only on the server into the
prepared run location. They never enter Git, the local project, `calc-sync`, or
either template library; `candidates/` is never a copy source, and PBS only reads the prepared files.

Select the permitted template layer and copy its approved assets to the
task-local `inputs/` layout. Change only parameters the user has
explicitly confirmed. Unconfirmed physical settings remain at the selected
template value, are not inferred from similar tasks, and are shown as unchanged
in the pre-submit checklist. A missing required choice blocks preparation or
submission.

Immediately before a submission script is run or recommended, present this
conversation-only checklist and obtain explicit user confirmation:

1. selected template layer and copied task-local files;
2. calculation purpose and method;
3. every confirmed key parameter change;
4. relevant physical settings retained from the template;
5. task path, run tag, and input snapshot boundary;
6. declared upstream handoff artifacts and their availability check, including
   each required large upstream file's source, purpose, target, and presence
   check;
7. scheduler resource settings and submission-script/PBS-script pairing; and
8. expected outputs and the PBS-side acceptance condition.

The checklist is not written into the task directory and does not create a
provenance file, manifest, task-YAML field, or task-local source record. If the
user rejects or amends an item, update only the user-confirmed task-local files,
then present the revised checklist and obtain explicit user confirmation before
a submission script is run or recommended.
