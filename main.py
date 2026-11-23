"""Verify assets/entry.png and copy it byte-for-byte to the output dir.

Standard library only. Checks: PNG signature, size <= 1 MiB, IHDR
width/height each <= 1024. Then copies to $MAKEFUN_OUTPUT_DIR
(default /output) as entry.png, re-reads the copy and compares bytes.
Prints path, size and sha256.
"""

import hashlib
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "assets", "entry.png")
PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_DIM = 1024


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def read_ihdr(data):
    """Return (width, height) from the IHDR chunk, or raise ValueError."""
    if len(data) < 8 or data[:8] != PNG_SIG:
        raise ValueError("not a PNG file (bad signature)")
    if len(data) < 33:
        raise ValueError("PNG too short for an IHDR chunk")
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def verify(data):
    if len(data) > MAX_BYTES:
        raise ValueError("PNG is %d bytes, over the %d-byte limit"
                         % (len(data), MAX_BYTES))
    width, height = read_ihdr(data)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError("PNG is %dx%d, over the %dx%d limit"
                         % (width, height, MAX_DIM, MAX_DIM))
    return width, height

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    with open(SRC, "rb") as f:
        data = f.read()
    width, height = verify(data)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as f:
        f.write(data)
    with open(dest, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("re-read of %s does not match source bytes" % dest)
    print("wrote %s (%d bytes, %dx%d) sha256=%s"
          % (dest, len(written), width, height, sha256_hex(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
