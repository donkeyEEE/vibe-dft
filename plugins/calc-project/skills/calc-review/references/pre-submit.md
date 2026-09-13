# Prepared Snapshot Checks

Inspect the exact prepared Run and report evidence; change nothing.

- Establish the current Spec task declaration, its Run row, the exact Run path,
  and the expected Run layout and backend inputs. A missing directory, file, or
  `prepared` status is an execution defect; report the exact missing or
  conflicting object.
- Compare every scientific setting with the current approved Spec and its
  named evidence. Templates and project source instructions are rendering
  baselines or mechanics, not authority for a missing or different scientific
  value.
- Check that every upstream handoff names the current accepted Run and exact
  source, that immutable copies match their sources, and that server-only HDF5,
  `CHGCAR`, and `WAVECAR` handling is explicit. A guessed source, stale current
  Run, mutable handoff, or local large-file transfer prevents submission.
- Inspect the intended executable environment, cluster, queue, resources,
  submission command, cost/concurrency effects, and expected products. Compare
  stable profile configuration with the current Run-specific probe evidence;
  defaults and stale probes are not current evidence.
- Look for evident waste, destructive behavior, output replacement, broad
  copies, path escape, hidden directory discovery, or changes made after
  preparation. Report the exact risk, affected object, and observed evidence.

`pass_with_warnings` is limited to findings that require no action or decision
before submission. A checksum establishes identity only; it is neither review
nor authorization.
