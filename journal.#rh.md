2026-3-17
- Iteration 1
  - ToDo
- Iteration 3
  - Hashtag regex: `(?<!\w)#([A-Za-z][A-Za-z0-9+-]*)` (case-insensitive in logic by lowercasing).
  - Text/markdown/code detection: extension allow-list (`.txt`, `.md`, and common code/config extensions), file size `<100KB`, and first 4KB must not contain NUL byte.
