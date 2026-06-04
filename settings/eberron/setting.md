---
name: Eberron
slug: eberron
system: D&D 5e
edition_baseline: 4e Eberron Campaign Guide (post-Last War, 998 YK)
suggested_start: Sharn, City of Towers
references:
  - campaign-guide
tags:
  - setting
  - eberron
---

# Eberron

A world where magic is industry and the dust has only just settled on a continent-wide
war. **Khorvaire** spent a century tearing itself apart in the **Last War**; the
**Treaty of Thronehold** (998 YK) froze that conflict into an uneasy peace between the
surviving nations, but none of the old grievances died with it. Arcane magic runs the
world like technology — lightning rails cross the land, elemental airships ply the sky,
and the **dragonmarked houses** wield economic power that rivals any crown. The tone is
pulp-noir intrigue and grit: cold-war espionage, ancient ruins, and morally grey
adventure rather than clean good-versus-evil.

A natural starting region is **Sharn, the City of Towers** — a vast vertical metropolis
of soaring spires, skybridges, and undercity warrens in the nation of Breland. Every
dragonmarked house, faith, and foreign power keeps agents there, and its districts range
from gleaming towers to the lawless depths of the Cogs, giving a party intrigue, urban
adventure, and easy hooks out into the wider continent.

## What this setting installs

Selecting this setting copies its bundled sourcebook extract into the vault's
`references/` directory:

- **`references/campaign-guide/`** — markdown extract of the *Eberron Campaign Guide*
  (DM-facing: the nations of Khorvaire, Sharn and other key locations, the Mournland,
  the dragonmarked houses, factions, native monster lore, adventure hooks, and NPC stat
  blocks).

The guide follows the standard layout: `_raw/full.md`, `_raw/pages/page-NNNN.md`, and
`_raw/images/`. The agent searches the markdown extract; the original PDF is not
included.

## What this setting does NOT install

The campaign bible (`campaign/world.md`, `geography.md`, `factions.md`, `roster.md`,
`party.md`, `session-log.md`) stays as the blank template. This setting provides the
**reference canon** for Eberron — you (or the custom-setting generator) still write your
own campaign's specifics on top of it. That keeps the setting reusable: two different
campaigns can both pull from the guide without inheriting each other's party, NPCs, or
plot.

## Source notes

The extract is drawn from the 4th-edition *Eberron Campaign Guide* (Wizards of the
Coast). Its baseline is the post-Last War era, **998 YK**, just after the Treaty of
Thronehold. If your campaign uses a different year or edition's assumptions (e.g. 5e's
*Eberron: Rising from the Last War*), override the affected canon in your `campaign/`
files — those always win over the references per the Source Hierarchy in `AGENTS.md`.

The source PDF is a scanned book, so the extracted text comes from its OCR layer and
contains scattered OCR artifacts (garbled punctuation, occasional split or mangled
words). Major proper nouns — Khorvaire, Sharn, the Mournland, the dragonmarked houses —
remain searchable, but grep with partial terms and read the surrounding lines when a
name looks mistranscribed. Cite the page filename (`_raw/pages/page-NNNN.md`) so the DM
can cross-check the original.
