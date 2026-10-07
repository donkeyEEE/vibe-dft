# TB2J 到 VAMPIRE 的交接

来源必须是准确且已接受的 TB2J `TB2J_results/Vampire/` 文件。执行 `run.sh prepare` 时，分别通过 `copy_immutable SOURCE DESTINATION || return 1` 复制 `vampire.UCF` 和 `vampire.mat`。从准确的 TB2J 来源在私有临时路径创建 `input`；只将 `output:material-magnetisation` 改成两个已批准的具名输出，然后以不可变方式复制。input 或模型中有其他差异都会阻止流程。

评审前，根据具名 TB2J 来源 UCF 和 material 文件创建 `model-source.sha256`，以不可变方式暂存，并使用准备好的副本进行验证。清单必须恰有两项：一项为有效的 SHA-256 digest，后接裸文件名 `vampire.UCF`；另一项后接裸文件名 `vampire.mat`。重复、缺失、多余、绝对路径或包含目录的名称都会在运行 VAMPIRE 前阻止流程。记录准确的来源与副本路径及校验和。之后若来源、准备好的模型、清单或环境发生变化，评审即失效；prepare 绝不覆盖内容不同的目标文件。
