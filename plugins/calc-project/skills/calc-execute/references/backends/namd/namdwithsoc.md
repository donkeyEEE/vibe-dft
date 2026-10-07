# NAMDwithSOC 1.5.2 执行

仅在 NAMDwithSOC 分支中，且在读取 `common.md` 后读取本参考。以下来源行为已针对 NAMDwithSOC 1.5.2 核实。其他实现或版本必须先在 `$calc-to-spec` 中提供相应证据，再准备 `inputs/run.pbs`；相似性不能代替证据。

## 表示约定

在 NAMDwithSOC 1.5.2 中，`couplings.f90` 初始化 `olap%ISPIN = inp%SOCTYPE`，并在解析的自旋分量数不匹配时拒绝 WAVECAR。`fileio.f90` 定义以下两种表示：

- `SOCTYPE=1` 表示 spin-adiabatic（自旋绝热），使用 `BMIN/BMAX`，每行 `INICON` 的格式为 `time_index band`。
- `SOCTYPE=2` 表示 spin-diabatic（自旋透热），使用 `BMINU/BMAXU` 和 `BMIND/BMAXD`，每行 `INICON` 的格式为 `time_index band spin`。

对于 VASP 6.5 非共线 SOC 来源，`OUTCAR` 可能报告生效的 `ISPIN =
1`，而 WAVECAR 存储 spinor 系数。已核实的选择是此情形使用自旋绝热 `SOCTYPE=1`。`LSORBIT=.TRUE.` 或 `LNONCOLLINEAR=.TRUE.` 不能证明应使用 `SOCTYPE=2`。若已批准的 Spec 给出其他设置，或 WAVECAR 表示方式尚未确定，阻止 Run 并将冲突交回 `$calc-to-spec`。

评审前，将已批准的 `BMIN/BMAX` 或 `BMINU/BMAXU`+`BMIND/BMAXD` 界限与每一帧 `EIGENVAL` 中的能带索引和占据数比较。`INICON` 中每个初始能带及可选自旋值都必须符合对应的已批准窗口和列约定。字段缺失、能带超出窗口或占据数不一致都会阻止流程；窗口或初始条件含义的变更交由 `$calc-to-spec`。

## 快照布局

耦合来源使用 `I0.<len(NSW)>` 格式化快照索引。`NSW=5` 时，准确布局为 `RUNDIR/1/WAVECAR` 到 `RUNDIR/5/WAVECAR`；五个目录名各为一位数，Run 需要四个耦合区间。其他 `NSW` 值须依据已安装来源推导位宽，或先通过小型接口测试确定，再渲染准确暂存路径。不能把 VASP 四位数字格式当作依据。

已批准 NAMD 输入中的 `RUNDIR` 值必须与 Run 内暂存根目录完全一致。准备时遵循 `common.md`，将每个具名快照暂存为服务器端的不可变输入，不修改来源 Run。具体的 `inputs/run.pbs` 只在私有 `outputs/` 工作树中重建已批准的相对目录结构，并运行已配置的 NAMDwithSOC 可执行文件；它不会扫描快照或修复名称。

## 针对性失败与成功证据

失败时保留完整日志和暂存内容。针对性扫描将 `File I/O
error`、`No. of spin components does NOT match`、fatal、abort 和 segmentation 标记作为失败证据。这些标记只指出预检类别，不能直接确定修补办法；缺少信息或存在相互竞争的诊断时，进入计算故障排查。

五快照接口情形的成功证据必须同时证明存在四个耦合区间、非空的 `COUPCAR`、`NATXT`、`EIGTXT`，以及至少一个非空的 `SHPROP.*` 或 `PSICT.*` 输出族；针对性扫描中不得出现任何失败标记。这些只是最低限度的接口成功检查。Run 能否验收仍由已批准 Spec 的生产观测量和决定性判据确定；接口 smoke test 不能验证生产轨迹。
