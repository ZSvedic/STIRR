--
tags: #Human
--

## Iteration 3
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

## Iteration 6
- Code for detection of both text type and finding the first hashtag:
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