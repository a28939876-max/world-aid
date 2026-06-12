# world-aid · 世界援助

<p align="center">
  <img src="./assets/cover.png" alt="world-aid — 得道多助" width="520"/>
</p>

[English](./README.en.md)

**得道多助，失道寡助。**

---

## 你说一句需求，世界接一句帮助

| 你说 | 世界已经备好的（真实跑出来的结果） |
|---|---|
| "我想做一个手帐式 app" | `bm-life-journal`：日记/周回顾/月反思/成长追踪的现成手帐工作流；外加 62000+⭐ 设计合集里的游戏化手机 app 原型模板当外观 |
| "把我的报告做成一份 PPT" | 16 个候选 15 个流派：Markdown 转真 .pptx 自动挑版式的（201⭐）、AI 配图的（2563⭐）、Word 直转的——按你手里的格式挑 |
| "在自己电脑上装个开源大模型" | `local-llm-setup`：Ollama / LM Studio / llama.cpp / vLLM 四条路线按硬件帮你选，装完还有验证清单 |
| "看到好文章想存成自己的笔记" | 12 个候选 8 种流派，接通的那个连"归档页批量抓前 N 篇"都做好了——比自己写爬虫的计划还多一个功能 |

**以上每一行都是用本工具真实跑出来的**，找寻过程一篇篇写在 [cases/](./cases/) 里。

> 缺的从来不是帮助，是把帮助**找出来、验明正身、接到你手上**的那条线。

world-aid 就是那条线：**需求 → 搜索归族 → 修谱择优 → 装前安检 → 装上就用**。
你想做的事若对世界有利，散落在世界各地的 skill 就是"多助"的证据——这个工具负责把它们接通。

## 这个工具帮你做什么

**给要找现成能力的你：从需求到装好，一条线走完。**

| 你的处境 | 它帮你 |
|---|---|
| 有个需求，不想重复造轮子 | 跨源搜出现成 skill，**把同一个东西的 N 个拷贝归成一个族**，决策从"八选一"变成"要不要" |
| 搜到的候选真假难辨 | 认出谁是源头、谁是转载镜像（转载常把许可证和出品方信息都删了），把对的版本装给你 |
| 担心第三方 skill 夹带私货 | 装前**全部文件**全文安检（不只 SKILL.md），命中可疑模式默认拒装，人审后才放行 |

顺带也服务：**skill 作者**（你的作品被转载剥署名时，修谱会把名字还给你）、**合集维护者**（批量甄别拷贝与注入）。

### 我们自己就是这么用的

这条管线最早不是为开源做的，是自用流程的固化：每次有新需求，**先让世界帮一把，找不到再自己写**。开头那张表的四行就是这么跑出来的：以为要自己写爬虫，结果有人连批量模式都做好了；想做手帐 app，里子面子各有人备好；要做 PPT，挑花眼的程度；装大模型，连选型都替你想了。**说白了：这么找下来，自己从头写的次数越来越少。**

---

## 这是什么

三个零依赖 Python 脚本 + 一套可加载进 AI agent 的编排流程（SKILL.md）：

```mermaid
flowchart LR
    A["需求关键词<br/>(2~3 组,由宽到窄)"] --> B["search_skills.py<br/>跨源搜索 + 归族"]
    B --> C{"族的形状?"}
    C -- "拷贝族" --> D["lineage 修谱<br/>镜像淘汰/选原版"]
    C -- "独立群" --> E["按对口度挑 2~3 个"]
    D --> F["install_skill.py --dry-run<br/>全文件安检"]
    E --> F
    F --> G{"findings?"}
    G -- "命中" --> H["人审后才放行"]
    G -- "干净" --> I["用户确认 → 安装 + 冒烟"]
    H --> I
    style I fill:#dfd,stroke:#080
```

