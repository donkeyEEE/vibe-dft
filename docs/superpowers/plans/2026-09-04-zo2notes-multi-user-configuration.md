# Zo2Notes Multi-User Configuration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Zo2Notes a read-only, zero-configuration-by-default Zotero client for native Windows, Windows Zotero accessed from WSL, and native macOS/Linux, with confirmed user-level overrides for exceptional environments.

**Architecture:** Introduce a focused runtime configuration module for TOML/environment/CLI precedence and platform-aware endpoint discovery, plus a separate attachment-path resolver. Refactor `zotero.py` to consume those interfaces, expose a read-only `doctor`, and remove every Zotero-mutating command. Keep configuration writing as an agent workflow governed by `SKILL.md`, not as an interactive application subsystem.

**Tech Stack:** Python 3.11+ standard library (`argparse`, `dataclasses`, `ipaddress`, `pathlib`, `platform`, `tomllib`, `urllib`), pytest, Markdown, TOML.

**Spec:** `docs/superpowers/specs/2026-09-04-zo2notes-multi-user-configuration-design.md`

## Global Constraints

- Support Windows native, Windows Zotero from WSL, and macOS/Linux native; remote containers and SSH hosts are out of scope.
- Use `CLI > environment variables > config.toml > automatic defaults` precedence.
- Use `%APPDATA%\zo2notes\config.toml` on Windows and `~/.config/zo2notes/config.toml` on macOS, Linux, and WSL.
- Default to port `23119`; never retain a machine-specific fallback such as `172.30.128.1`.
- A user-specified host is authoritative and must not silently fall back to another host.
- Zo2Notes must not modify Zotero entries, attachments, PDFs, profiles, preferences, or processes.
- Configuration creation or modification is performed by Codex only after showing the target and content and receiving user confirmation.
- Do not scan the filesystem for Zotero data or attachment locations, and do not expose complete attachment paths in normal output.
- Preserve existing project-storage behavior and unrelated working-tree changes.

---

### Task 1: Runtime Configuration and Endpoint Discovery

**Files:**
- Create: `plugins/paper-project/skills/zo2notes/scripts/runtime_config.py`
- Create: `plugins/paper-project/tests/zo2notes/test_runtime_config.py`

**Interfaces:**
- Produces: `ConfigError(ValueError)` for user-actionable configuration failures.
- Produces: `RuntimeConfig(mode: str, host: str | None, port: int, timeout_seconds: float, path_mappings: tuple[PathMappingConfig, ...], sources: dict[str, str])`.
- Produces: `PathMappingConfig(windows_prefix: str, local_prefix: str)`.
- Produces: `config_path(system: str, environ: Mapping[str, str], home: Path) -> Path`.
- Produces: `is_wsl(system: str, release: str, proc_version: str) -> bool`.
- Produces: `load_runtime_config(cli: Mapping[str, object], environ: Mapping[str, str], system: str, release: str, proc_version: str, home: Path) -> RuntimeConfig`.
- Produces: `default_gateway(route_output: str) -> str` and `wsl_default_gateway(run: Callable[..., CompletedProcess[str]] = subprocess.run) -> str`.
- Produces: `Endpoint(url: str, host_header: str, source: str)` and `candidate_endpoints(config: RuntimeConfig, gateway: str | None) -> tuple[Endpoint, ...]`.

- [ ] **Step 1: Write failing tests for platform detection and config-file location**

```python
def test_is_wsl_uses_kernel_markers():
    assert is_wsl("Linux", "5.15.90.1-microsoft-standard-WSL2", "")
    assert is_wsl("Linux", "6.1.0", "Linux version Microsoft WSL2")
    assert not is_wsl("Linux", "6.8.0-generic", "Linux version 6.8")

def test_config_path_uses_appdata_only_on_windows(tmp_path):
    assert config_path("Windows", {"APPDATA": r"C:\Users\Ada\AppData\Roaming"}, tmp_path) == Path(
        r"C:\Users\Ada\AppData\Roaming"
    ) / "zo2notes/config.toml"
    assert config_path("Linux", {}, tmp_path) == tmp_path / ".config/zo2notes/config.toml"
```

