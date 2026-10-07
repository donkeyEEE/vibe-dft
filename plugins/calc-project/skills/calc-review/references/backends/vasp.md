# VASP 只读检查

将准确的 prepared 文件与当前 Spec 的计算类型及批准证据比较。检查非空 `INCAR`、`POSCAR`、`KPOINTS`、`POTCAR`、`cluster-env.sh` 和 `run.pbs`；POSCAR/POTCAR 元素顺序；按元素索引的 DFT+U 与磁性数组；`ENCUT`、k 点定义、展宽、`ISPIN`/`MAGMOM`、`LORBIT`、`LWAVE`、`LCHARG` 及所选可执行文件。SOC 还须检查 `LSORBIT`、`SAXIS`、对称性、旋量 `NBANDS` 和已批准的非共线可执行文件。

确认 POTCAR/KPOINTS 生成保留批准的元素和 k 点含义；仅当替代方式在科学或操作上不等效时，才要求特定工具路径。检查指定上游 current Run 交接与预期产物。能带与 Wannier pre-run 检查准确的服务端 `CHGCAR`/`WAVECAR` 来源及不可变 prepared 交接。方向 MAE 检查已批准且可比较的一对计算、同一指定 SCF 电荷来源及 Spec 的能量约定。区分科学选择缺失与 prepared 文件或交接缺陷。
