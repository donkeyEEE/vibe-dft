---
name: phys-dft-dmft-double-counting
type: concept
tags:
  - dmft
  - dft-dmft
  - double-counting
updated_at: 2026-08-13
---

## Core statement

DFT+DMFT 双计数（DFT+DMFT double counting）的核心陈述是：DFT+DMFT double counting is intrinsically non-unique because an explicit local interaction Hamiltonian cannot be uniquely matched to the exchange-correlation contribution already encoded as a nonlinear density functional.

## Definition and distinctions

- **问题：** Adding U and J to the correlated subspace repeats an unknown portion of the interactions already represented by the Kohn-Sham potential, requiring a subtraction in local orbital energies and total energy.
- **无唯一精确扣除的原因：** Standard DFT does not decompose its exchange-correlation energy into the same orbital-resolved quadratic and quartic operators used by DMFT, so there is no uniquely identified overlap term.
- **物理作用：** The correction controls correlated-shell occupancy and relative alignment with ligand or itinerant bands; it can therefore change whether a calculation appears Mott-Hubbard-like or charge-transfer-like.
- **规范与相对能级：** A uniform shift of an isolated correlated manifold may be absorbed into chemical potential, but relative shifts matter when correlated and uncorrelated bands hybridize or exchange charge.
- **核验：** Name the formula and occupancy convention, report the resulting shell occupancy and p-d alignment, and test whether conclusions survive plausible alternative corrections or a physically justified occupancy constraint.
- **边界：** Agreement after tuning double counting is calibration, not independent validation of the microscopic mechanism; values are not transferable across different projectors, U definitions, or charge-self-consistency choices.

## Conditions and boundaries

- **核验：** Name the formula and occupancy convention, report the resulting shell occupancy and p-d alignment, and test whether conclusions survive plausible alternative corrections or a physically justified occupancy constraint.
- **边界：** Agreement after tuning double counting is calibration, not independent validation of the microscopic mechanism; values are not transferable across different projectors, U definitions, or charge-self-consistency choices.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-008（章节 19.5；书页 519, 520；PDF 页 544, 545）
- Supports: DFT+DMFT double counting has no unique exact subtraction because DFT and DMFT represent interactions in incommensurate density-functional and explicit-Hamiltonian forms, and its orbital shifts can change p-d alignment.
