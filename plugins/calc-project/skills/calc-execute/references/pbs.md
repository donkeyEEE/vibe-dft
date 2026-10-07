# PBS 提交

验证 Run 目标环境或提交准确的受评输入快照时读取本资料。

## 精确环境探测

向所属探测工具传入一个主机和一条已审查的只读远程命令：

```bash
bash ../scripts/probe-run-environment.sh HOST 'REMOTE_COMMAND'
```

工具原样将命令交给 `ssh`，显示 stdout 并返回 SSH 状态，不补加软件配置加载、可执行路径或回退。依据维护的项目软件配置及渲染后的 Run 构造命令；评审前将下表带引号的操作数替换为准确配置值：

| 目标 | 精确命令形式 |
|---|---|
| PBS / Torque | 在受评命令包含的准确配置初始化后执行 `command -v qsub && command -v qstat` |
| VASP SCF、band、Wannier pre-run 或 MAE | `test -x '/configured/vasp-executable' && test -x '/configured/vaspkit-executable' && command -v mpirun` |
| DMFT | `test -x '/configured/dmft-entrypoint'` |
| Hefei-NAMD | `test -x '/configured/namd'` |
| NAMDwithSOC | `test -x '/configured/namd_soc'` |
| Wannier90 | `test -x '/configured/wannier90.x' && command -v '/configured/mpi-launcher'` |
| TB2J | `conda run -n 'configured-environment' wann2J.py --help` |
| VAMPIRE | `test -x '/configured/vampire'` |

这些操作数是占位项，不是默认值。使用软件配置中的原始路径、环境名称、初始化和启动器。配置项缺失时停止该 Run 并返回 `calc-setup`，不能从历史 mu01 路径推断。多 backend 阶段所需命令分别执行，保留各自输出及失败归属。

## 提交门禁

依次准备、验证、瞬时 `calc-review`，紧接着复核可变环境和上游 current Run，再提交未变输入。评审仅适用于当前执行链；不在 Run 中持久化 digest、评审结论或授权标记。

使用本执行链验证成功时打印的 digest 提交：

```bash
bash /exact/task/RUN-NNN/inputs/run.sh submit "$reviewed_digest"
```

`submit` 先加载已评审的 Run-local 环境，再重新计算完整 `inputs/` 指纹，在 `qsub` 前拒绝缺失或不匹配的 digest。该顺序可检测环境加载对输入的副作用。提交自身不准备、验证、复制或编辑；它切换到 Run 目录，准确提交 `inputs/run.pbs`，将 PBS stdout 和 stderr 分别送至 `logs/pbs.stdout` 与 `logs/pbs.stderr`。

保留可见的 qsub 作业 ID，并简要记入 Spec 的 Run 行。校验和仅保护字节身份。选定 Spec 的执行委托授权在用户明确约束内提交已验证、已评审的 Run；提交前核实实际队列、资源、成本和并发。
