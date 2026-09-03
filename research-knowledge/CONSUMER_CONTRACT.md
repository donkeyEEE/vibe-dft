# Consumer Contract

This repository supplies optional shared knowledge. The requesting skill keeps
responsibility for its workflow, output, safety boundaries, and final quality.

## Read sequence

For every new invocation or explicit knowledge lookup, a consumer must:

1. read its own `references/knowledge-source.yaml`;
2. resolve the configured repository path;
3. read this contract;
4. read the relevant formal index under `cards/` or `templates/`;
5. read only the smallest relevant formal resource set.

Consumers discover content through a formal index. A resource is formal only
when its file exists under `cards/` or `templates/` and that index registers
it. Consumers must not use unindexed files as shared knowledge and must not run
an unbounded repository-wide search.

## Candidate boundary

Consumers must not read or search `candidates/`. Candidate material has not
completed Cangjie governance and, for calculation templates, calc-project
acceptance. It cannot be used as a fallback when formal knowledge is absent.

## Refresh behavior

Each new lookup reads the current working tree. Content already loaded during
an in-progress step is not monitored or refreshed automatically. A subsequent
explicit lookup may observe newer indexed content, including uncommitted
changes.

## Missing or malformed knowledge

If the configured repository, contract, index, or selected resource is missing
or malformed, warn and continue the requested task without shared knowledge.
Do not interrupt the task and do not silently fall back to a legacy copy
bundled in a consuming plugin.

