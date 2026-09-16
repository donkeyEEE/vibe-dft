---
status: accepted
---

# Allow confirmed derived progress reports from Show COT

`show-cot` remains read-only with respect to RQ, Spec, Task, Run, and every other authoritative record, but after displaying the complete COT it asks whether the user wants a standalone HTML progress report. On confirmation it may invoke `$show-me`, maintain the narrow `/.calc-project/` ignore rule, and replace prior generated progress reports with one dated, reproducible view. This keeps the ordinary conversational tree immediate and preserves Spec authority while allowing a richer visualization whose file-system effects are explicit and user-controlled.
