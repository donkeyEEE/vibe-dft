# Zo2Notes 多用户配置与跨平台访问设计

## 背景

Zo2Notes 当前把 Zotero Desktop 的访问固定为 Windows-to-WSL bridge，并在代码中写死 `172.30.128.1:23119`。主脚本还包含查找 Zotero profile、修改 `prefs.js`、启用或停用本地 API、重启 Zotero 的能力。这些行为依赖特定机器环境，也超出了 Zo2Notes 作为只读文献来源客户端的边界。

本设计将 Zo2Notes 改为面向多用户的只读客户端。首版正式支持：

- Windows 原生运行 Codex 与 Zotero；
- WSL 中运行 Codex、Windows 中运行 Zotero；
- macOS 或 Linux 原生运行 Codex 与 Zotero。

远程容器和 SSH 主机不在首版支持范围内。

## 目标与非目标

### 目标

- 普通用户在 Zotero 使用默认端口时无需创建配置。
- 自动识别原生环境与 WSL，并选择可用的本地 API 地址。
- 特殊环境允许通过用户配置、环境变量或命令行覆盖连接信息。
- 用户提供无法自动判断的信息，Codex 在展示变更并得到确认后代写配置。
- 支持 WSL 中的标准 Windows 附件路径转换和显式自定义映射。
- Zo2Notes 对 Zotero 保持只读，只在用户项目目录和经确认的用户配置文件中写入。

### 非目标

- 自动修改 Zotero profile、`prefs.js` 或数据目录。
- 自动启用或停用 Zotero 本地 API。
- 自动重启 Zotero。
- 扫描磁盘寻找 Zotero 数据目录或附件。
- 支持任意远程 Zotero 服务、容器网络或 SSH 转发。

## 总体架构

采用统一运行时配置层：

```text
zo2notes/
├── SKILL.md
├── references/
│   ├── configuration.md
│   └── troubleshooting.md
└── scripts/
    ├── zotero.py
    ├── runtime_config.py
    ├── attachment_paths.py
    └── project_storage.py
```

`runtime_config.py` 负责配置加载、覆盖优先级、平台识别、候选端点生成和连接选择。`attachment_paths.py` 只负责附件地址规范化、路径映射和存在性验证。`zotero.py` 保留只读 Zotero CLI，通过上述模块取得已解析的运行时设置，不再自行实现平台分支。

现有 `zotero_wsl_bridge.py` 不再作为独立接口。其安全的动态网关识别逻辑并入 `runtime_config.py`，随后删除该文件。

## 配置契约

### 配置位置

- Windows：`%APPDATA%\zo2notes\config.toml`
- macOS、Linux 和 WSL：`~/.config/zo2notes/config.toml`

默认不创建配置。只有自动探测失败或用户需要非默认行为时，才创建用户级配置。

### 格式

```toml
version = 1

[zotero]
mode = "auto"
host = ""
port = 23119
timeout_seconds = 5

[[attachments.path_mappings]]
windows_prefix = "Z:\\ZoteroStorage"
local_prefix = "/mnt/z/ZoteroStorage"
```

字段约束：

- `version` 必须为受支持的整数版本；首版只接受 `1`。
- `mode` 只接受 `auto`、`native` 或 `wsl`。
- 空 `host` 表示自动探测；非空值表示用户明确指定。
- `port` 必须是 1–65535 的整数，默认值为 `23119`。
- `timeout_seconds` 必须是正数。
- 路径映射按声明顺序匹配，第一个匹配项生效。

配置文件不得保存 Zotero 文献内容、API 密钥、项目路径或扫描所得路径。

### 覆盖优先级

```text
命令行参数 > 环境变量 > config.toml > 自动探测默认值
```

首版环境变量为：

- `ZO2NOTES_ZOTERO_MODE`
- `ZO2NOTES_ZOTERO_HOST`
- `ZO2NOTES_ZOTERO_PORT`

命令行参数与环境变量使用同一套类型和取值校验。`status --json` 报告每个最终值及其来源，但不得输出完整附件路径。

### Codex 代写流程

1. Codex 运行只读 `doctor`。
2. 自动探测成功时不创建配置。
3. 自动探测失败时，Codex只询问无法判断的 host、port 或路径映射。
4. Codex展示目标配置位置和拟写内容。
5. 用户确认后，Codex创建或修改配置。
6. Codex重新运行 `doctor` 验证。

首次创建和任何内容修改都必须确认。配置内容未变化时不重复确认或重写。

## 平台与连接探测

运行时配置层先识别环境，再产生有序候选端点：

- `native`：使用显式 host；未配置时只尝试 `127.0.0.1:<port>`。
- `wsl`：未配置 host 时先尝试 `127.0.0.1:<port>`，再尝试动态读取的 WSL 默认网关。
- `auto`：检测是否运行于 WSL；是则采用 `wsl`，否则采用 `native`。

用户明确指定 host 后，只尝试该 host，不静默回退到其他地址。所有 Zotero API 请求继续携带与实际端口一致的 `Host: 127.0.0.1:<port>` 以及 Zotero API version header，以兼容 Windows 侧受限转发。

