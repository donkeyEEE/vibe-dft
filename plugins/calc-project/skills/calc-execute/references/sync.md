# 预览式同步

远程检查、规划或传输选定 Task 时读取本资料。从计算项目根运行全部命令，并从本 skill 的安装目录解析随附脚本。

选定 Task 根目录保存 `calc-sync.yaml`：

```yaml
local: 02原始数据/example/TASK-001
server: cluster:/absolute/calculation/path/TASK-001
exclude:
  - "*.tmp"
```

映射恰有 `local`、`server` 和 `exclude`。`local` 相对于项目根，`exclude` 是安全相对 glob 模式列表。`server` 由明确 SSH 主机和绝对 Task 根路径组成；路径组件仅使用可移植字母、数字、`.`、`_` 和 `-`，不允许 shell 操作符、替换、通配符、空白或独立的 `.`、`..` 组件。文件只配置同步工具；Spec 保持 Task 与 Run 状态权威。

使用准确的 Task 根配置路径：

```bash
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py validate <task-root>/calc-sync.yaml
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py inspect <task-root>/calc-sync.yaml
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py plan <task-root>/calc-sync.yaml
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py plan <task-root>/calc-sync.yaml --direction push
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py push <task-root>/calc-sync.yaml --yes
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py pull <task-root>/calc-sync.yaml --yes
```

`inspect` 可选，用于远程列表诊断。`plan` 默认 pull，执行一次 `rsync --dry-run`，打印报告且不保存同步状态。检查计划，确认路径及传输方向服务于选定 Run，再以 `--yes` 执行对应 `push` 或 `pull`，随后报告传输。执行直接读取当前配置和文件系统，不绑定先前报告，也不检查评审以来的变化；动作前须核实当前情况。

所有扩展名大小写的 HDF5 文件、`CHGCAR` 和 `WAVECAR` 均留在服务端。两个方向均排除 `calc-sync.yaml`、`.calc-sync/`、本地缓存、配置模式和符号链接；传输不使用删除模式。工具验证配置及 Task 根位置，不逐文件远程探测，也不检查已保存计划、指纹、过期或不可变输入比较。
