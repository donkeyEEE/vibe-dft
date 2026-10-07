# VASP Wannier 预计算

使用 `assets/templates/vasp/wannier-prerun/cluster-env.sh.template` 和 `assets/templates/vasp/wannier-prerun/run.pbs.template`。评审前准备 POTCAR，并通过通用的不可变交接复制准确且已批准的 SCF `CHGCAR` 和 `WAVECAR`。

准备好的 INCAR 只包含 Spec 批准的宽预计算外窗口（`dis_win_min = -10`、`dis_win_max = 10`），不包含 `dis_froz_*`；它不用于确定最终子空间。以下各自旋通道文件都必须非空：`wannier90.1.{amn,mmn,eig,win}` 和 `wannier90.2.{amn,mmn,eig,win}`。任一通道缺失都会阻止交接。
