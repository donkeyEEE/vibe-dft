# Focus Glass VS Code Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create, install, activate, and verify a Windows-hosted VS Code theme named Focus Glass based on the WezTerm Focus palette, with a compatible Acrylic/translucent window layer.

**Architecture:** An unpacked local VS Code extension owns the color theme and remains functional without window patching. A separately installed Windows UI extension owns the Acrylic effect; its installed manifest is inspected before settings are written so version-specific keys are correct. Windows user settings are backed up and minimally updated.

**Tech Stack:** VS Code color-theme JSON, VS Code extension manifest, Windows VS Code CLI, JSONC-aware Node validation, Vibrancy Continued.

**Spec:** `docs/superpowers/specs/2026-09-12-focus-glass-vscode-theme-design.md`

## Global Constraints

- Install the local theme at `%USERPROFILE%\\.vscode\\extensions\\mr.focus-glass-0.1.0`.
- Preserve the WezTerm Focus base palette and low-distraction intent.
- Preserve every unrelated key in `%APPDATA%\\Code\\User\\settings.json`.
- Create a timestamped settings backup before mutation.
- Configure only settings proven valid by the installed Vibrancy Continued manifest.
- Keep the color theme usable when the glass layer is disabled.
- Do not modify WezTerm or install unrelated customization assets.

---

### Task 1: Build and validate the local theme extension

**Files:**
- Create: `/mnt/c/Users/MR/.vscode/extensions/mr.focus-glass-0.1.0/package.json`
- Create: `/mnt/c/Users/MR/.vscode/extensions/mr.focus-glass-0.1.0/themes/focus-glass-color-theme.json`
- Create: `/mnt/c/Users/MR/.vscode/extensions/mr.focus-glass-0.1.0/README.md`

**Interfaces:**
- Consumes: WezTerm Focus palette from `/home/donk/.config/wezterm/wezterm.lua`.
- Produces: theme contribution label `Focus Glass` with id `focus-glass`, backed by `./themes/focus-glass-color-theme.json`.

- [ ] **Step 1: Confirm the target does not collide with existing user data**

Run:

```bash
find /mnt/c/Users/MR/.vscode/extensions -maxdepth 1 -type d -name 'mr.focus-glass-*' -print
```

Expected: no output. If a directory exists, rename only that exact directory to a timestamped `.backup-*` sibling before proceeding.

- [ ] **Step 2: Write a failing structural assertion**

Run:

```bash
test -f /mnt/c/Users/MR/.vscode/extensions/mr.focus-glass-0.1.0/package.json \
  && test -f /mnt/c/Users/MR/.vscode/extensions/mr.focus-glass-0.1.0/themes/focus-glass-color-theme.json
```

Expected: FAIL because the extension files do not exist.

- [ ] **Step 3: Create the extension manifest and README**

Create `package.json` with publisher `mr`, name `focus-glass`, version `0.1.0`, `engines.vscode` set to `^1.80.0`, and one `contributes.themes` entry whose label is `Focus Glass`, `uiTheme` is `vs-dark`, and path is `./themes/focus-glass-color-theme.json`. Document provenance, activation, rollback, and the optional glass dependency in `README.md`.

- [ ] **Step 4: Create the theme JSON**

Define:

- workbench surfaces derived from `#0b0f14` with alpha values between `CC` and `F2`;
- foreground and focus colors from `#d8dee9`, `#7f8b99`, and `#88c0d0`;
- editor selection, find, hover, bracket, diff, Git, diagnostic, and status colors;
- all 16 integrated-terminal ANSI colors exactly as specified in the design;
- semantic token colors for namespace, type, class, enum, interface, function, method, variable, property, parameter, keyword, string, number, regexp, operator, decorator, comment, and deprecated symbols;
- TextMate scopes covering comments, strings, constants, keywords, storage/types, entities/functions, variables, tags, attributes, markup headings, links, code, inserted, deleted, and changed content.

- [ ] **Step 5: Validate JSON and contribution wiring**

Run:

```bash
node -e "const fs=require('fs'); const d='/mnt/c/Users/MR/.vscode/extensions/mr.focus-glass-0.1.0'; const p=JSON.parse(fs.readFileSync(d+'/package.json')); JSON.parse(fs.readFileSync(d+'/themes/focus-glass-color-theme.json')); const t=p.contributes.themes[0]; if(t.label!=='Focus Glass'||t.uiTheme!=='vs-dark'||!fs.existsSync(d+'/'+t.path)) process.exit(1)"
```

