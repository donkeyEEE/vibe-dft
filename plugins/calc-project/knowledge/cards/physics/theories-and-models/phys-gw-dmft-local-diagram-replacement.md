---
name: phys-gw-dmft-local-diagram-replacement
type: theory-model
tags:
  - dmft
  - gw-dmft
  - double-counting
updated_at: 2026-08-13
---

## Core statement

GW+DMFT 局域图形替换（local diagram replacement in GW+DMFT）的核心陈述是：GW+DMFT combines nonlocal weak-to-intermediate correlation with nonperturbative local correlation by replacing the correlated-subspace local GW self-energy and polarizability with impurity quantities rather than adding both contributions unchanged.

## Formulation

- **自能分解：** Construct Sigma_total(k,omega) = Sigma_GW(k,omega) - Sigma_GW,loc(omega) + Sigma_imp(omega), with projection and upfolding defined in one correlated basis.
- **极化分解：** Analogously use P_total(q,omega) = P_GW(q,omega) - P_GW,loc(omega) + P_imp(omega) before computing the screened interaction W.
- **避免重叠的原因：** The same explicitly identified local GW diagrams are removed before the impurity contribution is inserted, so the replacement has a diagrammatic overlap definition absent from generic DFT+DMFT.
- **保留的物理：** Momentum-dependent GW terms retain nonlocal exchange and screening, while the impurity supplies all local diagrams accessible to its solver, including strong multiplet and vertex effects.
- **基底要求：** Local projection, interaction tensor, impurity Green function, and the subtracted GW local pieces must use compatible orbitals and normalization.
- **边界：** Simple momentum averaging identifies the local GW/RPA pieces only within the stated low-order construction; higher-order diagrams can leave and return to a site, making locality and subtraction more complicated.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **基底要求：** Local projection, interaction tensor, impurity Green function, and the subtracted GW local pieces must use compatible orbitals and normalization.
- **边界：** Simple momentum averaging identifies the local GW/RPA pieces only within the stated low-order construction; higher-order diagrams can leave and return to a site, making locality and subtraction more complicated.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch21-001（章节 21.2 and 21.4；书页 557, 562；PDF 页 582, 587）
- Supports: GW+DMFT treats the full system at GW level and replaces the local correlated-subspace GW self-energy and polarizability by their impurity counterparts, making the subtraction diagrammatically identifiable.
