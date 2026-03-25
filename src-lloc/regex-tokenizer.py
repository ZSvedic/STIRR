#!/usr/bin/env python3
import re, os
# #Human
# A regex tokenizer that counts the # of lexical tokens / NLOC (non-empty lines) in each text file.

# Test online: https://regexr.com/8ldco
RE = re.compile(r'"(\\.|[^"])*"|\'(\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')

print(f"{'NLOC':<5} | {'SumToken':<8} | File")

for dp,_,fs in os.walk('.'):
    for f in fs:
        p = os.path.join(dp,f)
        try:
            s = open(p,encoding='utf-8',errors='ignore').read()
        except:
            continue
        lines = [l for l in s.splitlines() if l.strip()]
        tokens = RE.findall(s)
        print(f"{len(lines):<5} | {len(tokens):<8} | {p}")