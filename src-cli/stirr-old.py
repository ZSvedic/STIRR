#!/usr/bin/env python3
import glob
import os
import re
import sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
LEXTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')
MAX_TEXT_FILE_SIZE = 128 * 1024
HELP_TEXT = """USAGE:
  stirr.py [--dry-run] PATH1 [PATH2 ...]
  stirr.py --help

  <PATHx> ...
      A file(s)/dir(s) to check.
  ...
"""


def kb(size):
    return f"{size / 1024:.2f} KB"


def format_counts(items):
    return " ".join(f"{count}{tag}" for tag, count in items)


def sort_counts(counter, order=None, n=None):
    order = order or {}
    ranked = sorted(counter.items(), key=lambda item: (-item[1], order.get(item[0], 10**9), item[0]))
    return ranked if n is None else ranked[:n]


def get_file_text_hashtag(path):
    try:
        with open(path, "rb") as f:
            chunk = f.read(4096)
        if b"\x00" in chunk:
            return (False, None)
        text = chunk.decode("utf-8", "ignore")
        m = TAG_RE.search(text)
        return (True, m.group(0) if m else None)
    except:
        return (False, None)


def get_nloc_lextokens(txt):
    lines = [l for l in txt.splitlines() if l.strip()]
    tokens = LEXTOK_RE.findall(txt)
    return (len(lines), len(tokens))


def get_text_file_info(path):
    try:
        size = os.path.getsize(path)
    except OSError:
        return None
    if size >= MAX_TEXT_FILE_SIZE:
        return None
    is_text, first_tag = get_file_text_hashtag(path)
    if not is_text:
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
    except OSError:
        return None

    nloc, ltok = get_nloc_lextokens(txt)
    tags = [tag.lower() for tag in TAG_RE.findall(txt)]
    order = {}
    for tag in tags:
        order.setdefault(tag, len(order))

    return {
        "path": os.path.abspath(path),
        "name": os.path.basename(path),
        "size": size,
        "nloc": nloc,
        "ltok": ltok,
        "first_tag": first_tag,
        "counts": Counter(tags),
        "order": order,
    }


def traverse(paths):
    roots = [paths] if isinstance(paths, str) else list(paths)
    roots = [os.path.abspath(p) for p in roots]

    files = []
    totals = Counter()
    dirs = {}

    def ensure_dir(path):
        node = dirs.get(path)
        if node is None:
            node = {"path": path, "name": os.path.basename(path.rstrip(os.sep)) or path, "size": 0, "nloc": 0, "ltok": 0}
            dirs[path] = node
        return node

    for root in roots:
        if os.path.isdir(root):
            ensure_dir(root)
            candidates = glob.glob(os.path.join(root, "**", "*"), recursive=True)
        elif os.path.isfile(root):
            candidates = [root]
        else:
            candidates = []

        for candidate in candidates:
            if not os.path.isfile(candidate):
                continue
            info = get_text_file_info(candidate)
            if not info:
                continue
            files.append(info)
            totals.update(info["counts"])

            for possible_root in roots:
                if not os.path.isdir(possible_root):
                    continue
                if info["path"] == possible_root or info["path"].startswith(possible_root + os.sep):
                    parent = os.path.dirname(info["path"])
                    while parent == possible_root or parent.startswith(possible_root + os.sep):
                        node = ensure_dir(parent)
                        node["size"] += info["size"]
                        node["nloc"] += info["nloc"]
                        node["ltok"] += info["ltok"]
                        if parent == possible_root:
                            break
                        parent = os.path.dirname(parent)

    files.sort(key=lambda item: item["path"])
    return {"roots": roots, "files": files, "dirs": dirs, "totals": totals}


def print_file_info(info, indent=1):
    spacer = "·" * indent
    top3 = sort_counts(info["counts"], info["order"], 3)
    tags_part = f" {info['first_tag']}" if info["first_tag"] else ""
    top_part = f" ({format_counts(top3)})" if top3 else ""
    print(f"{spacer}{info['name']} {kb(info['size'])} ({info['nloc']} NLOC {info['ltok']} LTOK){tags_part}{top_part}")


def print_file_tree(data):
    print("== FILE TREE as NAME SIZE (NLOC LTOK) #FirstTag (Top 3 tags) ===")
    files_by_dir = {}
    for info in data["files"]:
        files_by_dir.setdefault(os.path.dirname(info["path"]), []).append(info)

    dir_children = {}
    for dpath in data["dirs"]:
        parent = os.path.dirname(dpath)
        if dpath != parent:
            dir_children.setdefault(parent, []).append(dpath)

    def print_dir(dpath, depth):
        node = data["dirs"].get(dpath, {"size": 0, "nloc": 0, "ltok": 0})
        name = os.path.basename(dpath.rstrip(os.sep)) or dpath
        print(f"{'·' * depth}{name}/ {kb(node['size'])} ({node['nloc']} NLOC {node['ltok']} LTOK)")

        entries = []
        for child in dir_children.get(dpath, []):
            if os.path.dirname(child) == dpath:
                entries.append(("dir", child, os.path.basename(child)))
        for info in files_by_dir.get(dpath, []):
            entries.append(("file", info, info["name"]))
        entries.sort(key=lambda entry: entry[2])

        for kind, value, _ in entries:
            if kind == "dir":
                print_dir(value, depth + 1)
            else:
                print_file_info(value, indent=depth + 1)

    for root in data["roots"]:
        if os.path.isdir(root):
            print_dir(root, 0)
        else:
            info = next((f for f in data["files"] if f["path"] == root), None)
            if info:
                print_file_info(info, indent=0)


def print_hahstags(data):
    print("== TAG TOTALS ===")
    ordered = sort_counts(data["totals"])
    print(format_counts(ordered) if ordered else "(none)")


def print_all(data):
    print_file_tree(data)
    print_hahstags(data)
    print(f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY', '')}")
    print(f"ANTHROPIC_API_KEY={os.getenv('ANTHROPIC_API_KEY', '')}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or "-h" in argv or "--help" in argv:
        print(HELP_TEXT.rstrip())
        return 0

    dry_run = "--dry-run" in argv
    paths = [a for a in argv if a != "--dry-run"]
    if not paths:
        print(HELP_TEXT.rstrip())
        return 0

    if dry_run:
        print("DRY RUN")
    print_all(traverse(paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
