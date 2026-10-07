# Run 准备

准备选定 Run 时读取本资料，按以下布局和物化规则完成输入准备。

## 物化 Run 输入

写入前解析选定 Run、Task、当前 Spec 及声明的上游 current Run。Run 包含 `inputs/`、`outputs/` 和 `logs/`；`run.sh` 与 `run.pbs` 位于该 Run 的 `inputs/`。选定路径已属于其他 Run 时停止，保留原对象。

从准确路径渲染 `../assets/templates/common/run.sh.template`，逐一替换以下集成点，每项仅一次：

- `__FINGERPRINT_SOURCE__`：所属 `../scripts/fingerprint_run.py` 的准确服务端可见路径。准备通过 `copy_immutable` 将其字节复制到 `inputs/fingerprint_run.py`。
- `__PREPARE_BODY__`：阶段特有的服务端交接和生成。每条命令用 `|| return 1` 传播失败。
- `__VALIDATE_BODY__`：阶段特有的前置条件与输入检查。每条命令用 `|| return 1` 传播失败。

`copy_immutable SOURCE DESTINATION` 仅供渲染后的 prepare 主体使用。来源须为已声明的普通文件，目标目录须已存在且位于该 Run 的 `inputs/` 下。它通过服务端 `rsync` 保留来源，接受字节相同的既有普通目标文件，拒绝链接或内容不同的目标。符合原地纠正条件时，先移除或替换指定受影响目标，再调用 `prepare`；辅助程序不判断纠正资格。逐个指定复制文件，不使用目录通配符。

匹配内置 backend 时，从其准确所属路径渲染资产。模板提供结构，科学值与上游身份来自已批准的当前 Spec 及其 current Runs。CHGCAR、WAVECAR 和 HDF5 留在服务端，在那里准备声明的 Run 输入交接，不下载。

## 完成准备

在拥有选定 Run 的环境中执行：

```bash
bash /exact/task/RUN-NNN/inputs/run.sh prepare
```

命令成功且声明输入已物化时，准备完成。随后按工作流验证、评审、同步和提交。
