---
status: accepted
---

# Keep PR Introduction maintenance with its owning skill

`pr-intro` owns both its Physical Review Introduction writing workflow and its
dedicated evaluation-driven maintenance assets. Every `pr-intro` invocation
uses the lightweight writing workflow; requests to optimize the skill do not
switch its runtime route. The co-located maintenance protocol remains available
only as a separately scoped repository-maintenance procedure, where it can
build or consume local Zotero-derived masked-continuation data and iterate
candidate skill files through isolated subagents. We reject a second optimizer
skill because the workflow has no independent user-facing purpose or other
skill consumer, and reject a plugin-level tool because its data contract,
rubric, and mutations are specific to `pr-intro`.
