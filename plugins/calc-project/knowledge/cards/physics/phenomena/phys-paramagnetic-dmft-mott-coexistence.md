---
name: phys-paramagnetic-dmft-mott-coexistence
type: phenomenon
tags:
  - dmft
  - mott-physics
  - phase-transition
updated_at: 2026-08-13
---

## Core statement

顺磁 DMFT 的 Mott 共存区（paramagnetic-DMFT Mott coexistence）的核心陈述是：In paramagnetically constrained single-site DMFT, metallic and insulating solutions coexist between two spinodals, producing a first-order Mott transition that ends at a finite-temperature critical point.

## Observable signatures

- **可观察特征：**
  - A metallic solution remains locally stable up to U_c2(T), where its quasiparticle weight vanishes.
  - An insulating solution remains locally stable down to U_c1(T), where its spectral gap closes.
  - Between U_c1 and U_c2 both self-consistent solutions exist; the thermodynamic first-order line lies inside this region and terminates at a critical endpoint.
  - Above the endpoint the sharp transition is replaced by a crossover with rapidly varying observables.
- **条件：** The cited phase diagram is for the half-filled one-band Hubbard model, a semicircular noninteracting density of states, single-site DMFT, and an enforced paramagnetic solution.
- **解释：** The two spinodals reconcile the quasiparticle-weight collapse and gap-closing pictures as limits of metastability rather than two identical transition criteria.
- **物理含义：** Bath self-consistency permits distinct metallic and insulating fixed points for the same control parameters, making the Mott transition a free-energy competition rather than only a continuous loss of quasiparticle weight.
- **边界：** Allowing antiferromagnetic or other broken-symmetry solutions can pre-empt the paramagnetic transition; the coexistence topology is not automatically the stable phase diagram of a finite-dimensional material.

## Conditions and boundaries

- **条件：** The cited phase diagram is for the half-filled one-band Hubbard model, a semicircular noninteracting density of states, single-site DMFT, and an enforced paramagnetic solution.
- **边界：** Allowing antiferromagnetic or other broken-symmetry solutions can pre-empt the paramagnetic transition; the coexistence topology is not automatically the stable phase diagram of a finite-dimensional material.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch16-008（章节 16.9；书页 448；图 16.5；PDF 页 473）；ev-ie-ch16-014（章节 16.9；书页 449；PDF 页 474）
- Supports: Paramagnetic single-site DMFT yields separate metallic and insulating spinodals, a coexistence region, and a first-order transition terminating at a critical point.; The paramagnetic coexistence result is symmetry constrained; allowing antiferromagnetic order can produce a lower-energy phase and qualitatively change the stable phase diagram.
