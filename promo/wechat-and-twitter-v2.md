<!-- 内部说明（发布时不要带上）：口语版推广文案，用"找油管字幕差点装了个走 Tor 的工具"这个真实例子，已过两轮 codex 反 slop 审稿。 -->

# world-aid 推广文案 v2（口语版）

## 一、微信公众号推文

### 标题候选
- A：我就想下个油管字幕，差点装了个土耳其人的 Tor 工具
- B：装之前多看一眼，这次救了我一台机器
- C：让 AI 帮我找工具，它反手拦了我一下

### 正文

前几天我想把一个 YouTube 视频转成文字。视频有点长，自己边听边记太累，就想找个现成的工具把字幕拉下来。

搁以前我会自己搜半天，找个看着靠谱的、别人写好的小工具装上完事。这回我让 world-aid 去找。这是我自己攒的一个小东西，你用大白话告诉它想干嘛，它满世界帮你找现成的，找着了先帮你验一遍再问你装不装。

它一下翻出来十几个能下字幕的。我扫了眼挑了个看着顺眼的，正要装，它把我拦下了，让我先看看这个。

我点开就乐了。这玩意儿是个土耳其人写的，注释全是土耳其语。下个字幕而已，它非要我先装个 Tor 把网络绕一圈，中间还得拿管理员权限改系统、起服务。最逗的是它存文件的地方写死了，写的是某个云端机器人的目录，跟我这台电脑根本不挨着。

它本身不坏。我让本机的 codex 把代码从头到尾读了一遍，它说没发现偷文件、碰密码这些事。不过它提了个醒，这脚本会自己拿管理员权限去起一个 Tor 服务，等于没问我一声就动了系统设置，让我装之前最好看一眼。这东西其实是给跑在云服务器上的机器人用的，绕 Tor 是为了躲开 YouTube 封 IP。

可它跟我要的不是一回事。我就想在自己电脑上下个字幕存下来，它却要我装 Tor、动系统、还往一个我这儿根本不存在的目录里写。真要是没看就装，照着说明一路点同意，我这台机器就被一个我没怎么细看的脚本改了。

world-aid 帮我把住的就是这一下。它不替我判断谁好谁坏，就是在我点"装"之前，把这东西到底是个啥摊开给我看，我再决定装不装。

### 它平时怎么帮我

这种事经历多了，我慢慢养成个习惯。有个需求，先让它去问问世界上有没有人做好了，没有我再自己动手。

它帮我省心的地方，主要在搜出来一堆重样的时候。同一个东西被转了八遍，它会归个类、算一份给我，省得我一个个点开发现都一样。它还会提醒我哪个是原版，哪个是被人转走偷偷改过的。真到要装了，它再过一遍安全，本机装了 codex 的话就让它把代码读一遍。哪步不放心，它就停下来等我点头。

### 收尾

world-aid 开源了，可以直接拿去用，懂代码的话也欢迎来提改动。

🔗 github.com/a28939876-max/world-aid
（仓库默认英文，中文看这个：github.com/a28939876-max/world-aid/blob/main/README.zh-CN.md）

要是这篇帮到你，转给那个啥都爱自己从头写的朋友。

---

## 二、推特 / X

### 中文帖（配 demo 图）

我想把个油管视频转成文字，让 world-aid 帮我找个下字幕的工具。它翻出来十几个，我挑了一个正要装，它拦下来让我先看看。

一看是个土耳其人写的，下个字幕居然要我先装 Tor、还得拿管理员权限改系统。我让本机 codex 读了遍代码，它说不偷东西，但会自己动系统去起 Tor 服务，其实是给云服务器上的机器人用的，跟我想要的本地下字幕根本两码事。

要不是拦这一下，我照着说明一路点同意就装上了。world-aid 干的就是这个，装之前让你看清它到底是个啥。
🔗 github.com/a28939876-max/world-aid

### 英文帖（投 HN / 技术圈）

I just wanted a transcript from one YouTube video. I asked world-aid to find a skill for it, picked one of the dozen it turned up, and as I hit install it stopped me.

Turns out it was written in Turkish and wanted me to install Tor and run sudo just to grab subtitles. I had the local codex read the code. Not malicious, but it quietly starts a Tor service with sudo, and it's really built for a bot running on a server, not my laptop.

Without that pause I'd have sudo'd my way through the README. world-aid just shows you what a skill actually is before you install it.
🔗 github.com/a28939876-max/world-aid
