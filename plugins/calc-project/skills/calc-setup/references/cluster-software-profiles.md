# 集群软件配置档案

仅在请求配置集群时创建项目根目录的 `software-profiles.md`。记录经用户审阅的主机、
组件标签、路径或调用方式，以及一条精确的非交互验证命令。默认值属于配置，不是验证证据。

在档案中保留此标记块，以便验证器只替换其中的内容：

```markdown
<!-- cluster-profile-status:start -->
## 验证状态

尚未运行探测。已配置的默认值未经验证。
<!-- cluster-profile-status:end -->
```

每次探测一项已审阅条目：

```bash
bash <calc-project-plugin-root>/skills/calc-setup/scripts/verify_cluster_profile.sh \
  <project-root>/software-profiles.md <ssh-host> <component-label> \
  '<reviewed-remote-command>'
```

验证器直接调用 `ssh -- "$host" "$remote_command"`。它既不在本地执行该命令，
也不添加 shell 初始化、路径或命令。探测后，它在现有标记块内记录给定标签和命令、
必要时明确截断的有限输出摘要，以及 `verified` 或 `unavailable`。后续探测保留其他
组件行，并替换相同组件标签的行。
SSH 失败是不具备可用性的证据；档案更新后会返回失败。重试前应审阅失败的探测；
不得将其重新标记为已验证。

## 档案条目示例

以下 mu01 示例仅为历史起点。仅当项目选择该条目时才复制它；审阅其当前路径和精确探测，
并在运行该探测前明确保持为 `unverified`。

| 组件 | 配置示例 | 探测示例 | 初始状态 |
|---|---|---|---|
| PBS / Torque | `qsub`, `qstat` after project-reviewed initialization | `source /etc/profile && qstat -B` | unverified |
| VASP standard | `/data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_std` | `test -x /data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_std` | unverified |
| VASP noncollinear | `/data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_ncl` | `test -x /data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_ncl` | unverified |
| VASPKIT | `/data1/yuzheli-alkemie/01Soft/vaspkit.1.3.5/bin/vaspkit` | `test -x /data1/yuzheli-alkemie/01Soft/vaspkit.1.3.5/bin/vaspkit` | unverified |
| Wannier90 | `/data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/wannier90.x` | `test -x /data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/wannier90.x` | unverified |
| postw90 | `/data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/postw90.x` | `test -x /data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/postw90.x` | unverified |
| TB2J | `conda run -n tb2j wann2J.py` | `conda run -n tb2j wann2J.py --help` | unverified |
| VAMPIRE | `/data1/yuzheli-alkemie/01Soft/vampire/linux/vampire` | `test -x /data1/yuzheli-alkemie/01Soft/vampire/linux/vampire` | unverified |
| Hefei-NAMD | `/data1/yuzheli-alkemie/07soft/Hefei-NAMD/src/namd` | `test -x /data1/yuzheli-alkemie/07soft/Hefei-NAMD/src/namd` | unverified |
| NAMDwithSOC | `/data1/yuzheli-alkemie/07soft/NAMDwithSOC/src/namd_soc` | `test -x /data1/yuzheli-alkemie/07soft/NAMDwithSOC/src/namd_soc` | unverified |

具体 Run 准备通过 `calc-execute` 重新检查精确且可变的环境；设置阶段的档案证据不授权提交。
