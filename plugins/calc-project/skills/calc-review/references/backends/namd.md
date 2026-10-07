# Hefei-NAMD 只读检查

将 prepared 表象和能带窗口与当前 Spec 比较。NAMDwithSOC 1.5.2 的自旋绝热（spin-adiabatic）输入须使用 `SOCTYPE=1`、`BMIN/BMAX` 和两列 `INICON`；自旋透热（spin-diabatic）输入须使用 `SOCTYPE=2`、上下自旋能带字段和三列 `INICON`。不能仅由 VASP 非共线或 SOC 标志推断 `SOCTYPE=2`；VASP 6.5 非共线 SOC 可能报告有效 `ISPIN=1`，同时保存旋量。

检查每个声明快照的非空 OUTCAR/EIGENVAL/WAVECAR 来源，有效 `ISPIN`、`NKPTS`、`NBANDS`、SOC 标志、索引、占据、`RUNDIR`、从已安装代码确定的 `I0.<len(NSW)>` 名称及来源只读保护。`NSW=5` 时名称为 `1` 至 `5`，不采用 VASP 风格的四位名称。检查 Task 指定的耦合、产物与失败标记。小型接口冒烟测试不能证明生产轨迹有效。报告时区分科学含义未确定的失配与暂存、保护、字段或环境缺陷。
