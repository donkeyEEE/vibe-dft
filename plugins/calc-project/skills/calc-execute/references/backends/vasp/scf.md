# VASP SCF 计算

使用 `assets/templates/vasp/scf/run.pbs.template`，并将 `__VASP_CHARGE_HANDOFF__` 渲染为 `none`。准备部分只生成 `common.md` 中说明且经 Spec 批准的 POTCAR 或 KPOINTS；不得把 VASPKIT 输入生成推迟到 PBS。验证部分检查所有具名输入、渲染后的集群环境、`mpirun` 和已配置的 VASP 可执行文件；每条命令都必须以 `|| return 1` 传递失败。

要求 `OUTCAR` 非空，并检查 Spec 指定的收敛和交接产物。保留原始的最终 `E-fermi`（记录在 `OUTCAR` 中）；下游 TB2J 使用这个已声明的约定，不推断其他费米能级值。
