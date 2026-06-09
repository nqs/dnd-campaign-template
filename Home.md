# [Campaign Name] — D&D 5e

The DM's knowledge base for an ongoing D&D 5e campaign set in **[Setting / Region]**. This wiki holds the campaign guide, per-session deliverables, and the operating docs that drive content generation.

## Campaign Guide

- [world](campaign/world.md) — setting overview, cosmology, timeline, tone
- [geography](campaign/geography.md) — regions, cities, travel distances, climate
- [factions](campaign/factions.md) — organizations, their goals, their conflicts
- [roster](campaign/roster.md) — NPCs and relationships
- [party](campaign/party.md) — current PCs, levels, classes, backstories, goals
- [session-log](campaign/session-log.md) — what's happened so far, loose ends, foreshadowing

## Sessions

Each session has a **landing page** — a short summary plus links to the adventure, its images, and its other assets.

- *(add session landing pages here as you run them)*
- Example: `[Session 001 — The Opening Hook](sessions/session%201/the-opening-hook-0-overview.md)`

## Reference Material

The agent treats your installed **setting** (sourcebook reference extracts under `references/`) as published canon. Pick a pre-built setting from the `settings/` library or generate a custom one — the easiest path is the `setup-campaign` skill (`/setup-campaign`). To add a sourcebook by hand, run `scripts/extract_pdf.py`:

```
python scripts/extract_pdf.py references/my-sourcebook.pdf references/my-sourcebook/_raw
```

This produces `references/<sourcebook>/_raw/full.md`, per-page files under `_raw/pages/page-NNNN.md`, and extracted figures under `_raw/images/` — the layout `AGENTS.md` expects. Grep these for a city/faction/NPC name to pull canon.

## DM Operating Doc

- [Campaign Keeper instructions](AGENTS.md) — source hierarchy, canon-first rules, generator handoff
- [Adventure Generator workflow](dnd-adventure-generator.md) — scope → outline → images → markdown → guide → PDF

---

# GitHub Wiki Setup

This content is authored as **GitHub-flavoured Markdown** so it renders cleanly both when browsing the repo and when published as a GitHub Wiki. There are no plugins to install and no app to configure.

**You only ever edit this repo.** The repo's GitHub Wiki is generated automatically from these files by the `Sync Wiki` GitHub Action (`.github/workflows/sync-wiki.yml`): on every push to `main` it runs `scripts/build_wiki.py` to stage a wiki-ready tree (extensionless page links, `session N` → `session-N`, references/PDFs linked back to the repo) and pushes it into the repo's `*.wiki.git`. No second repo to maintain by hand.

> [!IMPORTANT]
> **One-time setup:** the wiki repo must exist before the Action can push to it. Enable **Settings → Features → Wikis**, then open the **Wiki** tab and click **Create the first page** once (any content). After that the sync runs on its own. You can also trigger it manually from the **Actions → Sync Wiki → Run workflow** button.

## Layout

```
<your-campaign>/
├── README.md                     # GitHub repo landing page
├── Home.md                       # this file — wiki landing page + index
├── _Sidebar.md                   # wiki navigation sidebar
├── AGENTS.md                     # Campaign Keeper agent instructions (CLAUDE.md -> AGENTS.md)
├── dnd-adventure-generator.md    # Generation workflow (scope → outline → images → markdown → guide → PDF)
├── .claude/                      # Claude Code config + the setup-campaign skill
├── campaign/                     # campaign-guide canon
│   ├── world.md                  # setting overview
│   ├── geography.md              # regions, cities, travel
│   ├── factions.md               # organizations and their conflicts
│   ├── roster.md                 # NPCs and relationships
│   ├── party.md                  # current PCs
│   └── session-log.md            # campaign-wide session index + loose ends
├── sessions/                     # per-session deliverables
│   └── session <N>/              # landing page / adventure / combat-tracker / handouts / quick-ref / images / pdf
├── settings/                     # installable setting library (reference bundles)
└── references/                   # markdown extracts of the installed setting's sourcebooks
    └── <sourcebook>/
        └── _raw/                 # full.md, pages/, images/ (output of extract_pdf.py)
```

## Linking between pages

Pages link to one another with **standard relative Markdown links** — e.g. `[roster](campaign/roster.md)` — rather than Obsidian `[[wikilinks]]`. Relative links resolve correctly in the repo file browser, in pull-request diffs, and in the rendered GitHub Wiki. Spaces in session-folder paths are URL-encoded as `%20`.

> [!NOTE]
> If you publish these pages to the repo's actual GitHub Wiki (the separate `*.wiki.git`), GitHub also supports `[[Page Title]]` wikilink syntax there. The relative-link form used here was chosen because it works everywhere, including normal repo browsing.

## Callouts

Use **GitHub alerts** with a bold label that names the callout's purpose. The campaign content uses these conventions (the `scripts/obsidian_to_wiki.py` converter maps the old Obsidian/Admonition types to them):

| Purpose | GitHub alert | Bold label |
|---|---|---|
| DM-only note | `[!IMPORTANT]` | **DM:** |
| Adventure hook | `[!TIP]` | **Hook:** |
| Flag / warning | `[!WARNING]` | **Flag:** |
| Source citation | `[!NOTE]` | **Source:** |
| Read-aloud text | `[!NOTE]` | **Read-aloud:** |
| Lore aside | `[!NOTE]` | **Lore:** |

Example:

```markdown
> [!IMPORTANT]
> **DM:** The innkeeper knows more than she's letting on.
```

GitHub renders the five alert keywords (`NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`) with a coloured icon and rule.

## Stat blocks

Stat blocks are authored as plain Markdown tables and bolded prose inside each session's combat-tracker file — no Fantasy Statblocks / Initiative Tracker dependency. The ReportLab PDF pipeline (`scripts/build_pdf.py`) reads this Markdown directly.

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

## Printing & Export

PDFs are built from the Markdown with the repo's ReportLab script:

```
.venv/bin/python scripts/build_pdf.py [<session-number-or-folder>]
```

With no argument it builds the latest session; pass `3` or `"sessions/session 3"` to target a specific one. Final output lands at `sessions/session <N>/<adventure-slug>.pdf`. See `dnd-adventure-generator.md` for the full PDF specification.
