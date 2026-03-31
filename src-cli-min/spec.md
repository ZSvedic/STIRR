--
tags: #Human
--

# #ConventionRL
Read [#STIRR](../stirr-skill/SKILL.md). 

# #SDD
- Implement the `stirr-tree.py` script, py3 shebang, just py stdlib, `__main__` check.
- Examples:
    - [tests/tests.csv](tests/tests.csv) lists all the tests.
    - `tests/*.correct` files contain the expected test outputs.
- Code spec:
```py
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
        r = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return r.returncode == 0
    except:
        return False
```
- Func `traverse` returns all info for files/dirs:
    - Skip hidden (`glob.glob()` default) and `.gitignore` files/dirs.
    - LTok = sum(parsed files from that dir).
- Func `get_text_file_info`, proceed only for text files <128KB. 
- Separate pure from printing funcs: `print_file_tree`, `print_file_info`, `print_tags`, and `print_all`.
- Print tags and frequencies: FirstTag + Top3Tags per file, in the end all tags.

# #TDD
- Red/green `local` tests.
- Manual `.gitignore` check.

# #ImplementRL
Follow the goals order, first make it correct, then make it maintainable:
- No large functions, break into smaller ones.
- Have a docstring if non-trivial func.
- Use normal var names like path and dir, not p and d. They are both 1 LTok.
- Try to make it <1000 LTok.
