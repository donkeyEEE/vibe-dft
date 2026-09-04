---
name: phys-single-site-dmft-local-self-energy
type: theory-model
tags:
  - dmft
  - self-energy
updated_at: 2026-08-13
---

## Core statement

单站点 DMFT 的局域自能近似（local-self-energy approximation in single-site DMFT）的核心陈述是：Single-site DMFT approximates the lattice self-energy as local by retaining only on-site orbital matrix elements, so the self-energy has no crystal-momentum dependence.

## Formulation

- **定义：** In a translationally invariant single-site construction the self-energy is restricted to on-site orbital blocks, Sigma_ij(omega) = delta_ij Sigma_i(omega), which becomes Sigma_k(omega) -> Sigma(omega) in momentum space.
- **why used：** The approximation retains the full frequency dependence of local quantum correlations while replacing spatially nonlocal self-energy contributions by an effective medium.
- **物理含义：** All momentum dependence of G_k then enters through the independent-particle dispersion epsilon_k; local spectral renormalization and lifetime effects are carried by the same dynamic Sigma(omega) at every equivalent site.
- **assumptions：** The chosen site or correlated cell contains the dominant correlations, and correlations outside it are sufficiently weak or can be represented through self-consistent embedding.
- **consequences：**
  - The impurity self-energy can be inserted directly into the lattice Dyson equation.
  - Local observables and local dynamics can be nonperturbative even though explicit intersite self-energy structure is absent.
- **边界：** Correlations between distinct sites are treated only in an average sense; short-range magnetic, pairing, pseudogap, or other momentum-selective physics can require cluster or nonlocal extensions.
- **generalization：** Cluster DMFT replaces the single site by a correlated cell, retaining self-energy matrix elements inside that cell and thereby restoring a controlled subset of spatial correlations.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **assumptions：** The chosen site or correlated cell contains the dominant correlations, and correlations outside it are sufficiently weak or can be represented through self-consistent embedding.
- **边界：** Correlations between distinct sites are treated only in an average sense; short-range magnetic, pairing, pseudogap, or other momentum-selective physics can require cluster or nonlocal extensions.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch16-002（章节 16.2；书页 427；公式 16.5；PDF 页 452）；ev-ie-ch16-006（章节 16.2；书页 428；PDF 页 453）
- Supports: The single-site approximation restricts the self-energy to on-site matrix elements and removes its momentum dependence.; Single-site DMFT treats local correlations through the impurity problem but represents intersite correlations only in an average sense and supplies no direct intersite-correlation information.
