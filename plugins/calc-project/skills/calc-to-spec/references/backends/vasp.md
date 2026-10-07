# VASP 科学设计

Spec 承诺 VASP 物理设置时读取本参考资料。方法条件和参数来源用于由 `$domain-research` 指导的研究推理。

## 设计证据

读取已接受的 RQ 决策、材料特定计算记录、批准的结构和元素顺序、相关既有 Runs 及可用 VASP 能力。依据已接受的 RQ 和已核实证据确定计算类型及材料参数。通用或项目模板只提供基线，不能证明其中数值对本 Spec 物理有效。

## 需记录的承诺

- 明确弛豫、SCF、非自洽能带、SOC、DFT+U 或 VASP Wannier pre-run 范围及各 Task 在 DAG 中的作用。
- `ENCUT`、k 点密度、`ISPIN`/`MAGMOM`、展宽影响科学解释或可比性时，记录其值。`LORBIT`、`LWAVE` 或 `LCHARG` 影响目标可观测量或声明的下游交接时，也须记录；其他情况下这些输出控制属于执行参数，由 `$calc-execute` 按 Task 指定产物及下游需要确定。
- SOC 记录所选非共线可执行文件及 `LSORBIT`、`SAXIS`、对称性承诺。
- DFT+U 的每个按元素索引的数组须绑定选定 POSCAR/POTCAR 元素顺序。
- 声明 Task 完成要求及必要交接产物。由 `$domain-research` 按 Task Purpose 选择收敛或质量证据，保留所选材料特定来源及影响科学含义的偏离。

物理设置缺失或冲突时先调研；关键科学选择仍未解决时才访谈。不得从通用基线推断数值或将 RQ 扩展为新参数研究。
