---
name: phys-anderson-impurity-model
type: theory-model
tags:
  - impurity-solver
  - model-hamiltonian
  - quantum-embedding
updated_at: 2026-08-13
---

## Core statement

Anderson 杂质模型（Anderson impurity model, AIM）把一个具有局域相互作用的离散能级通过杂化耦合到无相互作用连续浴，是描述局域作用 (U) 与浴耦合尺度 \(\Delta\) 竞争的基本量子杂质模型，也是 DMFT 杂质映射的模型基础。

## Formulation

单轨道 AIM 可写为

\[
\hat H_{\mathrm{AIM}}=
\underbrace{\sum_\sigma\epsilon_0\hat n_{0\sigma}+U\hat n_{0\uparrow}\hat n_{0\downarrow}}_{\hat H_{\mathrm{site}}}
+\underbrace{\sum_{k\sigma}\left(V_k\hat c_{k\sigma}^{\dagger}\hat c_{0\sigma}+\mathrm{h.c.}\right)}_{\hat H_{\mathrm{hyb}}}
+\underbrace{\sum_{k\sigma}\epsilon_k\hat c_{k\sigma}^{\dagger}\hat c_{k\sigma}}_{\hat H_{\mathrm{host}}}.
\]

局域项允许形成双占据代价和局域矩，浴项提供连续单粒子态，杂化项允许粒子在杂质与浴之间交换。对于平坦浴态密度和能量无关的杂化 (V)，非相互作用共振宽度为

\[
\Delta=\pi\rho_{\mathrm{host}}V^2.
\]

## Variables and units

- (0) 表示杂质轨道，(k) 标记浴态，\(\sigma\) 为自旋。
- \(\epsilon_0\) 和 \(\epsilon_k\) 分别为杂质与浴能级，(U) 为杂质局域排斥，(V_k) 为杂化矩阵元。
- \(\rho_{\mathrm{host}}\) 是每单位能量的浴态密度，因此 \(\Delta\) 具有能量单位。

## Assumptions

- 教材中的基本模型只有一个自旋简并杂质轨道，且相互作用仅位于杂质上。
- 标量宽度公式假设浴态密度平坦且杂化与能量无关；一般情形应使用频率依赖杂化函数。

## Conditions and boundaries

- 固定浴 AIM 与 DMFT 辅助杂质问题不同：后者的浴由晶格局域格林函数自洽决定。
- 多轨道、动态相互作用或有相互作用浴需要推广模型，不能由单一 (U/\Delta) 完整刻画。
- Hartree–Fock 的静态破缺对称解不能替代精确的动态局域矩和 Kondo 屏蔽物理。

## Relations

- Related: DMFT 杂质自洽、杂化函数、杂质求解器接口和 Kondo resonance。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: 3.5 节，公式 3.8，书页 52，PDF 页 77，证据 ev-ie-ch03-005 与 ev-ie-ch03-006。
- Supports: AIM 的局域、杂化和浴三部分结构，以及平坦浴中 \(\Delta=\pi\rho_{\mathrm{host}}V^2\) 和 (U/\Delta) 竞争。
