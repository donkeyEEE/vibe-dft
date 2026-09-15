---
status: accepted
---

# Reduce calculation task statuses

Calculation Tasks use `pending`, `completed`, `failed`, and `needs-review`. `calc-execute` derives runnable work from the Spec DAG and conditions whenever it enters a Task, so `current` would only duplicate transient executor state. A false condition and explicit cancellation both mean that a Task cannot provide valid completion evidence for this Spec and are recorded as `failed`; `needs-review` remains distinct because it preserves previously accepted evidence whose upstream provenance changed. Run statuses remain independent.
