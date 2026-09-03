# PDF evidence strategy

Zo2Notes uses the least invasive source that can answer the reading question. Zotero remains the default text provider; the original local PDF is a targeted verification source, not the default full-document ingestion path.

## Routing order

1. Read Zotero highlights and child notes relevant to the question.
2. Read Zotero indexed full text when those notes are insufficient.
3. Check `indexedPages` against `totalPages` and inspect whether the relevant passage, formula, table, or caption is intelligible.
4. Access the original local PDF only when the indexed text is missing, corrupt, out of reading order, or lacks the spatial or visual evidence required by the question.
5. If no usable full text can be obtained, fall back to metadata and the original abstract without extrapolating body-text claims.

## Original PDF handling

- Resolve only the attachment belonging to the selected parent item. Do not scan Zotero storage or unrelated directories.
- Keep the PDF read-only and do not copy it into the project.
- Write extracted text, JSON, and screenshots only to a temporary directory unless the user explicitly requests another destination.
- Parse only the pages needed for the reading question whenever their page range is known.
- Do not expose the local attachment path in the research note or normal user-facing output.

## LiteParse modes

For a born-digital PDF with a usable text layer:

```bash
lit parse <pdf> --format json --no-ocr --target-pages "<pages>" -o /tmp/zo2notes-pdf.json
lit screenshot <pdf> --target-pages "<pages>" --dpi 150 -o /tmp/zo2notes-pages
```

Use structured JSON for bounding boxes and reading-order diagnosis. Use screenshots when the claim depends on a figure, dense table, equation layout, or other visual relation. Do not prefer layout-projected plain text over a complete, readable Zotero index for ordinary body-text reading.

For a scanned PDF or a missing, corrupt, or unusable text layer:

```bash
lit parse <pdf> --ocr-language eng --target-pages "<pages>" -o /tmp/zo2notes-ocr.txt
```

OCR is a fallback. It should not be enabled merely to reprocess a healthy text layer because it is slower and can degrade formulas, subscripts, symbols, and scientific notation. Increase DPI or use another OCR language only when the source requires it.

## Evidence labels

Use one or more of these `source_coverage` values in the note:

- `zotero-notes-highlights`
- `zotero-indexed-fulltext`
- `local-pdf-text-layer`
- `local-pdf-visual-check`
- `local-pdf-ocr`
- `metadata-abstract-only`

Record the page and evidence mode for any conclusion that depends on PDF-only verification. OCR-derived values, formulas, and symbols require visual confirmation before they are treated as decisive evidence.
