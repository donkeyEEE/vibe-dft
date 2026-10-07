# Hefei-NAMD 执行

每次 Hefei-NAMD 或 NAMDwithSOC Run 都读取本参考。它将准确且已批准的 VASP 快照暂存到 Run，验证接口证据，渲染 Run，并检查声明的产物。已批准 Spec 负责确定实现及版本、表示方式、快照集合、能带窗口、初始条件含义、观测量和生产计算验收标准。`$calc-review` 独立只读检查一个 prepared 快照。

## 准备准确的 Run

1. 阅读 Spec、已安装实现及版本证据、准确的当前来源 Runs、代表性来源记录和维护中的软件配置。表示方式或窗口信息缺失，或存在相互竞争的诊断时，停止并转交 `$calc-to-spec`；不得根据错误信息猜测补丁。
2. 按 Spec 指定的已批准来源说明选择输入和 PBS 的渲染方法。NAMD 没有通用 backend 模板。根据这些来源说明、准确的快照集合和已配置的可执行文件，渲染具体的 `inputs/run.pbs`。
3. 按照[通用 Run 模板](../../../assets/templates/common/run.sh.template)渲染 `inputs/run.sh`。将 `__FINGERPRINT_SOURCE__` 替换为准确的服务器可见来源路径，并将 `__PREPARE_BODY__` 和 `__VALIDATE_BODY__` 各替换一次。
4. 在 `__PREPARE_BODY__` 中，于服务器上使用 `copy_immutable SOURCE DESTINATION || return 1` 分别暂存每个声明文件。使用 shell 引号包住 Run 的 `inputs/` 下准确路径；不得使用通配符或推导来源 Run。WAVECAR 和 CHGCAR 只保留在服务器上，并排除在本地同步之外。
5. 保留所有来源 VASP Run，并按约定将其文件视为只读。准备过程可以把已声明的来源字节复制到新的不可变 Run 快照中；不得移动、重命名、编辑或删除来源 `WAVECAR`、`CHGCAR` 或 `POTCAR`。准备时记录并检查指定来源的身份，提交前立即再次核对。

在 `__VALIDATE_BODY__` 中，每条命令都以 `|| return 1` 结束，并检查每一个快照，不得只抽查代表帧：

- 每个声明的来源目录和所需 VASP 文件均非空；
- `OUTCAR` 证据包含生效的 `ISPIN`、`NKPTS`、`NBANDS`、`LSORBIT` 和 `LNONCOLLINEAR`；
- `EIGENVAL` 包含证明已批准窗口和初始能带所需的能带索引与占据数，且覆盖每一帧；
- `RUNDIR`、暂存目录名、表示字段、能带字段和 `INICON` 列数均与 Spec 一致。

字段缺失、初始条件超出窗口、来源身份变化或快照不一致，都会阻止评审前的验证。表示方式或能带窗口发生变化时，转交 `$calc-to-spec`。

## 渲染 PBS 并检查证据

具体的 `inputs/run.pbs` 保留已批准来源的准确输入语法、调用和操作顺序，同时遵循[PBS 执行](../../pbs.md)中的 Run 约定：解析 `PBS_O_WORKDIR`，绑定 `inputs/`、`outputs/` 和 `logs/`，加载渲染后的环境，拒绝非空输出，只暂存具名的不可变输入，在 `outputs/` 中运行，将命令及失败日志保存在 `logs/`，并要求 Spec 指定的每项产物。评审前和提交前立即再次运行该参考中对应 Hefei-NAMD 或 NAMDwithSOC 的精确环境探测。

接口 smoke test 只能证明已测试的文件/表示约定，不能验证生产轨迹，也不能替代 Spec 的生产观测量或验收标准。
排障期间保留失败日志和暂存证据；只有所需 Run 证据和 provenance 已保留后才能清理。
