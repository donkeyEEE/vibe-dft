# Diagnose failure mode before editing

Before rewriting, identify the main problem:

- wrong paper type logic
- missing gap or poor positioning
- claim without evidence
- evidence without a clear claim
- missing boundary or limitation
- Results and Discussion mixed together
- weak title or abstract signal
- inconsistent terminology, abbreviations, units, or notation across sections
- sentence-level clutter only
- condition or model assumption removed during compression
- mechanism claim without a discriminating control or comparator
- quantitative claim without its operational criterion or uncertainty
- predicted observable written as if it had been measured
- supplementary evidence carrying a missing main-text logical link

Prioritize fixes in this order:

`paper type -> central inference -> evidence dependency -> paragraph logic -> claim/evidence/boundary -> sentence polish`

Do not sentence-polish a draft whose section job is wrong. Surface the structural problem first, then polish.

Terminology consistency is a cross-cutting check that runs at every level: after following the shared-library protocol, load ATOM CARD `write-terminology-ledger`, build the Terminology Ledger on first contact, and enforce its canonical forms throughout the polish.
