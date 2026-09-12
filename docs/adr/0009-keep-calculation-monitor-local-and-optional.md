---
status: accepted
---

# Keep calculation monitoring local and optional

`calc-execute` owns an optional local Calculation Monitor that may be started after a PBS submission has been recorded in the authoritative Spec. Each monitored job gets one transient systemd user service that watches only whether the recorded job ID remains visible to `qstat`, then queues a caller-supplied continuation message to the submitting Codex thread; the resumed `calc-execute` remains responsible for scheduler accounting, logs, outputs, acceptance, and Spec updates. We deliberately reject PBS event outboxes, accounting checks inside the monitor, persistent delivery history, duplicate suppression, queue retries, and guarantees after Codex exits so the coordination mechanism stays small and separate from calculation truth.
