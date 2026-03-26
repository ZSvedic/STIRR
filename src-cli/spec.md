--
tags: #Human
--

- Read [#STIRR](../STIRR-rules.md). 
- Implement the `stirr-tree.py` script with py3 shebang, just py stdlib, `__main__` check.

# Examples
```bash
> ./stirr-tree.py -h
USAGE: 
  stirr-tree.py [--dry-run] PATH1 [PATH2 ...]
  stirr-tree.py --help

  <PATHx> ...
      A file(s)/dir(s) to check. 
  ...

> ./stirr-tree.py .
== FILE TREE as NAME SIZE (LOC LTOK) #FirstTag (Top 3 tags) ===
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
- LOC and LTOK:
```py
LEXTOK_RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')
def get_loc_lextokens(txt):
    lines = [l for l in txt.splitlines() if l.strip()]
    tokens = LEXTOK_RE.findall(txt)
    return (len(lines), len(tokens))
```

# Details
- Py func `traverse` traverses files/dirs and returns all info:
  - Dir size, loc, ltok calculated as sum(parsed files from that folder).
  - Use glob.glob() to recursively traverse non-hidden files (automatically skipped by glob). 
- For each file call function `get_text_file_info`, proceed only for text files <128KB. 
- Separate pure from printing funcs: `print_file_tree`, `print_file_info`, `print_hahstags`, and `print_all`.
- Print tags and frequencies: top 3 per file, in the end all tags.
- Display usage on --help, -h and no args.
- Print API keys envs (OPENAI_API_KEY and ANTHROPIC_API_KEY) after all tags.
- Each test:
    - Display Pass or FAIL: BashFailedCommandCommand.
    - Outputs analysis to a log file in the `tests` folder.
    - Works from any folder.
- Check that all tests pass.

# Current iteration
- Modify print functions to print to text stream.
- If `--dry-run` then:
    print to console
  else: 
    - Make a str/stream named `llm_query` with prompt to check project tree for #STIRR conformance. 
    - Append [STIRR-rules.md)](../STIRR-rules.md) to `llm_query` inside ```STIRR-rules.md ``` block.
    - Append `print_all` to `llm_query` inside ```bash ``` block.
    - If OPENAI_API_KEY or ANTHROPIC_API_KEY are provided, then make a call to with `llm_query` to one of them and print the result. If no key was provided, just print `llm_query` and print "COPY/PASTE TO YOUR LLM OF CHOICE."
- 'stirr-tree.py` < 1600 LTOK.