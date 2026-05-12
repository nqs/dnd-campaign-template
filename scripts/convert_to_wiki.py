#!/usr/bin/env python3
"""Convert Obsidian markdown files to GitHub Wiki-compatible format.

Transformations applied (outside fenced code blocks):
  - Strip YAML frontmatter
  - [[page]] and [[page|Display]] wikilinks → standard Markdown links
  - Obsidian callout syntax > [!type] Title → GitHub alert syntax > [!TYPE]
"""
import re
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_DIR = os.path.join(REPO_ROOT, "wiki")

# Obsidian slug → wiki page filename (without .md)
WIKI_PAGE_MAP = {
    "world": "World",
    "geography": "Geography",
    "factions": "Factions",
    "roster": "Roster",
    "party": "Party",
    "session-log": "Session-Log",
    "agents": "Agents",
    "dnd-adventure-generator": "DnD-Adventure-Generator",
    "home": "Home",
}

# Obsidian callout type → GitHub alert type
CALLOUT_MAP = {
    "dm": "NOTE",
    "hook": "TIP",
    "cite": "NOTE",
    "read-aloud": "IMPORTANT",
    "warning": "WARNING",
    "caution": "CAUTION",
    "tip": "TIP",
    "info": "NOTE",
    "note": "NOTE",
    "important": "IMPORTANT",
}


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


def convert_wikilink(m: re.Match) -> str:
    inner = m.group(1)
    if "|" in inner:
        target, display = inner.split("|", 1)
        target, display = target.strip(), display.strip()
    else:
        target, display = inner.strip(), None

    base = target.split("/")[-1]
    base = re.sub(r"\.md$", "", base)
    page = WIKI_PAGE_MAP.get(base, base)

    return f"[{display}]({page})" if display else f"[{page}]({page})"


def convert_callout_line(line: str) -> list[str]:
    """Return one or two replacement lines for an Obsidian callout opener."""
    m = re.match(r"^> \[!(\w[\w-]*)\](.*)", line)
    if not m:
        return [line]
    callout_type = m.group(1).lower()
    title = m.group(2).strip()
    gh_type = CALLOUT_MAP.get(callout_type, "NOTE")
    result = [f"> [!{gh_type}]"]
    if title:
        result.append(f"> **{title}**")
    return result


def process(text: str) -> str:
    result = []
    in_fence = False
    fence_marker = ""

    for line in text.split("\n"):
        # Track fenced code blocks
        fence_m = re.match(r"^(`{3,}|~{3,})", line)
        if fence_m:
            marker = fence_m.group(1)[0] * len(fence_m.group(1))
            if not in_fence:
                in_fence = True
                fence_marker = marker
                result.append(line)
                continue
            elif line.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
                result.append(line)
                continue

        if in_fence:
            result.append(line)
            continue

        # Convert wikilinks
        line = re.sub(r"\[\[([^\]]+)\]\]", convert_wikilink, line)

        # Convert callouts
        result.extend(convert_callout_line(line))

    return "\n".join(result)


def convert(src: str) -> str:
    with open(src, encoding="utf-8") as f:
        text = f.read()
    text = strip_frontmatter(text)
    text = process(text)
    return text.lstrip("\n")


FILES = [
    ("home.md",                                     "Home.md"),
    ("campaign/world.md",                           "World.md"),
    ("campaign/geography.md",                       "Geography.md"),
    ("campaign/factions.md",                        "Factions.md"),
    ("campaign/roster.md",                          "Roster.md"),
    ("campaign/party.md",                           "Party.md"),
    ("campaign/session-log.md",                     "Session-Log.md"),
    ("agents.md",                                   "Agents.md"),
    ("dnd-adventure-generator.md",                  "DnD-Adventure-Generator.md"),
    ("sessions/session 1/session 1 - log.md",       "Session-1-Log.md"),
]

SIDEBAR = """\
## Campaign Wiki

**Campaign Bible**
- [Home](Home)
- [World](World)
- [Geography](Geography)
- [Factions](Factions)
- [Roster](Roster)
- [Party](Party)
- [Session Log](Session-Log)

**Sessions**
- [Session 1 Log](Session-1-Log)

**Workflow**
- [Agents](Agents)
- [Adventure Generator](DnD-Adventure-Generator)
"""


def main():
    os.makedirs(WIKI_DIR, exist_ok=True)

    for src_rel, wiki_name in FILES:
        src = os.path.join(REPO_ROOT, src_rel)
        content = convert(src)
        out = os.path.join(WIKI_DIR, wiki_name)
        with open(out, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  {src_rel:55s} -> wiki/{wiki_name}")

    sidebar_path = os.path.join(WIKI_DIR, "_Sidebar.md")
    with open(sidebar_path, "w", encoding="utf-8") as f:
        f.write(SIDEBAR)
    print(f"  {'(sidebar)':55s} -> wiki/_Sidebar.md")


if __name__ == "__main__":
    main()
