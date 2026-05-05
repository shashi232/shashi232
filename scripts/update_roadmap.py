#!/usr/bin/env python3
"""
Reads roadmap.json and regenerates the
<!-- ROADMAP_START --> ... <!-- ROADMAP_END --> block in README.md.

Edit roadmap.json to update your learning progress — the workflow
will automatically sync it to your README every day.
"""

import json
import re
import sys
from datetime import datetime, timezone

README  = "README.md"
CONFIG  = "roadmap.json"
BAR_LEN = 20   # total chars in progress bar


def build_bar(percent: int) -> str:
    filled = round(percent / 100 * BAR_LEN)
    return "█" * filled + "░" * (BAR_LEN - filled)


def build_roadmap_block(skills: list) -> str:
    lines = []
    for skill in skills:
        bar     = build_bar(skill["percent"])
        status  = skill["status"]
        name    = skill["name"]
        pct     = skill["percent"]
        # Fixed-width columns so the bars align nicely
        lines.append(f"{status}  {name:<30} {bar}  {pct:>3}%")

    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return (
        "<!-- ROADMAP_START -->\n"
        "```\n"
        + "\n".join(lines)
        + f"\n```\n"
        f"*Last updated: {updated_at}*\n"
        "<!-- ROADMAP_END -->"
    )


def update_readme(new_block: str) -> None:
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- ROADMAP_START -->.*?<!-- ROADMAP_END -->"
    if not re.search(pattern, content, flags=re.DOTALL):
        print("[ERROR] Could not find ROADMAP_START / ROADMAP_END markers in README.md", file=sys.stderr)
        sys.exit(1)

    updated = re.sub(pattern, new_block, content, flags=re.DOTALL)

    with open(README, "w", encoding="utf-8") as f:
        f.write(updated)

    print("[OK] Roadmap updated successfully.")


if __name__ == "__main__":
    with open(CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)

    block = build_roadmap_block(config["skills"])
    print(f"[INFO] Generating roadmap for {len(config['skills'])} skills...")
    update_readme(block)
