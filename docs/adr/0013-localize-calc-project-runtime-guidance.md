---
status: accepted
---

# Localize Calc Project runtime guidance in place

`calc-project` keeps one Chinese authoritative version of each runtime Markdown document: its `SKILL.md` files and skill-owned `references/` files, including the natural-language portions of RQ and Spec templates. RQ and Spec template section titles may be Chinese, but their field names, table-column names, placeholders, IDs, paths, and enumerated values remain stable English structure. Other machine-consumed strings—including skill IDs, domain-object identifiers, commands, configuration keys, software names, code blocks, scripts, script comments, and calculation-template comments—remain unchanged; canonical identifiers such as RQ, Spec, Task, Run, and COT receive Chinese explanations rather than Chinese replacements. Existing project records are outside this localization scope. Test scenarios remain English, while tests that assert localized narrative text are revised to preserve the behavioral contract instead of English wording.
