#!/usr/bin/env python3
# #Human 
# Reviewed and edited output of Copilot CLI 1.0.14. (harness) + claude-sonnet-4.6 (model). 
# Prints a file tree with LTok counts and hashtag summaries.

import sys, os, glob, re, subprocess

USAGE = "USAGE:\n  stirr-tree.py PATH1 [PATH2 ...]\n  stirr-tree.py --help\n"

# Regex for hashtags, test it online at: https://regexr.com/8lduo
TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")

# Regex for lexical tokens, test it online at: https://regexr.com/8ldco
LTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')


def get_file_text_tag(path):
    '''Checks if a text file and returns the first tag.'''
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

def is_git_ignored(path, repo_root):
    '''Checks `.gitignore` skipping rules.'''
    try:
        rel = os.path.relpath(os.path.abspath(path), repo_root)
        r = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", rel],
             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return r.returncode == 0
    except:
        return False

def find_repo_root(path):
    try:
        r = subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    except:
        return None

def get_text_file_info(path):
    '''Returns (ltok, first_tag, tags) for a text file <128KB; first_tag and tags
    count all occurrences except the first (which is displayed as FirstTag).'''
    is_text, _ = get_file_text_tag(path)
    if not is_text:
        return None
    try:
        if os.path.getsize(path) >= 128 * 1024:
            return None
        text = open(path, 'rb').read().decode('utf-8', 'ignore')
    except:
        return None
    ltok = len(LTOK_RE.findall(text))
    matches = [m.group(0) for m in TAG_RE.finditer(text)]
    if not matches:
        return (ltok, None, [])
    first_tag = matches[0]
    first_key = first_tag.lower()
    counts = {}
    for tag in matches[1:]:
        key = tag.lower()
        if key not in counts:
            counts[key] = [first_tag if key == first_key else tag, 0]
        counts[key][1] += 1
    if first_key not in counts:
        counts[first_key] = [first_tag, 0]
    tags = sorted(counts.values(), key=lambda x: (-x[1], x[0].lower()))
    return (ltok, first_tag, tags)

def collect_global_tags(tag_infos):
    '''Merges per-file tag info into global counts (restoring the first occurrence).
    Returns list of (canonical, count) sorted by count desc then first-seen order.
    '''
    global_tags = {}
    for info in tag_infos:
        ltok, first_tag, tags = info
        key = first_tag.lower()
        if key not in global_tags:
            global_tags[key] = [first_tag, 0]
        global_tags[key][1] += 1
        for canonical, count in tags:
            k = canonical.lower()
            if k not in global_tags:
                global_tags[k] = [canonical, 0]
            global_tags[k][1] += count
    return sorted(global_tags.values(), key=lambda x: -x[1])

def traverse(root_path, repo_root):
    '''Returns (dir_ltok, children) for a directory, skipping hidden/.gitignored items.
    Each child is (name, is_dir, ltok, tag_info, sub_children).
    '''
    children = []
    for item in sorted(glob.glob(os.path.join(root_path, '*'))):
        if repo_root and is_git_ignored(item, repo_root):
            continue
        name = os.path.basename(item)
        if os.path.isdir(item):
            sub_ltok, subs = traverse(item, repo_root)
            children.append((name, True, sub_ltok, None, subs))
        else:
            info = get_text_file_info(item)
            children.append((name, False, info[0] if info else 0, info, []))
    return (sum(c[2] for c in children), children)

def format_tags(first_tag, tags):
    if first_tag is None:
        return "-"
    top3 = [f"{count}{canonical}" for canonical, count in tags[:3] if count > 0]
    return (first_tag + " + " + " ".join(top3)) if top3 else first_tag

def print_file_tree(children, indent=0):
    prefix = "  " * indent
    for name, is_dir, ltok, info, subs in children:
        if is_dir:
            print(f"{prefix}{name}/, {ltok} LTok, -")
            print_file_tree(subs, indent + 1)
        else:
            first_tag = info[1] if info else None
            tags = info[2] if info else []
            print(f"{prefix}{name}, {ltok} LTok, {format_tags(first_tag, tags)}")

def collect_all_tag_info(children):
    result = []
    for name, is_dir, ltok, info, subs in children:
        if is_dir:
            result.extend(collect_all_tag_info(subs))
        elif info and info[1] is not None:
            result.append(info)
    return result

def print_tags(global_tags):
    print("== TAG TOTALS ===")
    print(" ".join(f"{count}{canonical}" for canonical, count in global_tags))

def print_all(paths):
    '''Main entry: traverses paths and prints file tree + tag totals.'''
    root = paths[0] if os.path.isdir(paths[0]) else os.path.dirname(paths[0])
    repo_root = find_repo_root(os.path.abspath(root))
    all_children = []
    for path in paths:
        path = os.path.normpath(path)
        if os.path.isdir(path):
            dir_ltok, subs = traverse(path, repo_root)
            all_children.append((os.path.basename(path), True, dir_ltok, None, subs))
        elif os.path.isfile(path):
            info = get_text_file_info(path)
            all_children.append((os.path.basename(path), False, info[0] if info else 0, info, []))
    print("== FILE TREE as Name, X LTok, FirstTag + Top3Tags ===")
    print_file_tree(all_children)
    tag_infos = collect_all_tag_info(all_children)
    if tag_infos:
        print_tags(collect_global_tags(tag_infos))

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "--help" in args or "-h" in args:
        print(USAGE, end="")
        sys.exit(0)
    print_all(args)
