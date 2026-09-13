# Get Zotero 多用户配置

## 支持范围

正式支持 Windows 原生、Windows Zotero + WSL Codex、macOS/Linux 原生。远程容器、SSH 主机和远程 Zotero 服务不在当前支持范围内。

先运行：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py doctor --json
```

自动探测成功时不创建配置。默认端口是 `23119`。

## 配置位置与优先级

- Windows：`%APPDATA%\get-zotero\config.toml`
- macOS、Linux、WSL：`~/.config/get-zotero/config.toml`

优先级固定为：命令行参数 > 环境变量 > 用户 `config.toml` > 自动探测默认值。

环境变量为 `GET_ZOTERO_MODE`、`GET_ZOTERO_HOST`、`GET_ZOTERO_PORT`。CLI 对应 `--mode`、`--host`、`--port` 和 `--timeout-seconds`，且必须放在子命令之前。

## 配置格式

最小的非默认端口配置：

```toml
version = 1

[zotero]
mode = "auto"
host = ""
port = 24000
timeout_seconds = 5
```

WSL 网络盘或自定义挂载映射：

```toml
version = 1

[zotero]
mode = "wsl"
host = ""
port = 23119
timeout_seconds = 5

[[attachments.path_mappings]]
windows_prefix = "Z:\\ZoteroStorage"
local_prefix = "/data/zotero"
```

`mode` 只接受 `auto`、`native`、`wsl`。`host = ""` 表示自动探测；显式 host 是权威值，失败时不会静默改连其他主机。WSL 自动模式先尝试 `127.0.0.1`，再尝试动态发现的 Windows 主机地址，不保存易变化的 WSL 网关 IP。

已知运行环境且需要持久化显式 host 时，同时写入对应的明确 mode：WSL 写 `mode = "wsl"`，原生环境写 `mode = "native"`。只有无需固定环境行为时才保留 `mode = "auto"`。

Get Zotero 通过本地 API 读取题录与索引全文，因此不配置 Zotero profile 或 data directory。只有 PDF 原文定向核验遇到非标准网络盘、云盘或挂载点时才配置附件路径映射。

## Codex 代写协议

1. 运行 `doctor`，保留其只读诊断结果。
2. 只向用户询问诊断无法得到的 host、port 或路径映射。
3. 展示目标配置文件路径和完整 TOML 内容。
4. 得到用户明确确认后创建或修改配置；保留文件中无关的现有设置。
5. 配置内容没有变化时不重写。
6. 再运行 `doctor`，以 Get Zotero 的有效配置验证结果为完成标准。

用户级配置位于插件仓库之外；写入或修改属于外部环境变更，必须取得明确授权。
