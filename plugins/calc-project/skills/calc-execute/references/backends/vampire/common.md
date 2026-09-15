# VAMPIRE 执行

使用 `assets/templates/vampire/{cluster-env.sh.template,run.pbs.template}`，并暂存准确的
`scripts/vampire/plot.py`。准备的 input 必须包含 `output:temperature` 和
`output:mean-magnetisation-length`；列格式错误或缺失会在评审前阻止流程，绘图辅助程序也拒绝
格式错误的输出。

PBS 验证已评审模型校验和清单，仅将指定 input/model/helper 文件复制到私有 outputs，记录源与副本
校验和，执行配置的 VAMPIRE 二进制文件，并要求 `output` 和 `M_vs_T.png` 非空。它拒绝既有输出，
且绝不修改 `inputs/`。

`scripts/vampire/pack_magnetic_results.sh` 仅用于轻量结果；它排除 VAMPIRE 模型、Wannier
Hamiltonian、HDF5、`WAVECAR`、`CHGCAR`、`CHG` 和 `vasprun.xml`，并写入 included/skipped 清单。
