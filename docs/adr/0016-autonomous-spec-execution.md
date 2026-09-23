---
status: amended by ADR-0017
---

# Let Calc Execute complete an approved Spec autonomously

A request to execute a selected ready or active Spec authorizes `calc-execute`
to carry its existing scientific design through the execution lifecycle.
Within the user's explicit constraints, it may choose technical remedies,
submit and monitor jobs, synchronize results, cancel obsolete jobs, adjust
resources and cost, clean up execution artifacts, update Task and Run records,
and close the Spec when its approved evidence and stopping rules justify closure.
It records the action and evidence instead of pausing for another approval.
The execution handoffs to `calc-setup` and `show-cot` follow the same scope;
standalone calls to those skills retain their own approval rules.

A change to the Spec's scientific design is handled through `calc-to-spec` under
ADR-0017. The execution request does not authorize a
change to RQ decisions, source-repository installation or publication, or an
action the user explicitly excluded. Ambiguous scientific evidence remains
unresolved until approved authorities support a conclusion. Safety checks,
snapshot review, provenance, and preservation of accepted Run evidence remain
required.

This amends ADR-0011's manual promotion rule for verified execution knowledge
and ADR-0014's confirmation rule when `show-cot` is called by `calc-execute`.
