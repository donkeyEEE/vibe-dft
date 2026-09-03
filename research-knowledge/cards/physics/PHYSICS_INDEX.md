# Physics Knowledge Index

本索引是物理子库的唯一导航和卡片状态来源。读取物理卡片前，必须先读
[../SKILL.md](../SKILL.md) 和 [../INDEX.md](../INDEX.md)，再按本索引选择最小相关集合。

## Card types

| Type | Directory | Question answered |
|---|---|---|
| `concept` | `concepts/` | 物理对象是什么 |
| `phenomenon` | `phenomena/` | 物理对象表现为什么 |
| `theory-model` | `theories-and-models/` | 物理对象如何被解释或预测 |

卡片文件名使用 `phys-` 前缀。frontmatter 的 `type` 必须与所在目录一致。

## Card status

- `established`：核心陈述有清晰来源支持，目前没有实质冲突。
- `contested`：来源在定义、对同一证据的互斥解释、相互冲突的预测或无法用条件区分的适用范围上存在实质分歧。

状态只在本索引维护，不写入卡片 frontmatter。正式子库不保存草稿卡或重定向卡。

## Relation labels

关键语义关系成对维护：

- `Requires` ↔ `Prerequisite for`
- `Explains` ↔ `Explained by`
- `Generalizes` ↔ `Special case of`

`Related` 表示没有更精确关系的普通关联，不要求反向记录。所有本地关系目标必须存在。

## Registered tags

tag 使用单层 kebab-case 词汇且不包含层级分隔符。新增 tag 必须先登记在此处。

- `charge-transfer`
- `cluster-method`
- `constrained-dft`
- `constrained-rpa`
- `correlated-materials`
- `correlated-subspace`
- `crystal-field`
- `dft-dmft`
- `dmft`
- `doping`
- `double-counting`
- `dynamical-interaction`
- `effective-interaction`
- `electronic-structure`
- `exact-diagonalization`
- `gw-dmft`
- `heavy-fermion`
- `hund-coupling`
- `imaginary-time`
- `impurity-solver`
- `kondo-physics`
- `local-moment`
- `magnetic-order`
- `metal-insulator-transition`
- `model-hamiltonian`
- `momentum-space`
- `mott-physics`
- `multiorbital-interaction`
- `nonlocal-interaction`
- `phase-transition`
- `pressure`
- `pseudogap`
- `quantum-embedding`
- `quantum-monte-carlo`
- `screening`
- `self-consistency`
- `self-energy`
- `spectral-function`
- `spin-state-transition`
- `strong-correlation`
- `theory-experiment`
- `wannier-function`

## Concepts

| Card | Type | Status | Topics |
|---|---|---|---|
| [phys-correlated-subspace-nonuniqueness.md](concepts/phys-correlated-subspace-nonuniqueness.md) | `concept` | `established` | `dmft`, `correlated-subspace`, `wannier-function` |
| [phys-correlation-driven-gap-order-independence.md](concepts/phys-correlation-driven-gap-order-independence.md) | `concept` | `established` | `mott-physics`, `metal-insulator-transition`, `magnetic-order` |
| [phys-crystal-field-splitting-definition.md](concepts/phys-crystal-field-splitting-definition.md) | `concept` | `established` | `electronic-structure`, `crystal-field`, `correlated-materials` |
| [phys-dft-dmft-double-counting.md](concepts/phys-dft-dmft-double-counting.md) | `concept` | `established` | `dmft`, `dft-dmft`, `double-counting` |
| [phys-dmft-hybridization-function.md](concepts/phys-dmft-hybridization-function.md) | `concept` | `established` | `dmft`, `quantum-embedding` |
| [phys-gw-dmft-rest-screened-local-interaction.md](concepts/phys-gw-dmft-rest-screened-local-interaction.md) | `concept` | `established` | `gw-dmft`, `dynamical-interaction`, `screening` |
| [phys-imaginary-time-local-moment-diagnostic.md](concepts/phys-imaginary-time-local-moment-diagnostic.md) | `concept` | `established` | `dmft`, `local-moment`, `imaginary-time` |
| [phys-imaginary-time-solver-spectral-boundary.md](concepts/phys-imaginary-time-solver-spectral-boundary.md) | `concept` | `established` | `dmft`, `impurity-solver`, `spectral-function` |
| [phys-theory-experiment-spectral-comparison.md](concepts/phys-theory-experiment-spectral-comparison.md) | `concept` | `established` | `spectral-function`, `theory-experiment`, `dmft` |

## Phenomena

