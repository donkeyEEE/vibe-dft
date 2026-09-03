# Toolchain policy

Use the sibling `paper-project:liteparse` skill for document normalization.
Use PyMuPDF and Pillow only for evidence-preserving figure preparation through
`scripts/figure_assets.py`. Use `scripts/build_material_handoff.py` to validate
and atomically publish the minimal material directory.

Then invoke the bundled sibling `$ppt-master`. Paper2ppt has no renderer,
preview server, slide composer, template library, or PPTX audit stack. Do not
install dependencies unless an in-scope preparation command fails because a
declared requirement is unavailable and installation is allowed.
