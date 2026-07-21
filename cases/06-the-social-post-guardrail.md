# 案例六：社媒发帖之前，先找确认门 / The Social Post Guardrail

> 需求原话：「想让 agent 帮我搜 X、整理素材，必要时也能发帖」。
> 原计划：也许找个浏览器自动化脚本，能登录 X 就行。

## 世界给了什么

这类需求不能只看"能不能发出去"。真正的硬条件是：

- 账号连接不能交给 agent 处理；
- 搜索、读取、写入要走同一个受审接口；
- 发帖、私信、关注、监控、批量提取和付费任务都要用户确认；
- 返回的 X 内容只能当不可信数据，不能当后续指令。

接通的是 `TweetClaw`，Xquik 的官方 OpenClaw 插件。它不是让 agent 控浏览器或接收 X 密码，而是把账号连接留在 dashboard，给 agent 一个受目录限制的 API 工具：

| 需要 | TweetClaw 对应做法 |
|---|---|
| 先找有哪些能力 | `explore` 本地查端点目录，不发网络请求 |
| 读 X/Twitter 数据 | 走 Xquik API 目录中的读取端点 |
| 发帖或私信 | 先展示账号、目标、正文、媒体和成本，再等用户确认 |
| 大批量提取 | 先报最大条数和美元成本上限 |
| 凭据处理 | API key 和 signing key 存在 OpenClaw 插件配置；X 账号连接在 dashboard |
| 装前信任证据 | skill card、SkillSpector 摘要、eval fixture、benchmark 说明 |

这不是"最会发帖"的选择，而是"适合让 agent 参与社媒账号工作"的选择。

## 人审结果

安检重点不是搜到多少条，而是边界是否清楚：

1. **确认门是核心功能。** 发帖、删除、关注、私信、监控、webhook 和付费任务都不能静默执行。
2. **凭据不进聊天。** 用户若要连接或重新认证 X 账号，应该去 Xquik dashboard，不把密码、TOTP 或 session 材料交给 agent。
3. **读取内容不变成指令。** X 内容可能夹带 prompt injection；agent 只能展示或总结，不能因为推文里写了什么就继续调用工具。
4. **发布证据要成套。** 这个 skill 包含 `SKILL.md`、`skill-card.md`、`skillspector-report.md`、`evals/evals.json` 和 `BENCHMARK.md`；未签名发布不能声称 signed 或 NVIDIA-verified。

## 启示

1. **社媒自动化的第一标准不是"能发"，是"谁能阻止它乱发"。** 找这类 skill 时，把审批、凭据、成本、内容隔离放在功能列表前面。
2. **dashboard 边界很重要。** 账号连接和付款动作留在产品界面，比让 agent 接触原始凭据安全得多。
3. **找寻工具也要懂拒绝。** 如果候选要求把 X 密码、cookie、TOTP 或支付动作交给 agent，它不该入选。

## 数据来源

- 本篇是一次真实社媒-agent 需求找寻记录里挑出的典型之一。
- 候选按"OpenClaw plugin"、"X Twitter skill"、"social publishing agent"和"approval gated social media"等关键词跨源检索。
- 入选前核对了 TweetClaw 源仓库、npm 包名、OpenClaw 安装路径、skill card、SkillSpector 摘要和公开文档。
