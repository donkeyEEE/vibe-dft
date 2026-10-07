# VASP 方向性 MAE 计算

使用同一个明确指定的 SCF `CHGCAR` 准备两个新 Run，并使用 `assets/templates/vasp/scf/run.pbs.template`：MAE Run 将 `__VASP_CHARGE_HANDOFF__` 渲染为 `CHGCAR`，普通 SCF 则渲染为 `none`。对每个 MAE Run，准备部分调用 `copy_immutable EXACT_SCF_CHGCAR "$INPUTS_DIR/CHGCAR" || return 1`，验证部分在评审前调用 `test -s "$INPUTS_DIR/CHGCAR" || return 1`。渲染后的 PBS 脚本会准确指定、检查并复制该 `CHGCAR` 到私有输出工作目录，然后运行 VASP。以下设置必须符合要求：`ISTART=0`、`ICHARG=11`、`LSORBIT=.TRUE.`、`ISYM=-1`、已批准的 spinor `NBANDS`，以及每个离子三个 `MAGMOM` 分量，并以 `SAXIS` 为基底。

任一 Run 进入评审前，都要比较这对 Run 的完整输入。除已批准的 `SAXIS` 方向和不可避免的 Run 元数据外，两边必须逐字节等价。晶胞、k 网格、截断能、Hubbard 数组、收敛设置、电荷来源、磁序或未经批准的方向只要有一项不同，就阻止流程并转交 `$calc-to-spec`。保留两个 Run，并使用准确且已批准的差值约定和单位报告能量。
