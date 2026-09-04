---
name: phys-theory-experiment-spectral-comparison
type: concept
tags:
  - spectral-function
  - theory-experiment
  - dmft
updated_at: 2026-08-13
---

## Core statement

理论谱与实验光电子谱的比较（theory–experiment spectral comparison）的核心陈述是：Comparing a calculated many-body spectral function with photoemission requires constructing the corresponding experimental observable rather than placing a bare density of states beside a measured intensity curve.

## Definition and distinctions

- **状态匹配：** Match crystal structure, composition, magnetic phase, temperature, pressure, and surface or bulk sensitivity before interpreting agreement.
- **观测量映射：** Photoemission and inverse photoemission probe occupied and unoccupied removal/addition spectra weighted by photon-energy-dependent orbital matrix elements, cross sections, Fermi factors, and experimental geometry.
- **分辨率：** Convolve theory with the stated energy and momentum resolution only after preserving the unconvolved result; broadening can merge multiplets or conceal narrow quasiparticle peaks.
- **理论后处理：** Record projector definition, self-energy approximation, solver temperature, analytic-continuation method and uncertainty, and any background or lifetime broadening.
- **比较层级：** Separate qualitative feature correspondence, relative energy and weight agreement, and absolute quantitative agreement; success for a gap does not validate satellites or orbital character automatically.
- **推断边界：** Similar peak positions are not unique evidence for a microscopic mechanism because matrix elements, continuation priors, double counting, and adjustable U can produce compensating shifts.

## Conditions and boundaries

- **推断边界：** Similar peak positions are not unique evidence for a microscopic mechanism because matrix elements, continuation priors, double counting, and adjustable U can produce compensating shifts.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch20-004（章节 20.2；书页 532, 533；图 20.2；PDF 页 557, 558）
- Supports: Quantitative comparison of calculated and measured spectra requires matching temperature and phase, applying experimental resolution and orbital matrix-element weighting, and retaining analytic-continuation uncertainty.
