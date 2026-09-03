---
name: phys-dmft-three-peak-spectrum
type: phenomenon
tags:
  - dmft
  - mott-physics
  - spectral-function
updated_at: 2026-08-13
---

## Core statement

DMFT 三峰谱结构（DMFT three-peak spectral structure）的核心陈述是：In the strongly correlated paramagnetic Hubbard regime, DMFT can produce a narrow temperature-sensitive quasiparticle peak at the Fermi level between lower and upper atomic-like sidebands.

## Observable signatures

- **可观察特征：**
  - A narrow central spectral peak appears at the Fermi level with quasiparticle weight Z.
  - Broad lower and upper Hubbard sidebands carry incoherent weight of order 1 - Z and are separated on the interaction scale U.
  - The central low-energy peak is suppressed when temperature becomes comparable to its narrow coherence scale.
- **条件：** The cited demonstration is the half-filled, one-band Hubbard model constrained to the paramagnetic phase with a semicircular noninteracting density of states in single-site DMFT.
- **解释：** The central feature is a lattice-coherent quasiparticle resonance analogous to the low-temperature Kondo resonance of an impurity, while the sidebands retain atomic-like charge-excitation character.
- **物理含义：** The simultaneous narrow central feature and broad interaction-separated sidebands show that strong correlation redistributes spectral weight across both low- and high-energy scales.
- **边界：** A three-peak line shape is not universal proof of DMFT or of a unique microscopic mechanism; low-dimensional nonlocal correlations can replace the central peak with a pseudogap or gap, and material spectra require matrix-element and multiband analysis.

## Conditions and boundaries

- **条件：** The cited demonstration is the half-filled, one-band Hubbard model constrained to the paramagnetic phase with a semicircular noninteracting density of states in single-site DMFT.
- **边界：** A three-peak line shape is not universal proof of DMFT or of a unique microscopic mechanism; low-dimensional nonlocal correlations can replace the central peak with a pseudogap or gap, and material spectra require matrix-element and multiband analysis.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch16-007（章节 16.9；书页 447；图 16.4；PDF 页 472）；ev-ie-ch16-013（章节 16.9；书页 448；PDF 页 473）
- Supports: Increasing interaction produces a central quasiparticle peak of weight Z together with upper and lower atomic-like sidebands, and the low-energy peak is temperature sensitive.; The central low-energy peak resembles the Kondo resonance of an impurity, whereas lattice bath self-consistency allows the peak to terminate and a gap to open; the sidebands remain separated on the interaction scale.