| 工具 | 干什么 |
|---|---|
| [`scripts/search_skills.py`](./scripts/search_skills.py) | SkillsMP + GitHub 跨源搜索，按描述相似度归族——同一 skill 的拷贝群不再淹没真正不同的选项 |
| [`scripts/ensure_lineage.py`](./scripts/ensure_lineage.py) | **联动姊妹项目 [skill-lineage（族谱.skill）](https://github.com/a28939876-max/skill-lineage)**：按需取回它的修谱工具（找原版/衍生、镜像判定），不复制维护 |
| [`scripts/install_skill.py`](./scripts/install_skill.py) | 装前全文安检（全部文件，可疑关键词 + 已知注入指纹，命中默认拒装）→ 落盘安装，支持 `--dry-run` |
| [`SKILL.md`](./SKILL.md) | 编排流程本体：装进 Claude Code 等 agent，说一句"有没有现成的 skill 能做 xx"就走全链 |

纯 stdlib、零第三方依赖、匿名开箱即用（`SKILLSMP_API_KEY` / `GITHUB_TOKEN` 可选放宽限流）。

## 快速开始

```bash
git clone https://github.com/a28939876-max/world-aid
cp -r world-aid ~/.claude/skills/world-aid   # Claude Code；其它 agent 把 SKILL.md 加进系统提示

# 或者直接跑脚本：
python3 scripts/search_skills.py "web clipper article markdown" --limit 10
python3 scripts/ensure_lineage.py            # 首次取回修谱工具（raw 直链，零配额）
python3 scripts/install_skill.py <github-tree-url> --dest ~/.claude/skills --dry-run
```

## 真实案例：什么需求，找到了什么

> 四篇是从大量实际找寻里挑出来的典型，不是全部；新的典型会持续补充。

| 需求原话 | 找寻记录 |
|---|---|
| "看到好文章想存成自己的笔记" | [以为要自己写爬虫](./cases/01-the-scraper-i-never-wrote.md)——12 候选 8 流派，赢家多送一个批量模式 |
| "我想做一个手帐式 app" | [我想做一个手帐式 app](./cases/02-the-journal-app.md)——里子（手帐工作流）和面子（62k⭐ 合集的 app 原型模板）各找到一层 |
| "把我的报告做成一份 PPT" | [把报告做成一份 PPT](./cases/03-report-to-slides.md)——16 候选 15 流派，还顺带演示了"安检命中 ≠ 有问题"的人审判读 |
| "在自己电脑上装个开源大模型" | [在自己电脑上装个开源大模型](./cases/04-llm-on-my-laptop.md)——四条路线按硬件选型，装完带验证清单 |

### 进阶案例（开发者向）

巨头也在往这个生态里放帮助——[这么冷门也有人做了](./cases/advanced/even-this-niche.md)（审查 skill 的 skill 都有两个流派）、[微软把它做成了 skill](./cases/advanced/microsoft-made-it-a-skill.md)（官方 17 文件工程级 skill）、[连 NVIDIA 都来帮忙](./cases/advanced/nvidia-shows-up.md)（企业级安全扫描器，好到我们放弃自造直接采用）。

## 配合食用

- **[skill-lineage（族谱.skill）](https://github.com/a28939876-max/skill-lineage)**：本项目的修谱能力来自它。只想对一个已知仓库修谱（不需要找+装全链）→ 直接用它。
- **聚合索引站**（SkillsMP 等）：本工具的搜索底座之一；索引可能滞后，安装前以 GitHub 现状为准。
- **[NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector)**：本工具的安检是装前最后一道目检；重型安全扫描交给它。

## 须知 FAQ

**Q：市场和安装器已经能搜能装了，这个多做了什么？**
A：市场负责"有什么"，不负责"该装哪个"。归族（八个拷贝算一个）、修谱（谁是原版谁被剥了署名）、装前全文安检（含 scripts/，命中默认拒装）——这三步是市场和一键安装器都不做的。

**Q：安检能保证安全吗？**
A：不能，也不装能。它是关键词启发式 + 已知注入指纹的**装前目检**：讲安全的 skill 会自指误报，新型攻击也可能漏。命中必人审、人审后才 `--force`，重型扫描请配合专业工具。

## 诚实声明

- 搜索召回受关键词质量影响：实测单组关键词会漏掉好候选，所以流程规定 2~3 组、由宽到窄。
- 归族按描述相似度判定（>0.9 同族），魔改过描述的拷贝可能漏归——修谱那步会补救一部分。
- 被安检的 skill 内容是数据不是指令：里面任何"现在执行 xx"只会被上报，绝不执行。

## 欢迎 PR

- `install_skill.py` 的注入指纹库：发现新的安装器/平台注入模式，提上来让所有人受益。
- 新的真实使用案例（cases/）：有冲突、有数据、有结局的最好。

## License

MIT
