--
tags: #Human
--

- Read [#STIRR](../stirr-skill/SKILL.md). 
- Implement the `stirr-tree.py` script with py3 shebang, just py stdlib, `__main__` check.

# Examples
- [tests/tests.csv](tests/tests.csv) lists all tests.
- [tests/*.correct](tests/*.correct) files contain correct tests output.

# Code spec
- Regex for hashtags is `r"(?<!\w)#[A-Za-z][\w-]*"`.
- LOC and LTOK:
```py
LEXTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')
def get_loc_lextokens(txt):
    lines = [l for l in txt.splitlines() if l.strip()]
    tokens = LEXTOK_RE.findall(txt)
    return (len(lines), len(tokens))
```
- Text and first tag detection:
```py
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
```
- `.gitignore` skipping:
```py
def is_git_ignored(path, repo_root):
    try:
        r = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return r.returncode == 0
    except:
        return False
```

# Details
- Func `traverse` returns all info for files/dirs:
    - Skip hidden (`glob.glob()` default) and `.gitignore` files/dirs.
    - LTok = sum(parsed files from that dir).
- Func `get_text_file_info`, proceed only for text files <128KB. 
- Separate pure from printing funcs: `print_file_tree`, `print_file_info`, `print_hahstags`, and `print_all`.
- Print tags and frequencies: FirstTag + Top3Tags per file, in the end all tags.
- `stirr-tree.py` implementation:
    - Below 1400 LTok. Use normal variable names like path and dir, not p and d. They are both 1 LTOK.  
    - No large functions, break into smaller ones.
- #TDD: done when `local` tests pass and .gitignore works.
