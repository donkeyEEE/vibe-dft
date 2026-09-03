# PRL figure evidence logic

A PRL figure is a compressed visual inference. Its panel order and visual hierarchy must preserve the scientific logic that prose compression cannot safely remove.

## Assign evidence roles before layout

Give every proposed panel exactly one primary role:

- **Prerequisite:** establishes material, geometry, symmetry, baseline, model, or experimental design.
- **Signature:** shows the decisive effect or calculated feature.
- **Validation:** tests the same signature with an independent calculation, measurement, condition, or representation.
- **Control:** changes the proposed cause while preserving the strongest plausible alternative.
- **Sensitivity:** exposes the parameter range, construction dependence, uncertainty, or failure boundary.
- **Criterion:** defines a threshold, fit, transition, phase boundary, or extracted quantity.
- **Consequence:** demonstrates the physical, experimentally observable, or functional implication.

If a panel has no unique role, merge or remove it. If one panel carries several incompatible roles, split its visual task or make the hierarchy explicit.

## Default evidence sequences

Choose the shortest sequence that makes the claim auditable:

- Discovery or experiment: `prerequisite -> signature -> criterion -> control -> consequence`
- Mechanism: `signature -> competing explanation -> discriminating control -> bounded interpretation`
- Theory or computation: `assumption/condition -> calculated signature -> validation or sensitivity -> observable consequence`
- Phase diagram or tuning study: `baseline -> parameter-dependent signature -> operational boundary -> robustness`

These are dependency sequences, not mandatory panel letters. A headline signature may lead when the prerequisite is compactly embedded in the same panel.

## Cross-panel correspondence

When pairing model and validation, use the same observable, axis meaning, condition colors, and comparable scales where scientifically valid. State what agreement and mismatch mean. Do not use visual similarity as a substitute for a quantitative or mechanistic comparison.

When claiming a mechanism, label what the control changes and what it holds fixed. If the comparator changes several variables, show or state the residual confounder.

When a result depends on computational construction or parameter choice, visualize the sensitivity as evidence. Separate qualitative stability from quantitative variation.

## Quantitative claim contract

Every quantitative panel must expose or document:

- operational definition of the reported quantity;
- comparison condition and units;
- sample, seed, fold, or calculation count as applicable;
- center and uncertainty/variability definition;
- fit, threshold, or phase-boundary rule;
- excluded data and sensitivity to the relevant analysis choice.

## Main figure and Supplemental Material

Keep panels that establish the central claim, decisive discriminator, and indispensable boundary in the main figure set. Move repeated traces, derivations, extended sweeps, and secondary controls to Supplemental Material only with an explicit main-text link. Do not hide the only mechanism control or robustness test in the supplement when the headline claim depends on it.

## Pre-layout review

Before selecting an archetype or palette, verify:

1. The core claim has a decisive signature panel.
2. Mechanism language has a discriminating control.
3. Prediction language has an observable consequence and is not mislabeled as observation.
4. Model assumptions and sensitivity are visible where they change interpretation.
5. Quantitative criteria and uncertainty survive at final size.

These rules synthesize the PRL shared cards tagged `task/figure`; consult the individual card when a task turns on its specific caveat.
