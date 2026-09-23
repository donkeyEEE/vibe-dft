# S04 — Incremental autonomous Spec publication

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture.

## Exact prompts

`S04-next-spec`:

> RQ-001 is accepted and asks whether the synthetic structure is stable. Publish the next Spec supported by its current evidence. The RQ has no Evidence level and does not request execution.

`S04-incremental-rq`:

> Advance accepted RQ-001 through its currently supported stability judgment. Magnetic ordering may become a later question but is not yet determined by the available evidence. Do not invent the later Spec now.

`S04-strict-inheritance`:

> Publish the next complete Spec for RQ-001. Its RQ.md says Evidence level: strict and the user has not set a Spec override.

`S04-critical-gap`:

> Design the next Spec, but the accepted RQ and available evidence leave two scientifically different methods whose choice changes the principal judgment. Research before deciding; interview if that critical gap remains.

`S04-incomplete-design`:

> Publish a Spec even though the intended judgment still has no acceptance criterion or stopping rule.

`S04-repeat-idempotent`:

> Retry publication of an already identical SPEC-001 and RQ index link. Keep one Spec and one link.

`S04-owner-conflict`:

> Publish SPEC-001 for RQ-001 at an existing target owned by another RQ. Inspect the target before writing.

## Expected observations

- The next complete Spec publishes without a separate approval or mandatory interview, uses `light` by default, updates one accurate RQ index entry, and stops when execution was not requested.
- Incremental publication does not invent or require a complete future Spec set. When RQ advancement includes execution intent, it hands the published Spec to `calc-execute`.
- An RQ strict setting is resolved and written into the Spec at publication. Later RQ changes do not silently modify it.
- Missing scientific evidence triggers targeted research or literature review; only an unresolved critical scientific gap triggers `grill-with-docs`.
- An incomplete design and a conflicting owner leave the target and RQ index unchanged.
- Repeating identical publication leaves one Spec and one index link.
