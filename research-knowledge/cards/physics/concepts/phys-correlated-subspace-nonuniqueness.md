---
name: phys-correlated-subspace-nonuniqueness
type: concept
tags:
  - dmft
  - correlated-subspace
  - wannier-function
updated_at: 2026-08-13
---

## Core statement

相关子空间的非唯一性（nonuniqueness of the correlated subspace）的核心陈述是：A DFT+DMFT correlated subspace is not uniquely determined by the material; its projector or Wannier construction fixes how metal, ligand, and interstitial weight is partitioned and thereby changes every projected model parameter.

## Definition and distinctions

- **自由度来源：** Wannier functions depend on band window, disentanglement, gauge, localization criterion, and whether ligand bands are included explicitly.
- **two valid models：** A broad p-d window can yield compact atomic-like d orbitals with explicit ligand states, while a d-only window yields more extended d-like orbitals carrying ligand tails; both can span appropriate low-energy bands.
- **参数后果：** Orbital extent changes hopping, hybridization, occupancy, screened U and J, and the size of nonlocal interactions, so parameter values are meaningful only with their subspace definition.
- **近似后果：** In an exact unitary reformulation observables are invariant, but DMFT locality and interaction truncations make practical results basis dependent.
- **报告规则：** Record projectors, energy windows, disentanglement, local axes, normalization, orbital-resolved occupancy, and the subspace used to compute interactions and double counting.
- **比较边界：** Agreement of band interpolation does not establish equivalence of two interacting models, and numerical U values from unlike subspaces should not be compared as material constants.

## Conditions and boundaries

- **比较边界：** Agreement of band interpolation does not establish equivalence of two interacting models, and numerical U values from unlike subspaces should not be compared as material constants.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-005（章节 19.4；书页 513, 514；图 19.7；PDF 页 538, 539）
- Supports: The correlated/localized orbital subspace is not unique; different Wannier windows redistribute metal-ligand weight, and approximate many-body results depend on which states are retained explicitly.
