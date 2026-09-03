---
name: phys-ct-hyb-dynamical-interactions
type: theory-model
tags:
  - dmft
  - impurity-solver
  - dynamical-interaction
updated_at: 2026-08-13
---

## Core statement

CT-HYB 中的动态相互作用（dynamical interactions in CT-HYB）的核心陈述是：A density-coupled retarded local interaction can be incorporated into CT-HYB by representing screening with bosonic modes, which adds a pairwise imaginary-time factor between impurity events while retaining the usual fermionic hybridization sampling.

## Formulation

- **physical origin：** Screening by degrees of freedom outside the correlated subspace makes the effective charge interaction U frequency dependent rather than a single static constant.
- **representation：** A causal U(omega) is mapped to electrons coupled to a spectrum of bosonic modes; integrating out those modes yields a nonlocal-in-imaginary-time density interaction U(tau - tau').
- **algorithmic form：** After a Lang-Firsov-type transformation for the density-coupled construction, each CT-HYB configuration receives a bosonic weight exp(sum_ij s_i s_j K(tau_i - tau_j)) in addition to the fermionic determinant and local trace.
- **static and dynamic parts：** Screening shifts local one-particle energies and reduces the static interaction, while K(tau) retains the retarded part and can generate satellite structures beyond a static-U description.
- **计算代价：** In the construction described by the source, evaluating the bosonic pair factor is usually cheaper than the fermionic determinant work, so dynamic screening need not multiply the total cost dramatically.
- **边界：** This efficient factorization assumes an interaction representable by density-coupled bosonic screening modes; general frequency-dependent multiplet interactions can require more expensive algorithms, and spectral satellites are not attributable to a single mode without further analysis.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界：** This efficient factorization assumes an interaction representable by density-coupled bosonic screening modes; general frequency-dependent multiplet interactions can require more expensive algorithms, and spectral satellites are not attributable to a single mode without further analysis.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch18-006（章节 18.7；书页 496, 498；公式 18.36, 18.41；PDF 页 521, 523）
- Supports: A retarded local interaction U(tau) can be represented through bosonic screening modes and included in hybridization-expansion CTQMC as an additional pairwise imaginary-time weight, at modest extra cost in the stated density-coupled construction.
