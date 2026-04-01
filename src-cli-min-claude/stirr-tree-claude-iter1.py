#!/usr/bin/env python3
# #AI
import glob
import os
import re
import subprocess
import sys
from collections import Counter

# Regex for hashtags, test it online at: https://regexr.com/8lduo
TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
# Regex for lexical tokens, test it online at: https://regexr.com/8ldco
LTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')


def get_file_text_tag(path):
    """Checks if a text file and returns the first tag."""
    try:
        with open(path, 'rb') as f:
            chunk = f.read(4096)
        if b'\x00' in chunk:
            return (False, None)
        text = chunk.decode('utf-8', 'ignore')
        m = TAG_RE.search(text)
        return (True, m.group(0) if m else None)
    except:
        return (False, None)


def get_repo_root():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except:
        return None


def is_git_ignored(path, repo_root):
    """Checks `.gitignore` skipping rules."""
    try:
        r = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return r.returncode == 0
    except:
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
        text = open(path, encoding='utf-8', errors='ignore').read()
    except:
        return None
    raw_tags = TAG_RE.findall(text)
    counts, names = Counter(), {}
    for tag in raw_tags:
        key = tag.lower()
        counts[key] += 1
        if key not in names:
            names[key] = tag
    ltok = sum(1 for _ in LTOK_RE.finditer(text))
    return {'name': os.path.basename(path), 'ltok': ltok, 'first': first,
            'raw_tags': raw_tags, 'counts': counts, 'names': names}


def file_dir_ltok(file_info):
    """Adjusted LTok for directory accumulation (subtracts tag overhead)."""
    return max(0, file_info['ltok'] - len(file_info['counts']) - (1 if file_info['first'] else 0))


def new_dir_node(path):
    name = os.path.basename(path.rstrip(os.sep)) or path
    return {'name': name, 'ltok': 0, 'dirs': [], 'files': [], 'counts': Counter(), 'names': {}}


def merge_tags(node, counts, names):
    for key, count in counts.items():
        node['counts'][key] += count
        if key not in node['names']:
            node['names'][key] = names[key]


def traverse(path, repo_root):
    """Collects info for files/dirs, skipping hidden and git-ignored paths."""
    if is_git_ignored(path, repo_root):
        return None
    if os.path.isfile(path):
        file_info = get_text_file_info(path, repo_root)
        if not file_info:
            return None
        node = new_dir_node(path)
        node['files'] = [file_info]
        node['ltok'] = file_dir_ltok(file_info)
        merge_tags(node, file_info['counts'], file_info['names'])
        return node
    if not os.path.isdir(path):
        return None
    node = new_dir_node(path)
    for item_path in sorted(glob.glob(os.path.join(path, '*'))):
        if is_git_ignored(item_path, repo_root):
            continue
        if os.path.isdir(item_path):
            child = traverse(item_path, repo_root)
            if child:
                node['dirs'].append(child)
                node['ltok'] += child['ltok']
                merge_tags(node, child['counts'], child['names'])
        elif os.path.isfile(item_path):
            file_info = get_text_file_info(item_path, repo_root)
            if file_info:
                node['files'].append(file_info)
                node['ltok'] += file_dir_ltok(file_info)
                merge_tags(node, file_info['counts'], file_info['names'])
    return node


def top3_tags(file_info):
    """Top 3 tags excluding the first occurrence of first_tag, in frequency order."""
    counts = Counter(file_info['counts'])
    first_key = file_info['first'].lower() if file_info['first'] else None
    seen_first, order = False, {}
    for tag in file_info['raw_tags']:
        key = tag.lower()
        if first_key and key == first_key and not seen_first:
            seen_first = True
            counts[key] -= 1
            if counts[key] <= 0:
                del counts[key]
            continue
        if key in counts and key not in order:
            order[key] = len(order)
    return sorted(counts.items(), key=lambda kv: (-kv[1], order.get(kv[0], 10**9)))[:3]


def print_file_info(file_info, indent=''):
    first = file_info['first'] or '-'
    top3 = top3_tags(file_info)
    extra = ' + ' + ' '.join(f"{n}{file_info['names'][k]}" for k, n in top3) if top3 else ''
    print(f"{indent}{file_info['name']}, {file_info['ltok']} LTok, {first}{extra}")


def print_file_tree(node, indent=''):
    print(f"{indent}{node['name']}/, {node['ltok']} LTok, -")
    child_indent = indent + '  '
    for child in node['dirs']:
        print_file_tree(child, child_indent)
    for file_info in node['files']:
        print_file_info(file_info, child_indent)


def print_tags(counts, names, order):
    items = sorted(counts.items(), key=lambda kv: (-kv[1], order.get(kv[0], 10**9)))
    print(' '.join(f"{n}{names[k]}" for k, n in items))


def print_all(nodes):
    print("== FILE TREE as Name, X LTok, FirstTag + Top3Tags ===")
    all_counts, all_names, all_order = Counter(), {}, {}
    for node in nodes:
        print_file_tree(node)
        for key, count in node['counts'].items():
            all_counts[key] += count
            if key not in all_names:
                all_names[key] = node['names'][key]
                all_order[key] = len(all_order)
    print("== TAG TOTALS ===")
    print_tags(all_counts, all_names, all_order)


def print_usage():
    print("USAGE:")
    print("  stirr-tree.py PATH1 [PATH2 ...]")
    print("  stirr-tree.py --help")


def main(args):
    if not args or args[0] in {'-h', '--help'}:
        print_usage()
        return 0
    repo_root = get_repo_root()
    nodes = [node for arg in args if (node := traverse(os.path.normpath(arg), repo_root))]
    print_all(nodes)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
