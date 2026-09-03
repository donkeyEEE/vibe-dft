---
name: phys-localized-correlated-subspace-hamiltonian
type: theory-model
tags:
  - dmft
  - correlated-subspace
  - model-hamiltonian
updated_at: 2026-08-13
---

## Core statement

局域相关子空间哈密顿量（localized correlated-subspace Hamiltonian）的核心陈述是：A material-specific DMFT Hamiltonian is defined by a localized correlated subspace, and its one-body matrix elements, interaction tensor, impurity projection, and observables must all use that same orbital definition.

## Formulation

- **构造：** Choose localized orthonormal orbitals chi_m, express the full one-body Hamiltonian h_mm'(R), and add a screened four-index interaction U_mnn'm' only for the chosen correlated sites or cells.
- **separation：** States outside the correlated subspace remain part of the embedding problem and screen or hybridize with the local orbitals; they are not necessarily physically uncorrelated.
- **why local basis：** Atomic-like d and f interactions are compact in a localized representation, while hopping and hybridization retain their spatial and orbital structure.
- **一致性规则：** The projectors used to form the local Green function, the interaction parameters, the double-counting correction, occupancies, and reported orbital spectra must refer to the same chi_m.
- **动态边界：** A static U tensor approximates the generally frequency-dependent screened interaction after excluded degrees of freedom are integrated out.
- **边界：** The Hamiltonian is an effective model tied to a chosen energy window and basis; changing either changes its parameters and prevents term-by-term comparison without a transformation.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **动态边界：** A static U tensor approximates the generally frequency-dependent screened interaction after excluded degrees of freedom are integrated out.
- **边界：** The Hamiltonian is an effective model tied to a chosen energy window and basis; changing either changes its parameters and prevents term-by-term comparison without a transformation.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-001（章节 19.2；书页 508, 509；公式 19.3, 19.5；PDF 页 533, 534）
- Supports: A localized-orbital Hamiltonian separates a correlated d/f subspace from the rest, with one-body hopping/crystal-field matrix elements and screened four-index interactions defined in the same orbital basis.
