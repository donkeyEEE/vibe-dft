# Calculation Template Acceptance

- calc-project source revision: `5676de321777c90474b6efb69893311e157cd889`
- Owner: `calc-project`
- Scope: the fourteen formal `*.template` assets registered in
  `templates/INDEX.md`

The migrated templates passed their preparation, handoff, and immutable-input
boundary assertions with:

```bash
pytest -q tests/test_calculation_templates.py -k 'pbs_templates or magnetic_templates'
```

The same behavioral contracts originate from calc-project
`tests/test_pbs_input_layout.py` and `tests/test_magnetic_workflow.py`. After
consumer cutover, those full regression tests read this external template root.

