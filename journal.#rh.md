2026-3-17
- Iteration 3
  - Hashtag regex: r"(?<!\w)#[A-Za-z][\w-]*" (case-insensitive in logic by lowercasing).
  - Text/markdown/code detection code: 
  ```py
  def is_text_file(path):
    try:
        with open(path, 'rb') as f:
            chunk = f.read(4096)
        return b'\x00' not in chunk
    except:
        return False
  ```
- Iteration 4
  
