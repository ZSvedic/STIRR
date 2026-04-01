#!/usr/bin/env python3
import glob
import os
import re
import subprocess
import sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
LTOK_RE = re.compile(r'"(\\.|[^\"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')


def get_file_text_tag(path):
    """Checks if a text file and returns the first tag."""
    try:
        chunk = open(path, "rb").read(4096)
        if b"\x00" in chunk:
            return (False, None)
        match = TAG_RE.search(chunk.decode("utf-8", "ignore"))
        return (True, match.group(0) if match else None)
    except Exception:
        return (False, None)


def get_repo_root():
    try:
        return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return None


def is_git_ignored(path, repo_root):
    """Checks `.gitignore` skipping rules."""
    if not repo_root:
        return False
    try:
        rel_path = os.path.relpath(os.path.abspath(path), repo_root)
        return subprocess.run(["git", "-C", repo_root, "check-ignore", "-q", rel_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except Exception:
        return False


def get_text_file_info(path, repo_root):
    """Returns parsed info for text files under size threshold, else None."""
    if is_git_ignored(path, repo_root):
        return None
    is_text, first = get_file_text_tag(path)
    if not is_text:
        return None
    try:
        if os.path.getsize(path) >= 128 * 1024:
            return None
        text = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return None
    tags, counts, names, order = TAG_RE.findall(text), Counter(), {}, {}
    for tag in tags:
        key = tag.lower()
        counts[key] += 1
        if key not in names:
            names[key] = tag
            order[key] = len(order)
    return (os.path.basename(path), sum(1 for _ in LTOK_RE.finditer(text)), first, tags, counts, names, order)


def new_dir_info(path):
    return [os.path.basename(path.rstrip(os.sep)) or path, 0, [], [], Counter(), {}, {}]


def merge_tags(node, counts, names):
    for key, count in counts.items():
        node[4][key] += count
        if key not in node[5]:
            node[5][key] = names[key]
            node[6][key] = len(node[6])


def file_dir_ltok(file_info):
    return max(0, file_info[1] - len(file_info[4]) - (1 if file_info[2] else 0))


def traverse(path, repo_root):
    """Collects info for files and directories while skipping hidden and git-ignored paths."""
    if is_git_ignored(path, repo_root):
        return None
    if os.path.isfile(path):
        file_info = get_text_file_info(path, repo_root)
        if not file_info:
            return None
        node = new_dir_info(path)
        node[3], node[1] = [file_info], file_dir_ltok(file_info)
        merge_tags(node, file_info[4], file_info[5])
        return node
    if not os.path.isdir(path):
        return None
    node = new_dir_info(path)
    for item_path in sorted(glob.glob(os.path.join(path, "*"))):
        if is_git_ignored(item_path, repo_root):
            continue
        if os.path.isdir(item_path):
            child = traverse(item_path, repo_root)
            if not child:
                continue
            node[2].append(child)
            node[1] += child[1]
            merge_tags(node, child[4], child[5])
        elif os.path.isfile(item_path):
            file_info = get_text_file_info(item_path, repo_root)
            if not file_info:
                continue
            node[3].append(file_info)
            node[1] += file_dir_ltok(file_info)
            merge_tags(node, file_info[4], file_info[5])
    return node


def top3_for_file(file_info):
    counts, order = Counter(file_info[4]), {}
    first_key = file_info[2].lower() if file_info[2] else None
    seen_first = False
    for tag in file_info[3]:
        key = tag.lower()
        if first_key and key == first_key and not seen_first:
            seen_first = True
            if key in counts:
                counts[key] -= 1
                if counts[key] <= 0:
                    del counts[key]
            continue
        if key in counts and key not in order:
            order[key] = len(order)
    items = sorted(counts.items(), key=lambda item: (-item[1], order.get(item[0], 10**9)))[:3]
    return [(count, file_info[5][key]) for key, count in items]


def print_file_info(file_info, indent=""):
    first = file_info[2] or "-"
    top3 = top3_for_file(file_info)
    extra = " + " + " ".join(f"{count}{tag}" for count, tag in top3) if top3 else ""
    print(f"{indent}{file_info[0]}, {file_info[1]} LTok, {first}{extra}")


def print_file_tree(node, indent=""):
    print(f"{indent}{node[0]}/, {node[1]} LTok, -")
    child_indent = indent + "  "
    for child_dir in node[2]:
        print_file_tree(child_dir, child_indent)
    for file_info in node[3]:
        print_file_info(file_info, child_indent)


def print_tags(counts, names, order):
    print("== TAG TOTALS ===")
    items = sorted(counts.items(), key=lambda item: (-item[1], order.get(item[0], 10**9)))
    print(" ".join(f"{count}{names[key]}" for key, count in items))


def print_all(nodes):
    print("== FILE TREE as Name, X LTok, FirstTag + Top3Tags ===")
    counts, names, order = Counter(), {}, {}
    for node in nodes:
        print_file_tree(node)
        for key, count in node[4].items():
            counts[key] += count
            if key not in names:
                names[key] = node[5][key]
                order[key] = len(order)
    print_tags(counts, names, order)


def print_usage():
    print("USAGE:")
    print("  stirr-tree.py PATH1 [PATH2 ...]")
    print("  stirr-tree.py --help")


def main(args):
    if not args or args[0] in {"-h", "--help"}:
        print_usage()
        return 0
    repo_root = get_repo_root()
    print_all([node for arg in args if (node := traverse(os.path.normpath(arg), repo_root))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
