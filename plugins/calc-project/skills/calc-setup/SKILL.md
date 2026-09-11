---
name: calc-setup
description: Initialize, reorganize, or maintain one calculation project's stable structure, Tracker configuration, data boundaries, and optional cluster software profile.
---

# Calculation Project Setup

## Flow

1. Resolve exactly one project path and read its `AGENTS.md`, `CONTEXT.md`, and
   `ARCHITECTURE.md` when present. Ask the user when the target is ambiguous.
2. For initialization or reorganization, read [project structure](references/project-structure.md)
   and [project context](references/project-context.md). Propose the exact paths
   and document changes, including the `## Calculation Configuration` fields in
   `ARCHITECTURE.md`.
3. Obtain approval for that concrete proposal before writing. Stop before any
   data move, replacement, or deletion not included in the approval. Preserve
   calculation data and compare existing project documents before changing them.
4. Create or update only the approved stable structure and configuration. Report
   existing RQs and Specs without adopting or modifying them.
5. When cluster configuration is requested, read [cluster software profiles](references/cluster-software-profiles.md).
   Record reviewed project-specific values in `software-profiles.md`; probe each
   value with the bundled verifier and retain honest `verified` or `unavailable`
   evidence.
6. Confirm sibling skills can read all four calculation-configuration fields,
   inspect `git status --short`, and report changes and unresolved configuration.

## Authority

This skill owns stable project structure, data boundaries, Tracker storage
configuration, the generated Agent pointer, and maintained cluster/software
profiles. It creates no RQ, Decision Ticket, Spec, task, or Run. It performs no
data synchronization, job submission, or mutable Run-environment validation.

A configured project may proceed to `$calc-rq`. Route project configuration
problems back here; route open-ended workflow selection to `$ask-dnk`.
