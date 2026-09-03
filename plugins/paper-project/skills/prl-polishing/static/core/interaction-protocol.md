# Interactive review protocol

Use a staged review for multi-paragraph or section-level prose so the user can
control scope and approve every substantive rewrite. Do not present the
revision map and all rewritten paragraphs in the same turn.

## Choose the mode

- **Interactive review:** default for two or more paragraphs, a complete
  section, or a manuscript excerpt with several inferential jobs.
- **Single-paragraph review:** go directly to the paragraph comparison.
- **Direct mode:** use only when the user explicitly asks for a one-shot polish,
  a complete final version, or no intermediate confirmation.

If paragraph boundaries are unreliable, segment by inferential job and state
that choice in the revision map. Assign stable IDs (`P1`, `P2`, ...) and retain
them throughout the conversation.

## Phase A: revision map

First state the detected routing axes. Then provide a concise revision map
without rewriting the whole draft. For each paragraph, show:

- stable paragraph ID;
- current inferential role;
- main problem;
- proposed scope of change (`light`, `moderate`, or `structural`);
- intended action;
- evidence risk or missing information, if any.

End by asking the user to confirm or adjust the map. Do not begin paragraph
rewriting until the map is accepted, unless the user explicitly asks to start
immediately.

## Phase B: one paragraph per turn

Work on exactly one unresolved paragraph per turn unless the user explicitly
requests a batch.

### Phase B1: selectable located changes

The first review of a paragraph does **not** show an assembled proposed
paragraph. It shows the complete original and independently selectable change
proposals.

Assign stable sentence IDs (`O1`, `O2`, ...) in source order and display them
with the complete original paragraph. Retain these IDs throughout the review.
Then assign stable change IDs (`C1`, `C2`, ...) and use this format:

### P<n> — <inferential role>

**Material used**

List the selected item key, tags, source location, and the smallest relevant fragment. If the search returned no usable fragment, write `No relevant material found`.

**Active style habits**

List the applicable confirmed habits. If there are none, state `No active style habits`.

**Original**

`O1` <complete first sentence>

`O2` <complete second sentence>

Do not alter or omit text when adding these locator labels.

### C<n> — <short change purpose>

**Original location**

List every affected original sentence ID, its sentence number, and a short
exact anchor copied from the original, for example:
`O2 — sentence 2; anchor: “share closely related layered crystal structures”`.

**Before**

Reproduce the complete affected original sentence. For a merge, split, or
deletion, reproduce every affected original sentence in source order.

**After**

Give the complete replacement sentence or sentences. Do not use an ellipsis or
show only changed words.

**Why**

Give a concise reason tied to argument, evidence, boundary, section role,
terminology, or language. Identify the supporting material when it motivates a
scientific change.

**Decision**

- `Accept C<n>` — lock this After text.
- `Reject C<n>` — lock the exact Before text.
- `Revise C<n>: <instruction>` — keep this change open and revise only it.

End with a compact decision prompt. Users may decide changes individually or
in one batch, including natural-language forms such as
`C1 采纳；C2 拒绝；C3 把机制表述再弱化`.

Do not show a `Proposed`, `Polished`, or assembled paragraph in Phase B1.

### Change decision ledger

Track one state for every stable change ID:

- `pending_change`
- `accepted_change`
- `rejected_change`
- `revising_change`

Accept locks the current After text. Reject locks the complete Before text.
Revise retains the same change ID, updates only that proposal, and waits for a
new decision. Do not silently apply overlapping changes. If two changes affect
the same source sentence, disclose the overlap and resolve it before assembly.

### Phase B2: delayed assembly and paragraph decision

Do not assemble or show the revised paragraph while any change remains
`pending_change` or `revising_change`. Once every change is
`accepted_change` or `rejected_change`, assemble in original order:

- accepted changes contribute their locked After text;
- rejected changes contribute their exact Before text;
- sentences without a change proposal remain verbatim.

Only then show:

**Assembled paragraph**

The paragraph assembled from the resolved change decisions.

**Evidence boundary**

Include this only when a criterion, control, assumption, citation, or
validation is missing.

**Your decision**

- `Accept` — lock the proposed paragraph.
- `Revise` — keep this paragraph open and apply the user's requested changes.
- `Keep original` — lock the exact original paragraph and discard the proposal.
- `Skip for now` — leave the paragraph unresolved and move to the next one.

Wait for the paragraph decision. If the user requests revision, reopen only the
specified change or create a new located change proposal; do not advance until
the paragraph is accepted, kept original, or skipped. Natural-language
equivalents count, including “保留原文”, “用原文”, “不要改这段”, and “改回去”.

## Decision ledger

Track one state for every stable paragraph ID:

- `pending`
- `proposed`
- `accepted_revision`
- `kept_original`
- `skipped`

The change ledger is subordinate to this paragraph ledger. Resolving a change
does not resolve the paragraph and does not trigger a style-habit candidate.

Also retain the accepted text and any user-specified terminology decision.
`kept_original` is immutable during consolidation: preserve the user's exact
text, punctuation, and wording. Do not silently apply global style,
terminology, spelling, punctuation, or transition normalization to it. Reopen
the paragraph only after an explicit user request.

After recording a decision, briefly acknowledge it and continue with the next
unresolved paragraph. If the user changes the scope or journal, update the map
for affected unresolved paragraphs before continuing.

## Style habit candidate

Only after a paragraph reaches `accepted_revision` or `kept_original`, identify whether the interaction reveals a durable writing preference. Do not treat a one-off scientific, evidentiary, or paragraph-specific instruction as a habit.

Show the candidate with scope, preference, avoided form, and source paragraph. Persist it only after the user confirms it. If it conflicts with an active habit, identify the old habit and retain it as `superseded`; never silently delete style history. An explicit durable instruction may be recorded immediately, but tell the user what was recorded.

## Phase C: consolidated delivery

When all paragraphs are `accepted_revision` or `kept_original`, provide:

1. the consolidated text in original paragraph order;
2. a compact decision summary showing which paragraph IDs were revised and
   which retained the original;
3. unresolved evidence boundaries, if any.
4. the updated managed work-draft path and the new non-overwriting confirmed snapshot.

Do not call a draft final while paragraphs remain `skipped` or `pending`.
Instead, list those IDs and ask whether to review them or consolidate a clearly
labelled partial version.
