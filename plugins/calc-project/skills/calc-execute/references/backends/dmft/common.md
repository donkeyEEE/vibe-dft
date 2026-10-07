# DMFT 输入与运行

DMFT 输入和运行任务读取本参考。本流程执行已批准 Spec 确定的科学承诺。`$calc-to-spec` 负责确定关联子空间、PLO/局域轨道基组及轨道顺序、投影能窗、`U`/`J`、双计数、相互作用约定、求解器设置、PM/磁性范围、单次计算/CSC 范围、所需观测量和决定性判据。`$calc-review` 独立检查一个精确的 prepared 快照。

## 准备精确的 Run

1. 阅读已批准的 Spec、其中指定的 DMFT 参数/PLO/排障记录、当前上游 Runs，以及维护中的软件配置。科学承诺缺失或相互冲突时，转交 `$calc-to-spec`；可执行文件或配置条目缺失时，转交 `$calc-setup`。
2. 按 Spec 指定的已批准来源说明选择程序调用和渲染方法。Spec 是唯一的科学参数依据；来源说明只提供渲染方法，不能覆盖或补入缺失的科学参数。若与 Spec 冲突或缺少承诺，停止并转交 `$calc-to-spec`。DMFT 没有通用 backend 模板；根据已批准来源说明和 Spec 中的精确承诺，渲染具体的 `inputs/run.pbs`。
3. 按照[通用 Run 模板](../../../assets/templates/common/run.sh.template)渲染 `inputs/run.sh`。将 `__FINGERPRINT_SOURCE__` 替换为准确的服务器可见来源路径，并将 `__PREPARE_BODY__` 和 `__VALIDATE_BODY__` 各替换一次，填入下列阶段命令。
4. 在 `__PREPARE_BODY__` 中逐项写明每个已批准输入的来源和 Run 内目标路径。调用形式为 `copy_immutable SOURCE DESTINATION || return 1`；使用 shell 引号包住准确路径，包括 `inputs/` 下的目标路径。Spec 声明的 HDF5 输入也按相同方式仅在服务器端交接，不得进入本地项目、Git 或同步范围。
5. 在 `__VALIDATE_BODY__` 中，使用明确的 `test`、比较或已批准的验证命令，检查每个指定输入、其非空要求，以及已承诺的子空间/基组/顺序/能窗/相互作用/求解器设置。每条注入命令都以 `|| return 1` 结束。不得用通用默认值、文件名通配符或与旧任务相似来补足缺失值。

具体的 `inputs/run.pbs` 保留已批准来源中的程序调用和方法顺序，同时遵循[PBS 执行](../../pbs.md)中的 Run 约定：解析 `PBS_O_WORKDIR`，绑定 Run 的 `inputs/`、`outputs/` 和 `logs/`，加载准确渲染的环境，拒绝非空 outputs，只暂存具名输入，在 `outputs/` 中运行，将程序日志写入 `logs/`，并在成功前检查 Spec 指定的产物。不得虚构通用的 solid_dmft 命令行、科学求解器值、输入文件名或输出清单。环境初始化和调度资源可依据维护中的软件配置或其他确定性执行来源填写，并须记录在 Run inputs 中。

评审前，在服务器运行 `inputs/run.sh prepare` 和 `inputs/run.sh validate`，并运行[PBS 执行](../../pbs.md)指定的 DMFT 环境探测。提交前立即对照上游 current Run 重新核对 HDF5 来源身份。任何变化都要求重新验证和评审。

## 运行证据与验收

完整计算和 HDF5 均保留在服务器。只用针对性命令查看长日志，只带回 Spec 指定的轻量文本或图像证据。若 Spec 要求收敛检查，使用其中指定的 `conv_imp<N>.dat`、`observables_imp<N>.dat` 和自能证据；为 Run 写明具体文件，不用通配符发现文件。

依据已批准 Spec 的决定性判据评估这些证据。结果明确时，可判定满足或未满足判据。证据含糊或冲突，或需要改变物理承诺时，停止执行并将证据交回 `$calc-to-spec`；不得猜测阈值、虚报收敛或临时修改运行设置。
