# Consumer Contract

This plugin directory supplies optional local knowledge. The requesting skill
keeps responsibility for its workflow, output, safety boundaries, and final
quality.

For every explicit lookup, a consumer reads its own
`references/knowledge-source.yaml`, resolves the path relative to that file,
reads this contract, reads the relevant formal index under `cards/` or
`templates/`, and selects only the smallest relevant formal resource set.

A resource is formal only when it exists under `cards/` or `templates/` and is
registered by the relevant index. Consumers must not read or search
`candidates/` or `incubating/`, and must not run an unbounded knowledge-tree
search.

If the directory, contract, index, or selected resource is missing or
malformed, warn and continue the requested task without plugin knowledge. Do
not fall back to another knowledge location.
