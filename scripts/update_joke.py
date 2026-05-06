#!/usr/bin/env python3
"""
Fetches a fresh programming joke from JokeAPI and
updates the <!-- JOKE_START --> ... <!-- JOKE_END --> block in README.md.
"""

import re
import sys
import urllib.request
import urllib.error
import json

README = "README.md"

JOKE_API = (
    "https://v2.jokeapi.dev/joke/Programming"
    "?blacklistFlags=nsfw,racist,sexist,explicit"
    "&safe-mode"
)

FALLBACK_JOKES = [
    ("single", "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛"),
    ("single", "A SQL query walks into a bar, walks up to two tables and asks...\n'Can I join you?' 😄"),
    ("twopart", "Why don't programmers like nature?", "It has too many bugs and no debugging tool. 🌲🐛"),
    ("single", "There are only 10 types of people in this world:\nThose who understand binary, and those who don't. 🤓"),
    ("twopart", "How many programmers does it take to change a light bulb?", "None. It's a hardware problem. 💡"),
]


def fetch_joke() -> str:
    """Fetch a joke from JokeAPI; fall back to local list on error."""
    try:
        req = urllib.request.Request(JOKE_API, headers={"User-Agent": "github-readme-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        if data.get("error"):
            raise ValueError("API returned error flag")

        if data["type"] == "single":
            return data["joke"]
        else:
            return f"{data['setup']}\n\n> 👉 {data['delivery']}"

    except Exception as exc:
        print(f"[WARN] JokeAPI failed ({exc}), using fallback.", file=sys.stderr)
        import random, time
        random.seed(int(time.time()) % len(FALLBACK_JOKES))
        kind, *parts = random.choice(FALLBACK_JOKES)
        if kind == "single":
            return parts[0]
        return f"{parts[0]}\n\n> 👉 {parts[1]}"


def format_joke_block(joke: str) -> str:
    lines = joke.strip().split("\n")
    formatted = "\n".join(f"> {line}" if line else ">" for line in lines)
    return (
        "<!-- JOKE_START -->\n"
        f"{formatted}\n"
        "<!-- JOKE_END -->"
    )


def update_readme(new_block: str) -> None:
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- JOKE_START -->.*?<!-- JOKE_END -->"
    if not re.search(pattern, content, flags=re.DOTALL):
        print("[ERROR] Could not find JOKE_START / JOKE_END markers in README.md", file=sys.stderr)
        sys.exit(1)

    updated = re.sub(pattern, new_block, content, flags=re.DOTALL)

    with open(README, "w", encoding="utf-8") as f:
        f.write(updated)

    print("[OK] Joke updated successfully.")


if __name__ == "__main__":
    joke = fetch_joke()
    print(f"[INFO] Joke fetched:\n{joke}\n")
    block = format_joke_block(joke)
    update_readme(block)
