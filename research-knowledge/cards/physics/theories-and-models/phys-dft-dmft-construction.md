---
name: phys-dft-dmft-construction
type: theory-model
tags:
  - dmft
  - dft-dmft
  - electronic-structure
updated_at: 2026-08-13
---

## Core statement

DFT+DMFT 构造（DFT+DMFT construction）的核心陈述是：DFT+DMFT combines a Kohn–Sham description of the full material with an explicitly interacting impurity problem for a selected local subspace and joins them through projection, embedding, self-energy upfolding, and optionally charge self-consistency.

## Formulation

- **晶格输入：** A Kohn-Sham Hamiltonian supplies the full-band dispersion and hybridization, while projectors define the correlated local orbitals.
- **局域问题：** A screened local interaction tensor is added in that subspace and a double-counting potential is subtracted before the local Green function defines the impurity bath.
- **DMFT 循环：** The impurity solver returns a local self-energy, which is embedded into the lattice Green function; the projected local Green function then updates the impurity Weiss field until convergence.
- **电荷自洽：** In a charge-self-consistent implementation, the interacting density matrix updates the real-space charge density and Kohn-Sham potential, adding an outer DFT loop around the DMFT fixed point.
- **反馈的重要性：** Feedback is important when correlations substantially redistribute charge or change metal-ligand covalency; one-shot and charge-self-consistent results need not share the same Hamiltonian.
- **边界：** Kohn-Sham eigenvalues are auxiliary ground-state quantities, and DFT+DMFT excitation predictions remain conditional on projectors, U/J, double counting, solver, temperature, and continuation.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **边界：** Kohn-Sham eigenvalues are auxiliary ground-state quantities, and DFT+DMFT excitation predictions remain conditional on projectors, U/J, double counting, solver, temperature, and continuation.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch19-006（章节 19.5；书页 515, 521；公式 19.7；PDF 页 540, 546）
- Supports: DFT+DMFT augments a Kohn-Sham Hamiltonian with explicit local interactions and subtracts an orbital-dependent double-counting term; charge self-consistency feeds the DMFT density back into DFT.
