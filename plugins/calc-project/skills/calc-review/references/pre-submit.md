# Prepared Snapshot Checks

Inspect the exact prepared Run and report evidence; change nothing.

- Require the current Spec task declaration, its Run row with `prepared`
  status, the exact Run path, and complete `inputs/`, `outputs/`, and `logs/`
  directories. Require nonempty `inputs/run.sh` and `inputs/run.pbs` plus every
  backend-declared input. Conflicting identities, status, paths, or authorities
  stop review without a judgment.
- Compare every scientific setting with the current approved Spec and its
  named evidence. Templates and project source instructions are rendering
  baselines or mechanics, not authority for a missing or different scientific
  value.
- Check that every upstream handoff names the current accepted Run and exact
  source, that immutable copies match their sources, and that server-only HDF5,
  `CHGCAR`, and `WAVECAR` handling is explicit. A guessed source, stale current
  Run, mutable handoff, or local large-file transfer blocks.
- Inspect the intended executable environment, cluster, queue, resources,
  submission command, cost/concurrency effects, and expected products. Compare
  stable profile configuration with the current Run-specific probe evidence;
  defaults and stale probes are not current evidence.
- Look for evident waste, destructive behavior, output replacement, broad
  copies, path escape, hidden directory discovery, or changes made after
  preparation. Any required action, choice, or authorization is `block`.

`pass_with_warnings` is limited to findings that require no action or decision
before submission. A checksum establishes identity only; it is neither review
nor authorization.
