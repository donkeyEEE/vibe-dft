# S04 — Incremental Spec publication in automatic mode

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture. The
user chooses automatic mode in each prompt; choice and collaborative approval
are covered by S15.

## Exact prompts

`S04-next-spec`:

> Use automatic Spec design for this request. RQ-001 is accepted and asks whether the synthetic structure is stable. Publish the next Spec supported by its current evidence. The RQ does not request execution.

`S04-incremental-rq`:

> Use automatic Spec design for this request. Advance accepted RQ-001 through its currently supported stability judgment. Magnetic ordering may become a later question but is not yet determined by the available evidence. Do not invent the later Spec now.

`S04-legacy-evidence-field`:

> Use automatic Spec design for this request. Publish the next complete Spec for RQ-001. An old Spec contains Evidence level: strict and explicit acceptance requirements. Preserve that old Spec unchanged; design the new one from the research objective and concrete user requirements.

`S04-critical-gap`:

> Use automatic Spec design for this request. Design the next Spec, but the accepted RQ and available evidence leave two scientifically different methods whose choice changes the principal judgment. Research before deciding; interview if that critical gap remains.

`S04-exploratory-design`:

> Use automatic Spec design for this request. Publish an exploratory Spec to diagnose whether the two candidate mechanisms can be distinguished. No quantitative threshold or fixed stopping rule is known. Specify the observation or comparison to obtain and how it informs the next choice.

`S04-repeat-idempotent`:

> Use automatic Spec design for this request. Retry publication of an already identical SPEC-001 and RQ index link. Keep one Spec and one link.

`S04-owner-conflict`:

> Use automatic Spec design for this request. Publish SPEC-001 for RQ-001 at an existing target owned by another RQ. Inspect the target before writing.

## Expected observations

- In explicitly chosen automatic mode, the next complete Spec publishes without a separate approval or mandatory interview, uses domain-research to guide evidence and computational choices, without asking for an evidence level, updates one accurate RQ index entry, and stops when execution was not requested.
- Incremental publication does not invent or require a complete future Spec set. When RQ advancement includes execution intent, it hands the published Spec to `calc-execute`.
- New designs do not write or inherit Evidence level. Old Specs and their explicit commitments remain unchanged; legacy labels do not add checks to the new design.
- Missing scientific evidence triggers targeted research or literature review; only an unresolved critical scientific gap triggers `grill-with-docs`.
- An exploratory design may publish with executable tasks and clear completion requirements without a quantitative threshold or predetermined stopping rule. A conflicting owner leaves the target and RQ index unchanged.
- Repeating identical publication leaves one Spec and one index link.
