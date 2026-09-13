---
status: accepted
---

# Treat backend bundles as preferred execution knowledge

`calc-execute` treats its built-in backend bundles as preferred, tested
execution knowledge rather than a closed list of executable task types. When
an uncertainty cannot be resolved from current authorities, project files, or
deterministic configuration, it dispatches `$dev-engineering:research` and
stores the cited evidence under the calculation line's `02-计算规范/`
directory. Research may supply execution facts, but the Spec remains the
authority for scientific choices and acceptance, and normal review and
submission authorization remain mandatory. This avoids freezing execution to
the plugin's present template roster without allowing searched information to
silently become scientific authority.
