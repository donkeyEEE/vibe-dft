---
name: phys-exact-diagonalization-impurity-solver
type: theory-model
tags:
  - dmft
  - impurity-solver
  - exact-diagonalization
updated_at: 2026-08-13
---

## Core statement

精确对角化杂质求解器（exact-diagonalization impurity solver）的核心陈述是：An exact-diagonalization (ED) impurity solver replaces the continuous bath by finitely many optimized bath levels and solves the resulting interacting cell-plus-bath Hamiltonian, yielding controlled results for that finite representation but not for the original continuum automatically.

## Formulation

- **构造：** Choose bath energies epsilon_l and hybridizations V_l so that Delta_ED(z) = sum_l |V_l|^2/(z - epsilon_l) approximates the target Delta(z), then diagonalize the full finite Hamiltonian and construct Green functions from its many-body eigenstates.
- **成立原因：** The discretized problem is a finite quantum system whose eigenstates encode the interaction exactly up to numerical eigensolver tolerance; Lanczos and continued fractions can target low-energy states and spectral matrix elements without full dense diagonalization.
- **浴离散化：** Discreteness is a selection in energy space, not a finite real-space box. Low-energy Kondo or quasiparticle physics requires dense low-energy bath resolution, whereas integrated observables can converge with fewer levels than detailed spectra.
- **DMFT 迭代：** Because the target bath changes at every iteration, a distance or moment criterion is needed to refit bath parameters; convergence of the finite Hamiltonian alone does not prove convergence of the continuum embedding.
- **优势：** It accesses ground states and real-frequency poles directly, avoids Monte Carlo noise and analytic continuation, and is valuable for small multiorbital or cluster benchmarks.
- **边界：** Hilbert-space dimension grows exponentially with impurity plus bath orbitals, and finite baths produce discrete spectra; broadening those poles is visualization, not recovery of missing continuum information.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界：** Hilbert-space dimension grows exponentially with impurity plus bath orbitals, and finite baths produce discrete spectra; broadening those poles is visualization, not recovery of missing continuum information.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch18-002（章节 18.2；书页 481, 482；PDF 页 506, 507）
- Supports: Exact diagonalization represents both cell and bath by a finite Hamiltonian, has exponential Hilbert-space scaling, and introduces an energy-space bath discretization whose adequacy depends on the target observable.
