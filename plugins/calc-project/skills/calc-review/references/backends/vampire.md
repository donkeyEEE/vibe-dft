# VAMPIRE 只读检查

为 `vampire.UCF`、`vampire.mat` 和 `input` 确认准确、指定的 TB2J current Run 来源。比较来源的完整校验和清单与不可变 prepared 副本。模型须保留 Spec 批准的 TB2J 设置。仅用于后处理的编辑按 Spec 批准的变更检查，历史编辑模式不能作为通用要求。区分未批准的物理模型变更与机械渲染差异。

检查渲染环境、VAMPIRE 命令、指定输出列、绘图辅助输入、预期 `M_vs_T.png` 和轻量打包计划。计划须排除模型文件、Wannier Hamiltonian、HDF5、`WAVECAR`、`CHGCAR`、`CHG` 和 `vasprun.xml`。准确报告来源、prepared 副本、打包或物理模型差异。
