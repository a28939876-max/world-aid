# world-aid · 世界援助

<p align="center">
  <img src="./assets/cover.png" alt="world-aid — 得道多助" width="520"/>
</p>

[English](./README.en.md)

**得道多助，失道寡助。**

---

## 你想做的事，世界可能已经准备好帮你了

> 想剪藏网页？有人连"归档页批量抓前 N 篇"都做好了。
> 想要一个"审查 skill 的 skill"？这么冷门的需求，世界上有两个流派在做。
> 要部署 Azure 模型？微软官方把整套流程封装成了 skill。
> 担心第三方 skill 不安全？NVIDIA 开源了企业级扫描器。
>
> （以上全部出自真实找寻记录，见 [cases/](./cases/)。）
>
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

这条管线最早不是为开源做的，是自用流程的固化：每次有新需求，**先让世界帮一把，找不到再自己写**。[cases/](./cases/) 里的四篇就是从很多次实际找寻里挑出来的典型：以为要自己写爬虫，结果有人连批量模式都做好了；以为太冷门没人做，结果有两个流派；以为要啃文档手搓，结果微软官方有现成的；以为要自己维护扫描器，结果 NVIDIA 出手了。**说白了：这么找下来，自己从头写的次数越来越少。**

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

| 需求 | 世界给了什么 |
|---|---|
| [以为要自己写爬虫](./cases/01-the-scraper-i-never-wrote.md)：网页剪藏成本地 Markdown | 12 个候选 8 种流派，接通的那个连"归档页批量抓前 N 篇"都做好了——比原计划还多一个功能 |
| [这么冷门也有人做了](./cases/02-even-this-niche.md)：审查"已装 skill 质量"的工具 | 10+ 候选、两个成型流派（静态规则审计 vs 运行记录审计），恰好互补，两边机制都收了 |
| [微软把它做成了 skill](./cases/03-microsoft-made-it-a-skill.md)：部署 Azure OpenAI 模型 | 微软官方 17 文件完整工程（预设/自定义/容量发现三模式）；顺带从 8 条转载拷贝里认出官方源头装的原版 |
| [连 NVIDIA 都来帮忙](./cases/04-nvidia-shows-up.md)：给装 skill 配安全扫描 | NVIDIA 官方开源的企业级扫描器（64 模式×16 类）——好到让我们放弃自造，直接采用当后端 |

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
