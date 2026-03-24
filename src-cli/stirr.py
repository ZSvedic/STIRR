#!/usr/bin/env python3
import glob, os, re, sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
RULE_TAGS = "#TextRL #ConventionRL #SDD #TDD #ImplementRL #HITL #RepeatRL"
MAX_TEXT_FILE_SIZE = 128 * 1024
HELP_TEXT = """USAGE:
  stirr.py [--dry-run] PATH1 [PATH2 ...]
  stirr.py --help

  <PATHx> ...
      A file(s)/dir(s) to check.
"""


def kb(n): return f"{n / 1024:.2f}KB"
def fmt(items): return " ".join(f"{v}{k}" for k, v in items)

def top(cnt, order=None, n=5):
    order = order or {}
    return sorted(cnt.items(), key=lambda kv: (-kv[1], order.get(kv[0], 10**9), kv[0]))[:n]


def get_file_text_hashtag(path):
    try:
        with open(path, "rb") as f: chunk = f.read(4096)
        if b"\x00" in chunk: return (False, None)
        m = TAG_RE.search(chunk.decode("utf-8", "ignore"))
        return (True, m.group(0) if m else None)
    except Exception:
        return (False, None)


def get_text_file_info(path):
    try: size = os.path.getsize(path)
    except OSError: return None
    if size >= MAX_TEXT_FILE_SIZE: return None
    ok, first = get_file_text_hashtag(path)
    if not ok: return None
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f: txt = f.read()
    except OSError:
        return None
    tags = [t.lower() for t in TAG_RE.findall(txt)]
    order = {}
    for t in tags: order.setdefault(t, len(order))
    return {
        "path": os.path.abspath(path), "name": os.path.basename(path), "size": size,
        "first_tag": first, "counts": Counter(tags), "order": order,
    }


def traverse(paths):
    roots = [paths] if isinstance(paths, str) else list(paths)
    files, totals = [], Counter()
    for root in roots:
        if os.path.isfile(root):
            items = [root]
        elif os.path.isdir(root):
            items = glob.glob(os.path.join(root, "**", "*"), recursive=True)
        else:
            items = []
        for p in items:
            if not os.path.isfile(p): continue
            fi = get_text_file_info(p)
            if not fi: continue
            files.append(fi); totals.update(fi["counts"])
    files.sort(key=lambda f: f["path"])
    return {"roots": [os.path.abspath(p) for p in roots], "files": files, "dirs": {}, "totals": totals}


def print_file_info(fi):
    x = top(fi["counts"], fi["order"], 5)
    y = f" ({fmt(x)})" if x else ""
    print(f"  {fi['name']} {kb(fi['size'])} {fi['first_tag'] or '-'}{y}")


def print_file_tree(data):
    print("FILE TREE:")
    for root in data["roots"]:
        rp = root + os.sep
        inside = [f for f in data["files"] if f["path"] == root or f["path"].startswith(rp)]
        lbl = os.path.basename(root.rstrip(os.sep)) or root
        if os.path.isfile(root):
            print(f"{lbl} {kb(os.path.getsize(root) if os.path.exists(root) else 0)}")
        else:
            print(f"{lbl}/ {kb(sum(f['size'] for f in inside))}")
            for f in inside: print_file_info(f)


def print_hahstags(data):
    print("TAG TOTALS:")
    x = top(data["totals"], None, len(data["totals"]))
    print(fmt(x) if x else "(none)")


def print_all(data):
    print(f"RULE TAGS: {RULE_TAGS}")
    print_file_tree(data)
    print_hahstags(data)
    print("API KEYS:")
    print(f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY', '')}")
    print(f"ANTHROPIC_API_KEY={os.getenv('ANTHROPIC_API_KEY', '')}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if any(a in ("-h", "--help") for a in argv) or not argv:
        print(HELP_TEXT.rstrip()); return 0
    dry = "--dry-run" in argv
    paths = [a for a in argv if a != "--dry-run"]
    if not paths:
        print(HELP_TEXT.rstrip()); return 0
    if dry: print("DRY RUN")
    print_all(traverse(paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
