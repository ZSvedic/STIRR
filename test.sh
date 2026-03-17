#!/usr/bin/env bash

pattern='#[^[:space:]]+'

rg -n "$pattern" --no-hidden . | cut -d: -f1 | sort | uniq -c   # matches per file
du -Aak . | grep -v '/\.'                                       # sizes (KB)