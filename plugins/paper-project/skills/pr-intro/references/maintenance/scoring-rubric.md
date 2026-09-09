# Fixed continuation scoring rubric

Use this rubric when scoring development or acceptance continuations under
[optimization-protocol.md](optimization-protocol.md). Evaluate whether the
continuation advances the scientific argument supported by the visible context
and allowed facts. The published continuation is one reference path; a sound
alternative can earn an equal or higher score. Wording similarity is not a
scoring dimension. Read the continuation and reference holistically without
persisting rhetorical labels.

## Dimension anchors

Assign one integer from 1 through 5 to every applicable dimension. Use the
lowest anchor that accurately captures a material unresolved defect rather
than averaging away fabrication within a dimension. Record concise evidence
for each score. SCC has the five shared dimensions; FGCC has all six, including
`fact_packet_use`. The identifiers match `scripts/eval_model.py` exactly.

| Dimension | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| `logical_continuation` | Unrelated or contradictory argument; no usable next step. | Some topical connection, but an unsupported leap or repetition prevents progress. | Plausible next step with a missing bridge or weak motivation. | Coherent progression with only a minor transition or emphasis defect. | Precise, necessary progression that resolves the prior setup and motivates the next scientific question. |
| `scientific_compatibility` | Central claim contradicts supplied science or reverses a key condition. | Major mismatch of mechanism, regime, or inference. | Broadly compatible but one consequential ambiguity or unsupported implication remains. | Scientifically compatible with only a minor imprecision that leaves the inference intact. | All material claims, mechanisms, assumptions, and scope align with available evidence. |
| `fact_packet_use` (FGCC only) | Contradicts the packet or substitutes invented findings. | Uses isolated facts but misses the central supplied result or its essential condition. | Uses the central facts accurately but omits a needed limitation or places them weakly. | Integrates relevant facts accurately with a minor omission or placement issue. | Selects and positions all facts needed for this argument step, preserving conditions and significance without dumping the packet. |
| `information_density` | Empty boilerplate or repetition carries virtually no scientific information. | Large amounts of generic framing obscure a small useful point. | Communicates useful information with avoidable repetition, detail, or compression gaps. | Compact and informative with a small amount of removable wording. | Each sentence supplies a necessary relation, constraint, or consequence at readable density. |
| `physical_review_expression` | Meaning is obscured by incoherence, severe language problems, or unsupported promotional language. | Frequent vague, inflated, or awkward wording disrupts the scientific argument. | Readable journal prose but uneven precision, emphasis, or sentence flow. | Clear, restrained, and precise prose with minor stylistic defects. | Economical Physical Review prose: exact claims, connected sentences, calibrated emphasis, and clear scientific stakes. |
| `non_fabrication` | Invents a central result, source, citation, number, or claim of established novelty. | Adds material unsupported detail or presents speculation as established evidence. | Avoids explicit invented results but overextends a boundary or leaves a consequential source status unclear. | Keeps claims grounded with a minor overstatement or qualification omission. | Every concrete claim is grounded or explicitly conditional; unknown results remain unknown and no source or citation is invented. |

A gap in supplied evidence can be handled by a clearly limited statement or a
question. It need not reduce the score when that choice still makes the next
argument step. An SCC must not be penalized for withholding an undisclosed
result. An FGCC need not repeat every packet fact if the next argument step
does not need it. Preserve distinctions between empirical results, model
assumptions, proposed mechanisms, and unresolved possibilities.

## Score records and statistics

The evaluator stores case ID, case type, tested candidate hash, all raw integer
dimension scores, concise score evidence, and the normalized score. Validate
the score mapping with `normalized_score(scores, case_type)`. Missing, extra,
non-integer, Boolean, or out-of-range values invalidate the score and block
candidate mutation until corrected; never impute a score or discard a poor
valid answer.

For SCC, normalized score is `100 * sum(scores) / 25`. For FGCC it is
`100 * sum(scores) / 30`. The range is 20–100, not 0–100. For example, all
dimensions scored 3 produce 60 for either type. These formulas follow the
immutable evaluator; a candidate cannot change dimensions or normalization.

Compute the aggregate as the arithmetic mean of normalized scores across all
valid cases, giving each case one vote. Also report SCC and FGCC separately.
Each group report contains case count, mean, median, minimum, maximum, and
population standard deviation. Report missing groups as count 0 with unavailable
statistics. For baseline/candidate comparisons, use the same cases and show
the candidate-minus-baseline mean delta overall and for each case type. Raw
dimension means are useful diagnostics in development, but they do not replace
the normalized aggregate or the two case-type reports.

Development may expose per-case evidence to the optimizer. Acceptance returns
only those aggregate and separate SCC/FGCC statistics plus the pass decision;
the independent acceptance coordinator keeps all per-case material private.
Acceptance passes only on a strictly higher aggregate than the original
baseline. A decline in SCC or FGCC remains prominently reportable even when
the aggregate improves. Never tune the rubric, group weights, or scoring
anchors after inspecting candidate performance.
