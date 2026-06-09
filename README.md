# D&D Campaign Template

A reusable GitHub repo + toolchain for running a D&D 5e campaign. Clone it, fill in the placeholders, and you have a working DM workspace with:

- A structured campaign guide (world, geography, factions, NPCs, party, session log)
- An AI agent configuration for session prep and adventure generation
- A library of installable **settings** (pre-built sourcebook reference bundles) + a `setup-campaign` skill
- A ReportLab PDF pipeline for printing session handouts
- A GitHub Actions workflow that auto-publishes the repo content to the repo's **GitHub Wiki**
- A GitHub Actions workflow that auto-transcribes session audio with WhisperX

Everything is plain **GitHub-flavoured Markdown** — no Obsidian, no plugins, no app to configure. You edit Markdown in the repo; the wiki and PDFs are generated from it.

---

## Getting started

1. **Clone this repo** (or use it as a GitHub template) into a local folder, then run `git lfs install` once — binary assets (audio, PDFs, images) are tracked with Git LFS (see [Git LFS](#git-lfs)).
2. **Choose a setting** (see [Choosing a setting](#choosing-a-setting)). Pick a pre-built one from `settings/` — e.g. the Forgotten Realms — or generate a custom homebrew world.
3. Fill in the placeholders in `campaign/` — start with `world.md`, then `party.md`.
4. Rename `[Campaign Name]` / `[Setting Name]` references in `Home.md`, `README.md`, and `AGENTS.md` to your actual campaign.
5. Add more sourcebook PDFs to `references/` and extract them as needed (see [Reference material](#reference-material)).
6. Enable the GitHub Wiki and run the sync once (see [GitHub Wiki](#github-wiki)).
7. Set the `HF_TOKEN` secret (and, for speaker detection + drafted session logs, the `ANTHROPIC_API_KEY` secret) in your GitHub repo settings to enable auto-transcription (see [Transcription workflow](#transcription-workflow)).

`AGENTS.md` holds the Campaign Keeper agent instructions; `CLAUDE.md` is a symlink to it so Claude Code picks it up automatically.

---

## Repository layout

```
<your-campaign>/
├── README.md                       # GitHub repo landing page
├── Home.md                         # wiki landing page + index
├── _Sidebar.md                     # wiki navigation sidebar
├── AGENTS.md                       # Campaign Keeper agent instructions
├── CLAUDE.md                       # symlink → AGENTS.md (read by Claude Code)
├── dnd-adventure-generator.md      # adventure generation workflow
├── .claude/
│   ├── settings.json               # Claude Code sandbox/permission config
│   └── skills/
│       └── setup-campaign/         # skill: choose/install a setting on first setup
├── .gitattributes                  # Git LFS rules for audio + PDFs
├── campaign/
│   ├── world.md                    # setting overview, tone, cosmology, history
│   ├── geography.md                # regions, cities, travel distances
│   ├── factions.md                 # organizations and their conflicts
│   ├── roster.md                   # NPCs and relationships
│   ├── party.md                    # current PCs, levels, backstories
│   └── session-log.md              # campaign-wide index + loose ends tracker
├── sessions/
│   └── session <N>/                # one folder per session
│       ├── <slug>-0-overview.md       # session landing page (wiki front door)
│       ├── <slug>-1-adventure.md
│       ├── <slug>-2-combat-tracker.md
│       ├── <slug>-3-player-handouts.md
│       ├── <slug>-4-dm-quick-ref.md
│       ├── images/
│       │   ├── images.json         # image manifest (url, aspect_ratio, file)
│       │   └── <slug>.jpg          # one git-tracked jpg per generated image
│       ├── <slug>.pdf              # built by scripts/build_pdf.py
│       └── session <N> - log.md   # post-session write-up
├── references/
│   └── <sourcebook>/               # populated when you install a setting
│       └── _raw/
│           ├── full.md             # full concatenated markdown
│           ├── pages/              # page-NNNN.md per page
│           └── images/             # extracted figures
├── settings/                       # library of installable settings
│   ├── README.md
│   └── <slug>/                     # e.g. forgotten-realms
│       ├── setting.md              # manifest: name, blurb, source notes
│       └── references/             # extracts copied into ./references on install
├── scripts/
│   ├── build_pdf.py                # CLI: build session PDF (+ standalone handouts)
│   ├── md_to_pdf.py                # markdown → ReportLab renderer
│   ├── build_wiki.py               # stage repo content as a GitHub-wiki tree
│   ├── obsidian_to_wiki.py         # one-shot Obsidian → GitHub markdown converter
│   ├── extract_pdf.py              # PDF → markdown extractor
│   ├── transcribe.sh               # WhisperX wrapper → formatted .md transcript
│   ├── detect_speakers.py          # map diarized speakers to player names
│   ├── format_transcript.py        # WhisperX JSON → readable markdown transcript
│   └── update_session_log.py       # transcript → drafted session log (Claude)
└── .github/workflows/
    ├── sync-wiki.yml               # publish repo content to the GitHub Wiki
    ├── transcribe.yml              # auto-transcribe audio on push
    └── test.yml                    # CI tests for transcribe.sh
```

---

## GitHub Wiki

The repo is the single source of truth; the repo's GitHub Wiki is generated from it automatically. On every push to `main` that touches wiki content, the `Sync Wiki` workflow (`.github/workflows/sync-wiki.yml`) runs `scripts/build_wiki.py` to stage a wiki-ready tree and pushes it into the repo's `*.wiki.git`. **You only ever edit this repo** — never the wiki directly.

`scripts/build_wiki.py` flattens every page to the wiki's flat filename namespace (GitHub Wikis key pages by basename, not path), rewrites internal links to bare page names, and rewrites links to `references/` or `.pdf` assets back to repo blob URLs (those stay in the main repo, not the wiki).

**One-time setup:** the wiki repo must exist before the Action can push to it. Enable **Settings → Features → Wikis**, then open the **Wiki** tab and click **Create the first page** once (any content). After that the sync runs on its own; you can also trigger it from **Actions → Sync Wiki → Run workflow**.

### Converting legacy Obsidian content

If you have content authored with Obsidian `[[wikilinks]]` or `[!type]` Admonition callouts, run the one-shot converter once to rewrite it to GitHub-flavoured Markdown (relative links + GitHub alerts):

```bash
python scripts/obsidian_to_wiki.py
```

It rewrites files under `campaign/` and `sessions/` in place and prints what changed. New content should already be authored as plain GitHub Markdown, so this is only needed for a one-time migration.

---

## Choosing a setting

A **setting** is the reusable world canon your campaign runs in — chiefly the sourcebook reference extracts the agent treats as published canon. The `settings/` directory is a library of pre-built settings you can install, separate from your specific campaign (party, NPCs, sessions) which lives in `campaign/`.

On first setup, pick one:

- **A pre-built setting** — e.g. the **Forgotten Realms**, which bundles markdown extracts of the *Forgotten Realms Campaign Guide* and *Player's Guide*. Installing it copies those extracts into the top-level `references/` so the agent has canonical lore to draw on.
- **A custom homebrew world** — generate one from scratch; the lore gets written straight into your `campaign/` guide.

The easiest way is the **`setup-campaign` skill**: run `/setup-campaign` (or ask the agent to "choose a setting" / "set up my campaign") and it lists the available settings, installs the one you pick, and leaves your campaign guide blank to fill in. You can also install a setting by hand — just copy `settings/<slug>/references/*` into `references/`. See [`settings/README.md`](settings/README.md) for the library layout and how to add your own setting.

---

## Reference material

Sourcebook PDFs live in `references/`. The agent searches extracted markdown rather than raw PDFs, so you need to run the extractor after adding any new PDF. (Pre-built settings ship their extracts under `settings/<slug>/references/` and install them here — see [Choosing a setting](#choosing-a-setting).)

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

3. Add the sourcebook to the **Source Hierarchy** section in `AGENTS.md` so the Campaign Keeper agent knows to consult it.

### Git LFS

Binary assets are tracked with [Git LFS](https://git-lfs.com) so large files don't bloat the repo. The committed `.gitattributes` routes session audio (`*.m4a`), PDFs (`*.pdf`), and images (`*.png`) through LFS — run `git lfs install` once per machine before adding them. To also track extracted sourcebook PDFs/PNGs under `references/`:

```bash
git lfs track "references/**/*.pdf"
git lfs track "references/**/*.png"
git add .gitattributes
```

Alternatively, list the PDFs in `.gitignore` — the markdown extracts are what the agent actually uses.

---

## Transcription workflow

Pushing any audio file to the repo triggers a GitHub Actions job that runs [WhisperX](https://github.com/m-bain/whisperX) (`large-v2`, speaker-diarized) and commits a formatted `.md` transcript alongside the audio file. When an `ANTHROPIC_API_KEY` is available, the pipeline also names the diarized speakers from a roll-call intro and drafts a session log from the transcript.

### Supported formats

`.m4a`, `.mp3`, `.wav`, `.webm`, `.flac`, `.ogg`

### Setup

1. Obtain a [Hugging Face](https://huggingface.co) token (free account). The diarization model requires accepting the terms for `pyannote/speaker-diarization`.
2. Add it as a repository secret: **Settings → Secrets and variables → Actions → New repository secret** — name it `HF_TOKEN`.
3. *(Optional but recommended)* Add an `ANTHROPIC_API_KEY` repository secret to enable Claude-powered speaker naming (`detect_speakers.py`) and session-log drafting (`update_session_log.py`). Without it, transcription still runs; those two steps are skipped.

### How it works

- On every push, the workflow diffs against the previous commit and transcribes only **new or modified** audio files.
- WhisperX diarizes the audio; `format_transcript.py` renders it to a readable markdown transcript saved as `<audio-file>.md` in the same directory. Machine transcripts (`*.m4a.md`) are intentionally **not** published to the wiki.
- If a `speakers.json`/`speakers.yaml` mapping sits next to the audio it's applied directly; otherwise `detect_speakers.py` tries to infer speaker names from a roll-call intro (requires `ANTHROPIC_API_KEY`), cross-referencing `campaign/party.md` and `campaign/roster.md`.
- With `ANTHROPIC_API_KEY` set, `update_session_log.py` drafts a session log from the transcript using the campaign guide for names and tone. Review it like any generated content — it's a draft, not canon.
- Transcripts are committed back to the branch with `[skip ci]` to avoid a loop.
- To backfill all audio files in the repo at once, trigger the workflow manually via **Actions → Transcribe audio → Run workflow** and check *Transcribe every audio file in the repo*.

### Running locally

`scripts/transcribe.sh` wraps WhisperX for local use. It creates and manages a `whisper-env` virtualenv automatically inside the `scripts/` directory and chains the speaker-detection, formatting, and session-log steps.

**Prerequisites:** [pyenv](https://github.com/pyenv/pyenv) with Python 3.11.9 installed, and `ffmpeg` on your PATH.

```bash
# Transcribe a recording; output defaults to <input>.md
./scripts/transcribe.sh sessions/session\ 3/recording.m4a

# Specify an explicit output path
./scripts/transcribe.sh recording.m4a transcripts/session3.md
```

Set `HF_TOKEN` in your environment or place your token in a file called `huggingface.token` inside the `scripts/` directory. Set `ANTHROPIC_API_KEY` in your environment to enable speaker naming and session-log drafting. Override the WhisperX model with `WHISPERX_MODEL` (defaults to `large-v2`).

---

## PDF pipeline

Each session folder produces a single paginated PDF from the four markdown deliverables. The renderer is pure Python — no LaTeX or Pandoc required. Any standalone `*-handout.md` files in the folder (in-fiction letters, props) are additionally built as their own PDFs.

### Session file naming

The slug is inferred from the filename. Name files consistently:

```
sessions/session 3/the-haunted-mill-1-adventure.md
sessions/session 3/the-haunted-mill-2-combat-tracker.md
sessions/session 3/the-haunted-mill-3-player-handouts.md
sessions/session 3/the-haunted-mill-4-dm-quick-ref.md
sessions/session 3/images/images.json
sessions/session 3/images/<slug>.jpg
```

`images/images.json` is a list of `{"url", "description", "aspect_ratio", "file"}` objects — one per image embedded in the markdown files. It lets the renderer size images correctly without re-fetching metadata at build time, and the `file` key points at a git-tracked local jpg so the PDF still builds after the image host URL expires.

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

## AI agent

`AGENTS.md` contains instructions for the **Campaign Keeper** agent — an AI assistant you attach to this repo (e.g. via Claude Code or a compatible agent client). `CLAUDE.md` is a symlink to it, so Claude Code picks up the same instructions automatically. It knows:

- The campaign's source hierarchy: campaign files take precedence over sourcebook extracts, which take precedence over general D&D knowledge
- Which files to read for world state, faction status, NPC roster, and party details
- How to stay canon-first and flag when it's adding DM-invented content
- Working conventions: stay on `main`, don't commit unless asked, and scope sessions to ~2 hours of table time

`dnd-adventure-generator.md` contains the multi-step workflow the agent follows to generate a new session adventure: scope → outline → images → markdown files → campaign guide → PDF.

### Claude Code on the web

`.claude/settings.json` configures the sandbox for [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web): it allowlists `api.anthropic.com` for the transcript/session-log scripts and permits `WebFetch`. Add your image-generation MCP host (and any other services your agent calls) to `sandbox.network.allowedDomains` as needed. Keep personal overrides in `.claude/settings.local.json`, which stays gitignored.

---

## Python version

The PDF pipeline and PDF extractor require Python 3.11.9 (pinned in `.python-version`). The transcription script also requires 3.11.9 via pyenv.

```bash
pyenv install 3.11.9
pip install reportlab mistune pymupdf4llm
```
