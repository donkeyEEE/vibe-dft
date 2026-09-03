---
name: phys-gw-dmft-rest-screened-local-interaction
type: concept
tags:
  - gw-dmft
  - dynamical-interaction
  - screening
updated_at: 2026-08-13
---

## Core statement

GW+DMFT 中由其余体系屏蔽的局域相互作用（rest-screened local interaction in GW+DMFT）的核心陈述是：The retarded impurity interaction in GW+DMFT is the local Coulomb interaction screened by every degree of freedom outside the selected on-site polarization, because that excluded local screening is generated explicitly by the impurity solver.

## Definition and distinctions

- **定义关系：** Given projected fully screened W_loc and impurity irreducible polarization P_imp, define U(omega) = [W_loc^(-1)(omega) + P_imp(omega)]^(-1).
- **屏蔽内容：** U retains screening by uncorrelated orbitals and by correlated orbitals on other sites while excluding polarization processes internal to the same correlated site or cell.
- **排除局域屏蔽的原因：** Feeding a fully screened W directly into the impurity would screen once in the lattice calculation and again when impurity charge fluctuations generate W_imp.
- **自洽含义：** U is an auxiliary interaction during iteration and equals the intended rest-screened interaction only at the coupled bosonic fixed point.
- **与裸相互作用的区别：** It is neither the bare Coulomb tensor nor the fully screened W; its frequency dependence records the excitation spectrum of the degrees of freedom integrated out.
- **边界：** The precise separation depends on the correlated projector, site or cluster definition, polarization convention, and diagrammatic approximation used for the rest.

## Conditions and boundaries

- **边界：** The precise separation depends on the correlated projector, site or cluster definition, polarization convention, and diagrammatic approximation used for the rest.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch21-003（章节 21.4；书页 565；公式 21.10；PDF 页 590）
- Supports: The impurity interaction U(omega) is obtained by removing the on-site correlated-subspace screening from the fully screened local W, so it retains screening by all other orbitals and correlated sites.
