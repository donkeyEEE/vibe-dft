# 杨声远（Shengyuan A. Yang）：论文论证链与来源底稿

> 用途：为「理论凝聚态面试官」persona 提供可追溯的研究写作证据；不是对本人私下谈吐的转写。完成于 2026-08-21。
>
> 证据标记：**原文**是来源摘要/网页明确写出的内容；**转述**是忠实压缩；**推断**仅用于生成面试追问，不能伪装为杨教授的直接观点或口头原话。

## 一、来源范围与可靠性

| # | 来源（杨声远署名） | 类型 / 可靠性 | 能支持什么 |
|---|---|---|
| 1 | [PolyU 官方个人页](https://www.polyu.edu.hk/ap/people/academic-staff/prof-yang-shengyuan/) | 本人公开研究介绍；最高 | 官方列出 condensed-matter theory、topological states、transport theory、nonlinear responses、first-principles calculations 等兴趣。|
| 2 | [Chirality Hall Effect in Weyl Semimetals](https://arxiv.org/abs/1504.00732) | 本人一作预印本摘要；高 | 半经典/Berry 曲率 → 手性依赖横移 → 用栅压、应变、圆偏振光生成和探测。|
| 3 | [Predicted Unusual Magnetoresponse in Type-II Weyl Semimetals](https://arxiv.org/abs/1604.04030) | 合著预印本摘要及正文；高 | 倾斜这一低能参数 → Landau 能级塌缩 → 磁光/量子振荡的各向异性指纹。|
| 4 | [Type-II nodal loops: theory and material realization](https://arxiv.org/abs/1705.02076) | 合著预印本摘要；高 | 先重定义相交类型，再给倾斜导致的磁、光、输运差异，最后落到 K4P3。|
| 5 | [Nodal surface semimetals: Theory and material realization](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.97.115125) | APS 原刊摘要；高 | 以具体晶体/磁空间群对称性分类保护机制，再讨论 SOC、破缺条件和第一性原理候选材料。|
| 6 | [Quadratic contact point semimetal: Theory and material realization](https://arxiv.org/abs/1806.10458) | 合著预印本摘要；高 | 低能费米子与有效模型 → 强场 Landau 谱/对称破缺相变 → Cu2Se、RhAs3 候选。|
| 7 | [Progress on topological nodal line and nodal surface](https://wulixb.iphy.ac.cn/en/article/doi/10.7498/aps.68.20191538) | 本人合著受邀综述，期刊官网；高 | 综述的明示组织是「概念发展—特征与分类—材料实现」。|
| 8 | [Valley-Layer Coupling: A New Design Principle for Valleytronics](https://pubmed.ncbi.nlm.nih.gov/32031831/) | 合著 PRL 摘要，PubMed/DOI 索引；高 | 先指出现有范式的电控限制，提出 VLC，分析对称要求，以模型和第一性原理验证，并给可切换电控及光学后果。|
| 9 | [Observation of 2D Weyl Fermion States in Epitaxial Bismuthene](https://arxiv.org/abs/2303.02971) | 合著预印本摘要；高 | 衬底破坏反演对称性 → 无隙自旋极化 Weyl 色散；再以自旋 ARPES、STM/STS 给出实验信号。|
| 10 | [Tunable linear and nonlinear anomalous Hall transport in 2D CrPS4](https://research.polyu.edu.hk/en/publications/tunable-linear-and-nonlinear-anomalous-hall-transport-in-two-dime/) | PolyU Scholars Hub 的论文页及摘要；高 | 层数依赖磁性/对称性 → 线性与非线性 Hall 响应的允许/禁止 → Berry-connection polarizability 机制。|
| 11 | [Third-order nonlinear Hall effect induced by the Berry-connection polarizability tensor](https://pubmed.ncbi.nlm.nih.gov/34168343/) | 合著实验论文摘要，PubMed/DOI 索引；中高 | 非线性输运有不同对称性选择规则，且可把几何量变成可测响应；用作“理论—实验闭环”旁证。|

**边界。** 以上多数是多作者论文，抽象的行文不能机械归于单一作者；但跨 1–11 的题目、摘要结构和题材选择，可以支持对该研究群体/共同作者写作策略的谨慎归纳。未检得可稳定核验的杨声远本人完整演讲逐字稿；因此不要声称下述句式是他的口头原句。

## 二、反复出现的论证链

### A. 从“低能问题”到“可证伪的物理指纹”

1. **物理动机／既有限制（原文 + 转述）**
   - [VLC](https://pubmed.ncbi.nlm.nih.gov/32031831/) 摘要先指出既有二维谷电子学范式禁止以栅压实现完全电学的谷极化；这是“现有机制为何不够”的开场。
   - [QCP](https://arxiv.org/abs/1806.10458) 与 [2D Weyl](https://arxiv.org/abs/2303.02971) 都把焦点收在费米能附近的低能态/新准粒子，而非泛泛称材料“有潜力”。
2. **概念与对称性（原文 + 转述）**
   - 常见动作是定义一个可区分的对象（type-II loop、QCP、nodal surface、VLC），随后立即写明保护它的对称性、SOC 的作用，或哪一项破缺是必要条件。[Nodal surface](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.97.115125) 明列 PT、子晶格、非对称螺旋旋转及时间反演等机制。
3. **最小模型／计算（原文 + 转述）**
   - 不是把 DFT 当作第一句结论：论文先构造/分析 effective low-energy model，再以第一性原理寻找可实现材料。[QCP](https://arxiv.org/abs/1806.10458)、[VLC](https://pubmed.ncbi.nlm.nih.gov/32031831/) 和 [nodal surface](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.97.115125) 都明确包含模型、对称分析或 first-principles 层次。
4. **响应／区分度（原文 + 转述）**
   - 结论偏好“哪一个谱峰、方向依赖、横移、选择定则或 Hall 分量会不同”，而不是止于“存在拓扑”。例如 type-II Weyl 工作把临界夹角、Landau-level collapse 和磁光谱特征连成一条链；手性 Hall 工作把破反演导致的不平衡横移连到可控探测。[Type-II Weyl](https://arxiv.org/abs/1604.04030)；[chirality Hall](https://arxiv.org/abs/1504.00732)。
5. **材料与实验闭环（原文 + 转述）**
   - 候选材料与测量方案在摘要中显式出现：K4P3、Cu2Se/RhAs3，以及自旋 ARPES、STM/STS、磁光、Shubnikov–de Haas、栅压/应变等。[type-II loop](https://arxiv.org/abs/1705.02076)；[QCP](https://arxiv.org/abs/1806.10458)；[2D Weyl](https://arxiv.org/abs/2303.02971)。

**综合推断（高置信）。** 面试式追问应沿着「你观察到什么低能现象？哪条对称性允许/禁止？最小 (k\cdot p) 或机制是什么？什么可测张量/谱特征把它和平庸解释区分开？材料上如何调参与验证？」逐级收紧。该顺序是多篇摘要的共同论证骨架，不是其本人明说的面试流程。

### B. “允许—禁止—破缺—后果”的微型因果链

**原文短引（每则不足 25 个词；仅作证据锚点）：**

- type-II Weyl 摘要： “**there always exists a critical angle**” ([来源](https://arxiv.org/abs/1604.04030))。
- 2D Weyl 摘要： “**space-inversion-symmetry-breaking substrate perturbations**” ([来源](https://arxiv.org/abs/2303.02971))。
- 综述摘要： “**conceptual development, the character and classification, and the material realization**” ([来源](https://wulixb.iphy.ac.cn/en/article/doi/10.7498/aps.68.20191538))。

**转述。** 这些摘要常将结论收束为条件句：在何种对称性、是否含 SOC、场相对倾斜轴的方向、或层数/衬底条件下，某交叉或响应被保护、被禁阻、消失或转化。

**推断（中高置信）。** 一个只说“Berry curvature 很大”但未说明时间反演、反演、磁点群及张量分量的回答，最容易触发追问；一个只报 DFT 图而没把图与保护机制相连，也不够完整。

## 三、术语与问题框架（仅限有来源支撑）

| 术语/框架 | 证据与适合追问的方向 |
|---|---|
| **low-energy states / effective model** | QCP、type-II Weyl 直接以低能色散和 Landau 谱组织。追问：模型保留了哪些对称允许项，忽略项何时会改结论？|
| **symmetry-protected / symmetry breaking** | Nodal surface、VLC、2D Weyl 反复用保护和破缺给出存在条件。追问：哪一个生成元或反幺正组合在起作用？破哪一个对称性会如何劈裂/开隙？|
| **SOC 的有无与量级** | Nodal-surface 分类把 SOC 纳入相是否保持的条件。追问：无 SOC 的结论能否连续延至真实材料？|
| **Berry curvature / band geometry / nonlinear response** | Chirality Hall、third-order nonlinear Hall、CrPS4 以几何量和非线性 Hall 联系机制与输运。追问：响应的变换性质是什么，线性项为何允许/禁阻？|
| **distinct signature / probe** | type-II Weyl 与 2D Weyl 的摘要都把核心主张写成可测区分信号。追问：对照实验、角度扫描或费米能调节怎样排除普通多带效应？|
| **material realization / candidate** | 综述标题与多篇论文结尾都显式走向材料实现。追问：候选材料是否靠近费米能、稳定性怎样、所需应变/栅压是否现实？|

## 四、可供 persona 使用、但必须保留的限制

- **可以高置信模拟：** 从清晰物理问题出发，以对称性建立可否性，再要求模型、量化响应和实验判据的闭环。
- **不可以模拟为事实：** 语速、幽默、中文/英文口头习惯、情绪强度、对学生的态度，或“他一定会问某题”。目前源集主要是学术摘要，而非访谈语料。
- **署名提醒：** 将“论文显示/摘要提出”优先写成“该合著论文”，除非是 [Chirality Hall](https://arxiv.org/abs/1504.00732) 这种杨声远一作论文；不得把合作者的专属技术贡献归因给他个人。
