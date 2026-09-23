# Get Zotero 故障排查

始终先运行：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py doctor --json
```

## Zotero 不可达

确认 Zotero Desktop 正在目标机器运行。原生 Windows、macOS 和 Linux 默认连接 `127.0.0.1:23119`。WSL 先尝试 loopback，再动态读取 Linux 默认网关和 Windows `vEthernet (WSL…)` 接口地址。

不要写死其他机器的 WSL 网关。动态发现失败时，检查 WSL 网络模式、Windows Local API 与防火墙边界；保持自动探测，不创建用户配置文件。

## 本地 API 未启用

请用户在 Zotero 的设置界面启用“允许本机其他应用与 Zotero 通信”或对应版本中的 Local API 选项。Get Zotero 不读取或修改 `prefs.js`，也不代替用户重启 Zotero。用户完成界面操作后重新运行 `doctor`。

## 显式 host 不可达

显式 host 不会自动回退。核对命令行参数、环境变量和已有配置中的 host、port 与运行环境。不要在 Get Zotero 流程中自行创建配置、防火墙规则、端口代理或远程转发。

## PDF 附件不可访问

索引全文、批注和题录可用时继续处理，不因 PDF 路径失败阻断整个条目。只有阅读问题必须核验 PDF 时才处理附件地址。

- 标准 Windows 盘符由 WSL 自动转换，例如 `C:\Papers\a.pdf` → `/mnt/c/Papers/a.pdf`。
- UNC、网络盘、云盘和自定义挂载需要用户提供 Windows 路径前缀与本地挂载前缀。
- 非标准挂载无法自动解析时返回结构化限制，不在 Get Zotero 流程中创建路径映射配置。
- 不扫描磁盘寻找附件，不在普通回复或笔记中暴露完整本地路径。

## 配置解析失败

无效 TOML、未知字段、非 `version = 1`、非法 mode、越界端口或非正 timeout 会直接失败。修正明确错误后再运行 `doctor`；不得删除配置或静默回退默认值。
