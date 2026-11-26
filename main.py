#!/usr/bin/env python3
"""THE WORLD TODAY - 26 November 2026 in one picture.

Entry for make.fun news-image-20261126. The front page was drawn
by draw.py (PIL) from the 35 verified 26-Nov-2026 stories and saved
as entry.png in this repository. This program copies that image,
unchanged, to the output directory the grader gives it.

Deterministic: same bytes in, same bytes out, no network, no clock,
no randomness. Standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    # The IHDR chunk must follow the signature: 4-byte length, "IHDR", 13 bytes
    # of data, 4-byte CRC — so a valid PNG is at least 33 bytes and bytes 12-16
    # spell IHDR. Reject a truncated header before trusting the dimensions.
    if len(data) < 33 or data[12:16] != b"IHDR":
        print("entry.png has no valid IHDR chunk", file=sys.stderr)
        return 1
    # Width/height live in the IHDR chunk (bytes 16-24, big-endian).
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > MAX_SIDE or height > MAX_SIDE:
        print("entry.png exceeds 1024x1024", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst} ({len(data)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
