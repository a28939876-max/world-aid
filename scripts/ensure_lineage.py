#!/usr/bin/env python3
"""ensure_lineage.py — 按需取回姊妹项目 skill-lineage 的谱系工具（联动，不复制维护）。
Fetch the lineage tools from the sibling project skill-lineage on demand.

世界援助的修谱能力由 https://github.com/a28939876-max/skill-lineage 提供——
那是一个独立开源项目（族谱.skill），本脚本只负责把它的两个零依赖脚本
取到本地缓存（raw 直链，不耗 GitHub API 配额），已存在则直接复用。
World Aid's lineage capability comes from the standalone skill-lineage
project; this script just caches its two zero-dep scripts locally.

用法 / Usage:
  python3 ensure_lineage.py [--refresh]
  输出两个脚本的本地路径，之后直接：
  python3 scripts/lineage/find_derivatives.py <owner/repo> ...
  python3 scripts/lineage/diff_skill.py <urlA> <urlB>
"""
from __future__ import annotations

import argparse
import os
import urllib.request

LINEAGE_REPO = "a28939876-max/skill-lineage"
LINEAGE_REF = "main"
SCRIPTS = ["find_derivatives.py", "diff_skill.py"]
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lineage")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true",
                    help="忽略缓存重新拉取 / re-fetch even if cached")
    args = ap.parse_args()

    os.makedirs(CACHE_DIR, exist_ok=True)
    for name in SCRIPTS:
        dst = os.path.join(CACHE_DIR, name)
        if os.path.exists(dst) and not args.refresh:
            print(f"cached  {dst}")
            continue
        url = (f"https://raw.githubusercontent.com/{LINEAGE_REPO}/"
               f"{LINEAGE_REF}/scripts/{name}")
        req = urllib.request.Request(url, headers={"User-Agent": "world-aid/0.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dst, "wb") as fh:
            fh.write(data)
        print(f"fetched {dst}  (from {LINEAGE_REPO}@{LINEAGE_REF})")


if __name__ == "__main__":
    main()
