---
name: phys-imaginary-time-solver-spectral-boundary
type: concept
tags:
  - dmft
  - impurity-solver
  - spectral-function
updated_at: 2026-08-13
---

## Core statement

虚时间求解器的谱学边界（spectral boundary of imaginary-time solvers）的核心陈述是：Imaginary-time impurity solvers provide static and Matsubara-axis observables directly, whereas a real-frequency spectrum is an inverse problem obtained by analytic continuation and must not be treated as equally direct evidence.

## Definition and distinctions

- **直接输出：** Density, energy, susceptibilities, G(tau), and G(i omega_n) can be estimated in imaginary time without analytic continuation, subject to sampling and estimator errors.
- **逆问题关系：** The measured G(tau) or G(i omega_n) is an integral transform of a spectral density A(omega); the kernel smooths spectral detail, so inversion amplifies finite precision and Monte Carlo noise.
- **后果：** Maximum-entropy or related continuation methods regularize an underdetermined problem and can broaden peaks, merge nearby structures, or bias gaps and spectral weight according to priors and noise.
- **能隙检验：** A spectral gap has an imaginary-time signature through long-tau decay, but finite beta and poor statistics where G(tau) is small limit the smallest resolvable scale.
- **核验：** Report the imaginary-axis fit, noise model, continuation settings, stability across priors or methods, and only claim features robust to these variations.
- **边界：** Failure to resolve a narrow feature is not proof of its absence, and a smooth continued spectrum is not a direct Monte Carlo observable; zero-frequency extrapolations can be better conditioned but remain model-dependent.

## Conditions and boundaries

- **核验：** Report the imaginary-axis fit, noise model, continuation settings, stability across priors or methods, and only claim features robust to these variations.
- **边界：** Failure to resolve a narrow feature is not proof of its absence, and a smooth continued spectrum is not a direct Monte Carlo observable; zero-frequency extrapolations can be better conditioned but remain model-dependent.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch18-003（章节 18.3；书页 483, 485；PDF 页 508, 510）
- Supports: Imaginary-time Monte Carlo avoids explicit bath discretization but leaves statistical errors, possible sign problems, low-temperature cost, and an ill-conditioned analytic-continuation step for real-frequency spectra.