| Card | Type | Status | Topics |
|---|---|---|---|
| [phys-cluster-dmft-momentum-selective-pseudogap.md](phenomena/phys-cluster-dmft-momentum-selective-pseudogap.md) | `phenomenon` | `established` | `dmft`, `pseudogap`, `momentum-space` |
| [phys-dmft-three-peak-spectrum.md](phenomena/phys-dmft-three-peak-spectrum.md) | `phenomenon` | `established` | `dmft`, `mott-physics`, `spectral-function` |
| [phys-doping-induced-spectral-weight-transfer.md](phenomena/phys-doping-induced-spectral-weight-transfer.md) | `phenomenon` | `established` | `mott-physics`, `doping`, `spectral-function` |
| [phys-dynamical-screening-bandwidth-and-satellites.md](phenomena/phys-dynamical-screening-bandwidth-and-satellites.md) | `phenomenon` | `established` | `dynamical-interaction`, `screening`, `spectral-function` |
| [phys-heavy-fermion-coherence-crossover.md](phenomena/phys-heavy-fermion-coherence-crossover.md) | `phenomenon` | `established` | `dmft`, `heavy-fermion`, `kondo-physics` |
| [phys-kondo-resonance-in-anderson-impurity-model.md](phenomena/phys-kondo-resonance-in-anderson-impurity-model.md) | `phenomenon` | `established` | `kondo-physics`, `spectral-function`, `local-moment` |
| [phys-mott-transition-interaction-bandwidth-competition.md](phenomena/phys-mott-transition-interaction-bandwidth-competition.md) | `phenomenon` | `established` | `mott-physics`, `metal-insulator-transition`, `strong-correlation` |
| [phys-paramagnetic-dmft-mott-coexistence.md](phenomena/phys-paramagnetic-dmft-mott-coexistence.md) | `phenomenon` | `established` | `dmft`, `mott-physics`, `phase-transition` |
| [phys-pressure-driven-spin-state-competition.md](phenomena/phys-pressure-driven-spin-state-competition.md) | `phenomenon` | `established` | `correlated-materials`, `spin-state-transition`, `pressure` |

## Theories and models

| Card | Type | Status | Topics |
|---|---|---|---|
| [phys-anderson-impurity-model.md](theories-and-models/phys-anderson-impurity-model.md) | `theory-model` | `established` | `impurity-solver`, `model-hamiltonian`, `quantum-embedding` |
| [phys-cellular-dmft.md](theories-and-models/phys-cellular-dmft.md) | `theory-model` | `established` | `dmft`, `cluster-method` |
| [phys-constrained-dft-effective-interaction.md](theories-and-models/phys-constrained-dft-effective-interaction.md) | `theory-model` | `established` | `dft-dmft`, `effective-interaction`, `constrained-dft` |
| [phys-constrained-rpa-effective-interaction.md](theories-and-models/phys-constrained-rpa-effective-interaction.md) | `theory-model` | `established` | `constrained-rpa`, `effective-interaction`, `screening` |
| [phys-ct-hyb-dynamical-interactions.md](theories-and-models/phys-ct-hyb-dynamical-interactions.md) | `theory-model` | `established` | `dmft`, `impurity-solver`, `dynamical-interaction` |
| [phys-ct-hyb-impurity-solver.md](theories-and-models/phys-ct-hyb-impurity-solver.md) | `theory-model` | `established` | `dmft`, `impurity-solver`, `quantum-monte-carlo` |
| [phys-ct-int-impurity-solver.md](theories-and-models/phys-ct-int-impurity-solver.md) | `theory-model` | `established` | `dmft`, `impurity-solver`, `quantum-monte-carlo` |
| [phys-dft-dmft-construction.md](theories-and-models/phys-dft-dmft-construction.md) | `theory-model` | `established` | `dmft`, `dft-dmft`, `electronic-structure` |
| [phys-dmft-exact-limits.md](theories-and-models/phys-dmft-exact-limits.md) | `theory-model` | `established` | `dmft`, `strong-correlation` |
| [phys-dmft-impurity-self-consistency.md](theories-and-models/phys-dmft-impurity-self-consistency.md) | `theory-model` | `established` | `dmft`, `quantum-embedding` |
| [phys-dmft-impurity-solver-interface.md](theories-and-models/phys-dmft-impurity-solver-interface.md) | `theory-model` | `established` | `dmft`, `impurity-solver` |
| [phys-dynamical-cluster-approximation.md](theories-and-models/phys-dynamical-cluster-approximation.md) | `theory-model` | `established` | `dmft`, `cluster-method`, `momentum-space` |
| [phys-exact-diagonalization-impurity-solver.md](theories-and-models/phys-exact-diagonalization-impurity-solver.md) | `theory-model` | `established` | `dmft`, `impurity-solver`, `exact-diagonalization` |
| [phys-extended-dmft.md](theories-and-models/phys-extended-dmft.md) | `theory-model` | `established` | `dmft`, `nonlocal-interaction`, `screening` |
| [phys-gw-dmft-coupled-self-consistency.md](theories-and-models/phys-gw-dmft-coupled-self-consistency.md) | `theory-model` | `established` | `dmft`, `gw-dmft`, `self-consistency` |
| [phys-gw-dmft-local-diagram-replacement.md](theories-and-models/phys-gw-dmft-local-diagram-replacement.md) | `theory-model` | `established` | `dmft`, `gw-dmft`, `double-counting` |
| [phys-hubbard-model.md](theories-and-models/phys-hubbard-model.md) | `theory-model` | `established` | `mott-physics`, `model-hamiltonian`, `strong-correlation` |
| [phys-localized-correlated-subspace-hamiltonian.md](theories-and-models/phys-localized-correlated-subspace-hamiltonian.md) | `theory-model` | `established` | `dmft`, `correlated-subspace`, `model-hamiltonian` |
| [phys-mott-hubbard-versus-charge-transfer.md](theories-and-models/phys-mott-hubbard-versus-charge-transfer.md) | `theory-model` | `established` | `mott-physics`, `charge-transfer`, `correlated-materials` |
| [phys-rotationally-invariant-multiorbital-interaction.md](theories-and-models/phys-rotationally-invariant-multiorbital-interaction.md) | `theory-model` | `established` | `dmft`, `multiorbital-interaction`, `hund-coupling` |
| [phys-single-site-dmft-local-self-energy.md](theories-and-models/phys-single-site-dmft-local-self-energy.md) | `theory-model` | `established` | `dmft`, `self-energy` |
