# References

This directory holds sourcebook PDFs and their markdown extracts.

## Adding a sourcebook

1. **Place the PDF here:**
   ```
   references/my-sourcebook.pdf
   ```

2. **Extract it to markdown** using the included script:
   ```bash
   python scripts/extract_pdf.py references/my-sourcebook.pdf references/my-sourcebook/_raw
   ```
   This writes:
   - `references/my-sourcebook/_raw/full.md` — single concatenated markdown
   - `references/my-sourcebook/_raw/pages/page-NNNN.md` — one file per page
   - `references/my-sourcebook/_raw/images/` — extracted figures and maps

3. **Update `AGENTS.md`** — add the sourcebook to the Source Hierarchy section so the agent knows to consult it.

## Layout convention

```
references/
└── <sourcebook-slug>/
    └── _raw/
        ├── full.md
        ├── pages/
        │   ├── page-0001.md
        │   └── page-0002.md
        └── images/
            └── *.png
```

The agent searches by grepping `full.md` or the per-page files for location/faction/NPC names. The per-page files make it easy to cite a specific page number when referencing canon.

## Git LFS

Large PDFs and PNG extracts should be tracked with Git LFS rather than committed as regular files. Run:

```bash
git lfs track "references/**/*.pdf"
git lfs track "references/**/*.png"
git add .gitattributes
```

The PDFs themselves can also be listed in `.gitignore` if you prefer not to commit them at all — the markdown extracts are the working source the agent uses.
