--
tags: #Human
--

- Read [#STIRR](../STIRR-rules.md). 
- Implement the `stirr.py` script with py3 shebang, just py stdlib, `__main__` check.

# Examples
```bash
> ./stirr.py -h
USAGE: 
  stirr.py [--dry-run] PATH1 [PATH2 ...]
  stirr.py --help

  <PATHx> ...
      A file(s)/dir(s) to check. 
  ...

> ./stirr.py .
== FILE TREE as NAME SIZE (NLOC LTOK) #FirstTag (Top 3 tags) ===
src-cli/ 121.92 KB (3246 NLOC 28147 LTOK)
·ai-output.log 102.93 KB (2694 NLOC 23685 LTOK) #AI (16#textrl 14#conventionrl 13#human)
·implement.sh 0.18 KB (8 NLOC 54 LTOK) #Human (1#human)
...
··test-dir/ 0.08 KB (8 NLOC 32 LTOK)
···#AI.#Test 0.00 KB (0 NLOC 0 LTOK)
···test-hashtags.txt 0.08 KB (8 NLOC 32 LTOK) #human (4#foo 3#foobar 2#bar)
...
== TAG TOTALS ===
22#human 17#foo 17#textrl 14#conventionrl ...
OPENAI_API_KEY=oi...
ANTHROPIC_API_KEY=an...
```

# Code spec
- Regex for hashtags is `r"(?<!\w)#[A-Za-z][\w-]*"`.
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
- NLOC and LTOK:
```py
LEXTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')
def get_nloc_lextokens(txt):
    lines = [l for l in txt.splitlines() if l.strip()]
    tokens = LEXTOK_RE.findall(txt)
    return (len(lines), len(tokens))
```

# Details
- Py func `traverse` traverses files/dirs and returns all info:
  - Dir size, nloc, ltok calculated as sum(parsed files from that folder).
  - Use glob.glob() to recursively traverse non-hidden files (automatically skipped by glob). 
- For each file call function `get_text_file_info`, proceed only for text files <128KB. 
- Separate pure from printing funcs: `print_file_tree`, `print_file_info`, `print_hahstags`, and `print_all`.
- Print tags and frequencies: top 3 per file, in the end all tags.
- Display usage on --help, -h and no args.
- Print API keys envs (OPENAI_API_KEY and ANTHROPIC_API_KEY) after all tags.
- Tests display Pass/FAIL, each test outputs analysis to a log file in the `tests` folder.

# Current iteration
- Make `test2-mock.py` work from any folder (like test1 works), not just from parent folder.
    - Create a bash version of test2 as `test2-mock.sh`, try to make it shorter than py version. 
- Check that all tests that FAIL also display what failed.
- There is `stirr-old.py` but that is too complex for human review. 
    - Make a new `stirr.py` that is <1000 LTOK. 
    - Use `stirr-old.py` to check LTOK.