Read `#STIRR`.

## Iteration 5
- Implement the `stirr.#hc` script as py with python3 shebang.
- Requirements:
    - Just py stdlib.
    - Have py `__main__` check.
    - <60 LOC of py code, but don't cheat:
      - LOC longer than 80 into multiple lines.
      - Empty rows between functions and declarations.
    - Add one-liner comments where needed. 
- Features:
    - Traversal and printing of file/dir sizes in KB in py function `traverse`.
      - Dir size should be calculated as sum of parsed files from that folder, not filesystem size.
    - Use glob.glob() to recursevly traverse everything except hidden files.
      - I think hidden files/dirs are automatically skipped by glob(), so no extra function for that is needed. 
    - For each file:
        - Proceed only for text files smaller than <100KB. Use this to test for text:
        ```py
def is_text_file(path):
    try:
        with open(path, 'rb') as f:
            chunk = f.read(2048)
        return b'\x00' not in chunk
    except:
        return False
        ```
        - Find hashtags inside those files (r"(?<!\w)#[A-Za-z][\w-]*" regex), and add them to a specific file set and total set. 
        - Each file should be printed in one line with: 
        indent_dir_depth, filename_without_path, sizeKB, and top 5 tags in the file.
    - After all files print total tags with their frequency.
    - Don't implement anything else.
- For example, this could be output:
```console
FILE TREE:
. 19.62KB
  STIRR-rules.md 6.71KB 7#HC 6#FooBar
  scripts/ 0.14KB
    test-file.txt 0.12KB 2#RH
...
TAG TOTALS: 
101#HC 37#RH 20#FooBar ...
```
- Tests should:
  - Display Pass/FAIL.
  - Each test outputs file analysis to a log file.
- Check tests pass.
