---
name: phys-hubbard-model
type: theory-model
tags:
  - mott-physics
  - model-hamiltonian
  - strong-correlation
updated_at: 2026-08-13
---

## Core statement

单带 Hubbard 模型（single-band Hubbard model）在每个格点仅保留一个自旋简并轨道，以格点间跃迁和同一格点上的排斥作用描述电子离域与局域化的竞争；其物态不能由 (U/t) 单独决定，还依赖填充、温度、维度和跃迁几何。

## Formulation

模型哈密顿量写作

\[
\hat H=\epsilon_0\sum_{i\sigma}\hat n_{i\sigma}
+U\sum_i\hat n_{i\uparrow}\hat n_{i\downarrow}
-\sum_{i\ne j,\sigma}t_{ij}\hat c_{i\sigma}^{\dagger}\hat c_{j\sigma}.
\]

第一项给出局域单粒子能量，第二项惩罚双占据，第三项允许电子在格点间传播。最近邻 Hubbard 模型令所有最近邻跃迁具有共同幅值 (t)；加入长程跃迁、非局域相互作用或多个轨道后属于广义 Hubbard 模型。

## Variables and units

- (i,j) 为晶格格点，\(\sigma\in\{\uparrow,\downarrow\}\) 为自旋。
- \(\hat c_{i\sigma}^{\dagger}\)、\(\hat c_{i\sigma}\) 分别创建和湮灭电子，\(\hat n_{i\sigma}=\hat c_{i\sigma}^{\dagger}\hat c_{i\sigma}\)。
- \(\epsilon_0\)、\(U\)、\(t_{ij}\)、化学势和温度均使用一致的能量单位；常以最近邻跃迁 (t) 为能量标度。

## Assumptions

- 基本形式每个格点只保留一个自旋简并轨道。
- 相互作用只作用于同一格点上的相反自旋电子。
- 具体晶格、边界条件、填充和允许的对称性必须另行声明。

## Conditions and boundaries

- (U/t) 不是脱离模型背景的普适相图坐标；维度、填充、温度、跃迁范围和几何阻挫都会改变结果。
- 一维模型在零温半填充下对任意 (U>0) 都有电荷能隙，因此不存在随 (U/t) 变化的有限临界相互作用。
- 模型中的 (U) 是有效短程格点相互作用，不能自动代表真实材料中完整的长程库仑作用或多轨道屏蔽过程。

## Relations

- Related: Mott 转变、DMFT、自洽杂质映射和局域相关子空间模型。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: 3.2 节，公式 3.2，书页 44–45，PDF 页 69–70，证据 ev-ie-ch03-003 与 ev-ie-ch03-004。
- Supports: 单带 Hubbard 哈密顿量、最近邻参数化及其对维度、填充、温度和跃迁几何的依赖；一维半填充零温边界。
