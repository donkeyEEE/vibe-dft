# Managed writing workspace protocol

Use this protocol for manuscript or section revision. Free-floating single-paragraph examples that the user does not want persisted may remain conversational.

## Establish readiness

Locate the managed writing library before the revision map. Use `<project-root>/<research-line>/07-论文写作库/` for an existing research line or `<manuscript-parent>/论文写作库/` for a standalone manuscript. If it is absent, route material-library creation to `zo2notes`; require exactly one user-confirmed Zotero collection. Work from `草稿/01-工作稿/`, never the external manuscript or `草稿/00-原稿/`.

## Per-paragraph evidence and style sequence

For every unresolved paragraph, follow this order:

1. Identify its inferential role and one to three search topics.
2. **Search material** with `scripts/writing_workspace.py`: exact tags first, then title, then paragraph text.
3. Select only directly relevant fragments and retain item key and source location.
4. Read active style habits applicable to the section and language.
5. **Draft the proposal** with the original paragraph as authority, material as evidence context, and confirmed habits as style constraints.

Disclose the fragments actually used. If none matches, state `No relevant material found`; absence does not block ordinary language cleanup.

## Evidence boundary

A material fragment is not permission for a silent citation, for presenting a literature result as the authors' own result, or for unsupported strengthening. Do not automatically add a citation. Report a relevant source as a citation suggestion and ask the user before changing citation content. Put missing, ambiguous, or conflicting evidence under `Evidence boundary`.

## Persistence

After the existing paragraph decision resolves the paragraph, update only the managed working draft. A possible durable preference becomes a style-habit candidate; do not persist it until the user confirms it. Explicit durable instructions may be recorded immediately with disclosure. One-off content, evidence, or paragraph instructions are not habits.

When a confirmed habit replaces an active habit, retain the old record as `superseded`. After every paragraph is accepted or kept original, update the work draft and create a non-overwriting confirmed snapshot. Pending or skipped paragraphs allow only an explicitly requested `_partial` snapshot.
