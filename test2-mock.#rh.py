#!/usr/bin/env python3
import io, os, re, shutil, tempfile, types
from contextlib import redirect_stdout
from importlib.machinery import SourceFileLoader

mod = types.ModuleType("stirr")
SourceFileLoader("stirr", "./stirr.#rh").exec_module(mod)

tmp = tempfile.mkdtemp()
log_path = "test2-mock.log"
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

    out = io.StringIO()
    with redirect_stdout(out):
        mod.traverse(tmp)
    txt = out.getvalue()
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(txt)

    assert "FILE TREE:" in txt and "TAG TOTALS:" in txt
    assert re.search(r"a\.md .* 2#foo 1#bar", txt)
    assert re.search(r"b\.txt .* 1#foo 1#foo-bar", txt)
    assert "3#foo 1#bar 1#foo-bar" in txt
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
