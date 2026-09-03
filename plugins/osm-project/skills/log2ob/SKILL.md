---
name: log2ob
description: Use when the user issues $log2ob as a command to record project progress, or unequivocally asks to record the current conversation in an Obsidian project log.
---

# log2ob

Turn the complete current conversation into a minimal project-state snapshot, show the exact canonical draft, and write only that approved draft.

Classify the current request before any helper call:

- **Recording branch:** the user issues `$log2ob` as an actual command to start recording, or unequivocally asks to record the current project work in Obsidian. Enter the workflow below.
- **Informational branch:** the user asks what `$log2ob` does, merely mentions its name or logs, or states that work is ending without asking to record. Answer the request normally without `inspect` or `upsert`.
- **Unclear branch:** recording intent is plausible but ambiguous. Ask one concise question and wait without a helper call.

Resolve `scripts/journal.py` relative to this file. It is the only permitted mutation path for the vault at `/mnt/d/02LYZ_PKM`; use no general-purpose editor or direct filesystem write for vault Markdown. Read its JSON stdout as success and JSON stderr as failure.

## Structured helper transport

Every helper call uses one private, temporary JSON request. The shell command contains only the resolved helper path, a static `inspect` or `upsert` subcommand, and a filesystem-derived request path. Project names, revisions, dates, and field values exist only inside the JSON file.

For each call:

1. Run `mktemp -d /tmp/log2ob-request.XXXXXX` and retain the exact returned directory.
2. Use the `apply_patch` tool, whose file content is structured tool input rather than shell input, to create `<returned-directory>/request.json`. Serialize valid JSON with double-quoted keys and escaped JSON string values. The directory created by `mktemp -d` is private to the current user.
3. Invoke the helper with `python3 <resolved-skill-dir>/scripts/journal.py inspect --request <request-path>` or the corresponding static `upsert` subcommand. No request value appears elsewhere on this command line.
4. Capture and parse stdout or stderr, then remove the exact request file with `rm -- <request-path>` and its now-empty directory with `rmdir -- <returned-directory>`. Perform this cleanup after success and after error before continuing the workflow.

The request document for `inspect` has exactly this shape:

```json
{"vault":"/mnt/d/02LYZ_PKM","date":"YYYY-MM-DD","project":"<Project Identity>"}
```

The request document for `upsert` has exactly this shape and includes only approved, nonempty fields:

```json
{"vault":"/mnt/d/02LYZ_PKM","date":"YYYY-MM-DD","project":"<Project Identity>","expected_revision":"<revision>","fields":{"任务":"...","进展":"..."}}
```

## Workflow

Follow this sequence for every eligible request:

1. **Project Identity.** Derive the active repository or workspace name. The level-four heading is both the visible name and update key. Use the shortest name that distinguishes the project in today's note; add the shortest parent context for a same-name collision, such as `plugins/osm-project-dev`. Without reliable workspace evidence, propose a short conversation-derived name. Treat a rename as a new project unless the user explicitly maps it to an existing heading.
2. **Inspect.** Compute today's date in `Asia/Shanghai` as `YYYY-MM-DD`. Create an `inspect` JSON request through Structured helper transport and retain that date plus the returned `revision`, `project_exists`, and `fields`. If those fields clearly belong to a different same-name project, qualify the identity with parent context and inspect that identity before continuing. A missing Daily Note or structural/access error stops the workflow with the helper's recovery action.
3. **Recordable Progress.** Decide whether the complete current conversation contains substantive project progress: an implemented or diagnosed change, a consequential decision, verified evidence, or unresolved state needed to resume. When none exists, report that there is nothing useful to record and stop without a draft or write.
4. **Work Session Summary.** Compress the complete current conversation into these six ordered fields, omitting empty fields:

   - `任务`: the goal that organized the work.
   - `起点`: only the prior state needed to understand the change.
   - `进展`: substantive work actually completed.
   - `结论`: evidence and the conclusion it supports.
   - `未决`: unresolved issues that constrain continuation.
   - `入口`: the first resume action, including action, object, and completion criterion.

   Render the exact canonical draft with the helper's heading, blank line, and field layout (representative included fields shown):

   ```markdown
   #### <Project Identity>

   - **任务**：<value>
   - **进展**：<value>
   ```

   The heading is followed by one blank line; included field lines are adjacent and follow the six-field order above. Omit empty fields. Use semicolons only when multiple points are indispensable. Keep facts, conclusions, and planned work distinct; retain a failed route only when it prevents repeated work or constrains the result.
