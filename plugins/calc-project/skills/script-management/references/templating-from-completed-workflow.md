# Templating From a Completed Workflow

Use this reference only after a completed calculation has been selected as a
template source. The upstream workflow and method owner must identify the
reusable stages, assets, substitutions, and acceptance checks; do not infer them
from one historical run.

1. Obtain user confirmation, source task paths, verified inputs/scripts, and the
   downstream workflow's reusable-boundary decision.
2. Choose plugin-local `knowledge/candidates/templates/` for proposed
   cross-project assets; use project
   `calculation_templates/` for project- or material-specific baselines.
3. Copy only approved input and script sources. Exclude outputs, logs, job IDs,
   absolute cluster paths, HDF5, large data, generated results, and credentials.
4. Replace only method-approved task-specific values with explicit placeholders;
   do not turn a historical physical setting into a default.
5. Record source task paths, retained files, removed content, placeholders, target
   scope, and validation result in the template change record.
6. Validate shell/PBS syntax and any method-specified input checks. Do not write
   task copies while extracting the template.
