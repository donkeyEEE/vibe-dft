---
name: phys-cluster-dmft-momentum-selective-pseudogap
type: phenomenon
tags:
  - dmft
  - pseudogap
  - momentum-space
updated_at: 2026-08-13
---

## Core statement

团簇 DMFT 中的动量选择性赝能隙（momentum-selective pseudogap in cluster DMFT）的核心陈述是：In cluster DMFT calculations near half-filling, correlations can suppress low-energy antinodal spectral weight while leaving nodal sectors comparatively metallic, producing a momentum-selective pseudogap.

## Observable signatures

- **可观察特征：**
  - The spectral function develops a strong low-energy depression in the patch around the antinodal momentum (0, pi).
  - No comparable depression appears in the nodal patch around (pi/2, pi/2) in the cited calculation.
  - The effect strengthens as hole doping is reduced toward half-filling.
- **条件：** The cited result uses an eight-site DCA solution of a two-dimensional Hubbard model with U = 7t, next-neighbor hopping t_prime = -0.15t, and finite-temperature analytic continuation.
- **物理含义：** A momentum-independent self-energy cannot express this nodal-antinodal differentiation, so the result diagnoses important short-range spatial correlations within the model.
- **边界：** A patch-averaged pseudogap is not unique evidence for one microscopic mechanism and is not directly identical to an experimental ARPES spectrum; cluster choice, analytic continuation, temperature, and matrix elements matter.

## Conditions and boundaries

- **条件：** The cited result uses an eight-site DCA solution of a two-dimensional Hubbard model with U = 7t, next-neighbor hopping t_prime = -0.15t, and finite-temperature analytic continuation.
- **边界：** A patch-averaged pseudogap is not unique evidence for one microscopic mechanism and is not directly identical to an experimental ARPES spectrum; cluster choice, analytic continuation, temperature, and matrix elements matter.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch17-006（章节 17.6；书页 473；图 17.7；PDF 页 498）
- Supports: An eight-site DCA calculation finds a doping-dependent pseudogap near the antinodal patch but not near the nodal patch, demonstrating momentum-selective correlation effects absent from a local self-energy.
