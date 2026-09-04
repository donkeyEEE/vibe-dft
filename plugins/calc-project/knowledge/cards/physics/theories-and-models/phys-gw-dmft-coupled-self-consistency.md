---
name: phys-gw-dmft-coupled-self-consistency
type: theory-model
tags:
  - dmft
  - gw-dmft
  - self-consistency
updated_at: 2026-08-13
---

## Core statement

GW+DMFT 的耦合自洽（coupled self-consistency in GW+DMFT）的核心陈述是：Fully self-consistent GW+DMFT closes a fermionic embedding loop for G and Sigma together with a bosonic embedding loop for W and P, so both the impurity Weiss propagator and retarded interaction evolve with the lattice.

## Formulation

- **晶格步骤：** From the current total self-energy and polarizability compute lattice G(k,omega) and W(q,omega), including the explicit local replacements.
- **局域投影：** Project G and W into the correlated subspace to obtain G_loc and W_loc.
- **杂质输入：** Form the fermionic Weiss field G_0^(-1) = G_loc^(-1) + Sigma_imp and the bosonic Weiss interaction U^(-1) = W_loc^(-1) + P_imp.
- **杂质输出：** Solve the retarded-interaction impurity problem for G_imp, Sigma_imp, the reducible susceptibility, and the corresponding irreducible P_imp.
- **不动点：** Iterate until impurity and projected lattice G agree and the impurity-screened interaction agrees with projected W, alongside the chosen GW consistency level.
- **稳健性边界：** Multiple solutions, initialization dependence, analytic continuation, correlated-subspace choice, incomplete inner loops, and solver noise remain; self-consistency does not guarantee the physically stable phase or exactness.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **稳健性边界：** Multiple solutions, initialization dependence, analytic continuation, correlated-subspace choice, incomplete inner loops, and solver noise remain; self-consistency does not guarantee the physically stable phase or exactness.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch21-002（章节 21.4；书页 563, 566；公式 21.10, 21.12；PDF 页 588, 591）
- Supports: GW+DMFT closes coupled one-particle and two-particle loops for G/Sigma and W/P; the impurity bath and dynamic local interaction are auxiliary inputs that equal their projected lattice counterparts only at self-consistency.
