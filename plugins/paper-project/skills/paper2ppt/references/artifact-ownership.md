# Material handoff ownership

Paper2ppt owns only the content of `paper2ppt_handoff/`:

| Artifact | Paper2ppt responsibility |
|---|---|
| `brief.md` | Academic emphasis, audience, constraints, and selected-image provenance |
| `paper.md` | UTF-8 normalized paper text produced through `paper-project:liteparse` |
| `original/` | Byte-preserved user source files |
| `images/` | Optional, confirmed figure crops with preserved scientific context |

The handoff is immutable once published. It contains no rendering contract or
derived presentation artifact. After invocation, PPT Master owns its own
workspace, page count, template, layout, SVG, speaker notes, QA, and PPTX.
Neither skill writes inside the other skill's source tree.
