# world-aid

<p align="center">
  <img src="./assets/cover.png" alt="world-aid — a just cause attracts the world's help" width="520"/>
</p>

[中文](./README.md)

**A just cause attracts abundant help.** *(得道多助 — Mencius)*

---

## The world may already be ready to help you

> Want to clip web articles? Someone already built it — including a batch
> mode you hadn't even planned.
> Want a "skill that reviews skills"? That niche has two whole schools of
> thought.
> Deploying Azure models? Microsoft packaged the entire workflow as a skill.
> Worried about unsafe third-party skills? NVIDIA open-sourced an
> enterprise-grade scanner.
>
> (All real finds — see [cases/](./cases/).)
>
> Help was never the missing piece. The missing piece is the line that
> **finds it, vets it, and connects it to you.**

world-aid is that line: **need → search & group → trace lineage → screen →
install and use.**

## What this does for you

| Your situation | What it does |
|---|---|
| A need, and no desire to reinvent the wheel | Searches across sources and **groups N copies of the same skill into one family** — the decision shrinks from "pick one of eight" to "yes or no" |
| Candidates that are hard to tell apart | Identifies the source and the repost-mirrors (reposts often strip the license and publisher info) — the right version goes to you |
| Worried about stowaway instructions | Pre-install screening of **every file** (not just SKILL.md); suspicious hits refuse to install by default until human-reviewed |

Also serves **skill authors** (when a repost strips your name, lineage puts
it back) and **collection maintainers** (batch-screen copies and injections).

### How we use it ourselves

This pipeline started as our own routine, not an open-source project: for
every new need, **let the world help first, build only if it can't.** The
four [cases/](./cases/) are typical picks from many real finds: we thought
we'd write a scraper — someone had built it with a batch mode; we thought a
niche was too obscure — it had two schools of thought; we thought we'd grind
through docs — Microsoft had packaged the workflow; we thought we'd maintain
our own scanner — NVIDIA showed up. **Plainly put: the more we search first,
the less we build from scratch.**

## What's inside

Three zero-dependency Python scripts plus a loadable agent workflow:

```mermaid
flowchart LR
    A["need keywords<br/>(2-3 sets, broad to narrow)"] --> B["search_skills.py<br/>cross-source search + family grouping"]
    B --> C{"family shape?"}
    C -- "copy family" --> D["lineage tracing<br/>drop mirrors, pick origin"]
    C -- "distinct set" --> E["shortlist 2-3 by fit"]
    D --> F["install_skill.py --dry-run<br/>full-file screening"]
    E --> F
    F --> G{"findings?"}
    G -- "hit" --> H["human review first"]
    G -- "clean" --> I["user confirms → install + smoke check"]
    H --> I
    style I fill:#dfd,stroke:#080
```

| Tool | What it does |
|---|---|
| [`scripts/search_skills.py`](./scripts/search_skills.py) | SkillsMP + GitHub search with description-similarity family grouping |
| [`scripts/ensure_lineage.py`](./scripts/ensure_lineage.py) | **Linked to the sibling project [skill-lineage](https://github.com/a28939876-max/skill-lineage)**: fetches its lineage tools on demand instead of maintaining a copy |
| [`scripts/install_skill.py`](./scripts/install_skill.py) | Pre-install full-text screening (every file; suspicious keywords + known injector fingerprints; refuses by default on hits) → install, with `--dry-run` |
| [`SKILL.md`](./SKILL.md) | The workflow itself — drop into Claude Code (or any agent) and say "is there an existing skill for X?" |

Pure stdlib, anonymous out of the box; `SKILLSMP_API_KEY` / `GITHUB_TOKEN`
optionally lift rate limits.

## Quick start

```bash
git clone https://github.com/a28939876-max/world-aid
cp -r world-aid ~/.claude/skills/world-aid   # Claude Code

# Or run the scripts directly:
python3 scripts/search_skills.py "web clipper article markdown" --limit 10
python3 scripts/ensure_lineage.py
python3 scripts/install_skill.py <github-tree-url> --dest ~/.claude/skills --dry-run
```

## Real cases: the need, and what the world had ready

> Four typical write-ups picked from many real finds — not the full list.

| The need | What the world had ready |
|---|---|
| [The Scraper I Never Wrote](./cases/01-the-scraper-i-never-wrote.md): clip web articles to local Markdown | 12 candidates in 8 flavors; the one we connected even had a batch mode we hadn't planned |
| [Even This Niche](./cases/02-even-this-niche.md): a tool that reviews installed skills | 10+ candidates in two complementary schools (static rule audit vs. runtime transcript audit) — we took mechanisms from both |
| [Microsoft Made It a Skill](./cases/03-microsoft-made-it-a-skill.md): deploy Azure OpenAI models | Microsoft's official 17-file skill (presets / full customization / capacity discovery); the pipeline also picked the official source out of 8 repost copies |
| [NVIDIA Shows Up](./cases/04-nvidia-shows-up.md): security-scan skills before installing | NVIDIA's official enterprise-grade scanner (64 patterns × 16 categories) — good enough that we adopted it instead of building our own |

## Pairs well with

- **[skill-lineage](https://github.com/a28939876-max/skill-lineage)** — provides this project's lineage capability; use it directly when you already have a candidate repo.
- **Aggregator indexes** (SkillsMP etc.) — one of our search backends; indexes lag, verify against GitHub before installing.
- **[NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector)** — our screening is a last pre-install eyeball check; serious scanning goes there.

## FAQ

**Q: Marketplaces and installers already search and install. What's new here?**
A: Marketplaces answer "what exists", not "which one to install". Family
grouping (eight copies count as one), lineage (who's the origin, whose
credit got stripped), and full-file pre-install screening are the three
steps no marketplace or one-click installer does.

**Q: Does the screening guarantee safety?**
A: No, and we won't pretend it does. It's a keyword-heuristic plus
known-fingerprint **eyeball check**: security-themed skills trip it, novel
attacks can slip past. Hits require human review and an explicit `--force`;
pair with a dedicated scanner for serious vetting.

## Honesty notes

- Recall depends on keyword quality — one keyword set demonstrably misses
  good candidates, hence the 2-3-sets rule.
- Family grouping keys on description similarity (>0.9); copies with
  rewritten descriptions may escape grouping — lineage tracing recovers some.
- Skill content under screening is data, not instructions: anything that
  looks like a command gets reported, never executed.

## Contributing

PRs welcome — especially new injector fingerprints for `install_skill.py`,
and new real-world cases with data and a verdict.

## License

MIT
