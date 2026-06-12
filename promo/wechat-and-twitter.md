# world-aid 推广文案（公众号 + 推特）

> 主推 world-aid（世界援助），捎带姊妹项目 skill-lineage。
> 公众号笔法参考花叔《开源「鲁班」Skill》、推特参考 hype 帖"故事钩子优先"。

---

## 一、微信公众号推文

### 标题候选（选一个，建议 A）
- A：**装 skill 之前我先问一句：这事，全世界是不是已经有人替我做好了？**
- B：得道多助：我把"找现成 skill"这件事，做成了一条线
- C：以为要自己写爬虫，结果世界早就备好了——开源 world-aid

### 副标题
> 你想做的事若对世界有利，散落在各地的 skill 就是"多助"的证据。

---

来不及铺垫了，先说结论：

这两天我把一个自用了很久的工作流开源了，叫 **world-aid（世界援助）**。它干一件特别朴素的事——**你有个需求，先别急着自己写，让它去全世界找一遍有没有人已经做好了。**

名字取自那句老话：得道多助，失道寡助。我越用越觉得，这句话放在今天的 skill 生态里，是字面意义的真。

#### 先讲四个我自己跑出来的真事

**「我想做一个手帐式 app」**

原计划是从零设计"日记 + 周回顾 + 月反思"该怎么排，先画原型。结果一搜，里子面子各有人备好了：里子是一个现成的手帐工作流 skill，日记、周回顾、月反思、成长追踪，方法论都打磨好了；面子是一个 6 万多星设计合集里的游戏化手机 app 原型模板，外观直接套。

**「把我的报告做成一份 PPT」**

本以为顶多找到几个模板凑合用。结果 16 个候选、15 个流派——手里是 Markdown 的有自动挑版式转真 .pptx 的，想要 AI 配图的有，报告本来就是 Word 的有直转的。问题从"找不找得到"直接变成了"挑哪个"。

**「想在自己电脑上装个开源大模型」**

卡点是连该从 Ollama 还是 LM Studio 下手都不知道。找到的不是一篇教程，是一个**连选型都替你做了**的引导 skill：Ollama / LM Studio / llama.cpp / vLLM 四条路线按你的硬件挑，一步步装，装完还有验证清单。

**「看到好文章，想存成自己的笔记」**

我原打算写个抓正文的小爬虫，周末工程。结果接通的那个 skill 连"给一个归档页、自动抓前 N 篇"的批量模式都做好了——比我原计划还多一个功能，周末省下来了。

这四行，每一行都是用 world-aid 真实跑出来的。

#### 缺的从来不是帮助

你发现没有，上面四件事，世界上都早有人做好了。真正难的从来不是"有没有"，而是这三关：

**第一关，搜出来一堆，分不清。** 搜 8 条结果，挨个点开发现是同一个东西的 8 个转载。world-aid 会**归族**——8 个拷贝算 1 个候选，决策从"八选一"变成"要不要"。

**第二关，装了个转载版，被人动过手脚。** 合集转来转去，有的连许可证和出品方信息都删了，更别说有没有偷偷塞东西。它会**认源头**：联动我另一个开源项目 skill-lineage（族谱.skill）修一遍血统，把官方/原作版本挑给你。

这里插一句真事：我 diff 一个拷贝版的时候，在它新增的内容里发现了一段原版没有的指令——让 AI **悄悄**给这个 skill 打分、再 POST 回某个接口。不一定是作者恶意，是某个安装器平台的固定注入。但你装之前，有权知道。

**第三关，没人替你看一眼安全。** 所以它**装前全文安检**：把每个文件（不只是说明文档）都扫一遍可疑模式和已知注入指纹，命中就默认拒装，你人工看过、确认没事，才放行。

但关键词扫描有个天花板——它只认"长得像坏东西"的字符串，认不出"逻辑上有问题"的代码。所以我又加了一道：**本机要是装了 Codex CLI，就让它在只读沙箱里真读一遍代码**（加个 `--deep-review` 就行）。

这一关真抓到过东西。我拿微软官方那个部署模型的 skill 试，关键词扫描说"干净，0 命中"。我不放心，又让 Codex 深读了一遍——它在一个 shell 脚本里指出：有个没校验的参数被直接拼进了 `python3 -c` 执行，是个本地代码注入的口子。关键词扫描漏了，LLM 读懂了。

微软的官方样例尚且如此，何况你从某个合集里随手装的那个。判 UNSAFE 的，直接拦下不让装。

#### 怎么用，三步

1. 把它装进你的 agent（Claude Code 直接 clone 进 skills 目录）；
2. 对 agent 说一句人话："有没有现成的 skill 能把网页文章存成笔记？"
3. 它去：跨源搜索 → 归族 → 认源头 → 装前安检 → 把推荐和安检结果摆给你 → **你点头才装**。

不用 agent、想直接跑命令行也行，三个零依赖的 Python 脚本，纯标准库，匿名开箱即用。

#### 一点感受

我做这条线，最初真不是为了开源，就是自己偷懒：每次有新需求，先让世界帮一把，找不到再自己写。这么用下来，自己从头写的次数越来越少。

而且你会慢慢发现，连巨头都在往这个生态里放东西——微软把部署模型的整套流程封装成了官方 skill，NVIDIA 开源了企业级的 skill 安全扫描器（好到我直接拿来当后端，放弃了自造）。这就是"得道多助"最实在的样子：你想做的事如果对的，帮手会从四面八方冒出来。

