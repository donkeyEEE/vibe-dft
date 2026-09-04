---
name: phys-kondo-resonance-in-anderson-impurity-model
type: phenomenon
tags:
  - kondo-physics
  - spectral-function
  - local-moment
updated_at: 2026-08-13
---

## Core statement

Anderson 杂质模型中的 Kondo resonance（Kondo resonance in the Anderson impurity model）是局域矩区非微扰自旋翻转动力学产生的窄费米能级共振，其宽度约为 Kondo 温度 (T_K)；在对称大 (U) 情形下，它位于两个原子型加电子和去电子侧峰之间，而不要求静态杂质磁矩。

## Observable signatures

- 费米能级处出现宽度量级为 (T_K) 的窄低能共振，也称 Abrikosov–Suhl resonance。
- 对称大 (U) AIM 同时具有两个相隔约 (U) 的宽原子型电荷激发峰。
- 金属中的磁性杂质可表现出低温电阻反常：温度降至 (T_K) 附近以下时，普通金属式下降被反转。

三峰线形或电阻极小值都不是脱离模型和控制变量后确认唯一微观机制的充分证据。

## Conditions and boundaries

- 上述谱结构针对低温、局域矩区的对称自旋 (1/2) AIM。
- 有限阶弱耦合微扰在 (T\to0) 时失效，需要重整化群、Bethe ansatz 或数值精确杂质求解等非微扰方法。
- 不受限 Hartree–Fock 给出的固定方向磁矩是近似伪象；精确解可满足 \(\langle m\rangle=0\) 而 \(\langle |m|^2\rangle\ne0\)。
- 这里的固定浴杂质谱不同于 DMFT 的自洽晶格三峰谱；后者的中心峰还受浴自洽和晶格相干控制。
- 所选来源给出 (T_K) 的物理尺度和谱作用，但没有提供一般闭式公式。

## Interpretations

高能侧峰来自局域态的加电子和去电子代价；低能共振来自杂质与浴电子之间的自旋翻转和动态屏蔽。两种尺度共存体现局域电荷激发与低能多体相干并存。

## Relations

- Related: Anderson 杂质模型、DMFT 三峰谱结构、重费米子相干交叉和局域矩判据。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: 3.5 节，Figure 3.4，书页 52–53，PDF 页 77–78，证据 ev-ie-ch03-007 与 ev-ie-ch03-008。
- Supports: 低温电阻反常、微扰失效、对称 AIM 的三峰结构，以及由自旋翻转产生的窄 Abrikosov–Suhl resonance。
