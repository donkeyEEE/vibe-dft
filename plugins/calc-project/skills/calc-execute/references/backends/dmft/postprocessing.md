# DMFT 后处理执行

仅当已批准的 Spec 声明 DMFT 后处理时，才与 `common.md` 一起读取本参考。准备 `inputs/run.pbs` 前，Spec 必须指定方法、准确来源、输入、轻量产物和决定性判据。

## 选择已声明的操作

只使用下列匹配的项目批准来源：

- `calculation_templates/dmft-postprocessing/impurity_spectral_function/`：杂质谱函数的 MaxEnt 延拓及其图像；
- `calculation_templates/dmft-postprocessing/self_energy/maxent/`：自能 MaxEnt 延拓及其图像；
- `calculation_templates/dmft-postprocessing/self_energy/pade/`：自能 Pade 延拓及其图像；
- Spec 指定的已批准收敛绘图来源：绘制已同步的轻量收敛表格。

来源缺失、方法未确定或解析延拓选择发生变化时，停止设计并转交 `$calc-to-spec`。不得改用相邻目录或推断参数。

## 准备并运行

先渲染通用的 `inputs/run.sh`，具体步骤见 `common.md`。准备部分使用 `copy_immutable SOURCE DESTINATION || return 1` 逐项复制所有指定脚本和配置；每条验证命令均以 `|| return 1` 结束。根据选定的已批准来源说明渲染具体的 `inputs/run.pbs`；DMFT 后处理没有通用 PBS 模板。

杂质谱和自能延拓只在服务器运行。评审前，在服务器准备准确且已批准的 HDF5 交接，保持它与所选后处理子目录之间预期的相对路径关系 `../vasp.h5`，并从该子目录运行所选脚本。HDF5 来源和 Run 内交接文件不得进入本地项目、Git、同步计划或结果包。具体 PBS 脚本拒绝非空 `outputs/`，在私有的 Run 内输出树中运行，并在成功前检查 Spec 指定的每项轻量产物。

收敛绘图可以只读取 Spec 指定且已同步的轻量 `conv_imp<N>.dat` 和 `observables_imp<N>.dat` 文件。不得在本地读取 HDF5。结果包只包含已声明的 PNG/SVG 图像和文本摘要；脚本、完整日志和大型求解器数据不得放入结果包。

将生成的轻量证据与已批准 Spec 的决定性判据比较。收敛证据含糊或冲突时，转交 `$calc-to-spec`；不得虚构阈值，也不得仅凭图像存在就声称已收敛。
