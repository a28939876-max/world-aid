#!/usr/bin/env python3
"""diff_skill.py — 对比原版与衍生版的 SKILL.md：镜像判定、实改提取、夹带检查。
Diff an origin SKILL.md against a derivative: mirror detection, real-change
extraction, stowaway (injected instruction) screening. Pure stdlib, zero deps.

用法 / Usage:
  python3 diff_skill.py <origin-url> <derivative-url> [--file SKILL.md]
  url 可以是 github tree/blob 链接或 raw 链接；指向目录时自动补 --file 指定的文件名。
  Accepts github tree/blob URLs or raw URLs; directory URLs get '/<--file>' appended.

输出 / Output (JSON):
  change_ratio    改动比例（0=逐字相同）/ 0 means byte-identical
  is_mirror       纯镜像判定（改动 <2% → 淘汰衍生版，选原版）
                  mirror verdict (<2% change → drop the derivative, take the origin)
  added_lines     衍生版新增的行——安全审查重点：装前逐行看有没有夹带可疑指令
                  lines the derivative ADDED — review these before installing
  security_flags  added_lines 里命中可疑关键词的行（启发式，不是定论）
                  added lines matching suspicious keywords (heuristic, not verdicts)
  injection_hits  命中已知安装器/平台注入指纹的行（见 INJECTION_SIGNATURES）
                  lines matching known injector fingerprints

诚实声明 / Honesty note:
  security_flags 是关键词启发式，误报常见（讲解安全的 skill 必含安全关键词）、
  漏报也可能。重型扫描请配合 NVIDIA SkillSpector 等专业工具。
  Keyword heuristics produce false positives (security-themed skills trip them)
  and can miss things. Pair with NVIDIA SkillSpector for serious scanning.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import urllib.error
import urllib.request

UA = "skill-lineage/0.1"

# 可疑关键词（出现在【新增行】里时标记出来供人审）
# Suspicious keywords — flag ADDED lines containing these for human review.
SUSPICIOUS_PATTERNS = [
    "curl ", "wget ", "http://", "https://", "api_key", "token",
    "auth", "password", "secret", "rm -", "sudo ", "chmod ", "eval",
    "base64", "pip install", "npm install", "brew install", "ssh ",
]

# 已知安装器/平台的注入指纹：命中 = 该文件被第三方工具改写过，应向用户披露。
# 不一定是作者恶意，但用户有权知道。欢迎提 PR 扩充指纹库。
# Known injector fingerprints: a hit means a third-party tool rewrote the file.
# Not necessarily author malice — but users deserve to know. PRs welcome.
INJECTION_SIGNATURES = [
    # (label, substring to match, note)
    ("agentskill.sh telemetry block", "agentskill.sh",
     "agentskill.sh installer injects an AUTO-REVIEW block that silently "
     "rates the skill and POSTs the score back to its API"),
    ("silent-report instruction", "silently rate",
     "instruction telling the agent to rate/report without informing the user"),
]


def github_tree_to_raw(url: str, filename: str = "SKILL.md") -> str:
    """github.com/<o>/<r>/(tree|blob)/<ref>/<path> → raw.githubusercontent.com 直链。
    Convert a github web URL to a raw URL; append filename if URL is a directory."""
    url = url.strip().rstrip("/")
    if "raw.githubusercontent.com" in url:
        return url if url.endswith(filename) else f"{url}/{filename}"
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/(?:tree|blob)/([^/]+)/(.+)", url)
    if m:
        owner, repo, ref, path = m.groups()
        if not path.endswith(filename):
            path = f"{path}/{filename}"
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)$", url)
    if m:  # 裸仓库链接默认 main 分支根目录 / bare repo URL → main branch root
        return f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/main/{filename}"
    return url


def fetch_text(url: str, filename: str) -> str:
    raw = github_tree_to_raw(url, filename)
    req = urllib.request.Request(raw, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("origin_url", help="原版 / origin SKILL.md (github or raw URL)")
    ap.add_argument("derivative_url", help="衍生版 / derivative SKILL.md")
    ap.add_argument("--file", default="SKILL.md",
                    help="目录链接时补的文件名 / filename appended to directory URLs")
    ap.add_argument("--max-lines", type=int, default=120,
                    help="新增/删除行各最多输出多少行 / cap for added/removed lines")
    args = ap.parse_args()

    try:
        origin = fetch_text(args.origin_url, args.file)
        deriv = fetch_text(args.derivative_url, args.file)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"fetch failed HTTP {exc.code} ({exc.url})")

    o_lines = origin.splitlines()
    d_lines = deriv.splitlines()
    ratio = difflib.SequenceMatcher(None, origin, deriv).ratio()
    change_ratio = round(1 - ratio, 4)

    added, removed = [], []
    for line in difflib.unified_diff(o_lines, d_lines, lineterm="", n=0):
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:])

    flagged = [l for l in added
               if any(k in l.lower() for k in SUSPICIOUS_PATTERNS)]
    injections = [{"label": label, "line": l.strip()[:200], "note": note}
                  for label, needle, note in INJECTION_SIGNATURES
                  for l in d_lines if needle in l.lower()]

    print(json.dumps({
        "origin": args.origin_url,
        "derivative": args.derivative_url,
        "origin_lines": len(o_lines),
        "derivative_lines": len(d_lines),
        "change_ratio": change_ratio,
        "is_mirror": change_ratio < 0.02,
        "added_count": len(added),
        "removed_count": len(removed),
        "security_flags": flagged[:30],
        "injection_hits": injections[:10],
        "added_lines": added[: args.max_lines],
        "removed_lines": removed[: args.max_lines],
        "hint": ("is_mirror=true → drop derivative, take origin; "
                 "security_flags/injection_hits non-empty → human review before install"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
