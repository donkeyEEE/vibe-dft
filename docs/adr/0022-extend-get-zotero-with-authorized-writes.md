# 0022 — Extend get-zotero with authorized writes and complete attachment coverage

Date: 2026-10-14
Status: accepted

## Context

The user requested reusable Zotero library writes alongside existing retrieval. A separate writer would duplicate connection and authorization behavior. Existing consumers depend on get-zotero's command paths, configuration and content schema version 1. The current reader selects the first PDF, which can be SI instead of the article; the reported Fe3GaTe2/Fe3GeTe2 example confirmed this ordering in the real library.

## Decision

Extend get-zotero in place. Preserve existing read commands and content discriminators; add an attachment manifest and bundle for all direct attachments, and teach existing consumers to inspect every attachment. Role labels are hints until content is checked. Read commands remain non-mutating.

Add write-plan and write-apply. A plan fixes the library, objects, before/after values, versions, file hashes and deletion effects. The agent obtains authorization for concrete changes; an explicit user instruction can supply it. Deletion and file overwrite need separate authorization. Apply checks the approved digest, versions and scope, then reports and verifies individual results. Partial failure preserves successful changes. Restoration is a new concrete plan.

Use the application name Codex for all workflows. Per the user's later instruction, persist only remembered local grants in the user's configuration directory with restricted permissions, bound to Zotero Server ID and endpoint. Reuse grants across invocations; never store them in a project or expose them in artifacts. Revocation invalidates the cache. Application authorization and concrete change authorization remain separate.

## Consequences

The historical get-zotero name now includes library maintenance, avoiding path and consumer migrations. Its description and displayed name make writes discoverable. Compatible v1 consumers must inspect the added attachment list to meet the expanded coverage requirement.

Local writes require Zotero 10+ and the API's runtime capabilities. The local implementation can omit template routes; derive fields from its schema when needed. Unsupported operations or MIME types are reported rather than bypassing Zotero permissions or modifying the database directly. Cross-library copying and duplicate merging remain outside the promised operations.

## Validation

CLI tests use a simulated local API for preview, authorization, concurrency, partial failures, creation, deletion, index writes and file uploads. Real Zotero 10.0.6 validation used disposable objects and cleaned them up, while the reported paper was only read. No pre-existing literature was modified.