5. **Evidence and content safety.** Verify only claims relevant to work already present in the conversation, using available repository state, diffs, files, and test output. Prefer the evidence-backed current state when it conflicts with a conversational claim, while preserving the intended goal separately. Mark a material claim as unverified when available evidence cannot support it. Exclude secrets, credentials, tokens, personal data, and large raw diagnostic output. Use repository-relative paths unless an absolute path is essential to resume; state that sensitive detail was omitted when that omission changes interpretation.
6. **State Merge.** When `project_exists` is true, merge the new evidence into the returned `fields`: confirmed changes replace stale facts; old state untouched by this conversation remains; an old unresolved item disappears only when new evidence resolves or disproves it; a consequential resolved issue may be compressed into `结论`. Produce one complete replacement draft rather than an invocation history.
7. **Confirmation draft.** Present the Project Identity, proposed operation (`add` or `update`), the exact canonical level-four block, and semantic changes for either operation. The semantic-change list consists exactly of its non-empty categories and follows one of these shapes:

   - Add: `新增：新建 <Project Identity> 项目块，包含 <included fields>。`
   - Update: include only applicable lines selected from `新增：<new state>`, `修改：<old state> → <new state>`, and `移除：<resolved or disproved old state>`.

   Then wait for explicit approval of that exact draft. The mutation capability exists only when a direct approval such as `确认写入` or `同意该草稿` follows the displayed draft; urgency or a request to skip confirmation leaves the workflow at this approval wait. A requested edit creates a new exact draft and a new approval wait.
8. **Approved write.** Immediately before creating the `upsert` request, recompute today's date in `Asia/Shanghai`. The retained revision and approval are bound to the inspected date as well as the exact draft. If the recomputed date differs, discard the earlier write capability, return to Inspect for the new date, repeat State Merge against that note, present the new exact draft and semantic changes, and wait for new explicit approval. If the date is unchanged, create one `upsert` JSON request through Structured helper transport using the retained date and revision plus every exact approved, nonempty field. Report only the helper's returned `operation`: `added`, `updated`, or `unchanged`.
9. **Revision recovery.** If `upsert` reports a stale revision or concurrent change, return to Inspect, then repeat State Merge, present the fresh exact draft and semantic changes, and wait for new explicit approval before another `upsert`. The earlier approval authorizes only its earlier draft and revision.

## Examples

- **New project:** `inspect` returns `project_exists: false`. The conversation shows the parser was implemented and 18 tests passed. Present `add`, `#### log2ob`, fields such as `进展：实现项目块解析与 guarded upsert。` and `结论：18 项测试通过，当前实现已验证。`, then `新增：新建 log2ob 项目块，包含任务、进展、结论、入口。`; write only after the user explicitly approves that block.
- **Existing project:** returned `fields` include an unresolved packaging task; this conversation completes helper tests but says nothing about packaging. State Merge updates `进展` and `结论`, retains the packaging item in `未决`, and presents `update` with only the applicable `新增` or `修改` lines before waiting for approval.
- **Informational mention:** for “`$log2ob` 是做什么的？我现在还不想记录任何东西”, explain the capability and perform no inspection. A bare end-work statement or discussion of logs follows the same informational branch until the user asks to record.
- **Eligible but no progress:** the user issues `$log2ob 记录本次会话`, but the complete conversation contains only a greeting and no substantive project work. Derive the identity and run `inspect`; at Recordable Progress, report that there is nothing useful to record and stop with no draft and no `upsert`.
- **Sensitive content:** a diagnostic pasted an access token while establishing an authentication failure. Record `结论：认证失败已复现；敏感凭据已省略。`, excluding the token and raw trace from the draft.
- **Evidence conflict:** the conversation says “tests pass,” but the relevant fresh test output has two failures. Record the evidence-backed failures in `结论` or `未决` and keep passing the suite as the intended resume goal; do not claim completion.
- **Stale revision:** the user approves draft A, then `upsert` reports that the note changed since inspection. Inspect the new fields and revision, merge them with the conversation, present draft B and its semantic changes, and write only after explicit approval of draft B.
- **Shanghai midnight rollover:** inspection and draft A use `2026-08-30`, but the pre-upsert date check returns `2026-08-31`. Inspect the `2026-08-31` Daily Note, merge against that note, present draft B, and wait for explicit approval of draft B; draft A and its approval authorize no write on either date.
