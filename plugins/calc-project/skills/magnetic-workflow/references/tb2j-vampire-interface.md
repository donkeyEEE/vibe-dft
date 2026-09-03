# TB2J to VAMPIRE Interface

`wann2J.py` is the only source of `05-tb2j-<tag>/TB2J_results/Vampire/vampire.*`.
Treat it as read-only. For each simulation, copy every `vampire.*` to
`06-vampire-<tag>/VAMPIRE/<run-tag>/`, record source and copy checksums, and
verify they match.

The copied model is immutable. Its `input` inherits TB2J settings unchanged except
for `output:material-magnetisation` becoming `output:temperature` and
`output:mean-magnetisation-length`. Do not generate an alternate VAMPIRE input
template or edit the source. The VAMPIRE task stages `inputs/plot.py` and reads
those named `output` columns to generate `M_vs_T.png`.
