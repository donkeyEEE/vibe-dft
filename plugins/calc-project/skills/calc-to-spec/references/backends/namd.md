# Hefei-NAMD/NAMDwithSOC 科学设计

Spec 承诺 VASP-to-Hefei-NAMD/NAMDwithSOC 表象或能带窗口时读取本参考资料。以下版本规则已在 NAMDwithSOC 1.5.2 核实；其他版本需要各自证据。

## 设计证据

读取已接受的 RQ 决策、已安装 NAMD 实现/版本证据、来源 VASP 记录及覆盖目标快照的代表性 `OUTCAR` 和 `EIGENVAL` 证据。依据 RQ 和证据确定物理表象、`SOCTYPE`、能带窗口字段与边界、初始条件含义、来源快照集合、所需可观测量、生产验收及适用的停止准则。接口冒烟测试不能证明生产轨迹的科学有效性。

## 表象承诺

NAMDwithSOC 1.5.2 的 `couplings.f90` 从 `inp%SOCTYPE` 初始化 `olap%ISPIN`，并拒绝解析所得自旋分量数不匹配的 WAVECAR。输入表象对应如下：

- `SOCTYPE=1`：自旋绝热（spin-adiabatic），使用 `BMIN/BMAX`；每行 `INICON` 为 `time_index band`。
- `SOCTYPE=2`：自旋透热（spin-diabatic），使用 `BMINU/BMAXU` 和 `BMIND/BMAXD`；每行 `INICON` 为 `time_index band spin`。

VASP 6.5 非共线 SOC 计算的 `OUTCAR` 可能报告 `ISPIN = 1`，而 WAVECAR 保存旋量系数。已核实适用于该情形的是自旋绝热 `SOCTYPE=1` 分支。仅有 `LSORBIT=.TRUE.` 或 `LNONCOLLINEAR=.TRUE.` 不能证明应采用 `SOCTYPE=2`。

探索测试选择代表性快照检查有效 `ISPIN`、`NKPTS`、`NBANDS`、`LSORBIT`、`LNONCOLLINEAR`、能带索引及占据。生产轨迹验收前，须确认所有纳入帧的表象与能带兼容；由 `$domain-research` 根据轨迹和可观测量选择证据。Spec 须使 `SOCTYPE`、能带字段及 `INICON` 列含义一致。表象不确定或版本证据不完整时，设计决策仍未解决。
