---
status: accepted
---

# Rename repository and marketplace to vibe-dft

The repository and its Codex plugin marketplace are renamed from `yz-skills` / "YZ Skills" to
`vibe-dft` (all lowercase), including the marketplace name and display name in
`.agents/plugins/marketplace.json`, the install and upgrade commands in `README.md`, the
`CONTEXT.md` title, and the GitHub remote `donkeyEEE/yz-skills` → `donkeyEEE/vibe-dft`. The
rename is a brand change only: the four-plugin lineup (calc-project, paper-project, osm-project,
skill-incubator) and all skill identities stay unchanged.

`vibe-dft` is used as the canonical machine identifier everywhere (lowercase), so install
commands read `calc-project@vibe-dft`. The former name is retained only where it is historical or
path-bound: ADR titles, superpowers and scratch records, worktree/branch/tag names, the local
directory path `/home/donk/yz-skills`, the logo asset filename, and historical test fixture
strings. Contract tests that pin the marketplace name in live navigation text are updated to the
new name.
