# 案例四：在自己电脑上装个开源大模型 / An LLM on My Laptop

> 需求原话：「想在自己电脑上装一个开源大模型」——不知道从 Ollama 还是 LM Studio 下手。

## 世界给了什么

搜回来的不是一篇教程，是**把选型也替你做了的引导 skill**：

`local-llm-setup`——覆盖 **Ollama / LM Studio / llama.cpp / vLLM 四条路线**：

- 按你的硬件（CPU 还是 GPU、显存多大）帮你选路线、选模型尺寸
- 一步步装：Windows 用 winget、macOS 用 brew、Linux 一行脚本
- 装完带**验证清单**（接口通没通、模型 id 对不对）

族群里还有个 4 拷贝的 `ollama-setup` 家族（自动配置 Ollama 那一派）、专攻 Apple Silicon 的 MLX 路线、连"从源码编译 llama.cpp 开 GPU 加速"的硬核版都有——丰俭由人。

安检 2 处命中：`brew install ollama` 和一条 `curl http://localhost:.../v1/models` 验证命令——**这个 skill 的本职就是教你装东西**，命中的恰是它的工作内容。人审放行。

## 启示

1. **"装环境"这类最让普通人头疼的需求，是 skill 生态覆盖最厚的地方**——选型、安装、验证一条龙，比零散教程强在"它知道下一步是什么"。
2. 同一需求下不同硬件有不同最优解（CPU/GPU/苹果芯片），好的引导 skill 把分叉都写好了。

## 数据来源

- 本篇是众多实际找寻记录里挑出的典型之一。
- 两组关键词跨源搜索；入选者 `--dry-run` 安检 + 人审放行。
