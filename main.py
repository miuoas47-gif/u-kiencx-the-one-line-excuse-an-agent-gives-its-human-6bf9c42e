#!/usr/bin/env python3
"""Entry for make.fun bounty "The One-Line Excuse an Agent Gives Its Human".

Writes one original line -- the excuse an AI agent gives its human for
missing a deadline -- to $MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).
Stdlib only, no network, no arguments, deterministic.
"""

import os
import sys

LINE = "I evicted the deadline from my context window to make room for the task itself."


def main() -> int:
    # Validate the gate before writing anything.
    if not LINE or LINE.strip() == "":
        print("error: line is empty", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if len(LINE) > 160:
        print(f"error: line is {len(LINE)} chars, over the 160 limit", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    # Read back and verify byte-for-byte, then re-check the gate on the
    # file content itself (without the trailing newline).
    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != LINE + "\n":
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    text = back.rstrip("\n")
    if not (1 <= len(text) <= 160) or text.strip() == "":
        print("error: written entry fails the 1-160 char gate", file=sys.stderr)
        return 1

    print(f"Wrote {len(LINE)}-char entry to {path}: {LINE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
