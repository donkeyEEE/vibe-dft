---
name: phys-ct-int-impurity-solver
type: theory-model
tags:
  - dmft
  - impurity-solver
  - quantum-monte-carlo
updated_at: 2026-08-13
---

## Core statement

连续时间相互作用展开杂质求解器（continuous-time interaction-expansion impurity solver）的核心陈述是：Continuous-time interaction-expansion quantum Monte Carlo (CT-INT) samples the order, positions, and contractions of interaction vertices around the bath-dressed noninteracting action, eliminating Trotter discretization while shifting difficulty to expansion order and fermionic signs.

## Formulation

- **展开：** Write Z as a series in powers of the local interaction; a configuration contains k vertices at continuous imaginary times, and Wick contraction of the G_0 propagators produces determinants.
- **why it is unbiased：** Sampling all relevant orders and continuous vertex times removes a fixed time grid and its Trotter error; within ergodic sampling, remaining numerical uncertainty is statistical rather than an interaction-order truncation chosen in advance.
- **适用区间：** The characteristic order grows with beta and generally with interaction-expansion weight, so CT-INT is naturally competitive for weak-to-intermediate interactions and larger orbital spaces where determinant updates remain polynomial.
- **相互作用范围：** Standard determinant formulations are simplest for density-density interactions; shifts or auxiliary-field variants can change sign and sampling behavior but do not guarantee a benign sign problem.
- **可观测量：** Green functions and correlators are accumulated from inverse configuration matrices on the imaginary axis.
- **边界：** Continuous time means no time-step error, not zero systematic error; equilibration, autocorrelation, ergodicity, sign decay, finite statistics, and analytic continuation remain separate controls.

## Variables and units

公式中的频率、能量、相互作用强度、温度和带宽默认采用一致的能量单位；若取自然单位，则令 $\hbar=k_{\mathrm B}=1$。矩阵指标指向卡片所声明的局域轨道、团簇站点或动量扇区，具体符号约定以 Formulation 为准。

## Assumptions

本卡描述的理论对象以所列相关子空间、相互作用形式、对称性约束和自洽层级为前提；不能把某个受控极限或特定求解器的性质无条件外推到一般有限维材料。

## Conditions and boundaries

- **相互作用范围：** Standard determinant formulations are simplest for density-density interactions; shifts or auxiliary-field variants can change sign and sampling behavior but do not guarantee a benign sign problem.
- **边界：** Continuous time means no time-step error, not zero systematic error; equilibration, autocorrelation, ergodicity, sign decay, finite statistics, and analytic continuation remain separate controls.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch18-004（章节 18.5；书页 487, 490；公式 18.15, 18.16；PDF 页 512, 515）
- Supports: Continuous-time interaction expansion samples perturbation order and vertex times directly, eliminating Trotter time-step error; its efficiency and sign behavior depend on interaction strength, formulation, and orbital structure.