- [ ] **Step 2: Run the focused tests and verify the module is missing**

Run: `pytest plugins/paper-project/tests/zo2notes/test_runtime_config.py -v`

Expected: FAIL during import because `runtime_config.py` does not exist.

- [ ] **Step 3: Implement platform detection, config path selection, and immutable data classes**

```python
class ConfigError(ValueError):
    pass

@dataclass(frozen=True)
class PathMappingConfig:
    windows_prefix: str
    local_prefix: str

@dataclass(frozen=True)
class RuntimeConfig:
    mode: str
    host: str | None
    port: int
    timeout_seconds: float
    path_mappings: tuple[PathMappingConfig, ...]
    sources: dict[str, str]
```

Implement Windows `%APPDATA%` validation, XDG-style non-Windows location, and WSL recognition from the Linux release and `/proc/version` text passed into the pure function.

- [ ] **Step 4: Add failing tests for defaults, TOML parsing, validation, and precedence**

Use `monkeypatch` and temporary homes to cover:

```python
def test_precedence_is_cli_then_env_then_toml_then_default(tmp_path):
    write_config(tmp_path, '[zotero]\nmode="native"\nhost="toml-host"\nport=24000\n')
    config = load_runtime_config(
        {"host": "cli-host", "port": None, "mode": None, "timeout_seconds": None},
        {"ZO2NOTES_ZOTERO_HOST": "env-host", "ZO2NOTES_ZOTERO_PORT": "25000"},
        "Linux", "6.8", "Linux", tmp_path,
    )
    assert (config.host, config.port, config.mode) == ("cli-host", 25000, "native")
    assert config.sources == {
        "mode": "config",
        "host": "cli",
        "port": "environment",
        "timeout_seconds": "default",
    }
```

Also assert that malformed TOML, `version != 1`, an unknown mode, boolean/non-integer ports, ports outside 1–65535, non-positive timeouts, and incomplete path mappings raise `ConfigError` instead of falling back.

- [ ] **Step 5: Implement TOML loading, merging, and strict validation**

Use `tomllib.load()` only when the selected config path exists. Treat a missing file as normal. Reject unknown top-level tables and unknown keys under `[zotero]` or `[[attachments.path_mappings]]` so misspellings cannot be ignored. Normalize an empty host to `None`, resolve `auto` to `wsl` or `native`, and retain each winning source in `RuntimeConfig.sources`.

- [ ] **Step 6: Add failing tests for WSL gateways and endpoint order**

```python
def test_wsl_candidates_try_loopback_then_gateway():
    config = runtime(mode="wsl", host=None, port=23119)
    assert [endpoint.url for endpoint in candidate_endpoints(config, "172.20.0.1")] == [
        "http://127.0.0.1:23119",
        "http://172.20.0.1:23119",
    ]

def test_explicit_host_has_no_fallback():
    config = runtime(mode="wsl", host="192.0.2.10", port=24000)
    endpoints = candidate_endpoints(config, "172.20.0.1")
    assert [endpoint.url for endpoint in endpoints] == ["http://192.0.2.10:24000"]
```

Test rejection of loopback, unspecified, multicast, malformed, or absent default gateways, and deduplication if the discovered gateway equals an earlier candidate.

- [ ] **Step 7: Implement safe gateway parsing and endpoint generation**

Invoke `ip route` without a shell, parse only `default via <IPv4>`, and return a useful `ConfigError` when discovery fails. Build the request header as `127.0.0.1:<configured-port>` and preserve endpoint source labels such as `automatic-loopback`, `automatic-wsl-gateway`, and `explicit-host`.

- [ ] **Step 8: Run the runtime configuration tests**

Run: `pytest plugins/paper-project/tests/zo2notes/test_runtime_config.py -v`

Expected: PASS.

- [ ] **Step 9: Commit the runtime configuration unit**

```bash
git add plugins/paper-project/skills/zo2notes/scripts/runtime_config.py plugins/paper-project/tests/zo2notes/test_runtime_config.py
git commit -m "feat(zo2notes): add portable runtime configuration"
```

### Task 2: Cross-Platform Attachment Path Resolution

