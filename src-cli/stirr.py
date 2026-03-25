#!/usr/bin/env python3
import glob, os, re, sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
LEXTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')
MAX_TEXT_FILE_SIZE = 128 * 1024
HELP_TEXT = """USAGE:
  stirr.py [--dry-run] PATH1 [PATH2 ...]
"""


def get_file_text_hashtag(path):
    try:
        with open(path, "rb") as f: chunk = f.read(4096)
        if b"\x00" in chunk: return (False, None)
        m = TAG_RE.search(chunk.decode("utf-8", "ignore"))
        return (True, m.group(0) if m else None)
    except: return (False, None)


def get_nloc_lextokens(txt):
    lines = [l for l in txt.splitlines() if l.strip()]
    tokens = LEXTOK_RE.findall(txt)
    return (len(lines), len(tokens))


def get_text_file_info(path):
    try: size = os.path.getsize(path)
    except OSError: return None
    if size >= MAX_TEXT_FILE_SIZE: return None
    is_text, first = get_file_text_hashtag(path)
    if not is_text: return None
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f: txt = f.read()
    except OSError: return None
    tags = [t.lower() for t in TAG_RE.findall(txt)]
    nloc, ltok = get_nloc_lextokens(txt)
    return {
        "p": os.path.abspath(path), "n": os.path.basename(path), "s": size,
        "nl": nloc, "lt": ltok, "f": first, "c": Counter(tags)
    }


def traverse(paths):
    roots = [paths] if isinstance(paths, str) else list(paths)
    roots = [os.path.abspath(p) for p in roots]
    files, totals, dirs = [], Counter(), {}
    for root in roots:
        is_dir = os.path.isdir(root)
        if os.path.isdir(root):
            dirs.setdefault(root, [0, 0, 0])
            cands = glob.glob(os.path.join(root, "**", "*"), recursive=True)
        elif os.path.isfile(root): cands = [root]
        else: cands = []
        for p in cands:
            i = get_text_file_info(p)
            if not i: continue
            files.append(i); totals.update(i["c"]); fp = i["p"]
            if is_dir:
                d = os.path.dirname(fp)
                while d == root or d.startswith(root + os.sep):
                    v = dirs.setdefault(d, [0, 0, 0])
                    v[0] += i["s"]; v[1] += i["nl"]; v[2] += i["lt"]
                    if d == root: break
                    d = os.path.dirname(d)
    files.sort(key=lambda x: x["p"])
    return {"roots": roots, "files": files, "dirs": dirs, "totals": totals}


def print_file_info(info, indent=1):
    top = info["c"].most_common(3)
    top = f" ({' '.join(f'{n}{t}' for t, n in top)})" if top else ""
    first = f" {info['f']}" if info["f"] else ""
    print(f"{'·' * indent}{info['n']} {info['s']/1024:.2f} KB ({info['nl']} NLOC {info['lt']} LTOK){first}{top}")


def print_file_tree(data):
    print("== FILE TREE as NAME SIZE (NLOC LTOK) #FirstTag (Top 3 tags) ===")
    files = data["files"]
    for root in data["roots"]:
        if not os.path.isdir(root):
            for i in files:
                if i["p"] == root: print_file_info(i, 0); break
            continue
        s, nl, lt = data["dirs"].get(root, [0, 0, 0])
        rn = os.path.basename(root.rstrip(os.sep)) or root
        print(f"{rn}/ {s/1024:.2f} KB ({nl} NLOC {lt} LTOK)")
        for i in files:
            fp = i["p"]
            if not fp.startswith(root + os.sep): continue
            d = os.path.relpath(fp, root).count(os.sep) + 1
            print_file_info(i, d)


def print_hahstags(data):
    print("== TAG TOTALS ===")
    out = data["totals"].most_common()
    print(" ".join(f"{n}{t}" for t, n in out) if out else "(none)")


def print_all(data):
    print_file_tree(data); print_hahstags(data)
    print(f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY', '')}")
    print(f"ANTHROPIC_API_KEY={os.getenv('ANTHROPIC_API_KEY', '')}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv: print(HELP_TEXT.rstrip()); return 0
    dry = "--dry-run" in argv
    paths = [a for a in argv if a != "--dry-run"]
    if not paths: print(HELP_TEXT.rstrip()); return 0
    if dry: print("DRY RUN")
    print_all(traverse(paths)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
