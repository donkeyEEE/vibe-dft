---
name: phys-constrained-dft-effective-interaction
type: theory-model
tags:
  - dft-dmft
  - effective-interaction
  - constrained-dft
updated_at: 2026-08-13
---

## Core statement

约束 DFT 有效相互作用（constrained-DFT effective interaction）的核心陈述是：Constrained DFT estimates a static screened interaction for a specified correlated orbital by measuring the energy curvature or occupation response while the permitted screening degrees of freedom relax.

## Formulation

- **构造：** Constrain a local occupation with removed hybridization or a Lagrange-multiplier potential, relax the remaining electronic density, and obtain U from finite total-energy differences, curvature d2E/dn2, or an inverse response with a stated noninteracting subtraction.
- **屏蔽含义：** The resulting U is screened by whatever degrees of freedom were allowed to respond and excludes or includes channels according to the constraint protocol.
- **轨道依赖：** Compact atomic-like and extended ligand-mixed orbitals have different Coulomb matrix elements and screening, so their U values can differ even for the same material.
- **静态近似边界：** Ground-state constrained DFT yields a static parameter and does not reconstruct the full frequency-dependent U(omega) needed when retardation matters.
- **一致性规则：** Calculate U, J, occupancies, and the many-body Hamiltonian in the same correlated subspace and structure; state whether U denotes intraorbital, averaged, or another convention.
- **核验：** Check supercell or response convergence, constraint linearity, screening channels, functional dependence, and sensitivity of physical conclusions rather than treating one U as an experimentally fixed constant.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **静态近似边界：** Ground-state constrained DFT yields a static parameter and does not reconstruct the full frequency-dependent U(omega) needed when retardation matters.
- **核验：** Check supercell or response convergence, constraint linearity, screening channels, functional dependence, and sensitivity of physical conclusions rather than treating one U as an experimentally fixed constant.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-007（章节 19.5；书页 516, 519；公式 19.8, 19.11；PDF 页 541, 544）
- Supports: Static effective interactions from constrained DFT depend on the chosen correlated orbitals and screening response and must be computed consistently with the Hamiltonian in which they are used.
