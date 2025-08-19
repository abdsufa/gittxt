# gittxt

Local, Simple, Privacy-first exporter that turns a repository into a single **digest text file** optimized for LLM ingestion.

## Usage

```bash
$python3 git2txt.py /path/to/repo
```

### Options

`--max-bytes` : per-file size cap (default `1_000_000` bytes).

## Highlights

```bash
- Uses **`git ls-files`** for exact `.gitignore` fidelity (falls back to `os.walk` if not a Git repo).
- Skips binaries via **content sniffing** (not just by extension).
- Dynamic output name: **`gittxt-<repo_name>-repo.txt`**.
- Prioritizes **README.md** then **CHANGELOG.md**.
- Prints **token estimate** on completion.
- No external deps required 
    - optional: `tiktoken` for more accurate token counts -> $pip3 install tiktoken
```

## Example

```bash
python3 src/git2txt.py ~/projects/gittxt
# => writes ~/projects/my-repo/gittxt-my-repo-repo.txt
```

## Example Output

```bash
================================================
FILE: CHANGELOG.md
================================================
# Changelog

<file content ... >


================================================
FILE: CONTRIBUTING.md
================================================
<file content ... >


================================================
FILE: git2txt.py
================================================
#!/usr/bin/env python3
# git2txt.py --------

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import Iterable, List, Dict, Optional
import mimetypes

<file content ... >

================================================
FILE: LICENSE
================================================
# MIT License

Copyright (c) 2025 git2txt contributors

<file content ... >

```