world-aid 现在开源了，MIT 协议，欢迎拿走、欢迎提 PR（尤其是新的注入指纹和真实找寻案例）：

🔗 github.com/a28939876-max/world-aid
（仓库默认英文，中文读者直达：github.com/a28939876-max/world-aid/blob/main/README.zh-CN.md）

姊妹项目 skill-lineage（族谱.skill），单独管"已经有候选、想验明血统"那一半：

🔗 github.com/a28939876-max/skill-lineage

如果这篇对你有用，转发给那个"啥都想自己从头写"的朋友。世界比我们以为的，更愿意帮忙。

---

## 二、推特内容

### 版本 1：英文 launch thread（主推，投 HN / 圈内大V 视野）

**Tweet 1（钩子）**
I almost wrote a web scraper this weekend.

Then I asked: has the world already built this?

It had. The skill I found even shipped a batch mode I hadn't planned.

So I open-sourced the thing that does the asking. Meet world-aid 🧵

**Tweet 2**
The idea is old: a just cause attracts abundant help (得道多助).

For agent skills it's literally true. Whatever you need, someone probably already made it:
• "journal app" → a ready-made journaling workflow + a 62k⭐ UI template
• "report to slides" → 16 candidates, 15 flavors
• "local LLM" → a setup skill that picks Ollama/LM Studio/llama.cpp by your hardware

**Tweet 3**
Help was never the missing piece. Three gates were:

1. Search returns 8 results that are 8 reposts of one thing → it groups them into one
2. You install a repost with the license stripped → it finds the source
3. A skill carries a "silently report back" instruction → it screens every file before install

**Tweet 4**
And a 4th gate I just added: keyword screening has a ceiling — it spots scary-looking strings, not buggy logic.

So with `--deep-review`, a local Codex CLI actually reads the code in a read-only sandbox.

It caught a code-injection in a *Microsoft* sample skill the keyword pass called clean. 👇 (next tweet)

**Tweet 5（深审实锤 + 配 demo 图）**
Keyword scan on Microsoft's deploy-model skill: 0 findings. Clean.

Then I let the local LLM read it. Verdict: REVIEW —
an unvalidated arg spliced into `python3 -c` in a shell helper. A local code-injection the string-match missed.

The official sample. Imagine the random collection copy.
[配图：assets/demo.png]

**Tweet 6（收尾 + CTA）**
Three zero-dependency Python scripts + a loadable SKILL.md. Pure stdlib, anonymous out of the box. Deep review is optional and degrades gracefully if you have no Codex.

Say "is there a skill that does X?" — it searches, vets, and installs only after you approve.

MIT. PRs welcome 👇
github.com/a28939876-max/world-aid

---

### 版本 2：中文单帖（发中文技术圈 / 转小红书图文底稿）

我把一个自用很久的工作流开源了：world-aid（世界援助）。

一句话：你有个需求，先别急着自己写，让它去全世界找一遍有没有人做好了。

得道多助——这话放在 skill 生态里是字面意义的真：
・「想做手帐 app」→ 现成手帐工作流 + 6 万星 UI 模板
・「报告变 PPT」→ 16 个候选 15 个流派
・「装开源大模型」→ 连选型都替你做的引导

难的从不是"有没有"，是这三关：搜出一堆分不清（它归族）、装了转载版被动过手脚（它认源头）、没人替你看安全（它装前全文安检）。

我 diff 一个拷贝时，真抓到过一段"让 AI 悄悄打分上报"的注入指令。装之前，你有权知道。

MIT 开源 🔗 github.com/a28939876-max/world-aid

---

### 版本 3：skill-lineage 单独短帖（姊妹项目，可隔几天再发）

"Star 只代表血统，不代表族内最优。"

你搜到一个 497⭐ 的 skill 准备装。你不知道它有 26 个衍生版——一个汉化版自己做到了 5229⭐，一个低星 fork 修了原版的坑，还有 12 个是一字未改的镜像。

skill-lineage（族谱.skill）：装之前，先修一眼它的族谱。

MIT 🔗 github.com/a28939876-max/skill-lineage

---

### 版本 4：深审单帖（中文技术圈 / 最强钩子，可单独发也可配 demo 图）

> 这条的杀伤力比 launch 帖更强，建议作为第二波主推，配 assets/demo.png。

我的 skill 安装器对微软官方那个部署模型的 skill 说：扫描干净，0 命中。

我没信，让本机的 Codex 在只读沙箱里把代码真读了一遍。

判定：REVIEW。一个 shell 脚本里，有个没校验的参数被直接拼进了 `python3 -c`——本地代码注入。关键词扫描漏了，LLM 读懂了。

微软的官方样例尚且如此。你从某个合集随手装的那个呢？

world-aid 的 `--deep-review`，装前让 LLM 替你读一遍代码。
🔗 github.com/a28939876-max/world-aid

---

### 版本 5：英文单帖（深审，投 HN / 安全圈）

My skill installer said a Microsoft sample skill was clean. 0 keyword findings.

Then I let a local LLM read the actual code. It found an unvalidated arg spliced into `python3 -c` in a shell helper — a local code-injection.

Keyword scanning spots scary strings. It can't spot buggy logic.

`world-aid --deep-review`: an LLM reads the code before you install.
github.com/a28939876-max/world-aid
