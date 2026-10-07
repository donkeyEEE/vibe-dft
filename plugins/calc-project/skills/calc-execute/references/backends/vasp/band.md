# VASP 能带计算

使用 `assets/templates/vasp/band/run.pbs.template`。评审前，将准确的当前上游 SCF `CHGCAR` 复制到 `inputs/CHGCAR`，调用 `copy_immutable SOURCE DESTINATION || return 1`；将准确来源的辅助脚本 `scripts/wannier90/vest2.py` 暂存为 `inputs/vest2.py`，并准备 POTCAR。Spec 必须写明上游 Run 和来源文件；不得通过猜测目录来确定来源。

PBS 依次运行 VASP 能带计算、VASPKIT 菜单输入 `21 → 211 → 1`，然后精确运行 `printf '5\ny\n8\n' | python3 ./vest2.py`。以下文件都必须非空：`BAND.dat`、`DOSCAR`、`REFORMATTED_BAND_UP.dat`、`REFORMATTED_BAND_DW.dat`、`bandrange_spin0.dat` 和 `bandrange_spin1.dat`。VEST 用于报告自旋能带范围，不负责选择 Wannier 窗口。`scripts/vasp/plot_vasp_band.py` 可绘制无投影、以空行分隔的 `BAND.dat`。
