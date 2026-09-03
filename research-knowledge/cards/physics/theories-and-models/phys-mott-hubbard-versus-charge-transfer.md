---
name: phys-mott-hubbard-versus-charge-transfer
type: theory-model
tags:
  - mott-physics
  - charge-transfer
  - correlated-materials
updated_at: 2026-08-13
---

## Core statement

Mott–Hubbard 与电荷转移分类（Mott–Hubbard versus charge-transfer classification）的核心陈述是：The Mott–Hubbard versus charge-transfer distinction classifies a correlated insulator by the lowest charge excitation and the orbital character at its gap edges, not by the presence of a Hubbard interaction alone.

## Formulation

- **Mott–Hubbard 区间：** When ligand p states lie well below the correlated d manifold, the lowest occupied and empty states are predominantly d derived and the gap is governed mainly by splitting within the d sector.
- **电荷转移区间：** When the ligand-to-metal charge-transfer energy is below the effective d-d repulsion, the valence edge has substantial ligand-p weight and the lowest excitation transfers charge from ligand to metal.
- **physical consequence：** Hole doping in the charge-transfer regime initially removes weight from mixed ligand-metal states, so a d-only occupancy picture can misidentify the carriers.
- **模型后果：** A d-only low-energy model may encode ligand effects in extended Wannier orbitals, whereas an explicit p-d model retains ligand states and uses more atomic-like d orbitals; their U values are not interchangeable.
- **诊断：** Use orbital-resolved occupied and unoccupied spectra together with a specified projector basis and p-d alignment; total density of states or formal oxidation alone is insufficient.
- **边界：** Real materials can be strongly hybridized or intermediate between ideal limits, and double counting or projector choice can shift the apparent classification.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界：** Real materials can be strongly hybridized or intermediate between ideal limits, and double counting or projector choice can shift the apparent classification.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-003（章节 19.2；书页 511；图 19.6；PDF 页 536）
- Supports: In the Zaanen-Sawatzky-Allen distinction, a Mott-Hubbard gap separates predominantly d-derived states, whereas a charge-transfer gap places ligand-p weight at the valence edge and transfers charge from ligand to metal.
