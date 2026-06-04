---
name: setup-campaign
description: First-time campaign setup for this D&D vault — choose a pre-built setting from the settings/ library (e.g. Forgotten Realms) and install its reference material, or generate a custom homebrew setting. Use when the user is setting up the vault for the first time, says "set up my campaign", "choose a setting", "pick a setting", "start a new campaign", or asks which settings are available.
---

# Setup Campaign

Run the one-time setup that gives a fresh clone of this template a **setting**: either a
pre-built one from `settings/` (whose reference material is installed into the vault) or
a custom homebrew world (whose lore you write directly into `campaign/`).

A *setting* is reusable world canon — chiefly the sourcebook reference extracts the agent
treats as published canon. It is **not** a campaign: it carries no party, NPC roster, or
session history. Those stay in `campaign/` for the user to fill in per playthrough.

## When to use

- The user is setting up a freshly cloned template and needs to pick a world.
- The user asks "what settings are available?", "choose/pick a setting", "set up my
  campaign", or "start a new campaign".
- Invoked explicitly via `/setup-campaign`.

## Procedure

### 1. Discover available settings

List the candidate settings by reading every `settings/*/setting.md` manifest. From each
manifest's YAML frontmatter, collect `name`, `slug`, `system`, and `references`, plus the
one-paragraph blurb beneath the heading. Do **not** hard-code the list — always scan, so
settings added later are picked up automatically.

### 2. Check current vault state

Before offering choices, look at what's already installed so you can warn before
clobbering anything:

- Does top-level `references/` already contain installed guides (anything beyond its
  `README.md`)?
- Are the `campaign/` bible files still the blank template (placeholders in
  `[square brackets]`), or has the user already written real content?

If a setting already looks installed, surface that and confirm before overwriting.

### 3. Offer the choice

Use the `AskUserQuestion` tool. Present each discovered setting as an option (label =
name, description = blurb + what it installs), plus a final option:

- **Generate a custom setting** — build a homebrew world from scratch.

### 4a. Install a pre-built setting

When the user picks a setting with slug `<slug>`:

1. Re-read `settings/<slug>/setting.md` for the exact `references` list and any seed
   guidance.
2. Copy each bundled reference guide into the vault's top-level `references/`:
   ```bash
   cp -r "settings/<slug>/references/<guide>" "references/<guide>"
   ```
   Copy every guide listed in the manifest's `references:` array. Preserve the
   `<guide>/_raw/{full.md,pages/,images/}` layout — the agent reads canon from those
   exact paths (per `AGENTS.md` → *Source Hierarchy*). These extracts can be large
   (hundreds of files / 100s of MB); that is expected.
3. Do **not** touch the `campaign/` bible — a pre-built setting installs reference canon
   only. The user writes their own world/party/sessions on top of it.
4. Optionally offer to seed `campaign/world.md`'s **Setting Name** line with the
   setting's name (and `suggested_start` region, if the manifest has one). Only edit if
   the user agrees and the file is still a blank template.
5. Report what was installed (which guides, file/byte counts) and point the user at the
   next steps: fill in `campaign/world.md` and `campaign/party.md`, then read `AGENTS.md`.

### 4b. Generate a custom setting

When the user chooses a custom homebrew world, do **not** install bundled references.
Instead, interview the user and write their answers into the `campaign/` bible, following
the canon conventions in `AGENTS.md` (Source Hierarchy, "Canon First, Invention Second",
and never silently overwriting). Work the template files in this order, asking only for
what you can't reasonably infer:

1. `campaign/world.md` — setting name, elevator pitch, tone/genre, the big premise,
   cosmology (planes, pantheon), brief history, current conflicts, themes.
2. `campaign/geography.md` — the starting region, a few key locations, travel context.
3. `campaign/factions.md` — 2–4 organizations with goals and conflicts.
4. `campaign/roster.md` — a handful of starting NPCs (leave room to grow).

Leave `campaign/party.md` and `campaign/session-log.md` for the user to populate as they
make characters and play. If the user later wants to ground a homebrew world in published
sourcebooks, point them at the repo `README.md` → *Reference material* to extract PDFs
into `references/` (and, if reusable, at `settings/README.md` → *Adding your own
setting*).

## Guardrails

- **Never overwrite without confirming.** If `references/<guide>` or a filled-in
  `campaign/` file already exists, stop and confirm before replacing it.
- **Don't fabricate settings.** Only offer settings that actually exist under `settings/`,
  plus the custom-generation path.
- **Reference-only for pre-built settings.** Installing a stored setting copies
  references; it does not write campaign-specific lore. Keep that separation so settings
  stay reusable across campaigns.
- **Surface every change.** Summarize exactly what was copied or written; don't claim a
  file was modified if it wasn't.
