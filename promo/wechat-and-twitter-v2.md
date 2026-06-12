<!-- 内部说明（发布时不要带上）：口语版推广文案，重心放在"找"这套逻辑——先把一整片翻全、归族去重、看清全貌再挑。用"找油管字幕"这个真实例子，已过 codex / humanizer-zh 反 slop 审稿。 -->

# world-aid 推广文案 v2（口语版 · 重心"找"）

## 一、微信公众号推文

### 标题候选
- A：我就想下个油管字幕，世界给了我十几个答案
- B：装工具之前，先把世界翻一遍
- C：差点盯着"功能最全"那个就装了

### 正文

前几天我想把一个 YouTube 视频转成文字。视频有点长，自己边听边记太累，就想找个现成的工具。

搁以前我会自己去 GitHub 搜，翻几页，挑个 star 高的装上完事。这回我让 world-aid 去找。

它一下翻出来十几个能下字幕的，还先帮我归了个类。十几个里有四个是同一个东西被转来转去，它算作一份。剩下九个才是真不一样的，我这才看出来下字幕原来有这么多路子。有只下纯文字的，有顺手把视频画面也截出来的，有下完自动翻译的，有专门走 Tor 防封的，还有调别的现成服务、几行就搞定的。

这一片摊开看，最扎眼的是那个走 Tor 的。下字幕还能防 IP 封锁，听着功能最全，我差点就挑它了。

点开才发现不是那么回事。它是个土耳其人写的，注释全是土耳其语。下个字幕而已，它要我先装 Tor 把网络绕一圈，还得拿管理员权限改系统。它存文件的路径写死了，写的是某个云端机器人的目录，跟我这台电脑根本不挨着。这东西是给跑在服务器上的机器人用的，不是给我电脑的。

要不是把这些都找出来摆一块看，我可能就盯着那个"功能最全"的装了。看过一遍才发现，它解决的是别人的问题。我只是想下个字幕，低星那几个反而更顺手。

world-aid 干的差不多就是这事。你说个需求，它先到处找一圈，把重复的并掉，再把能用的几种摆出来。挑哪个是你的事，但至少你是看过一圈再挑的，不是搜到第一个就装。

### 它平时怎么帮我

这种事经历多了，我慢慢养成个习惯。有需求先让它去问问世界上有没有人做好了，没有我再自己写。

我主要是省在找这一步。搜出来一堆重样的，它归个类算一份，省得我挨个点开发现都一样。它还会告诉我哪个是原版，哪个是被人转走改过的。真到要装了，它再帮我过一遍安全，本机有 codex 的话就让它把代码读一遍。哪步不放心，它就停下来等我点头。

### 收尾

world-aid 开源了，可以直接拿去用，懂代码的话也欢迎来提改动。

🔗 github.com/a28939876-max/world-aid
（仓库默认英文，中文看这个：github.com/a28939876-max/world-aid/blob/main/README.zh-CN.md）

要是这篇帮到你，转给那个啥都爱自己从头写的朋友。

---

## 二、推特 / X

### 中文帖（配 demo 图）

我想把个油管视频转成文字，让 world-aid 帮我找下字幕的工具。它翻出来十几个，先帮我归类去重，剩九个真不一样的做法一字排开：有只下文字的，有顺手截画面的，有自动翻译的，有走 Tor 防封的。

最扎眼那个走 Tor 的，听着功能最全，我差点选它。点开才发现是土耳其人给服务器机器人写的，下字幕要装 Tor、动系统，跟我想要的本地工具不是一回事。

要不是把这些找出来摆一块看，我就盯着那个"功能最全"的装了。world-aid 干的就是这个：先替你多找一圈，再让你挑。
🔗 github.com/a28939876-max/world-aid

### 英文帖（投 HN / 技术圈）

I wanted to turn one YouTube video into text. Asked world-aid to find a skill for it. It pulled up a dozen, grouped the duplicates, and laid out the nine that were actually different: plain text, one that also grabs frames, one that auto-translates, one that routes through Tor.

The Tor one looked the most capable, so I almost picked it. Turned out it was written in Turkish for a bot running on a server, wanted me to install Tor and touch system settings, nothing like the local tool I had in mind.

If I hadn't seen all of them side by side, I'd have installed the flashiest one. That's what world-aid does: it does the searching first, so you choose with more context.
🔗 github.com/a28939876-max/world-aid
