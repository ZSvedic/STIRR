#!/usr/bin/env -S uv run
# /// script
# dependencies = ["lizard"]
# ///
# #Human: A script to analyze code complexity using lizard and print a summary of NLOC, SumCCN, and SumToken for each file.
import sys, lizard

def analyze(paths):
    print("NLOC  | SumCCN | SumToken | File")
    for f in lizard.analyze(paths=paths):
        if not f.function_list: 
            continue
        fc = len(f.function_list)
        cc = sum(fn.cyclomatic_complexity for fn in f.function_list)
        tk = sum(fn.token_count for fn in f.function_list)
        print(f"{f.nloc:<5} | {cc:<6} | {tk:<8} | {f.filename}")

if __name__ == "__main__":
    analyze = analyze([
        sys.argv[1] if len(sys.argv)>1 
        else "."])