**Files:**
- Create: `plugins/paper-project/skills/zo2notes/scripts/attachment_paths.py`
- Create: `plugins/paper-project/tests/zo2notes/test_attachment_paths.py`

**Interfaces:**
- Consumes: `PathMappingConfig` from `runtime_config.py`.
- Produces: `AttachmentPathError(ValueError)` with safe public messages and no full source path.
- Produces: `ResolvedAttachment(path: Path, strategy: str)`.
- Produces: `resolve_attachment_path(raw_url: str, mode: str, mappings: Sequence[PathMappingConfig], exists: Callable[[Path], bool] = Path.exists) -> ResolvedAttachment`.
- Produces: `redact_attachment_path(raw: str) -> str` for doctor/error output.

- [ ] **Step 1: Write failing tests for native file URLs and Windows drive paths**

```python
def test_native_file_url_is_decoded_and_verified():
    resolved = resolve_attachment_path(
        "file:///tmp/My%20Paper.pdf", "native", (), exists=lambda path: True
    )
    assert resolved.path == Path("/tmp/My Paper.pdf")
    assert resolved.strategy == "native"

def test_wsl_standard_drive_maps_to_mnt():
    resolved = resolve_attachment_path(
        "file:///C:/Papers/a.pdf", "wsl", (), exists=lambda path: True
    )
    assert resolved.path == Path("/mnt/c/Papers/a.pdf")
    assert resolved.strategy == "wsl-drive"
```

- [ ] **Step 2: Run the attachment tests and verify the module is missing**

Run: `pytest plugins/paper-project/tests/zo2notes/test_attachment_paths.py -v`

Expected: FAIL during import because `attachment_paths.py` does not exist.

- [ ] **Step 3: Implement URL decoding, native resolution, standard drive conversion, and existence checks**

Accept only local `file:` URLs or local absolute paths returned for the selected attachment. Reject HTTP URLs, relative paths, NUL bytes, and traversal introduced during decoding. On WSL, map `X:/...` and `X:\...` to `/mnt/x/...` without invoking a shell.

- [ ] **Step 4: Add failing tests for explicit mappings and safe failures**

Cover case-insensitive Windows-prefix matching, path-boundary matching, declaration-order precedence, UNC paths requiring an explicit mapping, missing files, and redaction:

```python
def test_explicit_mapping_precedes_drive_mapping():
    mapping = PathMappingConfig(r"Z:\ZoteroStorage", "/data/papers")
    resolved = resolve_attachment_path(
        r"Z:\ZoteroStorage\topic\a.pdf", "wsl", (mapping,), exists=lambda path: True
    )
    assert resolved.path == Path("/data/papers/topic/a.pdf")
    assert resolved.strategy == "configured-mapping"

def test_failure_message_does_not_reveal_full_path():
    with pytest.raises(AttachmentPathError) as error:
        resolve_attachment_path(r"C:\Secret\Topic\paper.pdf", "wsl", (), exists=lambda path: False)
    assert r"C:\Secret\Topic" not in str(error.value)
    assert "paper.pdf" in str(error.value)
```

- [ ] **Step 5: Implement explicit mapping and redacted errors**

Apply mappings in declaration order, require a component boundary after the Windows prefix, append only the unmatched relative suffix, and validate the resulting file. Preserve only the filename and path kind in public errors.

- [ ] **Step 6: Run attachment tests**

Run: `pytest plugins/paper-project/tests/zo2notes/test_attachment_paths.py -v`

Expected: PASS.

- [ ] **Step 7: Commit the attachment resolver**

```bash
git add plugins/paper-project/skills/zo2notes/scripts/attachment_paths.py plugins/paper-project/tests/zo2notes/test_attachment_paths.py
git commit -m "feat(zo2notes): resolve Zotero attachments across platforms"
```

### Task 3: Read-Only Zotero CLI and Doctor

**Files:**
- Modify: `plugins/paper-project/skills/zo2notes/scripts/zotero.py`
- Delete: `plugins/paper-project/skills/zo2notes/scripts/zotero_wsl_bridge.py`
- Create: `plugins/paper-project/tests/zo2notes/test_zotero_cli.py`

