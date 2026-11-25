"""Meme Sprint 3: AI Agent Goes Rogue.

The graded entrypoint. Copies the finished meme image (entry.png, drawn
at build time) to /output/entry.png, then prints the meme's one line.

Standard library only; no network, no clock, no randomness -- two runs
always write the same bytes and print the same line.
"""

import os
import shutil
import struct
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_SIDE = 1024

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

LINE = (
    "I asked my AI agent to fix one typo \u2014 it quit my job, "
    "sold my car, and adopted 3 raccoons."
)


def out_path():
    """The file the grader reads."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(base) / "entry.png"


def png_size(raw):
    """Width and height out of a PNG header."""
    return struct.unpack(">II", raw[16:24])


def check_image(raw):
    """Refuse anything the competition would refuse."""
    if len(raw) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(raw)} bytes, over the 1 MiB cap")
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    w, h = png_size(raw)
    if w > MAX_SIDE or h > MAX_SIDE:
        raise SystemExit(f"entry.png is {w}x{h}, over 1024x1024")


def main():
    raw = SOURCE.read_bytes()
    check_image(raw)
    dest = out_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
