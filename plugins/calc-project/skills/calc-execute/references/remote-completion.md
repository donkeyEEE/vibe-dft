# 远程完成检查

Run 已记录为 `submitted` 后读取，处理可选监控、恢复、完成判断与结果同步。

## 启动计算监控器

选定 Spec 需等待异步作业后恢复时启动。监控器负责本地协调；Run 状态、验收和 Spec 仍由 `calc-execute` 维护。
`qsub` 返回 job ID 且 Spec 已记录 `submitted` 后，解析配置的调度器 host、权威 Spec 与 current Run 路径，
从 `CODEX_THREAD_ID` 取线程。必需值缺失时不启动，报告 job ID 与手动查询命令。

将 `../scripts/calculation-monitor.py` 作为独立本地进程启动，使用当前平台可用的监督器，
优先 `systemd-run --user`，其他平台采用等价后台机制。使用 argv 数组，保留提交进程的 `PATH`，
丢弃监控器 stdout 和 stderr，报告已接受的启动方式。没有适用启动器时报告监控未启用，保留已提交作业。
Python 可执行文件、脚本路径及下列参数分别传入：

```text
--host CONFIGURED_HOST
--job-id QSUB_JOB_ID
--thread-id CODEX_THREAD_ID
--spec ABSOLUTE_SPEC_PATH
--run LOCAL_AUTHORITATIVE_RUN_PATH
--message CALLER_SELECTED_MESSAGE
--interval 30
```

本地 Run 路径须在监控机器存在；监控失败不改变或重复提交。

## 等待与恢复

活动监控器负责等待。后续调用先查本地监控单元；若仍活动，且没有完整 `PBS_JOB_LEFT_QSTAT` 消息
或用户明确状态查询，则继续等待。
监控器检查记录的作业是否仍对 `qstat` 可见；消息仅表示唤醒，SSH 或 `qstat` 失败也可能触发。
监控停止却没有消息时，诊断监控器并核对调度器，再决定是否重启；观察失败不导致重新提交作业。

## 判断完成

先重读权威 Spec、Task、Runs 和项目配置，将消息的 host、job ID、Spec、Run 与记录匹配，
确认 current Run 和真实生命周期。消息路径是启动时引用；过时消息不能推进替换 Run 或重复完成状态转换。

按[通用委派规则](../SKILL.md#原则)决定是否交子 agent 收集证据，提供已核实 Task/Run、job ID、host、
预期产物及当前 Acceptance 待提取数据。检查调度器或记账状态、产物、输出与日志时间戳、
针对性的完成或失败片段及验收测量。主 agent 审阅并补足关键证据，决定 Run 状态、Task 验收与后续动作。
证据不足或冲突时继续补查；作业仍活动时继续等待。观察失败或离开队列均不能单独证明成功，也不触发重提。

按实际结果更新 Spec 行与 Task 推进判断。失败时写简短原因，有前一 Run 时写实质差异。
调度器全文、原始片段和详细诊断保留在 Run 日志或排查记录，以路径引用，避免复制进 `Result`。
HDF5、`CHGCAR`、`WAVECAR` 保留服务端；结果可传输时读取[同步](sync.md)，按已检查的传输流程执行。
