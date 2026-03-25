--
tags: #Human
--

- Read [#STIRR](../STIRR-rules.md). 
- Implement the `stirr.py` script with py3 shebang, just py stdlib, `__main__` check.

## Examples
```bash
> ./stirr.py -h
USAGE: 
  stirr.py [--dry-run] PATH1 [PATH2 ...]
  stirr.py --help

  <PATHx> ...
      A file(s)/dir(s) to check. 
  ...

> ./stirr.py .
FILE TREE:
src-cli/ 86.20 KB (17218 NLOC 69739 LTOK)
·ai-output.log 74.68 KB (1721 NLOC 6973 LTOK) #AI (16#textrl 16#conventionrl 16#sdd) 
·example.txt 0.00 KB (0 NLOC, 0 LTOK)
·implement.sh 0.18 KB (8 NLOC 54 LTOK) #Human (1#human) 
...
·tests/ 3.55 KB (1218 NLOC 6739 LTOK)
··test1-run.log 0.11 KB (5 NLOC 44 LexTok) 
...
TAG TOTALS:
20#textrl 19#conventionrl 19#hitl 19#implementrl...
OPENAI_API_KEY=oi487356...
ANTHROPIC_API_KEY=an3742...
```

## Code spec
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

## Details
- Py func `traverse` traverses files/dirs and returns all info:
  - Dir size, nloc, ltok calculated as sum(parsed files from that folder).
  - Use glob.glob() to recursively traverse non-hidden files (automatically skipped by glob). 
- For each file call function `get_text_file_info`, proceed only for text files <128KB. 
- Separate pure from printing funcs: `print_file_tree`, `print_file_info`, `print_hahstags`, and `print_all`.
- Print tags and frequencies: top 3 per file, in the end all tags.
- Display usage on --help, -h and no args.
- Print API keys envs (OPENAI_API_KEY and ANTHROPIC_API_KEY) after all tags.
- Tests display Pass/FAIL, each test outputs analysis to a log file in the `tests` folder.
