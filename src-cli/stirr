#!/usr/bin/env python3
import glob, os, re
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")


def fmt_size(n):
    return f"{n/1024:.2f}KB"


def get_file_text_hashtag(path):
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


def get_text_file_info(path):
    is_text, first = get_file_text_hashtag(path)
    try:
        size = os.path.getsize(path)
        if (not is_text) or size >= 128 * 1024:
            return None
        with open(path, encoding='utf-8', errors='ignore') as f:
            found = [t.lower() for t in TAG_RE.findall(f.read())]
        tags, order = Counter(found), {}
        for i, t in enumerate(found):
            order.setdefault(t, i)
        return {"name": os.path.basename(path), "path": path, "size": size, "first": first, "tags": tags, "order": order}
    except:
        return None


def traverse(path):
    node = {"name": os.path.basename(path.rstrip(os.sep)) or ".", "path": path, "size": 0, "dirs": [], "files": [], "totals": Counter()}
    for p in sorted(glob.glob(os.path.join(path, '*'))):
        if os.path.isdir(p):
            d = traverse(p)
            node["dirs"].append(d); node["size"] += d["size"]; node["totals"].update(d["totals"])
        elif os.path.isfile(p):
            fi = get_text_file_info(p)
            if fi:
                node["files"].append(fi); node["size"] += fi["size"]; node["totals"].update(fi["tags"])
    return node


def print_file_info(fi, indent=''):
    top = sorted(fi["tags"].items(), key=lambda kv: (-kv[1], fi["order"].get(kv[0], 10**9), kv[0]))[:5]
    top_s = ' '.join(f"{c}{t}" for t, c in top)
    first = f" {fi['first']}" if fi["first"] else ''
    tail = f" ({top_s})" if top_s else ''
    print(f"{indent}{fi['name']} {fmt_size(fi['size'])}{first}{tail}")


def print_file_tree(node, indent=''):
    label = '.' if indent == '' else f"{node['name']}/"
    print(f"{indent}{label} {fmt_size(node['size'])}")
    for d in node["dirs"]:
        print_file_tree(d, indent + '  ')
    for fi in node["files"]:
        print_file_info(fi, indent + '  ')


def print_hahstags(totals):
    print("TAG TOTALS:")
    print(' '.join(f"{c}{t}" for t, c in sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))))


def print_all(info):
    print("FILE TREE:")
    print_file_tree(info)
    print_hahstags(info["totals"])


if __name__ == '__main__':
    print_all(traverse('.'))
