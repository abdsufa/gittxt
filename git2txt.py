#!/usr/bin/env python3
# git2txt.py --------

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import Iterable, List, Dict, Optional
import mimetypes

PRIORITY_FILES = ["README.md", "CHANGELOG.md"]

DEFAULT_IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
}

DEFAULT_IGNORE_FILES = {".DS_Store", "Thumbs.db"}


def which(cmd: str) -> bool:
    from shutil import which as _which

    return _which(cmd) is not None


def is_git_repo(root: Path) -> bool:
    return (root / ".git").exists() and (root / ".git").is_dir()


def git_list_files(root: Path) -> List[str]:
    cmd = ["git", "-C", str(root), "ls-files", "-z", "-co", "--exclude-standard"]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    return [s.decode("utf-8", errors="replace") for s in out.split(b"\x00") if s]


def fallback_walk(root: Path) -> List[str]:
    results: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE_DIRS]
        for fn in filenames:
            if fn in DEFAULT_IGNORE_FILES:
                continue
            rel = Path(dirpath).relative_to(root) / fn
            results.append(rel.as_posix())
    return results


def is_probably_text(path: Path, max_probe: int = 8192) -> bool:
    mime, _ = mimetypes.guess_type(str(path))
    if mime and any(
        mime.startswith(x) for x in ("image/", "audio/", "video/", "font/")
    ):
        return False
    if mime in {
        "application/zip",
        "application/x-tar",
        "application/gzip",
        "application/pdf",
    }:
        return False
    try:
        with path.open("rb") as f:
            chunk = f.read(max_probe)
        if b"\x00" in chunk:
            return False
    except Exception:
        return False
    return True


def load_text(path: Path, encoding="utf-8") -> Optional[str]:
    try:
        return path.read_text(encoding=encoding, errors="replace")
    except Exception:
        return None


def filter_files(root: Path, rels: Iterable[str], max_bytes: int) -> List[Path]:
    out: List[Path] = []
    for r in rels:
        p = root / r
        if not p.is_file():
            continue
        try:
            if p.stat().st_size > max_bytes:
                continue
        except OSError:
            continue
        if not is_probably_text(p):
            continue
        out.append(p)
    return sorted(out, key=lambda p: p.as_posix().lower())


def build_tree(paths: List[Path], root: Path) -> str:
    tree: Dict[str, Dict] = {}

    def insert(parts):
        node = tree
        for part in parts:
            node = node.setdefault(part, {})

    for p in paths:
        insert(p.relative_to(root).parts)

    def render(node, prefix=""):
        keys = sorted(node.keys(), key=str.lower)
        lines = []
        for i, k in enumerate(keys):
            last = i == len(keys) - 1
            connector = "└── " if last else "├── "
            lines.append(prefix + connector + k + ("/" if node[k] else ""))
            if node[k]:
                ext = "    " if last else "│   "
                lines.extend(render(node[k], prefix + ext))
        return lines

    lines = ["└── " + root.name + "/"]
    lines.extend(render(tree, "    "))
    return "\n".join(lines)


def estimate_tokens(text: str) -> int:
    try:
        import tiktoken

        enc = tiktoken.get_encoding("o200k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4


def assemble_digest(root: Path, files: List[Path], encoding="utf-8") -> str:
    tree = "Directory structure:\n" + build_tree(files, root) + "\n"
    sections = [tree]

    def sort_key(p: Path):
        name = p.name
        if name in PRIORITY_FILES and p.parent == root:
            return (0, PRIORITY_FILES.index(name))
        return (1, p.as_posix().lower())

    files_sorted = sorted(files, key=sort_key)
    for p in files_sorted:
        txt = load_text(p, encoding)
        if txt is None:
            continue
        rel = p.relative_to(root).as_posix()
        sections.append(
            "================================================\n"
            f"FILE: {rel}\n"
            "================================================\n"
            f"{txt}\n"
        )
    return "\n".join(sections)


def main():
    ap = argparse.ArgumentParser(
        description="Export a repo into a single text digest for LLMs."
    )
    ap.add_argument("path", help="Path to Git repo or folder")
    ap.add_argument(
        "--max-bytes",
        type=int,
        default=1_000_000,
        help="Skip files larger than this (default 1MB).",
    )
    args = ap.parse_args()
    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        sys.exit(1)
    repo_name = root.name
    output_filename = f"gittxt-{repo_name}-repo.txt"
    output_path = root / output_filename
    try:
        if is_git_repo(root) and which("git"):
            rels = git_list_files(root)
        else:
            rels = fallback_walk(root)
    except subprocess.CalledProcessError:
        rels = fallback_walk(root)
    files = filter_files(root, rels, args.max_bytes)
    files = [p for p in files if p.name != output_filename]
    digest = assemble_digest(root, files)
    output_path.write_text(digest, encoding="utf-8")
    tokens = estimate_tokens(digest)
    print(f"[git2txt] Export success -> {output_path}")
    print(f"[git2txt] Files included: {len(files)} | Tokens ~{tokens:,}")


if __name__ == "__main__":
    main()
