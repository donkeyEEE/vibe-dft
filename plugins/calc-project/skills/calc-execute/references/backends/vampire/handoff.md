# TB2J 至 VAMPIRE 交接

准确的已接受 TB2J `TB2J_results/Vampire/` 文件是来源。`run.sh prepare` 期间，逐个通过
`copy_immutable SOURCE DESTINATION || return 1` 复制 `vampire.UCF` 与 `vampire.mat`。从准确 TB2J
来源在私有临时路径创建 `input`，仅将 `output:material-magnetisation` 改为两个已批准的命名输出，
再不可变复制。任何其他 model/input 差异都阻止流程。

评审前从命名的 TB2J 源 UCF 与 material 文件创建 `model-source.sha256`，不可变暂存，并以准备好的副本验证。
清单恰有两项：有效 SHA-256 digest 后接裸文件名 `vampire.UCF` 的一项，以及后接裸文件名
`vampire.mat` 的一项。重复、缺失、额外、绝对路径或带目录的名称都会在执行 VAMPIRE 前阻止流程。
记录准确的源至副本路径和校验和。之后的源、准备模型、清单或环境变更会使评审失效；prepare 绝不
覆盖不同的目标。
