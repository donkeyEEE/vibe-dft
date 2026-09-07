---
status: accepted
---

# Separate presentation skills into Skill Incubator

`paper2ppt` and `ppt-master` form a presentation pipeline with a distinct
runtime, dependency set, release footprint, and upstream synchronization path.
They will move from `plugins/paper-project/` into a new independently
installable `plugins/skill-incubator/` publication unit. Both skills remain
`published`: relocation does not reverse their lifecycle history, and
`paper2ppt` continues to invoke the bundled sibling `ppt-master` after its
material handoff.

The new plugin owns both skill directories, the PPT Master upstream-sync
script and provenance record, the local OpenAI interface overlay, its plugin
manifest, lifecycle registry, and installation documentation. Paper Project
removes both skills from its lifecycle registry and release contract. Its
remaining research and writing skills stay in place.

Repository navigation, marketplace metadata, tests, and the migration log will
describe and validate the new four-plugin boundary. The migration must verify
that the old skill paths are absent, the new plugin validates independently,
all internal paths and qualified invocations resolve, and Paper Project no
longer packages presentation runtime assets. `CONTEXT.md` remains unchanged by
explicit user decision.
