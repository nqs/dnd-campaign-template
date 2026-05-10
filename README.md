# D&D Campaign Template

A reusable Obsidian vault + toolchain for running a D&D 5e campaign. Clone it, fill in the placeholders, and you have a working DM workspace with:

- A structured campaign bible (world, geography, factions, NPCs, party, session log)
- An AI agent configuration for session prep and adventure generation
- A ReportLab PDF pipeline for printing session handouts
- A GitHub Actions workflow that auto-transcribes session audio with WhisperX
- A print stylesheet for parchment-themed exports from Obsidian

---

## Getting started

1. **Clone this repo** (or use it as a GitHub template) into a local folder.
2. Open the folder as an Obsidian vault: **Obsidian → Open folder as vault → select this directory**.
3. Fill in the placeholders in `campaign/` — start with `world.md`, then `party.md`.
4. Rename `[Campaign Name]` references in `home.md` to your actual campaign name.
5. Add sourcebook PDFs to `references/` and extract them (see [Reference material](#reference-material)).
6. Set the `HF_TOKEN` secret in your GitHub repo settings to enable auto-transcription (see [Transcription workflow](#transcription-workflow)).

---

## Vault layout

```
<your-campaign>/
├── home.md                         # vault index + Obsidian setup guide
├── agents.md                       # Campaign Keeper agent instructions
├── dnd-adventure-generator.md      # adventure generation workflow
├── campaign/
│   ├── world.md                    # setting overview, tone, cosmology, history
│   ├── geography.md                # regions, cities, travel distances
│   ├── factions.md                 # organizations and their conflicts
│   ├── roster.md                   # NPCs and relationships
│   ├── party.md                    # current PCs, levels, backstories
│   └── session-log.md              # campaign-wide index + loose ends tracker
├── sessions/
│   └── session <N>/                # one folder per session
│       ├── <slug>-1-adventure.md
│       ├── <slug>-2-combat-tracker.md
│       ├── <slug>-3-player-handouts.md
│       ├── <slug>-4-dm-quick-ref.md   # optional
│       ├── images.json
│       ├── <slug>.pdf              # built by scripts/build_pdf.py
│       └── session <N> - log.md   # post-session write-up
├── references/
│   └── <sourcebook>/
│       └── _raw/
│           ├── full.md             # full concatenated markdown
│           ├── pages/              # page-NNNN.md per page
│           └── images/             # extracted figures
├── scripts/
│   ├── build_pdf.py                # CLI: build session PDF
│   ├── md_to_pdf.py                # markdown → ReportLab renderer
│   └── extract_pdf.py              # PDF → markdown extractor
├── transcribe.sh                   # local WhisperX wrapper
└── .github/workflows/
    ├── transcribe.yml              # auto-transcribe audio on push
    └── test.yml                    # CI tests for transcribe.sh
```

---

## Reference material

Sourcebook PDFs live in `references/`. The agent searches extracted markdown rather than raw PDFs, so you need to run the extractor after adding any new PDF.

### Adding a sourcebook

1. Copy the PDF into `references/`:
   ```
   references/my-sourcebook.pdf
   ```

2. Extract it to markdown:
   ```bash
   python scripts/extract_pdf.py references/my-sourcebook.pdf references/my-sourcebook/_raw
   ```

   This writes:
   - `references/my-sourcebook/_raw/full.md` — full concatenated text
   - `references/my-sourcebook/_raw/pages/page-NNNN.md` — one file per page (for page-accurate citations)
   - `references/my-sourcebook/_raw/images/` — extracted figures and maps

3. Add the sourcebook to the **Source Hierarchy** section in `agents.md` so the Campaign Keeper agent knows to consult it.

### Git LFS

Large PDFs and extracted PNGs should be tracked with Git LFS rather than committed as regular objects:

```bash
git lfs track "references/**/*.pdf"
git lfs track "references/**/*.png"
git add .gitattributes
```

Alternatively, list the PDFs in `.gitignore` — the markdown extracts are what the agent actually uses.

---

## Transcription workflow

Pushing any audio file to the repo triggers a GitHub Actions job that runs [WhisperX](https://github.com/m-bain/whisperX) (speaker-diarized transcription) and commits the resulting `.txt` transcript alongside the audio file.

### Supported formats

`.m4a`, `.mp3`, `.wav`, `.webm`, `.flac`, `.ogg`

### Setup

1. Obtain a [Hugging Face](https://huggingface.co) token (free account). The diarization model requires accepting the terms for `pyannote/speaker-diarization`.
2. Add it as a repository secret: **Settings → Secrets and variables → Actions → New repository secret** — name it `HF_TOKEN`.

### How it works

- On every push, the workflow diffs against the previous commit and transcribes only **new or modified** audio files.
- Each transcript is saved as `<audio-file>.txt` in the same directory.
- Transcripts are committed back to the branch with `[skip ci]` to avoid a loop.
- To backfill all audio files in the repo at once, trigger the workflow manually via **Actions → Transcribe audio → Run workflow** and check *Transcribe every audio file in the repo*.

### Running locally

`transcribe.sh` wraps WhisperX for local use. It creates and manages a `whisper-env` virtualenv automatically.

**Prerequisites:** [pyenv](https://github.com/pyenv/pyenv) with Python 3.11.9 installed, and `ffmpeg` on your PATH.

```bash
# Transcribe a recording; output defaults to <input>.txt
./transcribe.sh sessions/session\ 3/recording.m4a

# Specify an explicit output path
./transcribe.sh recording.m4a transcripts/session3.txt
```

Set `HF_TOKEN` in your environment or place your token in a file called `huggingface.token` in the repo root.

---

## PDF pipeline

Each session folder produces a single paginated PDF from three (or four) markdown files. The renderer is pure Python — no LaTeX or Pandoc required.

### Session file naming

The slug is inferred from the filename. Name files consistently:

```
sessions/session 3/the-haunted-mill-1-adventure.md
sessions/session 3/the-haunted-mill-2-combat-tracker.md
sessions/session 3/the-haunted-mill-3-player-handouts.md
sessions/session 3/the-haunted-mill-4-dm-quick-ref.md   # optional
sessions/session 3/images.json
```

`images.json` is a list of `{"url", "description", "aspect_ratio"}` objects — one per image embedded in the markdown files. It lets the renderer size images correctly without re-fetching metadata at build time.

### Building a PDF

```bash
# Install dependencies once
pip install reportlab mistune pymupdf4llm

# Latest session (auto-detected)
python scripts/build_pdf.py

# Specific session number
python scripts/build_pdf.py 3

# Full path
python scripts/build_pdf.py "sessions/session 3"

# Override title or output path
python scripts/build_pdf.py 3 --title "The Haunted Mill" --out /tmp/preview.pdf
```

Output is written to `sessions/session <N>/<slug>.pdf`.

### Stat blocks

Stat blocks are authored as plain markdown tables and bolded prose in the combat-tracker file — no Fantasy Statblocks plugin required. The renderer handles them natively and the PDF pipeline reads the raw markdown directly.

```markdown
**Guard Captain** · Medium humanoid · CR 1
**AC** 16 · **HP** 27 (5d8+5) · **Speed** 30 ft.

| STR | DEX | CON | INT | WIS | CHA |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 15 (+2) | 12 (+1) | 12 (+1) | 10 (+0) | 11 (+0) | 11 (+0) |

**Actions** *Longsword* — +4 to hit, 1d8+2 slashing.
```

---

## Obsidian setup

Open this folder as a vault in Obsidian, then install the community plugins below. Their IDs are already listed in `.obsidian/community-plugins.json`, so Obsidian will prompt you to install them. You'll need to **turn off Restricted Mode** first (Settings → Community plugins → Turn on community plugins).

### Plugins

| Plugin | ID | Purpose |
|---|---|---|
| **Admonition** | `obsidian-admonition` | `[!dm]`, `[!read-aloud]`, `[!cite]` callout boxes |
| **Style Settings** | `obsidian-style-settings` | UI controls for theme/snippet tweaks |
| **Dice Roller** | `obsidian-dice-roller` | Inline clickable dice — `` `dice: 2d6+3` `` |
| **Leaflet** | `obsidian-leaflet-plugin` | Interactive pinned maps from image files |
| **Better Export PDF** | `better-export-pdf` | Header/footer templates, page numbers, H1 page breaks |
| **Pandoc Plugin** | `obsidian-pandoc` | Export to PDF/DOCX/EPUB via Pandoc (needs Pandoc installed) |

### Print stylesheet

`.obsidian/snippets/dnd-print.css` applies automatically under `@media print` and inside Better Export PDF:

- Parchment background and dark-brown body text
- Serif headings in deep red (`#58180d`)
- Page break before each `# H1`
- Themed callouts for `[!dm]` and `[!read-aloud]`

To disable it: **Settings → Appearance → CSS snippets → dnd-print → toggle off**.

---

## AI agent

`agents.md` contains instructions for the **Campaign Keeper** agent — an AI assistant you attach to this repo (e.g. via Claude Code or a compatible agent client). It knows:

- The campaign's source hierarchy: campaign files take precedence over sourcebook extracts, which take precedence over general D&D knowledge
- Which files to read for world state, faction status, NPC roster, and party details
- How to stay canon-first and flag when it's adding DM-invented content

`dnd-adventure-generator.md` contains the multi-step workflow the agent follows to generate a new session adventure: scope → outline → images → markdown files → session bible → PDF.

---

## Python version

The PDF pipeline and PDF extractor require Python 3.11.9 (pinned in `.python-version`). The transcription script also requires 3.11.9 via pyenv.

```bash
pyenv install 3.11.9
pip install reportlab mistune pymupdf4llm
```
