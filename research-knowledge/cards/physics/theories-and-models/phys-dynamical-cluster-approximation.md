---
name: phys-dynamical-cluster-approximation
type: theory-model
tags:
  - dmft
  - cluster-method
  - momentum-space
updated_at: 2026-08-13
---

## Core statement

动力学团簇近似（dynamical cluster approximation）的核心陈述是：The dynamical cluster approximation (DCA) uses a periodic cluster to approximate the lattice self-energy by values that are constant within discrete Brillouin-zone patches and determines those sector self-energies self-consistently.

## Formulation

- **定义：** The Brillouin zone is divided into patches centered on cluster momenta K, with Sigma(K+k_tilde, omega) approximated by Sigma(K, omega) inside each patch.
- **增加的物理内容：** Multiple momentum sectors resolve nonlocal correlations and momentum differentiation while retaining translation symmetry at the cluster level.
- **粗粒化：** Lattice Green functions are averaged within each patch to define the cluster bath; the noninteracting dispersion itself remains unapproximated in the reconstructed lattice Green function.
- **收敛：** Increasing cluster size increases momentum resolution and approaches a continuous momentum-dependent self-energy.
- **边界：** Finite patches create discontinuous raw lattice self-energies and limit momentum resolution; smooth Fermi surfaces or dispersions require a causal interpolation or reconstruction whose uncertainty must be reported.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **收敛：** Increasing cluster size increases momentum resolution and approaches a continuous momentum-dependent self-energy.
- **边界：** Finite patches create discontinuous raw lattice self-energies and limit momentum resolution; smooth Fermi surfaces or dispersions require a causal interpolation or reconstruction whose uncertainty must be reported.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch17-003（章节 17.3；书页 463；公式 17.4；PDF 页 488）；ev-ie-ch17-004（章节 17.3；书页 464；PDF 页 489）
- Supports: DCA uses a periodic cluster and approximates the momentum-dependent self-energy as constant within Brillouin-zone patches.; DCA coarse-grains reciprocal space; it preserves the noninteracting lattice terms but has finite-patch resolution and requires interpolation for smooth momentum-resolved quantities.
