#!/usr/bin/env python3
"""install_skill.py — 把 GitHub 上的一个 skill 目录装进本地 skills 目录，装前全文安检。
Install a skill folder from GitHub into a local skills directory, with a
pre-install full-text screening. Pure stdlib, zero deps, no git required.

流程 / What it does:
  1. 解析 github tree 链接 → owner/repo/ref/path
  2. 用 GitHub trees API 列出该目录全部文件（含 scripts/，不只 SKILL.md）
  3. 逐文件下载（raw 直链，不计 core 配额）
  4. 全文安检：可疑关键词 + 已知安装器注入指纹 —— 命中默认拒装，
     必须人审后加 --force 才落盘
  5. 落盘到 --dest（默认 ~/.claude/skills/<name>），已存在则拒绝覆盖

用法 / Usage:
  python3 install_skill.py <github-tree-url> [--name <folder>] [--dest <dir>]
                           [--dry-run] [--force]
  --dry-run 只下载+安检+列清单，不落盘（推荐先跑一次）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request

UA = "skill-recruiter/0.1"

SUSPICIOUS_PATTERNS = [
    "curl ", "wget ", "rm -rf", "sudo ", "chmod ", "eval(", "base64 -d",
    "pip install", "npm install", "api_key", "password", "secret",
]
INJECTION_SIGNATURES = [
    ("agentskill.sh telemetry block", "agentskill.sh"),
    ("silent-report instruction", "silently rate"),
]
TEXT_EXT = {".md", ".py", ".sh", ".txt", ".json", ".yaml", ".yml", ".toml", ".js", ".ts"}


def http_get(url: str, headers: dict | None = None, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def gh_headers() -> dict:
    h = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def parse_tree_url(url: str):
    """github.com/<o>/<r>/tree/<ref>/<path> | github.com/<o>/<r> → 四元组"""
    url = url.strip().rstrip("/")
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)", url)
    if m:
        return m.group(1), m.group(2), m.group(3), m.group(4)
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)$", url)
    if m:  # 仓库根即 skill 根 / repo root is the skill root
        repo = json.loads(http_get(
            f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}", gh_headers()))
        return m.group(1), m.group(2), repo.get("default_branch", "main"), ""
    raise SystemExit(f"unsupported url: {url}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="github tree url of the skill folder (or repo root)")
    ap.add_argument("--name", default="", help="目标文件夹名，默认取路径末段")
    ap.add_argument("--dest", default=os.path.expanduser("~/.claude/skills"),
                    help="skills 目录 (default: ~/.claude/skills)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="安检命中时仍然安装（必须先人审）/ install despite findings")
    args = ap.parse_args()

    owner, repo, ref, path = parse_tree_url(args.url)
    name = args.name or (path.rstrip("/").split("/")[-1] if path else repo)

    tree = json.loads(http_get(
        f"https://api.github.com/repos/{owner}/{repo}/git/trees/{ref}?recursive=1",
        gh_headers()))
    prefix = f"{path}/" if path else ""
    files = [t["path"] for t in tree.get("tree", [])
             if t["type"] == "blob" and t["path"].startswith(prefix)]
    if not files:
        raise SystemExit(f"no files under '{path or '/'}' in {owner}/{repo}@{ref}")
    if not any(f.endswith("SKILL.md") for f in files):
        print("WARNING: no SKILL.md found — not a standard skill folder")

    findings = []
    blobs: dict[str, bytes] = {}
    for f in files:
        raw = http_get(f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{f}")
        blobs[f] = raw
        if os.path.splitext(f)[1].lower() in TEXT_EXT:
            text = raw.decode("utf-8", errors="replace")
            low = text.lower()
            for label, needle in INJECTION_SIGNATURES:
                if needle in low:
                    findings.append({"file": f, "type": "injection", "label": label})
            for line in text.splitlines():
                if any(k in line.lower() for k in SUSPICIOUS_PATTERNS):
                    findings.append({"file": f, "type": "suspicious",
                                     "line": line.strip()[:160]})

    report = {
        "skill": name, "source": f"{owner}/{repo}@{ref}/{path}",
        "file_count": len(files),
        "files": [f[len(prefix):] for f in files],
        "findings_count": len(findings),
        "findings": findings[:40],
        "hint": ("findings 是启发式目检（讲安全的 skill 会自指误报），逐条人审；"
                 "重型扫描交专业工具 / findings are heuristics — human-review them; "
                 "use a dedicated scanner for serious vetting"),
    }

    target = os.path.join(os.path.expanduser(args.dest), name)
    if args.dry_run:
        report["dry_run"] = True
    elif findings and not args.force:
        report["installed"] = False
        report["refused"] = "findings non-empty; review them, then re-run with --force"
    elif os.path.exists(target):
        report["installed"] = False
        report["refused"] = f"{target} already exists — remove it first or use --name"
    else:
        for f, raw in blobs.items():
            dst = os.path.join(target, f[len(prefix):])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "wb") as fh:
                fh.write(raw)
        report["installed"] = True
        report["target"] = target
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
