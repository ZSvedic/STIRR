#!/usr/bin/env python3
import os, glob

def hf(n):
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or u == "TB":
            return f"{int(n)}{u}" if u == "B" else f"{n:.1f}{u}"
        n /= 1024

for p in sorted(["."] + glob.glob("**/*", recursive=True)):
    s = os.path.getsize(p) if os.path.isfile(p) else sum(os.path.getsize(f) for f in glob.glob(f"{p}/**/*", recursive=True) if os.path.isfile(f))
    print(f"{hf(s):>8}  {p}")
