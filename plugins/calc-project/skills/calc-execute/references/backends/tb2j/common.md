# TB2J 执行

使用 `assets/templates/tb2j/{cluster-env.sh.template,run.pbs.template}`。评审前，以会传播失败的
`copy_immutable` 调用，将准确的 `POSCAR`、已接受 SCF `OUTCAR`、两份已批准
`wannier90.*_hr.dat` 和两份 `wannier90.*_centres.xyz` 复制到新 Run 的 inputs。

渲染 Spec 声明的磁性元素/轨道、截断、能量范围、自旋前缀、费米约定和 TB2J k mesh。模板从声明的
SCF OUTCAR 读取最终 `E-fermi`，并将该值及单独批准的 k mesh 传给 `wann2J.py`；绝不从 Wannier
`mp_grid` 推导 mesh。

要求 `TB2J_results/exchange.out`、`TB2J_results/Vampire/vampire.UCF`、`vampire.mat` 和 `input`
非空。缺失自旋交接或 VAMPIRE 产物会停止此分支。