候选端点通过轻量、只读健康检查依次验证。选定端点后，查询命令复用同一解析结果，不单独实现平台判断。

## Doctor 与 Zotero 只读边界

新增或规范化 `doctor` 命令，报告：

- 当前平台与识别出的运行模式；
- 配置文件是否存在；
- 最终配置值及来源；
- 每个候选端点是否可达；
- Zotero 本地 API 是否可用；
- 下一步修复建议。

删除 `enable`、`disable`、`restart`、`import-bibtex` 和 `import-ris` 命令，并删除只为这些命令服务的 profile 发现、`profiles.ini` 读取、`prefs.js` 修改、备份、进程重启和 Zotero Connector 导入代码。文档改为指导用户在 Zotero 界面中手动启用本地 API。

Zo2Notes 可以写入以下位置：

- 用户明确指定的项目笔记或论文写作库；
- 用户确认后的 Zo2Notes 用户级配置文件；
- 定向取证所需的临时目录。

Zo2Notes 不修改 Zotero 条目、附件、批注、PDF、profile 或应用设置。

## 附件路径解析

Zotero indexed full text 仍是默认正文来源。只有确实需要核验原始 PDF 时，才请求附件地址并解析本地路径。

路径处理规则：

- Windows、macOS 和 Linux 原生环境直接规范化并验证 Zotero 返回的路径。
- WSL 首先尝试用户声明的 `attachments.path_mappings`。
- 没有匹配的显式映射时，将标准 Windows 盘符路径转换为 WSL 挂载路径，例如 `C:\Papers\a.pdf` 转为 `/mnt/c/Papers/a.pdf`。
- UNC、网络盘、云盘和非标准挂载不进行猜测；必须由用户提供显式映射。
- 转换后必须验证目标文件存在，且只允许处理当前 Zotero 条目返回的附件路径。
- 失败时不得扫描磁盘。用户输出仅显示足以区分问题的脱敏路径摘要。

附件不可访问不阻断题录、摘要、批注或 Zotero indexed full text 的处理。只有请求确实依赖原始 PDF 证据时，才将附件路径错误报告为该取证步骤的失败。

## 错误处理

下列失败必须可区分，并提供针对性提示：

- 配置文件不存在：正常进入自动探测。
- 配置文件语法或字段无效：明确失败，不静默回退默认值。
- Zotero 未运行或端点不可达：列出已尝试的脱敏候选地址。
- 本地 API 未启用：指导用户在 Zotero 界面中启用。
- WSL 网关无法识别：建议显式提供 host，不回退到固定 IP。
- 附件路径无法转换或文件不存在：请求用户提供路径映射。
- 显式 host 不可达：只报告该 host 失败，不尝试其他主机。

错误信息不得暴露完整附件路径、文献正文或其他本地敏感信息。

## 文档调整

- `SKILL.md` 只保留 agent 必须执行的配置优先级、只读边界、探测和取证规则，并在需要时路由到详细参考文档。
- `references/configuration.md` 说明支持环境、配置位置、字段、覆盖优先级、Codex 代写流程和附件映射示例。
- `references/troubleshooting.md` 说明如何在 Zotero 界面启用本地 API，以及连接失败、WSL 网关和附件不可访问的处理方式。
- 删除所有固定 `172.30.128.1` 以及“所有请求必须走 Windows-to-WSL bridge”的规范性表述。
- PDF 页码链接保留为可选的 VS Code WSL 集成；不可用时继续降级为附件 key 与页码文本，不把该扩展列为跨平台前置条件。

## 测试策略

单元测试至少覆盖：

- Windows、WSL、macOS 和 Linux 的平台识别；
- `auto`、`native` 和 `wsl` 的候选端点顺序；
- CLI、环境变量、TOML 和默认值的覆盖优先级；
- TOML 语法、版本、mode、host、port 和 timeout 校验；
- WSL 动态网关以及 `127.0.0.1` 优先行为；
- 显式 host 禁止静默回退；
- Windows 盘符、UNC、自定义映射、最长前缀歧义和不存在文件；
- doctor 与错误输出不泄露完整附件路径；
- CLI 中不存在 `enable`、`disable`、`restart`、`import-bibtex` 和 `import-ris`；
- 既有只读查询与项目存储逻辑的回归行为。

发布包测试必须确认新增模块和参考文档都包含在 paper-project 插件发布单元中，且没有旧固定地址或已删除命令的活动引用。

## 验收标准

- 三类正式支持环境均不依赖源码中的机器专属地址。
- 默认 Zotero 配置下，普通用户无需配置即可连接。
- 特殊用户可提供 host、port 或附件路径映射，并由 Codex 在确认后写入用户配置。
- Zo2Notes 不查找或修改 Zotero profile 和应用设置。
- `doctor` 能区分连接、配置、API 和附件路径问题，并给出可执行的修复提示。
- 所有平台与配置优先级测试通过，发布包包含全部运行时依赖与文档。
