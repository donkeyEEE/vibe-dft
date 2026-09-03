---
name: namd-workflow
description: Prepare, validate, or diagnose the VASP-to-Hefei-NAMD/NAMDwithSOC interface. Use when a task needs SOC/spinor, snapshot, coupling, or NAMD interface work; do not use for generic VASP, DMFT, or remote synchronization workflows.
---

# NAMD Workflow

Use this skill for the VASP-to-NAMDwithSOC interface: SOC/spinor representation,
snapshot compatibility, coupling handoff, and interface diagnostics. Use
`calc-task` for metadata/routing and `calc-sync` for remote inspection or
transfer. `script-management` provides and validates approved template sources;
this workflow creates and validates confirmed task-local NAMD copies.

Read [the NAMDwithSOC interface reference](references/namdwithsoc-interface.md) before changing a workflow. It is authoritative for effective-`ISPIN`/`SOCTYPE` selection, `INICON` columns, snapshot naming, band-window preflight, source-file protection, error triage, and minimal success evidence. Apply [shared PBS rules](../calc-workflows/references/pbs.md) when a PBS script is needed.

Before new task preparation, read [the shared template-copy preflight](../calc-workflows/references/template-copy-preflight.md).
The NAMDwithSOC interface reference remains the method-specific parameter
authority; do not infer unconfirmed scientific settings.
When interpreting a calculation note or troubleshooting record whose stopping
condition is met, do not expand the calculation question; route any scope
expansion to `calc-workflows`.

Never infer representation from the presence of SOC alone, move or alter large VASP source files, or treat an interface smoke test as production-trajectory validation.
