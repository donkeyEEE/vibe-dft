# Wannier90 执行

使用 `assets/templates/wannier90/{cluster-env.sh.template,run.pbs.template,wannier-run.env.template}`。评审前，复制准确且已接受的预计算 Run 中两个自旋的 `.amn`、`.mmn`、`.eig` 和 `.win` 文件；另复制能带 Run 的两个非空范围文件、两份重排能带、`DOSCAR` 和两个所属来源提供的绘图辅助脚本。每个具名的 `copy_immutable SOURCE DESTINATION` 调用都以 `|| return 1` 结束；不得使用通配符或猜测目录。

将已批准 Spec 中上下自旋各自的四个外窗和冻结窗值逐项渲染到 `wannier-run.env`。值发生变化、两边共享、缺失或顺序错误都会阻止流程，并转交 `$calc-to-spec`；绘图范围不能代替窗口值。评审会检查 `NUM_WANN`、投影、冻结态最大数，以及已批准的窗口证据，然后才能提交。

以下自旋分辨文件都必须非空：`.wout`、`_hr.dat`、`_centres.xyz`、`_band.dat` 和 VASP 与 Wannier 拟合图。PBS 模板保留不可变的接口输入，只在私有输出副本中修改窗口键，并运行两个自旋初始点。可执行程序运行成功本身不能证明物理结果充分。
