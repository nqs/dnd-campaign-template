# [Campaign Name] — DM Vault

The DM's vault for an ongoing D&D 5e campaign set in **[Setting / Region]**.

## Campaign Bible

- [[world]] — setting overview, cosmology, timeline, tone
- [[geography]] — regions, cities, travel distances, climate
- [[factions]] — organizations, their goals, their conflicts
- [[roster]] — NPCs and relationships
- [[party]] — current PCs, levels, classes, backstories, goals
- [[session-log]] — what's happened so far, loose ends, foreshadowing

## Sessions

- *(add session links here as you run them)*
- Example: `[[sessions/session 1/the-opening-hook-1-adventure|Session 001 — The Opening Hook]]`

## Reference Material

PDFs live in `references/`. Run `scripts/extract_pdf.py` to extract a PDF to markdown:

```
python scripts/extract_pdf.py references/my-sourcebook.pdf references/my-sourcebook/_raw
```

This produces `_raw/full.md`, `_raw/pages/page-NNNN.md`, and `_raw/images/` — the layout `AGENTS.md` expects.

## DM Operating Doc

- [[AGENTS|Campaign Keeper instructions]] — source hierarchy, canon-first rules, generator handoff
- [[dnd-adventure-generator|Adventure Generator workflow]] — scope → outline → images → markdown → bible → PDF

---

# Obsidian Setup

Open this folder as a vault (**Obsidian → Open folder as vault → select this directory**), then install the plugins below from **Settings → Community plugins → Browse**. Their IDs are already listed in `.obsidian/community-plugins.json`, so once you click *Install* and *Enable* for each, the vault picks them up automatically.

You'll need to **turn off Restricted Mode** the first time (Settings → Community plugins → Turn on community plugins).

## Vault layout

```
<your-campaign>/
├── home.md                       # this file — vault index + Obsidian setup
├── AGENTS.md                     # Campaign Keeper agent instructions (CLAUDE.md symlinks here)
├── dnd-adventure-generator.md    # Generation workflow (scope → outline → images → markdown → bible → PDF)
├── campaign/                     # campaign-bible canon
│   ├── world.md                  # setting overview
│   ├── geography.md              # regions, cities, travel
│   ├── factions.md               # organizations and their conflicts
│   ├── roster.md                 # NPCs and relationships
│   ├── party.md                  # current PCs
│   └── session-log.md            # campaign-wide session index + loose ends
├── sessions/                     # per-session deliverables (root-level)
│   └── session <N>/              # adventure / combat-tracker / handouts / images.json / pdf
└── references/                   # sourcebook PDFs and their markdown extracts
    └── <sourcebook>/
        └── _raw/                 # full.md, pages/, images/ (output of extract_pdf.py)
```

Wikilinks like `[[roster]]` resolve regardless of folder, so bullets here work whether the target is at root or under `campaign/`. Path-prefixed wikilinks (e.g. `[[sessions/session 1/...]]`) point at the root-level `sessions/` tree.

## Formatting

Stat blocks in this vault are authored as plain markdown tables and bolded prose inside each session's combat-tracker file. Fantasy Statblocks / Initiative Tracker are intentionally **not** used — the ReportLab PDF pipeline reads markdown directly.

| Plugin | ID | What it does |
|---|---|---|
| **Admonition** | `obsidian-admonition` | Callout boxes for *DM Notes*, *Read-Aloud*, *Secrets*, *Rules*. Provides a sidebar to define custom callout types and icons. |
| **Dice Roller** | `obsidian-dice-roller` | Inline clickable dice — `` `dice: 2d6+3` `` or `` `dice: 1d20` `` becomes a roll button you can use at the table. |
| **Leaflet** | `obsidian-leaflet-plugin` | Interactive maps. Drop a map image into a `\`\`\`leaflet` block and pin locations that link back to notes. |
| **Style Settings** | `obsidian-style-settings` | Exposes UI controls for any theme/snippet that opts in. Useful for tweaking the print snippet without editing CSS. |

## Printing & Export

| Plugin | ID | What it does |
|---|---|---|
| **Better Export PDF** | `better-export-pdf` | Drop-in replacement for Obsidian's built-in PDF export with header/footer templates, page numbers, table of contents, and proper page breaks before H1. Use this for player handouts. |
| **Pandoc Plugin** | `obsidian-pandoc` | Export notes to PDF / DOCX / EPUB / LaTeX via Pandoc. Better for long-form (a full adventure write-up) than Better Export PDF. Requires Pandoc installed locally; on macOS: `brew install pandoc basictex`. |

## Print stylesheet

`.obsidian/snippets/dnd-print.css` is enabled in `appearance.json`. It activates under `@media print` (and inside Better Export PDF), giving printed/exported notes:

- Parchment background (`#f5ecd7`) and dark-brown body text
- Bookman / Palatino serif body, Trajan-style headings in `#58180d` red
- Page break before each `# H1` so each top-level section starts on a new page
- Avoid-break rules on stat blocks, callouts, tables, code blocks
- Themed callouts for `[!dm]` and `[!read-aloud]`
- Hides Obsidian UI chrome that shouldn't print

If you don't like it, disable it in **Settings → Appearance → CSS snippets**.

## Quick reference: useful syntax

### Stat block (markdown table — vault convention)

```markdown
**Guard Captain** · Medium humanoid · CR 1
**AC** 16 · **HP** 27 (5d8+5) · **Speed** 30 ft.

| STR | DEX | CON | INT | WIS | CHA |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 15 (+2) | 12 (+1) | 12 (+1) | 10 (+0) | 11 (+0) | 11 (+0) |

**Saves** Str +4, Con +3 · **Senses** passive Perception 10
**Actions** *Longsword* — Melee, +4 to hit, reach 5 ft., 1d8+2 slashing.
```

See any session's combat tracker (`sessions/session <N>/<slug>-2-combat-tracker.md`) for live examples.

### DM callout (Admonition)

```markdown
> [!dm] DM Note
> The innkeeper knows more than she's letting on.
```

### Read-aloud callout

```markdown
> [!read-aloud]
> The road narrows. Torchlight flickers ahead where the forest presses close on both sides.
```

### Inline dice

```markdown
The bandit strikes for `dice: 1d6+2` piercing damage.
```

## Recommended workflow for adventure printing

1. Draft the session note in Markdown (stat-block tables, read-aloud callouts, dice).
2. Preview in Obsidian's Reading View — confirm formatting and that no stat-block table or callout straddles a page boundary.
3. Export with **Better Export PDF** (single note) or **Pandoc** (chained notes, e.g. session + relevant NPCs).
4. The print snippet handles the parchment/serif treatment automatically.
