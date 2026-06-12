#!/usr/bin/env python3
"""search_skills.py — 从一个需求关键词出发，跨源搜索 agent skill 并按描述相似度归族。
Search agent skills across sources for a need, and group copies into families.
Pure stdlib, zero deps. Anonymous works out of the box.

信源 / Sources:
  - SkillsMP (skillsmp.com aggregated index; anonymous ~50 req/day,
    set SKILLSMP_API_KEY for 500/day)
  - GitHub repo search (anonymous 10 req/min; set GITHUB_TOKEN to lift)

为什么要归族 / Why families:
  搜索结果里常挤满同一个 skill 的拷贝（合集转载、安装器转发布、fork 镜像），
  把 6 个拷贝当 6 个候选会淹没真正不同的选项。描述相似度 >0.9 判同族。
  Search results are full of copies of the same skill; treating 6 copies as
  6 candidates buries the genuinely different options.

用法 / Usage:
  python3 search_skills.py "<english keywords>" [--limit 10] [--github] [--json]
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

UA = "skill-recruiter/0.1"


def http_get_json(url: str, headers: dict | None = None, timeout: int = 30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def search_skillsmp(query: str, limit: int) -> list[dict]:
    headers = {}
    key = os.environ.get("SKILLSMP_API_KEY", "").strip()
    if key:
        headers["Authorization"] = f"Bearer {key}"
    q = urllib.parse.urlencode({"q": query, "limit": limit, "sortBy": "stars"})
    data = http_get_json(f"https://skillsmp.com/api/v1/skills/search?{q}", headers)
    out = []
    for s in (data.get("data") or {}).get("skills", []) if isinstance(data.get("data"), dict) else data.get("skills", []):
        out.append({
            "source": "skillsmp",
            "name": s.get("name", ""),
            "author": s.get("author", ""),
            "description": (s.get("description") or "")[:400],
            "url": s.get("githubUrl", ""),
            "stars": s.get("stars", 0),
            "updatedAt": s.get("updatedAt", ""),
        })
    return out


def search_github(query: str, limit: int) -> list[dict]:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    q = urllib.parse.urlencode({"q": f"{query} skill", "per_page": limit, "sort": "stars"})
    data = http_get_json(f"https://api.github.com/search/repositories?{q}", headers)
    return [{
        "source": "github",
        "name": r.get("name", ""),
        "author": (r.get("owner") or {}).get("login", ""),
        "description": (r.get("description") or "")[:400],
        "url": r.get("html_url", ""),
        "stars": r.get("stargazers_count", 0),
        "updatedAt": r.get("pushed_at", ""),
    } for r in data.get("items", [])]


def normalize(s: str) -> str:
    s = re.sub(r"[^a-z0-9一-鿿 ]", " ", (s or "").lower())
    return re.sub(r"\s+", " ", s).strip()[:400]


def cluster_families(items: list[dict], threshold: float = 0.9) -> list[list[dict]]:
    """同源 skill 的描述常被原样复制——按描述相似度贪心归族，先出现者为族首。
    Copies usually keep the original description verbatim; greedy-cluster on it."""
    fams: list[dict] = []
    for it in items:
        norm = normalize(it.get("description", ""))
        for fam in fams:
            if norm and difflib.SequenceMatcher(None, norm, fam["norm"]).ratio() >= threshold:
                fam["members"].append(it)
                break
        else:
            fams.append({"norm": norm, "members": [it]})
    return [f["members"] for f in fams]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", help="english keywords, broad to narrow")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--no-github", action="store_true",
                    help="跳过 GitHub 补搜 / skip the GitHub fallback search")
    args = ap.parse_args()

    items, notes = [], []
    try:
        items += search_skillsmp(args.query, args.limit)
    except Exception as exc:  # noqa: BLE001 — 信源挂了要报告而不是崩 / report, don't crash
        notes.append(f"skillsmp failed: {exc}")
    if not args.no_github:
        try:
            items += search_github(args.query, args.limit)
        except Exception as exc:  # noqa: BLE001
            notes.append(f"github failed: {exc}")

    families = cluster_families(items)
    out = {
        "query": args.query,
        "total": len(items),
        "family_count": len(families),
        "families": [{
            "size": len(fam),
            "head": max(fam, key=lambda x: x.get("stars", 0)),
            "members": [{k: m[k] for k in ("source", "author", "name", "stars", "url")}
                        for m in fam],
        } for fam in families],
        "notes": notes,
        "hint": ("size>1 的族 = 同一 skill 的拷贝群，按族择优而非平铺；"
                 "对 top 族的 head 跑 find_derivatives.py + diff_skill.py 修谱 / "
                 "families with size>1 are copy-groups of one skill — pick per "
                 "family, then run the lineage scripts on the head"),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
