---
name: write-thesis-task-local-reproducibility-contract
type: method-constraint
tags: [domain/paper-writing, section/methods]
updated_at: 2026-08-10
---

# 为每个研究章建立局部复现契约

每个研究章应独立报告复现该章所需的模型构建、边界条件、关键参数、采样路径和判据，并引用共同方法定义。

## Explanation

**适用范围：** DFT、AIMD、机器学习势和NEGF研究章。

应把这项约束作为相关结论成立的门槛；门槛未满足时，需要降低结论强度并声明缺失证据。

## Caveats

当前范文只支持结构原则，参数完备性需另行审计。

## References

- 高雅（2025），《二维载体原子级分散催化剂电催化合成氨的理论研究》：`G-E004`，全章，PDF 第 55、79 页，direct：统一介绍DFT、AIMD、电化学模型与机器学习方法。
- 李开旗（2024），《锑碲相变存储材料多态结构及相变机理的理论研究》：`L-E004`，全章，PDF 第 43、66 页，direct：DFT、AIMD、结构分析和机器学习势覆盖不同尺度。
- 张伟明（2025），《低功耗高性能一维晶体管的量子输运研究》：`Z-E004`，全章，PDF 第 60、79 页，direct：DFT和NEGF共同连接材料电子结构与双电极器件输运。
