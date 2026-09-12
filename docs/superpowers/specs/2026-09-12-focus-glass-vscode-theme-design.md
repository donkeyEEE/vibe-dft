# Focus Glass VS Code Theme Design

## Goal

Create and activate a Windows-side VS Code color theme named **Focus Glass**. The theme preserves the palette and low-distraction intent of the user's WezTerm `Focus` profile while adding a restrained Acrylic/translucent presentation. The active VS Code window is connected to WSL, but the theme and window-effect extension belong to the Windows UI host.

## Source of truth

The palette comes from `/home/donk/.config/wezterm/wezterm.lua`, profile `Focus`:

- canvas: `#0b0f14`
- foreground: `#d8dee9`
- focus/cursor accent: `#88c0d0`
- selection: `#2b3b4d` / `#eceff4`
- active surface: `#1b2633`
- inactive surface: `#101720`
- muted foreground: `#7f8b99`
- ANSI normal: `#111820`, `#e06c75`, `#98c379`, `#e5c07b`, `#61afef`, `#c678dd`, `#56b6c2`, `#d8dee9`
- ANSI bright: `#3b4652`, `#ef7b84`, `#a9d18e`, `#f0d08b`, `#77bdfb`, `#d28ae5`, `#6cc8d2`, `#ffffff`

## Architecture

### Local color-theme extension

Install a local extension at `%USERPROFILE%\\.vscode\\extensions\\mr.focus-glass-0.1.0` containing:

- `package.json`: extension metadata and a single dark color-theme contribution.
- `themes/focus-glass-color-theme.json`: workbench colors, editor colors, integrated-terminal ANSI colors, semantic token colors, and TextMate token colors.
- `README.md`: local provenance and uninstall instructions.

The theme maps the WezTerm palette by role rather than blindly reusing ANSI colors. UI chrome stays quieter than source text; focus borders and interactive state use cyan-blue; errors, warnings, success states, Git decorations, diffs, and syntax families use the matching palette colors.

### Glass layer

Use the Windows-host extension `Vibrancy Continued` to provide actual desktop translucency/Acrylic. The theme uses translucent workbench surfaces derived from `#0b0f14`, with the editor most transparent and navigation surfaces slightly more opaque. The intended result is visible but subdued wallpaper texture without reducing text contrast.

If the window-effect extension is incompatible with the installed VS Code version, keep Focus Glass active as a normal dark theme and remove only the vibrancy-specific settings. The color theme must remain usable independently.

### Activation

Update the Windows VS Code user settings at `%APPDATA%\\Code\\User\\settings.json`:

- set `workbench.colorTheme` to `Focus Glass`;
- set `workbench.preferredDarkColorTheme` to `Focus Glass`;
- retain all unrelated existing settings;
- add only the settings required by the installed vibrancy extension.

Back up the settings file before editing. Because `window.autoDetectColorScheme` is enabled, the preferred dark theme ensures Focus Glass is selected when Windows is in dark mode; an explicit `workbench.colorTheme` makes it active immediately.

## Installation and compatibility

The theme is installed directly as an unpacked local extension so it does not require publishing or a marketplace account. The window-effect extension is installed through the Windows VS Code CLI. Configuration keys and accepted values are taken from the installed extension's manifest rather than assumed from older documentation.

VS Code may report that its installation is modified after a window-effect extension injects workbench CSS. That warning is an expected consequence of this class of extension. VS Code upgrades may require reapplying the glass effect.

## Safety and rollback

Before mutation:

1. Copy the current Windows `settings.json` to a timestamped sibling backup.
2. Confirm that no `mr.focus-glass-*` directory already exists; if one exists, preserve it before replacement.

Rollback consists of selecting another color theme, restoring the backed-up settings file, disabling/uninstalling Vibrancy Continued, and deleting only the exact local extension directory created by this work.

## Verification

Completion requires all of the following evidence:

1. Both extension JSON files parse successfully.
2. The theme manifest contributes `Focus Glass` and points to the existing theme JSON file.
3. Windows VS Code lists the local theme extension.
4. Windows user settings select `Focus Glass` and retain the pre-existing unrelated settings.
5. VS Code status confirms the active Windows client and WSL remote remain operational after reload.
6. The installed window-effect extension manifest confirms that the configured keys and values are valid for that installed version.

Visual quality will be checked against representative Python, JSON, Markdown, and terminal scopes available in the current workspace. The acceptance target is readable code, distinguishable comments/strings/keywords/types, visible selection and cursor, and unobtrusive chrome.

## Out of scope

- Publishing the theme to the Visual Studio Marketplace.
- Changing the WezTerm `Focus` profile.
- Modifying repository code or tests beyond this design record.
- Installing unrelated fonts, icon themes, wallpaper, or Windows customization utilities.