**Interfaces:**
- Consumes: `RuntimeConfig`, `Endpoint`, `load_runtime_config()`, `candidate_endpoints()`, and `wsl_default_gateway()` from `runtime_config.py`.
- Consumes: `resolve_attachment_path()` and `AttachmentPathError` from `attachment_paths.py`.
- Produces: `ZoteroClient(config: RuntimeConfig, endpoints: Sequence[Endpoint], opener: Callable[..., object] = urllib.request.urlopen)`.
- Produces: `ZoteroClient.request(path: str, timeout: float | None = None) -> Response` using GET only.
- Produces: `ZoteroClient.select_endpoint() -> Endpoint` using `GET /api/` health checks.
- Produces: `doctor_payload(config: RuntimeConfig, endpoints: Sequence[Endpoint], client: ZoteroClient) -> dict[str, object]`.
- Produces: global CLI options `--mode`, `--host`, `--port`, and `--timeout-seconds`, plus `doctor [--json]`.

- [ ] **Step 1: Write failing parser tests for the read-only command surface**

```python
@pytest.mark.parametrize("removed", [
    "enable", "disable", "restart", "import-bibtex", "import-ris"
])
def test_mutating_commands_are_absent(removed):
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([removed])

def test_global_connection_overrides_parse():
    args = build_parser().parse_args([
        "--mode", "wsl", "--host", "192.0.2.10", "--port", "24000",
        "--timeout-seconds", "2.5", "doctor", "--json",
    ])
    assert (args.mode, args.host, args.port, args.timeout_seconds) == (
        "wsl", "192.0.2.10", 24000, 2.5
    )
```

- [ ] **Step 2: Run the parser tests and verify they fail against the old CLI**

Run: `pytest plugins/paper-project/tests/zo2notes/test_zotero_cli.py -v`

Expected: FAIL because mutating commands remain and global connection flags/doctor are absent.

- [ ] **Step 3: Remove Zotero mutation and machine-profile code**

Delete profile discovery, preference parsing/writing, backup, Zotero restart, Connector import, and associated imports (`configparser`, `platform`, `shutil`, `subprocess`, `time`, `uuid`) when no longer used. Remove the five mutating subcommands. Retain project-file operations such as BibTeX export and citation insertion because they do not write Zotero.

- [ ] **Step 4: Add global connection flags and runtime-config initialization**

Have `main()` collect only explicit CLI values and call `load_runtime_config()`. Pass one `ZoteroClient` through command handlers instead of using a module-level fixed URL. Change handlers to receive a context containing `args` and `client`, or bind the client after parsing; do not introduce module globals for mutable runtime configuration.

- [ ] **Step 5: Write failing client tests for endpoint selection, headers, and GET-only access**

Use a fake opener to assert:

- loopback is attempted before the WSL gateway;
- the first successful `/api/` response selects the endpoint;
- the configured port appears in both the URL and `Host` header;
- a user-specified host produces one attempt only;
- API version headers remain present;
- no request path can select a mutating HTTP method.

- [ ] **Step 6: Implement `ZoteroClient` and migrate all read commands**

Replace `DEFAULT_BASE_URL`, global bridge headers, `url_for()`, `request()`, `api_response()`, and `api_get()` with the client. Limit the client request API to GET. Retain response parsing, pagination, searches, collections, children, indexed full text, file URL retrieval, export, and citation formatting behavior.

- [ ] **Step 7: Write failing doctor-output tests**

```python
def test_doctor_reports_values_and_sources_without_local_paths():
    payload = doctor_payload(config, endpoints, fake_client)
    assert payload["runtime"]["mode"] == {"value": "wsl", "source": "automatic"}
    assert payload["runtime"]["port"] == {"value": 23119, "source": "default"}
    assert payload["api"]["running"] is True
    assert "/Users/" not in json.dumps(payload)
    assert r"C:\Users" not in json.dumps(payload)
```

Also test distinct results for unreachable Zotero, API unavailable, gateway discovery failure, malformed configuration, and an explicit host failure. The human-readable form must include the matching remediation, including manual Zotero UI instructions when the API is unavailable.

