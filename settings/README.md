# Settings library

Pre-built **campaign settings** you can install into the vault, plus the home for any
custom setting you generate. A "setting" here is the reusable **world canon** for a
campaign — primarily the sourcebook reference extracts the agent treats as published
canon. It is *not* a specific campaign: it carries no party, no NPC roster, and no
session history. Those live in `campaign/` and are yours to write per playthrough.

## How a setting is used

On first setup you pick one stored setting (or generate a custom one). The
**`setup-campaign` skill** does the install: invoke it with `/setup-campaign`, or just
ask the agent to "set up my campaign" / "choose a setting." It is also fine to do the
copy by hand — the skill is a convenience, not a requirement.

Installing a setting copies its `references/` into the vault's top-level `references/`
directory, so the agent finds canon at the standard path (`references/<guide>/_raw/…`)
described in `AGENTS.md`. The campaign bible under `campaign/` is left as the blank
template for you to fill in.

## Layout

```
settings/
└── <slug>/
    ├── setting.md          # manifest: name, blurb, what it installs, source notes
    └── references/         # sourcebook extracts copied into ./references on install
        └── <guide>/_raw/
            ├── full.md
            ├── pages/page-NNNN.md
            └── images/
```

`setting.md` carries YAML frontmatter (`name`, `slug`, `system`, `references`, …) the
setup skill reads to present and install the setting.

## Available settings

| Slug | Name | System | Bundled references |
|------|------|--------|--------------------|
| `forgotten-realms` | Forgotten Realms | D&D 5e | Campaign Guide, Player's Guide |

## Adding your own setting

1. Create `settings/<your-slug>/` with a `setting.md` manifest (copy an existing one as
   a template).
2. Add sourcebook extracts under `settings/<your-slug>/references/<guide>/_raw/` using
   `scripts/extract_pdf.py` (see the repo `README.md` → *Reference material*).
3. The setting now appears as an install option for the `setup-campaign` skill.

Generating a brand-new homebrew setting instead? Use the `setup-campaign` skill's
**custom setting** path — it interviews you and fills in the `campaign/` bible directly
rather than installing pre-built references.
