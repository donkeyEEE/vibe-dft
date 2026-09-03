---
name: phys-dmft-impurity-self-consistency
type: theory-model
tags:
  - dmft
  - quantum-embedding
updated_at: 2026-08-13
---

## Core statement

DMFT 杂质自洽（DMFT impurity self-consistency）的核心陈述是：Single-site DMFT maps a lattice site to an interacting impurity in a bath and determines that bath by requiring equality of the impurity and lattice-local Green functions and self-energies.

## Formulation

- **映射：** The interacting Hamiltonian of the chosen lattice site is retained, while the rest of the lattice is replaced by a dynamical bath specified through G_0 or Delta.
- **equations：**
  - **lattice green function：** G_k(omega) = [omega - epsilon_k - Sigma(omega)]^(-1)
  - **局域投影：** G_loc(omega) = N_k^(-1) sum_k G_k(omega)
  - **impurity dyson equation：** Sigma_imp(omega) = G_0^(-1)(omega) - G_imp^(-1)(omega)
  - **self consistency：** G_loc(omega) = G_imp(omega) and Sigma(omega) = Sigma_imp(omega)
- **iterative logic：**
  - Choose a trial local self-energy and calculate the lattice and local Green functions.
  - Update G_0 or Delta for the embedded site from the local Dyson relation.
  - Solve the interacting impurity problem to obtain G_imp and Sigma_imp.
  - Return Sigma_imp to the lattice and repeat until the local quantities agree.
- **物理含义：** The impurity is not a dilute defect; it is an auxiliary representative of every equivalent correlated site, and the bath carries the feedback of the lattice onto that site.
- **assumptions：** The selected local interacting Hamiltonian and correlated subspace are fixed, and the impurity solver faithfully solves the specified auxiliary problem.
- **边界：** Equality of local one-particle quantities does not make the auxiliary impurity identical to the full lattice for nonlocal correlations or arbitrary higher-order observables.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **assumptions：** The selected local interacting Hamiltonian and correlated subspace are fixed, and the impurity solver faithfully solves the specified auxiliary problem.
- **边界：** Equality of local one-particle quantities does not make the auxiliary impurity identical to the full lattice for nonlocal correlations or arbitrary higher-order observables.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch16-003（章节 16.2；书页 428；公式 16.6；PDF 页 453）；ev-ie-ch16-012（章节 16.5；书页 439；图 16.3；PDF 页 464）
- Supports: Single-site DMFT equates the embedded-site and lattice local Green functions and self-energies, which determines the bath self-consistently.; The DMFT iteration updates the impurity bath from the lattice-local Green function, solves the embedded interacting problem, returns the impurity self-energy to the lattice, and repeats until both local Green functions and self-energies agree.
