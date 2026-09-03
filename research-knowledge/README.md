# Research Knowledge

This repository is the live, plugin-level content source shared by research
writing and calculation workflows. It is an independent Git repository, not an
installable Codex plugin.

Formal cards live under `cards/`; accepted reusable calculation templates live
under `templates/`. Work in progress lives under `candidates/` and is never a
consumer input. `paper-project` owns Cangjie and `prl-shared` governance;
`calc-project` owns the semantic and executable acceptance of calculation
templates.

Consumers must follow [CONSUMER_CONTRACT.md](CONSUMER_CONTRACT.md). Formal
content may be read from an uncommitted working tree, while each consuming
project remains responsible for recording a Git revision when reproducibility
requires it.

