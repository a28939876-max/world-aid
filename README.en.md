# world-aid

<p align="center">
  <img src="./assets/cover.png" alt="world-aid — a just cause attracts the world's help" width="520"/>
</p>

[中文](./README.md)

**A just cause attracts abundant help.** *(得道多助 — Mencius)*

---

## You state a need, the world answers

| You say | What the world had ready (real pipeline runs) |
|---|---|
| "I want to build a journal app" | `bm-life-journal`: a ready-made journaling workflow (diary / weekly review / monthly reflection / growth tracking) — plus a gamified phone-app prototype template from a 62,000+ star design collection for the looks |
| "Turn my report into slides" | 16 candidates in 15 flavors: Markdown-to-real-.pptx with auto layouts (201 stars), AI-illustrated decks (2,563 stars), Word-to-PPT direct — pick by the format you have |
| "Run an open-source LLM on my laptop" | `local-llm-setup`: four routes (Ollama / LM Studio / llama.cpp / vLLM) chosen by your hardware, with a post-install verification checklist |
| "Save good articles as my own notes" | 12 candidates in 8 flavors; the winner shipped a batch mode the DIY plan never had |

**Every row above is a real run of this tool** — the full stories live in
[cases/](./cases/).

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
four rows in the opening table came from exactly such runs: we thought we'd
write a scraper — someone had built it with a batch mode; the journal app
came with both the workflow and the looks; slides had more flavors than we
could pick from; the local-LLM guide even did the hardware matchmaking.
**Plainly put: the more we search first, the less we build from scratch.**

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

| The need, verbatim | The find |
|---|---|
| "Save good articles as my own notes" | [The Scraper I Never Wrote](./cases/01-the-scraper-i-never-wrote.md) — 12 candidates, 8 flavors, winner shipped a bonus batch mode |
| "I want to build a journal app" | [The Journal App](./cases/02-the-journal-app.md) — help arrived in two layers: the journaling workflow and the app-prototype looks |
| "Turn my report into slides" | [Report to Slides](./cases/03-report-to-slides.md) — 16 candidates in 15 flavors, plus a live demo of "a screening hit ≠ a problem" |
| "Run an open-source LLM on my laptop" | [An LLM on My Laptop](./cases/04-llm-on-my-laptop.md) — four routes matched to your hardware, verification checklist included |

### Advanced cases (developer-facing)

The giants are placing help into this ecosystem too: [Even This Niche](./cases/advanced/even-this-niche.md) (even "a skill that reviews skills" has two schools), [Microsoft Made It a Skill](./cases/advanced/microsoft-made-it-a-skill.md) (an official 17-file engineering-grade skill), [NVIDIA Shows Up](./cases/advanced/nvidia-shows-up.md) (an enterprise-grade scanner so good we adopted it instead of building our own).

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
