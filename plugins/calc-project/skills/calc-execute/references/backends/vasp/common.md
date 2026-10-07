# VASP 通用执行要求

仅当 Spec 已确定计算类型、结构与元素顺序、`ENCUT`、k 网格、`ISPIN`/`MAGMOM`、展宽方式，以及适用的 SOC 或 DFT+U 承诺后，才使用本参考。模板不提供这些承诺的物理默认值；承诺缺失或冲突时，转交 `$calc-to-spec`。若 Spec 未指定 `LORBIT`、`LWAVE` 或 `LCHARG`，只能根据 Spec 指定的产物和已声明的下游交接来推导所需值，并将其记录在 Run inputs 中。

将 `assets/templates/vasp/cluster-env.sh.template`、所选 VASP PBS 模板和通用 `assets/templates/common/run.sh.template` 渲染到所选 Run 的 `inputs/`。评审前重新检查配置文件路径。在私有临时目录中准备 `POTCAR`，使用已配置或项目批准且可确定复现的方法，保持其元素顺序与已批准的 `POSCAR` 一致，并记录足够的复现证据。VASPKIT task 103 是内置方法，不是通用科学要求；只有 Spec 要求生成 KPOINTS 时，task 102 才生成 KPOINTS。通过 `copy_immutable TEMP/POTCAR "$INPUTS_DIR/POTCAR" || return 1` 复制结果。每条准备命令都必须传递失败状态。

`INCAR`、`POSCAR`、`KPOINTS`、`POTCAR`、`cluster-env.sh`、`run.pbs` 和各阶段交接文件都必须非空。检查 POSCAR/POTCAR 的元素顺序，以及按元素索引的 INCAR 数组。必须保留上游 VASP 输入时，暂存 `scripts/vasp/compare_incar_parameters.sh`，并且只将 Spec 声明的例外键传给它。任何不匹配都会在评审前阻止流程。

若磁性含义取决于原子身份或顺序，必须明确建立准备后按索引排列的 `MAGMOM` 赋值与 Spec 批准的位点或层磁矩之间的映射。可以选择任何可复现的证据形式；逐原子表格并非必需。若预期的物理顺序尚未确定，自动修复渲染缺陷后仍须停止。总磁矩较小或下游 Run 成功都不能证明顺序符合预期。

PBS 将准确的 Run 目录作为 `PBS_O_WORKDIR`，仅读取不可变的 `inputs/`，把具名且已批准的文件复制到私有 `outputs/`，并将 backend 命令输出记入 `logs/`。若已有任何输出就拒绝运行，不删除产物，也不猜测其他 Run。