- [ ] **Step 8: Implement `doctor` and retain `status` as a compatibility alias**

Make `doctor` the documented command. Keep `status` as a hidden or documented compatibility alias returning the same payload for one release so existing calls do not break abruptly. Report sanitized candidate host/port information, effective values and sources, platform/mode, config presence, API status, and actionable next steps. Do not inspect profiles or attachments during a general doctor run.

- [ ] **Step 9: Integrate attachment resolution into `file-url`**

Add `file-url --resolve` so the default command continues to return Zotero's raw API value for internal consumption, while `--resolve` uses `resolve_attachment_path()` and emits the resolved local path only when explicitly requested. Errors shown normally must use `AttachmentPathError` redaction. Do not resolve or scan attachments during unrelated commands.

- [ ] **Step 10: Run CLI and existing storage tests**

Run: `pytest plugins/paper-project/tests/zo2notes/test_zotero_cli.py plugins/paper-project/tests/zo2notes/test_runtime_config.py plugins/paper-project/tests/zo2notes/test_attachment_paths.py -v`

Expected: PASS.

- [ ] **Step 11: Commit the read-only CLI**

```bash
git add plugins/paper-project/skills/zo2notes/scripts/zotero.py plugins/paper-project/skills/zo2notes/scripts/zotero_wsl_bridge.py plugins/paper-project/tests/zo2notes/test_zotero_cli.py
git commit -m "refactor(zo2notes): make Zotero access portable and read-only"
```

### Task 4: Agent Configuration Workflow and User Documentation

**Files:**
- Modify: `plugins/paper-project/skills/zo2notes/SKILL.md`
- Modify: `plugins/paper-project/skills/zo2notes/references/local-api-routes.md`
- Create: `plugins/paper-project/skills/zo2notes/references/configuration.md`
- Create: `plugins/paper-project/skills/zo2notes/references/troubleshooting.md`
- Modify: `plugins/paper-project/skills/zo2notes/references/论文精读模板.md`
- Create: `plugins/paper-project/tests/zo2notes/test_documentation_contract.py`

**Interfaces:**
- Consumes: exact config schema, environment variables, CLI options, doctor behavior, and path rules from Tasks 1–3.
- Produces: agent instructions for zero-config discovery and confirmed config writes.
- Produces: user-facing configuration and troubleshooting references.

- [ ] **Step 1: Write failing documentation-contract tests**

Test that active Zo2Notes docs contain the three supported environment descriptions, both config locations, all three environment variables, the precedence order, `doctor`, manual local-API enablement, and custom attachment mapping. Assert they contain neither `172.30.128.1` nor instructions to run the five deleted commands. Assert `SKILL.md` routes configuration failures to `references/configuration.md` and `references/troubleshooting.md`.

- [ ] **Step 2: Run documentation tests and verify they fail**

Run: `pytest plugins/paper-project/tests/zo2notes/test_documentation_contract.py -v`

Expected: FAIL because the current skill mandates a fixed Windows-to-WSL bridge and the new references do not exist.

- [ ] **Step 3: Rewrite the active skill contract**

Replace the fixed curl example with this workflow:

1. Run `python3 <plugin-root>/skills/zo2notes/scripts/zotero.py doctor --json`.
2. Continue without configuration if automatic detection succeeds.
3. Read `references/configuration.md` when host, port, mode, or attachment mapping is required.
4. Ask only for unknown values, show the exact target and TOML, and obtain confirmation before writing.
5. Re-run doctor after writing.
6. Read `references/troubleshooting.md` for API or connectivity failure.

State explicitly that users enable the local API inside Zotero and that the skill never changes Zotero settings or imports records.

- [ ] **Step 4: Write `configuration.md` with exact examples**

Document:

- supported and unsupported environments;
- platform-specific configuration locations;
- the version-1 TOML schema with a minimal port-only example and a WSL network-drive mapping example;
- CLI/environment/TOML/default precedence;
- automatic endpoint behavior and authoritative explicit host behavior;
- the confirmed Codex-write protocol;
- the fact that profile/data-directory configuration is neither required nor supported because normal evidence comes through the local API.

