---
name: write-thesis-global-local-method-split
type: writing-pattern
tags: [domain/paper-writing, section/methods]
updated_at: 2026-08-10
---

# 分离全局方法原理与研究章局部设置

共同理论和算法原理放在全局方法章，体系特有模型、参数和偏离设置放在对应研究章，避免重复与失去可复现性。

## Explanation

**适用范围：** 多研究章共享计算平台。

写作或审核时，应检查正文是否显式呈现该信息关系，而不是让读者依靠目录、图题或跨章猜测补全。

## Caveats

学校模板可能要求不同的方法集中程度。

## References

- 高雅（2025），《二维载体原子级分散催化剂电催化合成氨的理论研究》：`G-E004`，全章，PDF 第 55、79 页，direct：统一介绍DFT、AIMD、电化学模型与机器学习方法。
- 李开旗（2024），《锑碲相变存储材料多态结构及相变机理的理论研究》：`L-E004`，全章，PDF 第 43、66 页，direct：DFT、AIMD、结构分析和机器学习势覆盖不同尺度。
- 张伟明（2025），《低功耗高性能一维晶体管的量子输运研究》：`Z-E004`，全章，PDF 第 60、79 页，direct：DFT和NEGF共同连接材料电子结构与双电极器件输运。
