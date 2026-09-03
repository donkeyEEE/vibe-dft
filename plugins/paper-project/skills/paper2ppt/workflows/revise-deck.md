# Revision routing

Route a revision by what the user wants to change:

- If the paper interpretation, central message, emphasis, terminology, figure
  selection, or source evidence changes, return to paper2ppt. Reconfirm the
  affected outline or visual intent, build a new empty handoff directory, and
  invoke `$ppt-master` again.
- If page count, slide order, template, layout, SVG, wording on slides, speaker
  notes, QA, or PPTX output changes, continue directly with PPT Master.
- If a request spans both sides, paper2ppt first republishes the source
  material; PPT Master then revises its independently owned project.

There is no automated merge protocol between the two plugins. Never edit the
old handoff in place and never make paper2ppt depend on PPT Master's workspace.
