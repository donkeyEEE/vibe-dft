---
name: phys-dmft-exact-limits
type: theory-model
tags:
  - dmft
  - strong-correlation
updated_at: 2026-08-13
---

## Core statement

DMFT 的三个精确极限（three exact limits of DMFT）的核心陈述是：DMFT is constructed to recover the isolated interacting-site limit, the noninteracting lattice limit, and the infinite-dimensional limit where its local mean-field construction is exact.

## Formulation

- **isolated interacting site limit：**
  - **定义：** The intersite hopping tends to zero, t_ij -> 0, so the lattice separates into interacting isolated sites and the DMFT bath hybridization tends to zero.
  - **精确原因：** The auxiliary site retains the full local interacting Hamiltonian and becomes the same isolated many-body problem as a lattice site.
  - **物理含义：** DMFT retains atomic multiplets and interaction-driven addition or removal excitations instead of averaging the local interaction into a static one-particle potential.
  - **边界：** A degenerate atomic ground state can be selected by arbitrarily small intersite coupling, so exactness at t_ij = 0 does not by itself determine the ordered finite-hopping ground state.
- **noninteracting lattice limit：**
  - **定义：** The interaction tends to zero, U -> 0, and the interaction self-energy vanishes, Sigma(k, omega) -> 0.
  - **精确原因：** DMFT obtains the interaction contribution through the auxiliary self-energy but leaves the independent-particle dispersion epsilon_k unapproximated.
  - **物理含义：** The full noninteracting lattice Green function G_k(omega) = [omega - epsilon_k]^{-1} is recovered rather than an atomic or local approximation to the band structure.
  - **边界：** This exactness does not constrain errors caused by the local-self-energy approximation once interactions generate important nonlocal correlations.
- **infinite dimensional limit：**
  - **定义：** The dimension or coordination tends to infinity with hopping scaled to keep the kinetic energy finite, conventionally t proportional to Z_coord^(-1/2).
  - **精确原因：** Under this scaling the irreducible self-energy becomes local, Sigma_ij(omega) = delta_ij Sigma(omega), matching the single-site DMFT locality ansatz.
  - **物理含义：** The impurity mapping and its self-consistent bath retain the surviving local quantum dynamics while spatial self-energy corrections vanish in the limit.
  - **边界：** Exactness in infinite dimensions does not imply that short-range magnetic or other spatial correlations are negligible in finite-dimensional or low-dimensional systems.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- 本卡没有额外分项。

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch16-001（章节 Chapter 16 introduction；书页 422；PDF 页 447）；ev-ie-ch16-009（章节 16.2；书页 427；PDF 页 452）；ev-ie-ch16-010（章节 16.2；书页 427；PDF 页 452）；ev-ie-ch16-011（章节 16.9；书页 447；PDF 页 472）
- Supports: DMFT is constructed to recover the isolated interacting-site, noninteracting lattice, and infinite-dimensional limits.; In the noninteracting limit the self-energy vanishes while the independent-particle dispersion remains unapproximated, so DMFT recovers the noninteracting lattice result.; With no coupling between sites the auxiliary system becomes an isolated atom or cell with no bath and the same local Hamiltonian as the lattice site.; For the infinite-coordination Bethe lattice the hopping is scaled with the number of neighbors, and mean-field theory is exact in the infinite-dimensional limit.
