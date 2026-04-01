#!/usr/bin/env python3
import glob
import os
import re
import subprocess
import sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
LTOK_RE = re.compile(
    r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]'
)


def get_file_text_tag(path):
    """Checks if a text file and returns the first tag."""
    try:
        with open(path, "rb") as file:
            chunk = file.read(4096)
        if b"\x00" in chunk:
            return (False, None)
        text = chunk.decode("utf-8", "ignore")
        match = TAG_RE.search(text)
        return (True, match.group(0) if match else None)
    except Exception:
        return (False, None)


def get_repo_root():
    """Return git repository root, or None if not inside a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def is_git_ignored(path, repo_root):
    """Checks `.gitignore` skipping rules."""
    if not repo_root:
        return False
    try:
        rel_path = os.path.relpath(os.path.abspath(path), repo_root)
        result = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", rel_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def build_tag_stats(tags):
    """Map lowercase tag key to counts, display form, and discovery order."""
    counts = Counter()
    display_names = {}
    order = {}
    for tag in tags:
        key = tag.lower()
        counts[key] += 1
        if key not in display_names:
            display_names[key] = tag
            order[key] = len(order)
    return counts, display_names, order


def get_text_file_info(path, repo_root):
    """Parse a small text file for LTok and tag stats; skip non-text and huge files."""
    if is_git_ignored(path, repo_root):
        return None
    is_text, first = get_file_text_tag(path)
    if not is_text:
        return None
    try:
        if os.path.getsize(path) >= 128 * 1024:
            return None
        with open(path, encoding="utf-8", errors="ignore") as file:
            text = file.read()
    except Exception:
        return None
    tags = TAG_RE.findall(text)
    counts, display_names, tag_order = build_tag_stats(tags)
    ltok = sum(1 for _ in LTOK_RE.finditer(text))
    return {
        "name": os.path.basename(path),
        "ltok": ltok,
        "first": first,
        "tags": tags,
        "counts": counts,
        "display_names": display_names,
        "tag_order": tag_order,
    }


def new_dir_node(path):
    """Empty directory node with aggregated totals."""
    name = os.path.basename(path.rstrip(os.sep)) or path
    return {
        "name": name,
        "dir_ltok": 0,
        "dirs": [],
        "files": [],
        "totals": Counter(),
        "totals_names": {},
        "totals_order": {},
    }


def merge_totals(node, counts, display_names):
    """Add per-file or child-directory hashtag counts into node totals."""
    for key, count in counts.items():
        node["totals"][key] += count
        if key not in node["totals_names"]:
            node["totals_names"][key] = display_names[key]
            node["totals_order"][key] = len(node["totals_order"])


def file_dir_ltok(file_info):
    """Directory rollup: file LTok minus distinct tag keys and one if there is a first tag."""
    discount = len(file_info["counts"]) + (1 if file_info["first"] else 0)
    return max(0, file_info["ltok"] - discount)


def traverse(path, repo_root):
    """Walk path; skip hidden entries (via glob), gitignored paths, and huge/binary files."""
    if is_git_ignored(path, repo_root):
        return None
    if os.path.isfile(path):
        file_info = get_text_file_info(path, repo_root)
        if not file_info:
            return None
        node = new_dir_node(path)
        node["files"] = [file_info]
        node["dir_ltok"] = file_dir_ltok(file_info)
        merge_totals(node, file_info["counts"], file_info["display_names"])
        return node
    if not os.path.isdir(path):
        return None
    node = new_dir_node(path)
    pattern = os.path.join(path, "*")
    for item_path in sorted(glob.glob(pattern)):
        if is_git_ignored(item_path, repo_root):
            continue
        if os.path.isdir(item_path):
            child = traverse(item_path, repo_root)
            if not child:
                continue
            node["dirs"].append(child)
            node["dir_ltok"] += child["dir_ltok"]
            merge_totals(node, child["totals"], child["totals_names"])
        elif os.path.isfile(item_path):
            file_info = get_text_file_info(item_path, repo_root)
            if not file_info:
                continue
            node["files"].append(file_info)
            node["dir_ltok"] += file_dir_ltok(file_info)
            merge_totals(node, file_info["counts"], file_info["display_names"])
    return node


def top3_tags_for_file(file_info):
    """Top three hashtag groups excluding the first occurrence of the first tag."""
    counts = Counter(file_info["counts"])
    first_key = file_info["first"].lower() if file_info["first"] else None
    seen_first = False
    order_after_strip = {}
    for tag in file_info["tags"]:
        key = tag.lower()
        if first_key and key == first_key and not seen_first:
            seen_first = True
            if key in counts:
                counts[key] -= 1
                if counts[key] <= 0:
                    del counts[key]
            continue
        if key in counts and key not in order_after_strip:
            order_after_strip[key] = len(order_after_strip)
    items = sorted(
        counts.items(),
        key=lambda item: (-item[1], order_after_strip.get(item[0], 10**9)),
    )[:3]
    return [(count, file_info["display_names"][key]) for key, count in items]


def print_file_info(file_info, indent=""):
    first = file_info["first"] or "-"
    top3 = top3_tags_for_file(file_info)
    extra = " + " + " ".join(f"{count}{tag}" for count, tag in top3) if top3 else ""
    print(f"{indent}{file_info['name']}, {file_info['ltok']} LTok, {first}{extra}")


def print_file_tree(node, indent=""):
    print(f"{indent}{node['name']}/, {node['dir_ltok']} LTok, -")
    child_indent = indent + "  "
    for child_dir in node["dirs"]:
        print_file_tree(child_dir, child_indent)
    for file_info in node["files"]:
        print_file_info(file_info, child_indent)


def print_tags(counts, display_names, order):
    print("== TAG TOTALS ===")
    items = sorted(
        counts.items(),
        key=lambda item: (-item[1], order.get(item[0], 10**9)),
    )
    print(" ".join(f"{count}{display_names[key]}" for key, count in items))


def print_all(nodes):
    print("== FILE TREE as Name, X LTok, FirstTag + Top3Tags ===")
    counts = Counter()
    display_names = {}
    order = {}
    for node in nodes:
        print_file_tree(node)
        for key, count in node["totals"].items():
            counts[key] += count
            if key not in display_names:
                display_names[key] = node["totals_names"][key]
                order[key] = len(order)
    print_tags(counts, display_names, order)


def print_usage():
    print("USAGE:")
    print("  stirr-tree.py PATH1 [PATH2 ...]")
    print("  stirr-tree.py --help")


def main(arguments):
    if not arguments or arguments[0] in {"-h", "--help"}:
        print_usage()
        return 0
    repo_root = get_repo_root()
    nodes = []
    for raw_path in arguments:
        node = traverse(os.path.normpath(raw_path), repo_root)
        if node:
            nodes.append(node)
    print_all(nodes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
