# Output format

Interactive review is the default for multi-paragraph prose. Follow
`interaction-protocol.md` for the revision map, paragraph comparison, decision
ledger, and consolidated delivery. In particular, every paragraph review must
offer `Keep original`, and a paragraph in `kept_original` state must remain
verbatim in the consolidated text.

Direct-mode output:

1. The polished text as plain prose, not in a code block.
2. `Revision notes:` with `3-5` short bullets on the major structural and stylistic changes.
3. If the rewrite changed section logic, say so explicitly.
4. If evidence is insufficient for the requested wording, add `Evidence boundary:` and name the missing criterion, control, assumption, or validation rather than silently weakening or strengthening the claim.

For a single-paragraph interactive review, first provide the complete original
with stable `O<n>` sentence locators and selectable `C<n>` change proposals.
Every change must contain `Original location`, complete `Before`, complete
`After`, `Why`, and `Accept/Reject/Revise C<n>` decisions. Do not show an
assembled `Polished` or `Proposed` paragraph until every change is accepted or
rejected. After delayed assembly, offer the paragraph-level `Accept`, `Revise`,
`Keep original`, and `Skip for now` decisions.

If any paragraph's structural problem could not be fixed without inventing content, say so under `Revision notes:` instead of papering over it.

For managed manuscripts, disclose material matches before proposals, apply only active confirmed habits, update `草稿/01-工作稿/`, and create the confirmed snapshot only after all paragraph decisions resolve. Label any explicitly requested incomplete snapshot as partial.
