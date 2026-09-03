---
name: phys-imaginary-time-local-moment-diagnostic
type: concept
tags:
  - dmft
  - local-moment
  - imaginary-time
updated_at: 2026-08-13
---

## Core statement

虚时间局域矩判据（imaginary-time local-moment diagnostic）的核心陈述是：The local spin autocorrelation C(tau) = <S_z(tau)S_z(0)> separates instantaneous moment formation from moment lifetime: C(0) measures fluctuation amplitude, while slow decay across imaginary time indicates a persistent local moment.

## Definition and distinctions

- **瞬时量：** C(0) = <S_z^2> is nonzero whenever local spin fluctuations exist, including itinerant systems with rapidly fluctuating moments.
- **持续性：** The shape and long-tau value diagnose how slowly the spin orientation or magnitude relaxes; a plateau-like correlation over a substantial fraction of beta indicates a long-lived moment on thermal time scales.
- **与长程序的区别：** Because C(tau) is local and dynamical, it can identify moments in a paramagnet where <S_z> = 0 and no static symmetry breaking exists.
- **温度边界：** The maximum observable imaginary time is beta/2 by symmetry, so finite temperature limits the longest resolvable lifetime and prevents literal inference of infinite-time stability.
- **比较规则：** Compare curves at matched temperature, normalization, orbital definition, and spin component; C(0), integrated susceptibility, and long-tau behavior answer different questions.
- **推断边界：** A persistent local autocorrelation does not by itself establish intersite magnetic order, exchange mechanism, or a unique effective spin model.

## Conditions and boundaries

- **温度边界：** The maximum observable imaginary time is beta/2 by symmetry, so finite temperature limits the longest resolvable lifetime and prevents literal inference of infinite-time stability.
- **推断边界：** A persistent local autocorrelation does not by itself establish intersite magnetic order, exchange mechanism, or a unique effective spin model.

## Relations

- Related: 本批次中的 DMFT、相关子空间、杂质求解器与谱学卡片；暂不登记需要双向维护的强关系。

## Sources

### Martin–Reining–Ceperley 教材

- Reference: Richard M. Martin, Lucia Reining, and David M. Ceperley, *Interacting Electrons: Theory and Computational Approaches*, Cambridge University Press (2016).
- Locator: ev-ie-ch20-002（章节 20.4；书页 539；图 20.6；PDF 页 564）
- Supports: The equal-time spin correlation measures instantaneous moment magnitude, while its imaginary-time decay measures persistence; a slow decay supports a localized moment even without static magnetic order.
