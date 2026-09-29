---
status: accepted
---

# Separate presentation skills into Skill Incubator

`paper2ppt` and `ppt-master` form a presentation pipeline with a distinct
runtime, dependency set, release footprint, and upstream synchronization path.
They belong in the independently installable
`plugins/skill-incubator/` publication unit. `paper2ppt` continues to invoke
the bundled sibling `ppt-master` after its material handoff.

Skill Incubator owns both skill directories, the PPT Master upstream-sync
script and provenance record, its plugin manifest, and installation
documentation. Paper Project keeps its research and writing skills.

The four-plugin boundary lets presentation runtime assets ship independently
from Paper Project's research and writing resources.
