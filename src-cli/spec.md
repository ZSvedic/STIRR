--
tags: #Human
--

## General
- Read [#STIRR](../STIRR-rules.md). 
- Implement the `stirr.py` script as: 
  - py with python3 shebang.
  - Just py stdlib.
  - Use a py `__main__` check.
- Example:
```console
> ./stirr.py
FILE TREE:
. 19.62KB
  STIRR-rules.md 6.71KB #Human (7#HC 6#FooBar 3#Human 2#AI)
  scripts/ 0.14KB
    test-file.txt 0.12KB #human (...
...
TAG TOTALS: 
101#HC 37#RH 20#FooBar ...
```
- Regex for hashtags is `r"(?<!\w)#[A-Za-z][\w-]*"`.
- Code for text detection and the first tag:
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
- Py func `traverse` traverses files/dirs and returns all info:
  - Dir size = sum(parsed files from that folder).
  - Use glob.glob() to recursively traverse all except hidden files (automatically skipped by glob). 
- For each file call function `get_text_file_info`, proceed only for text files smaller than <128KB. 
- Separate pure from printing functions: `print_file_tree`, `print_file_info`, `print_hahstags`, and `print_all`.
- Print tags and frequencies: top 5 per file, in the end all tags.
- Tests display Pass/FAIL, each test outputs analysis to a log file in the `tests` folder.

## Iteration 2
- Display usage and accept args, e.g. (improve):
```console
> ./stirr.py -h
USAGE: 
  stirr.py [--dry-run] PATH1 [PATH2 ...]
  stirr.py --help

  <PATHx> ...
      A file(s)/dir(s) to check. 
  ...
```
- Create bash test3-help.sh to check if either -h, --help, or calling without PATH, displays help by searching for "USAGE:".
- Create bash test4-dry-run.sh to check if "--dry-run" displays file tree by searching for "test-dir", "test-hashtags.txt", and "#FooBar".
- Print API keys envs (OPENAI_API_KEY and ANTHROPIC_API_KEY) after all tags.
- Use [lizard](lizard-filter.py) to check `stirr.py` script has SumToken <1000. 
