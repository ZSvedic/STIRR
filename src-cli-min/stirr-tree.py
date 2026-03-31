#!/usr/bin/env python3

import collections
import glob
import os
import re
import subprocess
import sys

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
LTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')
MAX_TEXT_FILE_SIZE = 128 * 1024


def print_usage():
    print("USAGE:")
    print("  stirr-tree.py PATH1 [PATH2 ...]")
    print("  stirr-tree.py --help")


def get_file_text_hashtag(path):
    """Checks if text file and returns first hashtag."""
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


def is_git_ignored(path, repo_root):
    """Checks `.gitignore` skipping."""
    try:
        result = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def find_repo_root(path):
    """Finds git repository root for the given path, if any."""
    start = path
    if os.path.isfile(start):
        start = os.path.dirname(start)
    try:
        result = subprocess.run(
            ["git", "-C", start, "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return os.getcwd()


def parse_text_file(path):
    """Parses a text file and returns LTOK count and hashtag data."""
    try:
        if os.path.getsize(path) >= MAX_TEXT_FILE_SIZE:
            return None
    except OSError:
        return None

    is_text, first_tag = get_file_text_hashtag(path)
    if not is_text:
        return None

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()
    except Exception:
        return None

    ltok_count = sum(
        1
        for match in LTOK_RE.finditer(text)
        if match.group(0) not in {":", "`", "'"}
    )
    matches = [match.group(0) for match in TAG_RE.finditer(text)]
    total_counts = collections.Counter(tag.lower() for tag in matches)

    variant_counts = collections.defaultdict(collections.Counter)
    for tag in matches[1:]:
        variant_counts[tag.lower()][tag] += 1

    top_counts = collections.Counter(tag.lower() for tag in matches[1:])
    top_keys = sorted(top_counts.keys(), key=lambda tag: (-top_counts[tag], tag))[:3]

    top_tags = []
    first_tag_lower = first_tag.lower() if first_tag else None
    for tag_key in top_keys:
        display_tag = tag_key
        if tag_key == first_tag_lower and variant_counts[tag_key]:
            display_tag = sorted(
                variant_counts[tag_key].keys(),
                key=lambda item: (-variant_counts[tag_key][item], item),
            )[0]
        top_tags.append((display_tag, top_counts[tag_key]))

    return {
        "ltok": ltok_count,
        "first_tag": first_tag,
        "first_tag_key": first_tag.lower() if first_tag else None,
        "top_tags": top_tags,
        "total_counts": total_counts,
    }


def should_skip(path, repo_root):
    """Checks whether file or directory should be skipped."""
    name = os.path.basename(path)
    if name.startswith("."):
        return True
    if name == ".gitignore":
        return True
    rel_path = os.path.relpath(path, repo_root)
    return is_git_ignored(rel_path, repo_root)


def traverse(path, repo_root):
    """Traverses files and directories, collecting tree and hashtag data."""
    tag_totals = collections.Counter()
    first_tag_keys = set()

    if os.path.isdir(path):
        children = []
        total_ltok = 0
        for child_path in sorted(glob.glob(os.path.join(path, "*"))):
            if should_skip(child_path, repo_root):
                continue
            child_info, child_totals, child_first_tag_keys = traverse(child_path, repo_root)
            if child_info is None:
                continue
            children.append(child_info)
            total_ltok += child_info["ltok"]
            tag_totals.update(child_totals)
            first_tag_keys.update(child_first_tag_keys)

        return {
            "name": os.path.basename(path),
            "is_dir": True,
            "ltok": total_ltok,
            "first_tag": None,
            "top_tags": [],
            "children": children,
        }, tag_totals, first_tag_keys

    if os.path.isfile(path):
        file_info = parse_text_file(path)
        if file_info is None:
            return {
                "name": os.path.basename(path),
                "is_dir": False,
                "ltok": 0,
                "first_tag": None,
                "top_tags": [],
                "children": [],
            }, tag_totals, first_tag_keys

        tag_totals.update(file_info["total_counts"])
        if file_info["first_tag_key"]:
            first_tag_keys.add(file_info["first_tag_key"])
        return {
            "name": os.path.basename(path),
            "is_dir": False,
            "ltok": file_info["ltok"],
            "first_tag": file_info["first_tag"],
            "top_tags": file_info["top_tags"],
            "children": [],
        }, tag_totals, first_tag_keys

    return None, tag_totals, first_tag_keys


def format_tag_info(first_tag, top_tags):
    """Formats FirstTag + Top3Tags text."""
    if first_tag is None and not top_tags:
        return "-"
    if not top_tags:
        return first_tag
    top_text = " ".join(f"{count}{tag}" for tag, count in top_tags)
    return f"{first_tag} + {top_text}"


def print_file_tree(node, depth=0):
    """Prints directory tree lines."""
    indent = "  " * depth
    name = node["name"] + ("/" if node["is_dir"] else "")
    tag_text = format_tag_info(node["first_tag"], node["top_tags"])
    print(f"{indent}{name}, {node['ltok']} LTOK, {tag_text}")
    for child in node["children"]:
        print_file_tree(child, depth + 1)


def print_all(path_infos, tag_totals, first_tag_keys):
    """Prints final report."""
    print("== FILE TREE as Name, X LTok, FirstTag + Top3Tags ===")
    for path_info in path_infos:
        print_file_tree(path_info)
    print("== TAG TOTALS ===")
    keys = sorted(tag_totals.keys(), key=lambda tag: (-tag_totals[tag], tag))
    tail_keys = [tag for tag in keys if tag in first_tag_keys]
    keys = [tag for tag in keys if tag not in first_tag_keys] + tail_keys
    if keys:
        print(" ".join(f"{tag_totals[key]}{key}" for key in keys))


def main(argv):
    if not argv or argv[0] in {"-h", "--help"}:
        print_usage()
        return 0 if argv and argv[0] in {"-h", "--help"} else 1

    path_infos = []
    all_tag_totals = collections.Counter()
    all_first_tag_keys = set()

    for arg_path in argv:
        root_path = os.path.abspath(arg_path)
        repo_root = find_repo_root(root_path)

        if should_skip(root_path, repo_root):
            continue

        path_info, tag_totals, first_tag_keys = traverse(root_path, repo_root)
        if path_info is None:
            continue

        path_infos.append(path_info)
        all_tag_totals.update(tag_totals)
        all_first_tag_keys.update(first_tag_keys)

    print_all(path_infos, all_tag_totals, all_first_tag_keys)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
