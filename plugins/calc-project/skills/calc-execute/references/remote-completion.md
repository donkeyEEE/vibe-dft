# Remote completion evidence

Read this reference when a submitted Run may have completed and before planning a pull.

Inspect only the selected Run and correlate all of these signals:

- scheduler state or accounting evidence for the recorded job ID;
- the backend's expected output files;
- output and log modification times relative to submission and job timing;
- short, targeted completion or failure excerpts from the declared logs.

Queue disappearance alone is not completion evidence. A missing scheduler record is a limitation to report, then cross-check expected outputs, timestamps, and targeted log evidence. Conflicting, stale, or incomplete signals keep the Run active or route it for diagnosis; they do not justify acceptance.

Keep HDF5, `CHGCAR`, and `WAVECAR` on the server. After completion evidence is coherent, read [reviewed synchronization](sync.md), create the exact pull plan, obtain review for that plan, and consume only its saved file list.
