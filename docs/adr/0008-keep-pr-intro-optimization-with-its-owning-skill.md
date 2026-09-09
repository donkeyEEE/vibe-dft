---
status: accepted
---

# Keep PR Introduction optimization with its owning skill

`pr-intro` will own both its Physical Review Introduction writing workflow and its dedicated evaluation-driven maintenance workflow. Ordinary writing loads only the lightweight runtime path; an explicit request to optimize `pr-intro` loads the co-located maintenance protocol, which builds or consumes local Zotero-derived masked-continuation data and iterates candidate skill files through isolated subagents. We reject a second optimizer skill because the workflow has no independent user-facing purpose or other skill consumer, and reject a plugin-level tool because its data contract, rubric, and mutations are specific to `pr-intro`.
