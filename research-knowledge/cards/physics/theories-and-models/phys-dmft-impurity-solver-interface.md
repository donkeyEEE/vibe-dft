---
name: phys-dmft-impurity-solver-interface
type: theory-model
tags:
  - dmft
  - impurity-solver
updated_at: 2026-08-13
---

## Core statement

DMFT 杂质求解器接口（DMFT impurity-solver interface）的核心陈述是：A dynamical mean-field theory (DMFT) impurity solver acts only on the interacting embedded subsystem, mapping the bath-defined effective bare Green function to an interacting local Green function and hence a local self-energy for the outer lattice loop.

## Formulation

- **输入：** The auxiliary problem requires the local one-body Hamiltonian, chemical potential, local interaction tensor, temperature, and a bath representation. After integrating out the bath, one may provide the effective bare Green function G_0(z), or equivalently Delta(z) together with the local one-body terms, using G_0^(-1)(z) = z + mu - h_loc - Delta(z).
- **等价表示：** G_0 and Delta are not two independent physical inputs once h_loc and mu are fixed. An implementation may store both for convenience or consistency checks, but specifying either representation completely and consistently defines the same noninteracting part of the auxiliary action.
- **求解操作：** The solver evaluates the interacting local Green function G(z) for the chosen cell, interactions, chemical potential, and temperature; it does not explicitly solve the crystal lattice.
- **输出：** The local self-energy follows from Dyson's relation Sigma(z) = G_0^(-1)(z) - G^(-1)(z) and is returned to the DMFT self-consistency loop.
- **物理含义：** This interface separates the nonlocal embedding problem from the explicit local many-body problem, allowing different solver algorithms to be exchanged without changing the logical fixed point.
- **矩阵推广：** For multiple orbitals or cluster sites, G_0, G, Delta, and Sigma are matrices in correlated-subspace indices.
- **边界：** Solver exactness is always conditional on the specified auxiliary problem; it does not remove errors from the correlated-subspace choice, local-self-energy ansatz, bath fit, statistical sampling, or self-consistency convergence.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界：** Solver exactness is always conditional on the specified auxiliary problem; it does not remove errors from the correlated-subspace choice, local-self-energy ansatz, bath fit, statistical sampling, or self-consistency convergence.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch18-001（章节 18.1；书页 480, 481；公式 18.1, 18.3；PDF 页 505, 506）
- Supports: An embedded-system solver maps the bath input G_0 or Delta to the interacting local Green function G, from which the local self-energy is obtained; the crystal enters only through the embedding loop.