Expected: exit 0.

### Task 2: Install and inspect the Windows glass provider

**Files:**
- Read: `/mnt/c/Users/MR/.vscode/extensions/illixion.vscode-vibrancy-continued-*/package.json`

**Interfaces:**
- Consumes: Windows VS Code CLI and Marketplace extension id `illixion.vscode-vibrancy-continued`.
- Produces: an installed Windows UI extension plus an exact list of supported configuration keys and enum values.

- [ ] **Step 1: Install through the Windows host CLI**

Run the Windows `code.cmd` from the detected VS Code installation with:

```text
--install-extension illixion.vscode-vibrancy-continued --force
```

Expected: the CLI reports successful installation or that the current version is already installed.

- [ ] **Step 2: Verify host-side installation**

Run the same Windows CLI with `--list-extensions --show-versions` and require a line beginning with `illixion.vscode-vibrancy-continued@`.

- [ ] **Step 3: Inspect configuration schema**

Parse the installed extension's `package.json` and list `contributes.configuration.properties`. Select a Windows Acrylic preset and opacity values only from keys and enums present in that schema. If the extension declares an incompatible VS Code engine or has no valid Windows configuration, stop glass configuration but continue with the independent color theme.

### Task 3: Back up and activate Windows settings

**Files:**
- Backup: `/mnt/c/Users/MR/AppData/Roaming/Code/User/settings.json.focus-glass-backup-<timestamp>`
- Modify: `/mnt/c/Users/MR/AppData/Roaming/Code/User/settings.json`

**Interfaces:**
- Consumes: theme label `Focus Glass` and validated Vibrancy Continued configuration keys.
- Produces: active Focus Glass selection and valid window-effect settings without losing existing configuration.

- [ ] **Step 1: Back up settings**

Copy the exact current file to a timestamped sibling and verify the backup is byte-identical before editing.

- [ ] **Step 2: Apply a JSONC-preserving settings update**

Use a Node script with VS Code's installed `jsonc-parser` when available; otherwise, because the current file is strict JSON, parse it with `JSON.parse`, mutate only these keys, and serialize it with four-space indentation:

```json
{
    "workbench.colorTheme": "Focus Glass",
    "workbench.preferredDarkColorTheme": "Focus Glass"
}
```

Add the validated Vibrancy Continued settings selected in Task 2. Keep `window.autoDetectColorScheme` and every unrelated key unchanged.

- [ ] **Step 3: Validate the resulting settings**

Parse the file and assert that both theme keys equal `Focus Glass`; compare the pre-change backup to ensure every original key/value other than `workbench.preferredDarkColorTheme` remains present and equal.

### Task 4: Reload and perform completion audit

**Files:**
- Read: Windows VS Code extension inventory, user settings, theme extension files, VS Code status.

**Interfaces:**
- Consumes: installed theme and glass provider.
- Produces: authoritative completion evidence or a precise residual manual action.

- [ ] **Step 1: Request a VS Code window reload**

Invoke the Windows VS Code CLI against the current WSL folder with `--reuse-window`; if the CLI cannot force a running window to reload extension contributions, record that a single `Developer: Reload Window` action is required rather than claiming live activation.

- [ ] **Step 2: Verify extension inventory and files**

Assert the Focus Glass directory and both JSON files exist, parse, and match the manifest. Assert Vibrancy Continued appears in the Windows extension inventory.

- [ ] **Step 3: Verify settings preservation and activation**

Parse the final settings and backup, confirm `Focus Glass` is selected, validate all glass settings against the installed manifest, and confirm unrelated settings are preserved.

- [ ] **Step 4: Verify the remote session remains healthy**

Run `code --status` and require both the Windows client section and `Remote: WSL: Ubuntu-24.04` section.

- [ ] **Step 5: Review representative token mappings**

Inspect the final theme mappings for Python, JSON, Markdown, and terminal roles. Require distinct colors for comments, strings, keywords, functions/types, numbers, errors, warnings, selection, cursor, and all terminal ANSI slots.

- [ ] **Step 6: Commit the completed plan state**

Mark completed checkboxes in this plan, run `git diff --check`, and commit only the plan update. Windows user-profile artifacts remain outside the repository.
