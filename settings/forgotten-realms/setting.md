---
name: Forgotten Realms
slug: forgotten-realms
system: D&D 5e
edition_baseline: 4e sourcebooks (post-Spellplague, ~1479 DR)
suggested_start: Shadowdale, The Dalelands
references:
  - campaign-guide
  - players-guide
tags:
  - setting
  - forgotten-realms
---

# Forgotten Realms

The default high-fantasy setting of Dungeons & Dragons: Faerûn and the wider world of
Toril — a sprawling continent of free cities, fallen empires, scheming factions, and a
deep, well-documented pantheon. Sword-and-sorcery adventure with room for political
intrigue, dungeon delving, and planar weirdness.

A natural starting region is **Shadowdale** in **The Dalelands** — a small, unwalled
village beneath the granite dome of Old Skull, caught between the elf-realm of Myth
Drannor, the merchant empire of Sembia, and the looming shadow of Netheril. It gives a
party a quiet home base with real threats (drow in the tunnels below, fey politics in
the woods) close at hand.

## What this setting installs

Selecting this setting copies its bundled sourcebook extracts into the vault's
`references/` directory:

- **`references/campaign-guide/`** — markdown extract of the *Forgotten Realms Campaign
  Guide* (DM-facing: region overviews, political structures, dungeon locations, monster
  lore, adventure hooks, native NPC stat blocks).
- **`references/players-guide/`** — markdown extract of the *Forgotten Realms Player's
  Guide* (player-facing: cosmology, major cities, factions, races, deities, background
  flavor).

Each guide follows the standard layout: `_raw/full.md`, `_raw/pages/page-NNNN.md`, and
`_raw/images/`. The agent searches the markdown extracts; the original PDFs are not
included.

## What this setting does NOT install

The campaign bible (`campaign/world.md`, `geography.md`, `factions.md`, `roster.md`,
`party.md`, `session-log.md`) stays as the blank template. This setting provides the
**reference canon** for the Realms — you (or the custom-setting generator) still write
your own campaign's specifics on top of it. That keeps the Realms reusable: two
different campaigns can both pull from these guides without inheriting each other's
party, NPCs, or plot.

## Source notes

Both extracts are drawn from the 4th-edition *Forgotten Realms Campaign Guide* and
*Forgotten Realms Player's Guide* (Wizards of the Coast). Their baseline is the
post-Spellplague era, roughly **1479 DR**. If your campaign uses a different year or
edition's assumptions (e.g., Mystra restored, the Sundering, 5e's 1490s DR baseline),
override the affected canon in your `campaign/` files — those always win over the
references per the Source Hierarchy in `AGENTS.md`.
