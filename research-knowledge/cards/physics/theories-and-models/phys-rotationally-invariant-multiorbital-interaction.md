---
name: phys-rotationally-invariant-multiorbital-interaction
type: theory-model
tags:
  - dmft
  - multiorbital-interaction
  - hund-coupling
updated_at: 2026-08-13
---

## Core statement

旋转不变多轨道相互作用（rotationally invariant multiorbital interaction）的核心陈述是：A rotationally invariant multiorbital local interaction couples charge and orbital-spin configurations through intraorbital repulsion, interorbital repulsion, Hund exchange, spin flip, and pair hopping rather than through one universal scalar U.

## Formulation

- **密度项：** In the spherical Kanamori form, two electrons in the same orbital cost U, opposite spins in different orbitals cost U-prime, and parallel spins in different orbitals cost U-prime minus J.
- **旋转不变关系：** For an ideal rotationally invariant shell, U-prime = U - 2J; spin-flip and pair-hopping terms with strength J are required alongside density terms to preserve that invariance.
- **物理含义：** U controls charge fluctuations, while Hund coupling J changes relative multiplet energies and favors high-spin configurations; neutral multiplet splittings can therefore remain important even when monopole charge interactions are strongly screened.
- **记号边界：** Values called U may mean intraorbital U, spherical average F0, or a Hund-ground-state charging energy such as U - 3J; these differ quantitatively and must be named.
- **approximation boundary：** Density-density truncation conserves orbital occupations but removes transverse exchange and pair transfer, which can alter degeneracies, multiplet spectra, and impurity dynamics.
- **晶体环境边界：** The Kanamori reduction assumes an approximately degenerate shell and spherical relations; low symmetry or strongly orbital-dependent screening may require the full four-index tensor.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **记号边界：** Values called U may mean intraorbital U, spherical average F0, or a Hund-ground-state charging energy such as U - 3J; these differ quantitatively and must be named.
- **approximation boundary：** Density-density truncation conserves orbital occupations but removes transverse exchange and pair transfer, which can alter degeneracies, multiplet spectra, and impurity dynamics.
- **晶体环境边界：** The Kanamori reduction assumes an approximately degenerate shell and spherical relations; low symmetry or strongly orbital-dependent screening may require the full four-index tensor.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-004（章节 19.3；书页 512, 513；公式 19.6；PDF 页 537, 538）
- Supports: A rotationally invariant multiorbital interaction requires more than one scalar U; density terms obey U_prime = U - 2J under spherical symmetry and spin-flip and pair-hopping terms complete the interaction.
