---
name: phys-constrained-rpa-effective-interaction
type: theory-model
tags:
  - constrained-rpa
  - effective-interaction
  - screening
updated_at: 2026-08-13
---

## Core statement

约束随机相位近似有效相互作用（constrained-RPA effective interaction）的核心陈述是：Constrained random-phase approximation (cRPA) constructs a frequency-dependent partially screened interaction by removing polarization transitions internal to a declared correlated subspace from the RPA screening channels.

## Formulation

- **分解：** Partition the independent-particle polarizability into excluded correlated-subspace transitions P_d and the remaining screening P_r, then evaluate U(omega) = [v^(-1) - P_r(omega)]^(-1) in the correlated basis.
- **预期用途：** A subsequent low-energy solver restores the excluded correlated screening and interactions, avoiding their prior inclusion in the input U.
- **动态信息：** Re U gives the energy-dependent screened strength, while Im U identifies screening continua or collective modes and is linked to Re U by causality.
- **子空间依赖：** Band window, Wannier functions, disentanglement, and treatment of mixed d-rest transitions decide which channels are excluded and can materially change U.
- **与 GW+DMFT 的区别：** Standard cRPA produces a fixed input and excludes correlated-subspace transitions on all sites; GW+DMFT instead updates a site-excluded interaction through bosonic self-consistency and includes additional nonlocal polarization.
- **边界：** cRPA inherits RPA vertex neglect and independent-particle starting-point dependence; it is a controlled channel construction within those approximations, not a unique material constant.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界：** cRPA inherits RPA vertex neglect and independent-particle starting-point dependence; it is a controlled channel construction within those approximations, not a unique material constant.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch21-004（章节 21.5；书页 568, 569；图 21.6；PDF 页 593, 594）
- Supports: Constrained RPA defines U(omega) by excluding selected correlated-subspace transitions from RPA screening; the result depends on the subspace and on how mixed cross transitions are partitioned.
