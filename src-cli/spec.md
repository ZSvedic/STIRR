--
tags: #Human
--

## General
- Read [#STIRR](../STIRR-rules.md). To confirm reading rules, repeat hashtags of every rule in the CLI coding agent.
- Implement the `stirr` script as py with python3 shebang.
- Just py stdlib.
- Have py `__main__` check.
- Regex for hastags is r"(?<!\w)#[A-Za-z][\w-]*".
- Sizes in KB.
- Traversal of files/dirs in py function `traverse` that returns all info.
  - Dir size should be calculated as sum of parsed files from that folder, not filesystem size.
- Use glob.glob() to recursevly traverse everything except hidden files.
  - Hidden files/dirs are automatically skipped by glob(), no extra code for hidden. 
- For each file call function `get_text_file_info`:
  - Proceed only for:
    - text files, 
    - smaller than <128KB. 
  - Use this to test for text and first hashtag:
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
  - Find and return file size, is_text, first hashtag, and hashtags with their frequency.
- After processing a file, add hashtags to a global set and print in one line:
indent_dir_depth, filename_without_path, sizeKB, first tag found, and top 5 tags in the file with frequency.
- Separate pure from printing functions: `print_file_tree`, `print_file_info`, `print_hahstags`, and `print_all`.
- After all files print total tags with their frequency.
- Don't implement anything else.
- For example, this could be output:
```console
FILE TREE:
. 19.62KB
  STIRR-rules.md 6.71KB #Human (7#HC 6#FooBar 3#Human 2#AI)
  scripts/ 0.14KB
    test-file.txt 0.12KB #human (...
...
TAG TOTALS: 
101#HC 37#RH 20#FooBar ...
```
- Tests should:
  - Display Pass/FAIL.
  - Each test outputs file analysis to a log file in the same folder.
- Check tests pass.

## Iteration 8
- <100 LOC