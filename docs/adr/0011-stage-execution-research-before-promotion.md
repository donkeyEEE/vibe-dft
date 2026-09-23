---
status: amended by ADR-0016
---

# Stage execution research before promotion

`calc-execute` continues to prefer its tested backend knowledge and delegates
unresolved software facts to `$dev-engineering:research`, using a Luna
background agent so source reading stays outside the main execution context.
Research first writes one cited artifact to a uniquely scoped `/tmp` location;
after troubleshooting succeeds, the user decides whether its reusable evidence,
effective solution, and applicability boundary should be promoted to the
calculation line's `02-计算规范/` directory. This replaces automatic persistence:
temporary investigation should not silently become stable project knowledge,
while the Spec remains the scientific authority throughout.
