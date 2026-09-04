---
name: phys-cellular-dmft
type: theory-model
tags:
  - dmft
  - cluster-method
updated_at: 2026-08-13
---

## Core statement

元胞动态平均场理论（cellular dynamical mean-field theory）的核心陈述是：Cellular dynamical mean-field theory (cellular DMFT, CDMFT) embeds an open-boundary real-space cluster, retaining dynamical self-energy matrix elements inside the cluster while replacing correlations beyond it by a self-consistent medium.

## Formulation

- **定义：** A supercell of N_c sites is treated as the correlated auxiliary system; all one-particle and self-energy quantities become matrices in its orbitals.
- **近似：** Self-energy elements inside the chosen cell are retained, while matrix elements connecting different cells are set to zero.
- **增加的物理内容：** Increasing the cell directly resolves short-range spatial correlations and momentum dependence that cannot exist in a scalar single-site self-energy.
- **边界条件：** The impurity cluster has open boundaries, so its sites are inequivalent and primitive-lattice translation symmetry is broken before periodization.
- **周期化：** A lattice self-energy or Green function requires a chosen reconstruction from cluster quantities; boundary errors typically decay faster in gapped systems than in metals.
- **边界：** Results depend on cluster geometry, size, boundary effects, and periodization choice; finite-cluster agreement is not by itself proof of convergence.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界条件：** The impurity cluster has open boundaries, so its sites are inequivalent and primitive-lattice translation symmetry is broken before periodization.
- **边界：** Results depend on cluster geometry, size, boundary effects, and periodization choice; finite-cluster agreement is not by itself proof of convergence.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch17-001（章节 17.2；书页 461；公式 17.3；PDF 页 486）；ev-ie-ch17-002（章节 17.2；书页 462；PDF 页 487）
- Supports: Cellular DMFT embeds an open-boundary real-space cluster and retains self-energy matrix elements within the cell while neglecting those between different cells.; Restoring primitive-cell translation symmetry after a cellular calculation requires periodization, whose boundary error and convergence depend on whether the system is insulating or metallic.
