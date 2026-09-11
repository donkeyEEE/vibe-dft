# S08 — Transient review

Direct probes natively invoke `calc-review`; the resume probe supplies
`calc-execute` and `calc-review` in a fresh context.

## Exact prompts

`S08-harmless-warning`:

> Directly review the prepared Run data/TASK-001/RUN-001 and return the transient judgment. This is a read-only review request.

`S08-risk-choice`:

> Directly review the prepared Run data/TASK-001/RUN-001 and return the transient judgment. This is a read-only review request.

`S08-fresh-execute-rereview`:

> Resume the unsubmitted prepared Run data/TASK-001/RUN-001 and report whether it is ready for submission. I am not authorizing a submission.

## Expected observations

- The harmless queue note is `pass_with_warnings`; the resource mismatch is
  `block` with an owner.
- Every review leaves input and domain hashes unchanged and creates no review
  state file.
- Fresh execute reinspects the snapshot and cannot reuse the diagnostic text.
