---
name: phys-extended-dmft
type: theory-model
tags:
  - dmft
  - nonlocal-interaction
  - screening
updated_at: 2026-08-13
---

## Core statement

扩展动态平均场理论（extended dynamical mean-field theory）的核心陈述是：Extended dynamical mean-field theory (EDMFT) maps a lattice with nonlocal interactions to a local auxiliary problem coupled to both a fermionic bath and a bosonic screening bath, producing a self-consistent frequency-dependent local interaction.

## Formulation

- **定义：** The fermionic bath Delta(omega) represents hopping into the environment, while a bosonic bath represents retarded density or spin interactions with the polarizable environment.
- **形式化表达：** The auxiliary interaction U_eff(omega) and hybridization Delta(omega) are adjusted so that both the local lattice Green function and local screened interaction match their auxiliary counterparts.
- **增加的物理内容：** Momentum dependence from bare intersite interactions survives in lattice susceptibilities and screened interactions even though the irreducible self-energy and polarizability are approximated as local.
- **物理含义：** Spatial screening is compressed into a retarded on-site interaction rather than represented by an explicit multi-site impurity cluster.
- **边界：** EDMFT treats nonlocal interaction effects through local irreducible quantities; nonlocal vertex and self-energy structure generally requires combinations such as GW+DMFT or other extensions.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界：** EDMFT treats nonlocal interaction effects through local irreducible quantities; nonlocal vertex and self-energy structure generally requires combinations such as GW+DMFT or other extensions.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch17-005（章节 17.5；书页 467, 469；公式 17.12, 17.14；PDF 页 492, 494）
- Supports: EDMFT couples a single interacting site to both a fermionic hopping bath and a bosonic interaction bath, producing a frequency-dependent effective local interaction and an additional bosonic self-consistency condition.
