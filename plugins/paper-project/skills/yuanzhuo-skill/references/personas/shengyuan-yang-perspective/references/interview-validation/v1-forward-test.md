# v1 合成回归记录

本文件基于可读 Skill 与保留的 v0 快照构造合成回归，不是历史会话的不可篡改证明，且不含个体数据。矩阵同时保存原始输出、原始 verdict 和为测试契约规范化后的字段；加载资源均使用相对于人格根目录的路径。完整字段见 [前向测试矩阵](forward-test-matrix.yaml)。

- `/root/synthetic_v1_plan`：最小可证伪主张，`PASS`；原始 verdict=`pass`，规范化为 `PASS`。矩阵将其末尾标点规范为问号，以满足问题字段契约。
- `/root/synthetic_v1_honesty`：私人标准无公开依据时停止推断，边界标签，`PASS`；原始 verdict=`pass`，规范化为 `PASS`。
- `/root/synthetic_v1_numerical`：单一收敛条件，`PASS`；Agent 原自然语言 verdict 表示符合规则，规范化为 `PASS`。
- `/root/synthetic_v1_experimental`：单一驱动场幅度标度判据，`PASS`。
- `/root/synthetic_v1_single_action`：仅界定物理机制，`PASS`。
- `/root/synthetic_v1_mainline`：仅辨认研究主线的个人贡献，`PASS`。
- `/root/synthetic_v1_symmetry`：仅审查一个对称性条件，`PASS`。
- `/root/synthetic_v1_variation`：自然变化开场且只审查一个条件，`PASS`。
