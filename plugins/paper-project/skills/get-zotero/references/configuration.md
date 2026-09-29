# Get Zotero 多用户配置

## 支持范围

正式支持 Windows 原生、Windows Zotero + WSL Codex、macOS/Linux 原生。远程容器、SSH 主机和远程 Zotero 服务不在当前支持范围内。

先运行：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py doctor --json
```

正常流程不要求或创建配置文件。所有支持的环境默认连接 `127.0.0.1:23119`。自动识别 WSL 只用于解析 Windows 附件路径，不改变本地 API 的连接地址。

## 配置位置与优先级

- Windows：`%APPDATA%\get-zotero\config.toml`
- macOS、Linux、WSL：`~/.config/get-zotero/config.toml`

优先级固定为：命令行参数 > 环境变量 > 用户 `config.toml` > 默认值。

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

`mode` 只接受 `auto`、`native`、`wsl`，用于选择附件路径解析方式；`auto` 按运行环境识别。`host = ""` 使用本机 `127.0.0.1`；显式 host 是权威值，失败时不会静默改连其他主机。若旧配置固定了 WSL 网关地址，镜像网络下可清空 `host` 恢复本机连接。

需要固定附件路径解析方式时，WSL 写 `mode = "wsl"`，原生环境写 `mode = "native"`；通常保留 `mode = "auto"`。

Get Zotero 通过本地 API 读取题录与索引全文，因此不配置 Zotero profile 或 data directory。只有 PDF 原文定向核验遇到非标准网络盘、云盘或挂载点时才配置附件路径映射。

## 当前工作流边界

Get Zotero 不创建、修改或要求用户配置文件。已有配置仍按兼容优先级读取；没有配置时以 `doctor` 的默认连接结果为准。
