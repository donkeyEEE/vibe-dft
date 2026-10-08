# Wannier90 执行

使用 `assets/templates/wannier90/{cluster-env.sh.template,run.pbs.template,wannier-run.env.template}`。评审前，复制准确且已接受的预计算 Run 中两个自旋的 `.amn`、`.mmn`、`.eig` 和 `.win` 文件。每个具名的 `copy_immutable SOURCE DESTINATION` 调用都以 `|| return 1` 结束；不得使用通配符或猜测目录。

将已批准 Spec 中上下自旋各自的四个外窗和冻结窗值逐项渲染到 `wannier-run.env`。值发生变化、两边共享、缺失或顺序错误都会阻止流程，并转交 `$calc-to-spec`；绘图范围不能代替窗口值。评审会检查 `NUM_WANN`、投影、冻结态最大数，以及已批准的窗口证据，然后才能提交。

后端准备 Task 所需的输入和产物；诊断计算与图件按 Task 要求安排。在 `wannier-run.env` 中设置 `WANNIER_FIT_PLOT`：需要 VASP/Wannier 拟合图时为 `1`，否则为 `0`。启用时，另复制准确能带来源的 `REFORMATTED_BAND_UP.dat`、`REFORMATTED_BAND_DW.dat`、`DOSCAR` 和两个绘图脚本，填写 `PLOT_EMIN`、`PLOT_EMAX`，并确认 `.win` 包含对应路径。范围文件仅在所选窗口证据需要时携带；模板绘图不消费它们。旧输入未设置开关时保留原有绘图行为。

核心自旋分辨产物 `.wout`、`_hr.dat` 和 `_centres.xyz` 必须非空；启用拟合图时另检查 `_band.dat` 和两份拟合图。Task 要求的其他证据按其 Acceptance 核对。PBS 模板保留不可变的接口输入，只在私有输出副本中修改窗口键，并运行两个自旋初始点。可执行程序运行成功本身不能证明物理结果充分。
