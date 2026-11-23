#!/usr/bin/env python3
"""Dad Joke Showdown entry: writes one original dad joke to /output/entry.txt.

The joke was picked from three hand-written candidates for the cleanest
single pun, the freshest wording and the best read-aloud rhythm, against
the judge's brief (a father of three judging on the groan).

The winning joke: a TV remote that answers back. The pun lands in the
last three words -- "changed the subject": the remote changes channels,
and it also changes the subject of the conversation. "Muted me" sets it
up without giving the turn away.
"""

import os

# The chosen joke. Original, written for this bounty, 88 characters.
JOKE = "I told the TV remote a joke. It didn't laugh \u2014 it just muted me and changed the subject."

MAX_CHARS = 200


def pick_output_path():
    """Prefer the grader's /output, fall back to a local ./output dir."""
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def local_output_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def write_entry(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    # The grader collects outputs as another user: make it world-readable.
    # (Never use tempfile/mkstemp here: those create mode 0600 files.)
    os.chmod(path, 0o644)
    # Read back and confirm the file holds exactly the joke we meant.
    with open(path, "r", encoding="utf-8") as fh:
        if fh.read() != text:
            raise SystemExit("written entry does not match the joke")


def main():
    text = JOKE.strip()
    if not text:
        raise SystemExit("joke is empty")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            "joke is %d characters, over the 200 limit" % len(text)
        )
    # One joke, one line: collapse any stray newlines inside the text.
    text = " ".join(text.splitlines()).strip()
    path = pick_output_path()
    try:
        write_entry(path, text)
    except (OSError, PermissionError):
        # /output exists but is not writable here: use the local fallback
        # instead of failing outright (the grader's sandbox has a
        # writable /output, so this branch only triggers in local runs).
        write_entry(local_output_path(), text)


if __name__ == "__main__":
    main()