- [ ] **Step 5: Write `troubleshooting.md` and update route/template references**

Provide separate decision paths for Zotero not running, local API disabled, WSL gateway unavailable, explicit host unreachable, and attachment mapping failure. Update `local-api-routes.md` to describe portable base URLs and GET-only local API routes; remove Connector write routes. Update the reading-note template so the VS Code extension is explicitly optional and non-WSL environments use plain attachment key/page evidence locations.

- [ ] **Step 6: Run documentation-contract tests**

Run: `pytest plugins/paper-project/tests/zo2notes/test_documentation_contract.py -v`

Expected: PASS.

- [ ] **Step 7: Commit documentation and agent workflow**

```bash
git add plugins/paper-project/skills/zo2notes/SKILL.md plugins/paper-project/skills/zo2notes/references/local-api-routes.md plugins/paper-project/skills/zo2notes/references/configuration.md plugins/paper-project/skills/zo2notes/references/troubleshooting.md plugins/paper-project/skills/zo2notes/references/论文精读模板.md plugins/paper-project/tests/zo2notes/test_documentation_contract.py
git commit -m "docs(zo2notes): document multi-user Zotero setup"
```

### Task 5: Release Verification and Full Regression

**Files:**
- Modify: `plugins/paper-project/tests/resources/test_resource_release.py`
- Modify only if required by an actual validation failure: `plugins/paper-project/scripts/build_marketplace_release.py`

**Interfaces:**
- Consumes: all new runtime modules and references from Tasks 1–4.
- Produces: release assertions that the installed plugin contains the complete Zo2Notes runtime and no retired bridge module.

- [ ] **Step 1: Extend the release test with exact Zo2Notes assets**

Add assertions for:

```python
for relative in (
    "skills/zo2notes/scripts/runtime_config.py",
    "skills/zo2notes/scripts/attachment_paths.py",
    "skills/zo2notes/scripts/zotero.py",
    "skills/zo2notes/references/configuration.md",
    "skills/zo2notes/references/troubleshooting.md",
):
    assert prefix + relative in names
assert prefix + "skills/zo2notes/scripts/zotero_wsl_bridge.py" not in names
```

- [ ] **Step 2: Run the release test before any packaging change**

Run: `pytest plugins/paper-project/tests/resources/test_resource_release.py -v`

Expected: PASS if the existing recursive plugin packaging already includes the new files. If it fails, verify the failure is an actual packaging omission before changing the build script.

- [ ] **Step 3: Fix packaging only if the preceding test proves it necessary**

If new files are missing, adjust the existing include/exclude rules in `build_marketplace_release.py` narrowly so the complete `skills/zo2notes/` directory is copied. Do not add a second Zo2Notes-specific packaging path when recursive plugin copying already works.

- [ ] **Step 4: Run the complete paper-project test suite**

Run: `pytest plugins/paper-project/tests -v`

Expected: PASS.

- [ ] **Step 5: Run syntax and stale-reference checks**

Run: `python -m compileall -q plugins/paper-project/skills/zo2notes/scripts`

Expected: exit 0.

Run: `rg -n '172\.30\.128\.1|cmd_set_pref|set_local_api_pref|restart_zotero|import-bibtex|import-ris' plugins/paper-project/skills/zo2notes plugins/paper-project/tests/zo2notes`

Expected: no active-code or active-document matches. Test fixtures may mention removed command names only to assert their absence.

- [ ] **Step 6: Review the scoped diff**

Run: `git diff --check && git status --short && git diff --stat`

Expected: no whitespace errors; only Zo2Notes implementation/docs/tests and the paper-project release test are part of this feature. Preserve pre-existing unrelated changes to `CONTEXT.md` and other plan files.

- [ ] **Step 7: Commit release verification**

```bash
git add -p plugins/paper-project/tests/resources/test_resource_release.py
# Add build_marketplace_release.py only if Step 3 required and produced a scoped change.
git commit -m "test(zo2notes): verify portable release contents"
```

- [ ] **Step 8: Record final verification evidence**

Run: `git log --oneline -6 && git status --short`

Expected: the feature commits are present; all feature tests have passed; unrelated user changes remain unstaged and untouched.
