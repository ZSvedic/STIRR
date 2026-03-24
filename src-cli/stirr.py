#!/usr/bin/env python3
import glob
import os
import re
import sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
RULE_TAGS = "#TextRL #ConventionRL #SDD #TDD #ImplementRL #HITL #RepeatRL"
MAX_TEXT_FILE_SIZE = 128 * 1024
HELP_TEXT = """USAGE:
  stirr.py [--dry-run] PATH1 [PATH2 ...]
  stirr.py --help

  <PATHx> ...
      A file(s)/dir(s) to check.
"""
