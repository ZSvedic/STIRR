Read `#STIRR`.

## Iteration 3
- Implement the `stirr.#hc` script as py with python3 shebang.
- Requirements:
    - Just py stdlib.
    - Have py `__main__` check.
    - <50 LOC of py code, but don't cheat, LOC longer than 80 into multiple lines.
    - Add one-liner comments where needed. 
- Features:
    - Traversal and printing of file/dir sizes in KB in py function `traverse`.
    - Use glob.glob() to recursevly traverse everything except hidden files.
    - For each file:
        - Proceed only for text, md, or code file (add to journal how to detect) and is <100KB.
        - Find hashtags inside those files (e.g. #HC, #FooBar, #foo-bar etc., add to journal exact regex), and add them to a specific file set and total set. 
        - Each file should be printed in one line with: 
        indent_dir_depth, filename_without_path, file_sizeKB, and top 5 tags in the file.
    - After all files print total tags with their frequency.
    - Don't implement anything else.
- Check that the test passes.
- For example, this could be output (check it is logical):
```console
FILE TREE:
. 19.6KB
  STIRR-rules.md 6.7KB 7#HC 6#FooBar
  /scripts/ 0.1KB
    test-file.txt 0.1KB 2#RH
...
TAG TOTALS: 
101#HC 37#RH 20#FooBar ...
```
