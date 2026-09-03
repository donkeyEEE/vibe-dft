---
name: phys-crystal-field-splitting-definition
type: concept
tags:
  - electronic-structure
  - crystal-field
  - correlated-materials
updated_at: 2026-08-13
---

## Core statement

晶场劈裂的操作性定义（operational definition of crystal-field splitting）的核心陈述是：Crystal-field splitting must be defined operationally because the term may denote a bare on-site potential splitting or an effective separation of orbital-resolved band centers after covalency and interactions.

## Definition and distinctions

- **静电含义：** In a localized Hamiltonian, the nonspherical part of the on-site one-body matrix lifts atomic degeneracy according to site symmetry.
- **配体场含义：** Hybridization with neighboring ligand states shifts and broadens different orbitals unequally; these covalent shifts can dominate the electrostatic contribution.
- **能带中心含义：** Some literature reports the difference between centers of orbital-character bands, which includes on-site potential, hybridization, and possibly interaction-dependent shifts.
- **对称性示例：** Cubic symmetry separates d states into e_g and t_2g representations, while lower symmetry can split these further; away from high-symmetry momenta, band labels generally indicate dominant character rather than pure eigenstates.
- **测量与比较规则：** State the basis, energy-window definition, whether centers or on-site matrix elements are used, and which interaction correction is included before comparing values.
- **边界：** A quoted Delta_cf without this definition cannot uniquely identify an electrostatic crystal field or be transferred between DFT, Wannier, and spectroscopic analyses.

## Conditions and boundaries

- **边界：** A quoted Delta_cf without this definition cannot uniquely identify an electrostatic crystal field or be transferred between DFT, Wannier, and spectroscopic analyses.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-002（章节 19.2；书页 509, 510；图 19.5；PDF 页 534, 535）
- Supports: Crystal-field splitting may denote the nonspherical on-site potential alone or the separation of band centers after hybridization and interactions, so its operational definition must be stated.
