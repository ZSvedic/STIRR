--
tags: #Human
--

- Read [#STIRR](../stirr-skill/SKILL.md). 
- Implement the `stirr-tree.py` script with py3 shebang, just py stdlib, `__main__` check.

# Examples
```bash
> ./stirr-tree.py -h
USAGE: 
  stirr-tree.py PATH1 [PATH2 ...]
  stirr-tree.py --help

  <PATHx> ...
      A file(s)/dir(s) to check. 
  ...

> ./stirr-tree.py .
== FILE TREE as NAME SIZE (LOC LTOK) FirstTag (Top 3 tags) ===
src-cli/ 121.92 KB (3246 LOC 28147 LTOK)
·ai-output.log 102.93 KB (2694 LOC 23685 LTOK) #AI (16#textrl 14#conventionrl 13#human)
·implement.sh 0.18 KB (8 LOC 54 LTOK) #Human (1#human)
...
··test-dir/ 0.08 KB (8 LOC 32 LTOK)
···#AI.#Test 0.00 KB (0 LOC 0 LTOK)
···test-hashtags.txt 0.08 KB (8 LOC 32 LTOK) #human (4#foo 3#foobar 2#bar)
...
== TAG TOTALS ===
22#human 17#foo 17#textrl 14#conventionrl ...
```

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
- Py func `traverse` traverses files/dirs and returns all info:
  - Dir size, loc, ltok calculated as sum(parsed files from that folder).
  - Use glob.glob() to recursively traverse non-hidden files (automatically skipped by glob). 
  - Ignore all files/dirs specified in `.gitignore`.
- For each file call function `get_text_file_info`, proceed only for text files <128KB. 
- Separate pure from printing funcs: `print_file_tree`, `print_file_info`, `print_hahstags`, and `print_all`.
- Print tags and frequencies: top 3 per file, in the end all tags.
- Display usage on --help, -h and no args.
- Each test:
    - Display Pass or FAIL: bash_failed_cmd.
    - Outputs analysis to a log file in the `tests` folder.
    - Works from any folder.
- Implementation in `stirr-tree.py`:
    - Below 1500 LTOK. Use normal variable names like path and dir, not p and d. They are both 1 LTOK.  
    - No large functions, break into smaller ones.
    - Keep current recursive parsing architecture. 
    - Separate functions for git ignore check.
- You are done when tests 1-3 pass and .gitignore works.

# Current iteration
- `stirr-tree.py` and `tests/` are perfect, don't change them.
- However `implement-*` and `stirr-check.sh`:
    - Currently support only codex and claude agents.
    - In `stirr-check.sh`: add support for 'copilot' (`copilot --help`) and 'cursor' (`agent --help`) commands, both are installed on this machine.
    - Make new `implement.sh` with the same logic as `stirr-check.sh` (arg for provider): 
      USAGE: implement.sh <codex|claude|copilot|cursor>
    - Just add minimal lines to implement the changes above.
- Make new `install-skill.sh` with installs [../stirr-skill/](../stirr-skill/) to 4 cli agent default path below. 
    For first 3, take a look at paths from this unrelated skill:
    ```bash
    mkdir -p \
    /root/.copilot/skills \
    /root/.claude/skills \
    /root/.codex/skills

    cp -r /gembox-skills/gembox-skill /root/.copilot/skills/gembox-skill
    cp -r /gembox-skills/gembox-skill /root/.claude/skills/gembox-skill
    cp -r /gembox-skills/gembox-skill /root/.codex/skills/gembox-skill
    ```
    Google for def cursor path. 
    But, try not to copy skill dir but make a symbolic link it, so it changes with updates to skill.
    I will test that one manually.