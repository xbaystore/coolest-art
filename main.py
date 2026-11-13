#!/usr/bin/env python3
"""Coolest Art entry (make.fun coolest-art-01): "The Lighthouse at the
Edge of the Desert Sea".

The artwork ships beside this program as art.jpg: a flat-poster
illustration of a lighthouse standing on the crest of a desert dune
shaped like a giant ocean wave, its beam cutting across a teal dusk
while a pale sun rises over the sands. The concept is the collision of
two landscapes that never meet — a sea made of sand, patrolled by a
light that has nothing to warn.

This program's job is delivery, nothing more: it validates the asset's
format from its magic bytes and copies it, byte for byte, to
entry.png in the output directory (MAKEFUN_OUTPUT_DIR, defaulting to
/output). The judge sees exactly the file that ships in this
repository, and every run writes identical bytes, because the copy is
a pure function of the bundled asset.
"""

import os
from pathlib import Path

ASSET_NAME = "art.jpg"
OUTPUT_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
MAX_BYTES = 1_048_576  # the gate's 1 MiB cap on the image


def image_size(data: bytes) -> tuple[int, int]:
    """Read the pixel dimensions from the image header: PNG keeps them
    in the IHDR chunk right after the magic; JPEG in a Start-Of-Frame
    segment found by walking the marker segments."""
    if data.startswith(PNG_MAGIC):
        return (int.from_bytes(data[16:20], "big"),
                int.from_bytes(data[20:24], "big"))
    pos = 2  # skip the JPEG SOI marker
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            break
        marker = data[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0/1/2 carry the frame size
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        pos += 2 + int.from_bytes(data[pos + 2:pos + 4], "big")
    raise ValueError("no frame header found")


def read_asset(source: Path) -> bytes:
    """Return the asset's bytes, refusing anything the gate would turn
    away: not a whole PNG or JPEG, over the size cap, or over the
    1024x1024 pixel cap."""
    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"{source.name}: {len(data)} bytes exceeds the 1 MiB cap")
    if not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
        raise ValueError(f"{source.name}: not a PNG or JPEG image")
    width, height = image_size(data)
    if width > 1024 or height > 1024:
        raise ValueError(f"{source.name}: {width}x{height} exceeds 1024x1024")
    return data


def main() -> None:
    source = Path(__file__).resolve().parent / ASSET_NAME
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # Write to a sibling temp file, then rename: a reader of entry.png
    # only ever sees the whole picture, never a half-copied one.
    target = out_dir / OUTPUT_NAME
    tmp = out_dir / (OUTPUT_NAME + ".tmp")
    tmp.write_bytes(read_asset(source))
    os.replace(tmp, target)


if __name__ == "__main__":
    main()
