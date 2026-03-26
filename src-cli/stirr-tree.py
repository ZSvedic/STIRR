#!/usr/bin/env python3
# #Human
# Traverses provided paths and prints text file info like lexical tokens sizes and tags.

import glob, os, re, sys
from collections import Counter

# Regex for hashtags, test online at: https://regexr.com/8lduo
TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")

# Regex for lexical tokens, test online at: https://regexr.com/8ldco
LEXTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')

# If text file is larger than this, it would just pollute the output.
MAX_TEXT_FILE_SIZE = 128 * 1024

# Output format for file tree and usage help text.
TREE_INFO = "NAME SIZE (LOC LTOK) FirstTag (Top3Tags)"
TREE_FMT = f"{{}} {{:.2f}} KB ({{}} LOC {{}} LTOK)"
HELP_TEXT = f'''USAGE:
  stirr-tree.py PATH1 [PATH2 ...]

  Prints a file tree for the given paths in the format: {TREE_INFO}. 
  In the end prints totals for all tags. 
'''


def get_file_text_hashtag(path):
    '''Returns (is_text, first_hashtag) for the file at the given path.'''
    try:
        with open(path, "rb") as f: 
            chunk = f.read(4096)
        if b"\x00" in chunk: 
            return (False, None)
        m = TAG_RE.search(chunk.decode("utf-8", "ignore"))
        return (True, m.group(0) if m else None)
    except: 
        return (False, None)


def get_loc_lextokens(txt):
    '''Returns (loc, lextokens) counts for the given text.'''
    lines = [l for l in txt.splitlines() if l.strip()]
    tokens = LEXTOK_RE.findall(txt)
    return (len(lines), len(tokens))


def get_text_file_info(path):
    '''Returns a dictionary with text file info for the given path.'''
    try: 
        size = os.path.getsize(path)
    except OSError: 
        return None
    if size >= MAX_TEXT_FILE_SIZE: 
        return None
    is_text, first = get_file_text_hashtag(path)
    if not is_text: 
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f: 
            txt = f.read()
    except OSError: 
        return None
    tags = [t.lower() for t in TAG_RE.findall(txt)]
    loc, ltok = get_loc_lextokens(txt)
    return {
        'path': os.path.abspath(path), 'name': os.path.basename(path), 'size': size,
        'loc': loc, 'ltok': ltok, "f": first, "c": Counter(tags)
    }


def traverse(paths):
    '''Traverses the given paths and returns a dictionary with file and directory info.'''
    roots = [paths] if isinstance(paths, str) else list(paths)
    roots = [os.path.abspath(p) for p in roots]
    files, totals, dirs = [], Counter(), {}
    for root in roots:
        is_dir = os.path.isdir(root)
        if os.path.isdir(root):
            dirs.setdefault(root, [0, 0, 0])
            cands = glob.glob(os.path.join(root, "**", "*"), recursive=True)
        elif os.path.isfile(root): 
            cands = [root]
        else: 
            cands = []
        for p in cands:
            i = get_text_file_info(p)
            if not i: 
                continue
            files.append(i)
            totals.update(i["c"])
            fp = i['path']
            if is_dir:
                d = os.path.dirname(fp)
                while d == root or d.startswith(root + os.sep):
                    v = dirs.setdefault(d, [0, 0, 0])
                    v[0] += i['size']
                    v[1] += i['loc']
                    v[2] += i['ltok']
                    if d == root: 
                        break
                    d = os.path.dirname(d)
    files.sort(key=lambda x: x['path'])
    return {"roots": roots, "files": files, "dirs": dirs, "totals": totals}


def print_file_info(info, indent=1):
    '''Prints information about a single file.'''
    top = info["c"].most_common(3)
    top = f" ({' '.join(f'{n}{t}' for t, n in top)})" if top else ""
    first = f" {info['f']}" if info["f"] else ""
    print(TREE_FMT.format("·" * indent + info['name'], info['size']/1024, info['loc'], info['ltok']) \
          + first + top)


def print_file_tree(data):
    print(f"== FILE TREE as {TREE_INFO} ===")
    files = data["files"]
    for root in data["roots"]:
        if not os.path.isdir(root):
            for i in files:
                if i['path'] == root: 
                    print_file_info(i, 0)
                    break
            continue
        size, loc, ltok = data["dirs"].get(root, [0, 0, 0])
        dir_name = os.path.basename(root.rstrip(os.sep)) or root
        print(TREE_FMT.format(dir_name+'/', size/1024, loc, ltok))
        for i in files:
            fp = i['path']
            if not fp.startswith(root + os.sep): 
                continue
            d = os.path.relpath(fp, root).count(os.sep) + 1
            print_file_info(i, d)


def print_hashtags(data):
    print("== TAG TOTALS ===")
    out = data["totals"].most_common()
    print(" ".join(f"{n}{t}" for t, n in out) if out else "(none)")


def print_all(data):
    print_file_tree(data) 
    print_hashtags(data)


def main(argv):
    if not argv or "-h" in argv or "--help" in argv:
        print(HELP_TEXT.rstrip())
    else:
        print_all(traverse(argv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
