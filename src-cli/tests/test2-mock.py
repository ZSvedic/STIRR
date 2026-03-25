#!/usr/bin/env python3
# #AI

import io, os, shutil, tempfile, types
from contextlib import redirect_stdout
from importlib.machinery import SourceFileLoader

mod = types.ModuleType("stirr.py")
SourceFileLoader("stirr.py", "./stirr.py").exec_module(mod)

tmp = tempfile.mkdtemp()
log_path = "tests/test2-mock.log"
ok = False
try:
    os.makedirs(os.path.join(tmp, "sub"), exist_ok=True)
    os.makedirs(os.path.join(tmp, ".hidden"), exist_ok=True)
    with open(os.path.join(tmp, "a.md"), "w", encoding="utf-8") as f:
        f.write("#Foo #foo #Bar\n")
    with open(os.path.join(tmp, "sub", "b.txt"), "w", encoding="utf-8") as f:
        f.write("#foo-bar #Foo\n")
    with open(os.path.join(tmp, ".hidden", "skip.md"), "w", encoding="utf-8") as f:
        f.write("#NOPE\n")
    with open(os.path.join(tmp, "sub", "bin.dat"), "wb") as f:
        f.write(b"\x00\x01\x02")

    info = mod.traverse(tmp)
    assert isinstance(info, dict) and "files" in info and "totals" in info

    out = io.StringIO()
    with redirect_stdout(out):
        mod.print_all(info)
    txt = out.getvalue()
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(txt)

    assert "FILE TREE:" in txt and "TAG TOTALS:" in txt
    assert "a.md" in txt and "#Foo (2#foo 1#bar)" in txt
    assert "b.txt" in txt and "#foo-bar (1#foo-bar 1#foo)" in txt
    assert "3#foo 1#bar 1#foo-bar" in txt or "3#foo 1#foo-bar 1#bar" in txt
    assert "skip.md" not in txt and "bin.dat" not in txt
    ok = True
except Exception as e:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\nERROR: {e}\n")
finally:
    shutil.rmtree(tmp)

print("Pass" if ok else "FAIL")
if not ok:
    raise SystemExit(1)
