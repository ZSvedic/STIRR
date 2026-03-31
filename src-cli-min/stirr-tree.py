#!/usr/bin/env python3
import glob
import os
import re
import subprocess
import sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
LTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')


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
    """Returns git repository root path or None when unavailable."""
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
        abs_path = os.path.abspath(path)
        rel_path = os.path.relpath(abs_path, repo_root)
        result = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", rel_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def count_ltok(text):
    """Counts lexical tokens in text."""
    return sum(1 for _ in LTOK_RE.finditer(text))


def build_casefold_tags(tags):
    """Builds case-insensitive counts preserving first-seen canonical casing and order."""
    counts = Counter()
    canonical = {}
    order = {}
    for index, tag in enumerate(tags):
        key = tag.lower()
        counts[key] += 1
        if key not in canonical:
            canonical[key] = tag
            order[key] = index
    return counts, canonical, order


def get_text_file_info(path, repo_root):
    """Returns parsed info for text files under size threshold, else None."""
    if is_git_ignored(path, repo_root):
        return None

    is_text, first_tag = get_file_text_tag(path)
    if not is_text:
        return None

    try:
        size = os.path.getsize(path)
        if size >= 128 * 1024:
            return None

        with open(path, encoding="utf-8", errors="ignore") as file:
            text = file.read()

        tags = TAG_RE.findall(text)
        tag_counts, tag_canonical, tag_order = build_casefold_tags(tags)
        return {
            "kind": "file",
            "name": os.path.basename(path),
            "path": path,
            "ltok": count_ltok(text),
            "first": first_tag,
            "tags_raw": tags,
            "tag_counts": tag_counts,
            "tag_canonical": tag_canonical,
            "tag_order": tag_order,
        }
    except Exception:
        return None


def new_dir_info(path):
    """Creates an empty directory info object."""
    base_name = os.path.basename(path.rstrip(os.sep)) or path
    return {
        "kind": "dir",
        "name": base_name,
        "path": path,
        "ltok": 0,
        "dirs": [],
        "files": [],
        "tag_counts": Counter(),
        "tag_canonical": {},
        "tag_order": {},
        "_next_tag_index": 0,
    }


def merge_tag_maps(dst, src_counts, src_canonical, src_order):
    """Merges case-insensitive tag maps, preserving destination first-seen canonical casing."""
    for key, count in src_counts.items():
        dst["tag_counts"][key] += count
        if key not in dst["tag_canonical"]:
            dst["tag_canonical"][key] = src_canonical[key]
            dst["tag_order"][key] = dst["_next_tag_index"]
            dst["_next_tag_index"] += 1


def file_dir_ltok(file_info):
    """Returns a directory-level LTok contribution for a file."""
    return max(0, file_info["ltok"] - len(file_info["tag_counts"]) - (1 if file_info["first"] else 0))


def traverse(path, repo_root):
    """Collects info for files and directories while skipping hidden and git-ignored paths."""
    if is_git_ignored(path, repo_root):
        return None

    if os.path.isfile(path):
        file_info = get_text_file_info(path, repo_root)
        if file_info is None:
            return None
        node = new_dir_info(path)
        node["files"].append(file_info)
        node["ltok"] = file_dir_ltok(file_info)
        merge_tag_maps(node, file_info["tag_counts"], file_info["tag_canonical"], file_info["tag_order"])
        return node

    if not os.path.isdir(path):
        return None

    node = new_dir_info(path)
    for item_path in sorted(glob.glob(os.path.join(path, "*"))):
        if is_git_ignored(item_path, repo_root):
            continue
        if os.path.isdir(item_path):
            child = traverse(item_path, repo_root)
            if child is None:
                continue
            node["dirs"].append(child)
            node["ltok"] += child["ltok"]
            merge_tag_maps(node, child["tag_counts"], child["tag_canonical"], child["tag_order"])
        elif os.path.isfile(item_path):
            file_info = get_text_file_info(item_path, repo_root)
            if file_info is None:
                continue
            node["files"].append(file_info)
            node["ltok"] += file_dir_ltok(file_info)
            merge_tag_maps(node, file_info["tag_counts"], file_info["tag_canonical"], file_info["tag_order"])

    return node


def sorted_tags(tag_counts, tag_order):
    """Sorts tags by count descending, then first-seen order."""
    return sorted(tag_counts.items(), key=lambda kv: (-kv[1], tag_order.get(kv[0], 10**9)))


def top3_for_file(file_info):
    """Returns top 3 tags for the file, excluding one first-tag occurrence if present."""
    counts = Counter(file_info["tag_counts"])
    order = {}
    first_tag = file_info["first"]
    first_seen_skipped = False
    seen = set()
    for tag in file_info["tags_raw"]:
        key = tag.lower()
        if first_tag and key == first_tag.lower() and not first_seen_skipped:
            first_seen_skipped = True
            if counts.get(key, 0) > 0:
                counts[key] -= 1
                if counts[key] == 0:
                    del counts[key]
            continue
        if key in counts and key not in seen:
            seen.add(key)
            order[key] = len(order)

    ordered = sorted_tags(counts, order)
    result = []
    for key, count in ordered[:3]:
        result.append((count, file_info["tag_canonical"][key]))
    return result


def print_file_info(file_info, indent=""):
    """Prints one file line in expected output format."""
    first_tag = file_info["first"] or "-"
    top3 = top3_for_file(file_info)
    if top3:
        top3_part = " ".join(f"{count}{tag}" for count, tag in top3)
        tags_part = f"{first_tag} + {top3_part}"
    else:
        tags_part = first_tag
    print(f"{indent}{file_info['name']}, {file_info['ltok']} LTok, {tags_part}")


def print_file_tree(node, indent=""):
    """Prints directory and file tree recursively."""
    print(f"{indent}{node['name']}/, {node['ltok']} LTok, -")
    child_indent = indent + "  "
    for child_dir in node["dirs"]:
        print_file_tree(child_dir, child_indent)
    for file_info in node["files"]:
        print_file_info(file_info, child_indent)


def print_tags(all_counts, all_canonical, all_order):
    """Prints total tag frequencies."""
    print("== TAG TOTALS ===")
    ordered = sorted_tags(all_counts, all_order)
    print(" ".join(f"{count}{all_canonical[key]}" for key, count in ordered))


def print_all(nodes):
    """Prints full report output."""
    print("== FILE TREE as Name, X LTok, FirstTag + Top3Tags ===")
    merged_counts = Counter()
    merged_canonical = {}
    merged_order = {}
    next_index = 0

    for node in nodes:
        print_file_tree(node)
        for key, count in node["tag_counts"].items():
            merged_counts[key] += count
            if key not in merged_canonical:
                merged_canonical[key] = node["tag_canonical"][key]
                merged_order[key] = next_index
                next_index += 1

    print_tags(merged_counts, merged_canonical, merged_order)


def print_usage():
    """Prints CLI usage."""
    print("USAGE:")
    print("  stirr-tree.py PATH1 [PATH2 ...]")
    print("  stirr-tree.py --help")


def main(args):
    """CLI entrypoint."""
    if not args or args[0] in {"-h", "--help"}:
        print_usage()
        return 0

    repo_root = get_repo_root()
    nodes = []
    for arg in args:
        path = os.path.normpath(arg)
        node = traverse(path, repo_root)
        if node is not None:
            nodes.append(node)

    print_all(nodes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
