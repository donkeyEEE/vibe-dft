# VASP 服务器端交接

从所选 Spec 指定的准确上游 Task 和 current Run 解析每个来源。不得从相邻目录推测上游 Run。大型 `CHGCAR` 和 `WAVECAR` 保留在服务器，并排除在本地传输之外。

执行 `run.sh prepare` 时，对每个声明文件分别调用一次 `copy_immutable SOURCE DESTINATION || return 1`。Band 使用已接受 SCF 的 `outputs/CHGCAR`；Wannier pre-run 使用已接受 SCF 的 `outputs/CHGCAR` 和 `outputs/WAVECAR`；MAE 的两个方向 Run 使用同一个已批准 SCF 的 `outputs/CHGCAR`。目标路径已有不同文件时，准备必须停止。验证和瞬时评审前记录来源与目标路径，并比较文件字节。
