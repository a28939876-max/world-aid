#!/usr/bin/env python3
"""find_derivatives.py — 给定一个仓库，找它的衍生版（forks / 同名 / 提及）并向上溯源。
Find the descendants (and the parent) of a skill repo. Pure stdlib, zero deps.

为什么 / Why:
  高星 skill 的改良衍生版可能更对口，即使衍生版星级很低。
  Star count reflects ancestry, not which family member is best.
  A 3-star fork that fixed the original's bugs may beat the 4000-star origin.

三路信号 / Three signals:
  1. forks         按更新时间降序；fork 建立后仍有 push 的标记 active=true（重点嫌疑人）
                   forks sorted by pushed_at; active=true means pushed after creation
  2. same-name     同名 skill 的非 fork 仓库（捕获复制改良，GitHub 不记 fork 关系的那种）
  3. mentions      README/描述里提及原仓库的（credit 信号）

用法 / Usage:
  python3 find_derivatives.py <owner/repo> [--skill-name <name>] [--limit 15]

限流 / Rate limits:
  匿名 core API 60 次/时、search 10 次/分。设 GITHUB_TOKEN 环境变量可放宽。
  Anonymous: 60 core req/hour, 10 search req/min. Set GITHUB_TOKEN to lift.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
UA = "skill-lineage/0.1"


def http_get_json(url: str, timeout: int = 30):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": UA}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def repo_brief(r: dict, relation: str) -> dict:
    return {
        "repo": r["full_name"],
        "stars": r.get("stargazers_count", 0),
        "pushed_at": r.get("pushed_at", ""),
        "created_at": r.get("created_at", ""),
        # fork 建立后还有 push → 不是纯收藏，值得 diff
        # pushed after creation → not a bookmark-fork, worth diffing
        "active": r.get("pushed_at", "") > r.get("created_at", ""),
        "relation": relation,
        "description": (r.get("description") or "")[:200],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", help="owner/repo")
    ap.add_argument("--skill-name", default="",
                    help="skill 名，用于同名搜索 / skill name for same-name search")
    ap.add_argument("--limit", type=int, default=15)
    args = ap.parse_args()

    out: dict = {"origin": args.repo, "parent": None, "derivatives": [], "notes": []}

    # 原仓库信息 + 向上溯源 / origin info + trace upward
    try:
        origin = http_get_json(f"{API}/repos/{args.repo}")
        out["origin_stars"] = origin.get("stargazers_count", 0)
        out["origin_pushed_at"] = origin.get("pushed_at", "")
        if origin.get("fork") and origin.get("parent"):
            out["parent"] = repo_brief(origin["parent"], "parent")
    except urllib.error.HTTPError as exc:
        out["notes"].append(f"origin fetch failed HTTP {exc.code}")

    # 1) forks，按最近更新排 / forks, newest first
    try:
        forks = http_get_json(
            f"{API}/repos/{args.repo}/forks?sort=newest&per_page={args.limit}")
        out["derivatives"] += [repo_brief(f, "fork") for f in forks]
    except urllib.error.HTTPError as exc:
        out["notes"].append(f"forks fetch failed HTTP {exc.code}")

    seen = {d["repo"] for d in out["derivatives"]} | {args.repo}

    # 2) 同名 skill 的非 fork 仓库 / same-name non-fork repos
    if args.skill_name:
        try:
            q = urllib.parse.urlencode(
                {"q": f"{args.skill_name} in:name", "per_page": args.limit})
            data = http_get_json(f"{API}/search/repositories?{q}")
            for r in data.get("items", []):
                if r["full_name"] not in seen:
                    seen.add(r["full_name"])
                    out["derivatives"].append(repo_brief(r, "same-name"))
        except urllib.error.HTTPError as exc:
            out["notes"].append(f"same-name search failed HTTP {exc.code}")

    # 3) 提及原仓库的仓库（credit 信号）/ repos mentioning the origin
    try:
        q = urllib.parse.urlencode({"q": f'"{args.repo}"', "per_page": args.limit})
        data = http_get_json(f"{API}/search/repositories?{q}")
        for r in data.get("items", []):
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                out["derivatives"].append(repo_brief(r, "mentions-origin"))
    except urllib.error.HTTPError as exc:
        out["notes"].append(f"mentions search failed HTTP {exc.code}")

    # active 的、更新比原版晚的排前面 / active & recently-pushed first
    out["derivatives"].sort(key=lambda d: (d["active"], d["pushed_at"]), reverse=True)
    out["derivative_count"] = len(out["derivatives"])
    out["hint"] = ("active=true 且 pushed_at 晚于原版的衍生版优先 diff / "
                   "diff active derivatives pushed later than origin first")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
