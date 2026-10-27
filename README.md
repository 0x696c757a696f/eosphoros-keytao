<a id="top"></a>

<div align="center">

# 🌟 晨星键道

**Eosphoros KeyTao** · 键道6 的 Rime 方案

*循星而行，以键成文。*

<a href="https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/0x696c757a696f/eosphoros-keytao?display_name=tag&style=flat-square&color=f5b301"></a>
<a href="https://github.com/0x696c757a696f/eosphoros-keytao/actions/workflows/package-master.yml"><img alt="Build and test" src="https://img.shields.io/github/actions/workflow/status/0x696c757a696f/eosphoros-keytao/package-master.yml?branch=master&style=flat-square&label=CI"></a>
<img alt="librime 1.9.0 or newer" src="https://img.shields.io/badge/librime-%E2%89%A5%201.9.0-476b9e?style=flat-square">
<img alt="Platforms" src="https://img.shields.io/badge/平台-Windows%20·%20macOS%20·%20Android%20·%20iOS%20·%20Linux-6f42c1?style=flat-square">
<img alt="Entries" src="https://img.shields.io/badge/词条-约%20117%20万-2ea44f?style=flat-square">

<br>

<a href="https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rime-full.zip"><img alt="下载通用完整版" src="https://img.shields.io/badge/⬇_下载-通用完整版-f5b301?style=for-the-badge"></a>
<a href="#如何使用"><img alt="安装指南" src="https://img.shields.io/badge/📦_安装-指南-476b9e?style=for-the-badge"></a>
<a href="https://keytao.rea.ink/practice"><img alt="在线练习" src="https://img.shields.io/badge/⌨️_在线-练习-2ea44f?style=for-the-badge"></a>

<a href="#适合怎样的使用者">适合谁</a> ·
<a href="#如何使用">下载与安装</a> ·
<a href="#-各平台皮肤与样式">皮肤</a> ·
<a href="#键道6编码概要">编码规则</a> ·
<a href="#词库组成">词库</a> ·
<a href="#上游来源与自动同步">来源与更新</a>

</div>

<br>

<table>
<tr>
<td width="33%" valign="top">

**⚡ 顶功盲打**<br>
双拼定音、笔画选字，下一个字的编码自动把上一个字顶上屏，很少按空格。

</td>
<td width="33%" valign="top">

**🌍 五个平台**<br>
小狼毫、鼠须管、同文、Fcitx5、元书、仓、玉兔毫、小小输入法，都有现成的包。

</td>
<td width="33%" valign="top">

**🔒 完全离线**<br>
不连云端，不收集输入。词库、Lua、OpenCC 都在本地，出了问题一查就知道。

</td>
</tr>
<tr>
<td valign="top">

**📚 117 万条词**<br>
常用词、医药化学、地名人名、基督宗派用语和英文，按需选 Full、Standard、Lite。

</td>
<td valign="top">

**🧰 工具齐全**<br>
`i` 英文、`u` 全拼反查、`v` 二分、`o` 生僻字，还有自造词、计算器、Emoji 和简繁。

</td>
<td valign="top">

**🔄 自动更新**<br>
上游词库每周自动同步、校验、合并，每月两次自动发布新版。

</td>
</tr>
</table>

## ✨ 关于晨星键道

晨星键道是键道6的一个 Rime 方案，Windows、macOS、Android、iOS 和 Linux 上的常见 Rime 前端都能用，另外也提供 Fcitx5 原生码表和小小输入法版本。方案 ID 是 `eosphoros`，仓库名是 `eosphoros-keytao`。

这个方案不是从零写起的。它的脉络是“星空键道 6.2 → 星猫键道 6 → 晨星键道”，大部分编码、词条和使用经验来自历代维护者，本仓库也已获得相关授权。我在这里做的，主要是在不改变键道手感的前提下，把词库理清楚、把各平台的安装包做齐，并让后续更新尽量自动完成。

<details>
<summary><b>🌅 名字的由来</b></summary>

“晨星”是黎明前最亮的那颗星。《默示录》22:16 里，耶稣自称“明亮的晨星”，这个名字也带着这层意思：光、指引和盼望。“键道”沿用原方案的名字，键是手里的工具，道是要走的路。顶功、音形结合和简单的取码规则，让字顺着熟悉的按键一路打出来。

晨星未必照亮整片长夜，却足以指明将明的方向。

</details>

<details>
<summary><b>🔗 相关链接</b></summary>

- 仓库：[0x696c757a696f/eosphoros-keytao](https://github.com/0x696c757a696f/eosphoros-keytao)
- 下载：[Releases](https://github.com/0x696c757a696f/eosphoros-keytao/releases/)
- 直接上游：[hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere)
- 星猫键道6 的使用笔记：[飞书文档](https://hu0w1jn4xq.feishu.cn/docx/ZgQ8deGPlozhWCxOyeucBvHJnPe)（原方案维护者整理，不是本仓库的文档）
- 键道6 练习：[直连](https://keytao.rea.ink/practice) · [Vercel 镜像（需代理）](https://keytao.vercel.app/practice)

</details>

<a id="适合怎样的使用者"></a>

## 💡 适合谁用

键道6用双拼定音，再用几个笔画和字根区分同音字。打字时下一个字的编码会把上一个字顶上屏，所以很少需要按空格或数字选字。会拼音、愿意花几天记一套双拼键位的人，上手不会太难。遇到不会读的字，可以用二分拆字或 GBK 编码反查。

它适合想完全离线打字、想知道每个字为什么是这个编码、愿意自己维护一点个人词库，或者需要在好几个设备之间用同一套方案的人。它不接云端，也不做长句预测，所以隐私和稳定性有保障，但整句联想比不过现代的云拼音。

如果你只想用全拼，或者很依赖整句预测，建议先去练习页试几天再决定。

这个方案的几个特点：

- 保留键道6原有的短码、顶功、飞键和首笔辅助码，老用户不需要重新适应。
- 内置约 117 万条码表记录，包括单字、常用词、医药化学等专业词、基督宗派用语和英文。长句、模板化的数字年份、重码代价高的低频词会被主动去掉，所以总数可能比某些上游少。
- `i` 开头直接打英文，`u`、`v`、`o` 分别是全拼、二分和 GBK 生僻字反查，不用切换方案。
- 带自造词、逐码提示、630 提示、计算器、日期时间、打字统计、Emoji、简繁和火星文。
- 词典、Lua、OpenCC 数据分别放在 `dicts/eosphoros/`、`lua/eosphoros/`、`opencc/eosphoros/`，出问题时容易查。
- 所有上游词库都锁定到具体的 Git commit，生成结果有校验值，更新靠自动化完成，详见[来源与自动更新](#上游来源与自动同步)。

> [!NOTE]
> 方案依赖 `librime-lua`，比纯码表方案大一些，配置也多一些。如果你更看重零学习成本，纯拼音或更精简的键道配置可能更合适。

<a id="快速安装"></a>
<a id="如何使用"></a>

## 📦 下载与安装

大致步骤只有三步：下载对应前端的压缩包，解压到 Rime 用户目录，然后重新部署。不确定选哪个就用通用包 [`eosphoros-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rime-full.zip)。前端需要支持 `librime-lua`，librime 建议 1.9.0 或更新。

> [!IMPORTANT]
> 解压时请保留压缩包里的 `dicts/eosphoros/`、`lua/eosphoros/` 和 `opencc/eosphoros/` 三个目录。只复制根目录下的 YAML 文件，词库、顶功、自造词、英文、Emoji 和简繁转换都会不完整。

<!-- release-download-table:start -->
| 平台 | 输入法 / 引擎 | 完整版 Full | 标准版 Standard | 精简版 Lite | 主题 / 皮肤 |
| --- | --- | --- | --- | --- | --- |
| 通用 | Rime | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rime-lite.zip) | [按所用前端选择](https://github.com/0x696c757a696f/eosphoros-keytao#-各平台皮肤与样式) |
| Windows | 小狼毫 Weasel | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-weasel-windows-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-weasel-windows-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-weasel-windows-rime-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-weasel-windows-rime-full.zip) |
| Windows | 玉兔毫 Rabbit | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rabbit-windows-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rabbit-windows-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rabbit-windows-rime-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rabbit-windows-rime-full.zip) |
| Windows | 小小输入法 Yong | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-windows-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-windows-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-windows-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-windows-full.zip)；[单独下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-desktop-skins.zip) |
| macOS | 鼠须管 Squirrel | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-squirrel-macos-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-squirrel-macos-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-squirrel-macos-rime-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-squirrel-macos-rime-full.zip) |
| macOS | Fcitx5 + Rime | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-rime-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-rime-full.zip) |
| macOS | Fcitx5 原生 Table | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-full.zip) |
| Android | 同文 Trime | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-trime-android-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-trime-android-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-trime-android-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-trime-android-full.zip) |
| Android | Fcitx5 + Rime | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-rime-lite.zip) | [独立主题包](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-themes.zip) |
| Android | Fcitx5 原生 Table | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-lite.zip) | [独立主题包](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-themes.zip) |
| Android | 小小输入法 Yong | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-android-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-android-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-android-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-android-full.zip) |
| iOS | 元书输入法 | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-lite.zip) | [.cskin 包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-full.zip) |
| iOS | 仓输入法 Hamster | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-hamster-ios-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-hamster-ios-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-hamster-ios-rime-lite.zip) | [.hskin 包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-hamster-ios-rime-full.zip) |
| Linux | Fcitx5 + Rime | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-rime-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-rime-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-rime-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-rime-full.zip) |
| Linux | Fcitx5 原生 Table | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-full.zip) |
| Linux | 小小输入法 Yong | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-linux-full.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-linux-standard.zip) | [下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-linux-lite.zip) | [包内提供](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-linux-full.zip)；[单独下载](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-desktop-skins.zip) |
<!-- release-download-table:end -->

**Fcitx5 用户选哪个包？** 名字里没有 `-rime` 的是 Fcitx5 官方 Table 码表，装起来最简单，不需要 Rime。带 `-rime` 的保留完整的 Rime 功能，需要装对应平台的 Rime 插件，Linux 上还要有 librime-lua。两种只能选一种，不要放进同一个数据目录。原生 Table 也有 `i` 英文、`u` 全拼、`v` 二分和 `o` 单字四个入口（例如 `ihello`、`uhao`），但模糊音、反查注释、Lua、OpenCC 和自造词只有 Rime 版才有。

### 🎚️ 三个词库档位

每个平台都有 Full、Standard、Lite 三档。它们的编码、Lua、OpenCC、自造词和主题完全一样，区别只在预装了多少词：

- **Full**：所有词库都装上，包括 51 万行的长尾扩展 `fjcy`。适合电脑和存储空间充足的手机。
- **Standard**：去掉 `fjcy` 和几类很专业的万象词（药品、医学、化学、台风），常用词、ICE、宗派词和地名人名都在。部署更快。
- **Lite**：只留单字、基础词组、核心短码和英文，适合内存小的手机。

<!-- dictionary-profile-stats:start -->
| 档位 | 当前记录数 | 同码记录数 | 同码记录率 | 实际组成 |
| --- | ---: | ---: | ---: | --- |
| Full | 1,176,793 | 57,019 | 4.845% | Standard + `fjcy` + 万象药品／医学／化学／台风 + xmjd6-rere 新增扩展词 |
| Standard | 629,018 | 21,362 | 3.396% | Lite + 宗派专题 + ICE + 万象地名／名人／基础词 + xmjd6-rere 新增基础词 |
| Lite | 251,430 | 11,931 | 4.745% | 用户词库 + 单字 + 基础词组 + 核心码 + `i` 英文 |

同码记录率指最终编码和别的词条相同的记录占该档位全部记录的比例。这是当前词库的静态快照，不包括你后来造的词，也不考虑客户端的词频调整。它适合拿来比较本项目的三个档位，和统计方法不同的其他方案直接比没有意义。
<!-- dictionary-profile-stats:end -->

拿不准就选 Full。一台设备只装一个档位，换档位后要重新部署或重新导入码表。

<details>
<summary><b>📂 各前端的用户目录</b></summary>

| 平台 | 前端 | 用户目录 |
| --- | --- | --- |
| Windows | [小狼毫 Weasel](https://github.com/rime/weasel/releases/latest) | `%APPDATA%\Rime` |
| macOS | [鼠须管 Squirrel](https://github.com/rime/squirrel/releases/latest) | `~/Library/Rime` |
| macOS | [Fcitx5 for macOS + Rime](https://fcitx-contrib.github.io/docs/im/rime.html) | `~/.local/share/fcitx5/rime/` |
| macOS | [Fcitx5 for macOS 原生 Table](https://github.com/fcitx/fcitx5-macos) | 在应用里导入码表 |
| Android | [同文 Trime](https://github.com/osfans/trime/releases/latest) | `/storage/emulated/0/rime/` |
| Android | [Fcitx5 for Android + Rime](https://github.com/fcitx5-android/fcitx5-android) | `/storage/emulated/0/Android/data/org.fcitx.fcitx5.android/files/data/rime/` |
| Android | [Fcitx5 for Android 原生 Table](https://github.com/fcitx5-android/fcitx5-android) | 在“输入法 → 码表管理”里直接导入 ZIP |
| Android | [小小输入法 Yong](https://yong.dgod.net/read.php?fid=2&tid=1) | `/storage/emulated/0/yong/.yong/` |
| iOS | [仓输入法](https://apps.apple.com/app/id6446617683)、[元书输入法](https://apps.apple.com/app/id6744464701) | 用应用自带的本地导入功能；仓输入法不支持在线下载方案 |
| Linux | [Fcitx5 + Rime](https://github.com/fcitx/fcitx5-rime) | `~/.local/share/fcitx5/rime/` |
| Linux | [Fcitx5 原生 Table](https://github.com/fcitx/fcitx5-chinese-addons) | `~/.local/share/fcitx5/` |
| Linux | [小小输入法 Yong](https://yong.dgod.net/read.php?fid=7&tid=6) | `~/.yong/` 或 `$XDG_CONFIG_HOME/yong/` |

部署失败，或者更新后候选还是旧的，先确认文件放进了前端真正在用的那个目录，再执行一次“重新部署”。大多数问题到这一步就解决了。

</details>

### 🪟 Windows

<details>
<summary><b>🪟 小狼毫 Weasel</b></summary>


1. 安装[小狼毫正式版](https://github.com/rime/weasel/releases/latest)或[测试版](https://github.com/rime/weasel/releases/tag/latest)。也可以用[水龙月 Fork 版](https://github.com/Techince/weasel/releases/latest)，从原版换过去时最好先卸载原版并重启一次。
2. 下载 `eosphoros-weasel-windows-rime-full.zip`（或其他档位），把里面的文件和目录全部复制到 `%APPDATA%\Rime`。
3. 在小狼毫菜单里点“重新部署”，然后在方案选单里选“晨星键道”。
4. 以后更新时直接覆盖同名文件再重新部署。个人词放在 `dicts/eosphoros/eosphoros.user.dict.yaml`，个人设置写在 `*.custom.yaml`，这样更新不会冲掉它们。

</details>

<details>
<summary><b>🪟 小小输入法便携版</b></summary>


1. 下载 [`eosphoros-yong-windows-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-windows-full.zip)（或其他档位）。包里已经有[小小输入法](https://yong.dgod.net/)程序、晨星配置和对应档位的码表，解压就能用，不需要再导入 Rime 方案。
2. 请解压到自己有写入权限的普通目录，比如 `D:\Apps\Yong`。放进 `Program Files` 的话，设置界面保存不了皮肤等配置。
3. 默认用 <kbd>Ctrl</kbd>+<kbd>Space</kbd> 激活。
4. 包里带了“晨星·极简”“晨星·黎明”“晨星·石墨”三套皮肤，初始仍是小小的默认皮肤。可以在设置里换，也可以把 `[IM]/skin` 改成 `skin/Eosphoros-Mono`、`skin/Eosphoros-Dawn` 或 `skin/Eosphoros-Graphite` 后重载。

</details>

<details>
<summary><b>🐰 玉兔毫 Rabbit</b></summary>


1. 玉兔毫现在在 [rimeinn/rabbit](https://github.com/rimeinn/rabbit) 维护。下载 [`eosphoros-rabbit-windows-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rabbit-windows-rime-full.zip)（或其他档位），解压到路径里没有空格的目录。
2. 运行玉兔毫，选晨星键道即可。方案文件已经在包里，不用再复制通用包。
3. `rabbit.custom.yaml` 默认用“晨星·黎明”，Windows 切到深色模式时自动换成“晨星·夜色”。
4. 输入 `\` 可以直接造词。想把造的词整理进正式词库，双击包根目录的 `ZZZC-Merge.cmd`；要撤回最近一次合并，运行 `ZZZC-Rollback.cmd`。这两个脚本会自己处理 Rabbit 的 `Data/` 和 `Rime/` 两个目录。

</details>

### 🍎 macOS

<details>
<summary><b>🍎 鼠须管 Squirrel</b></summary>


1. 安装[鼠须管正式版](https://github.com/rime/squirrel/releases/latest)或[测试版](https://github.com/rime/squirrel/releases/tag/latest)。
2. 解压 `eosphoros-squirrel-macos-rime-full.zip`（或其他档位），把全部内容复制到 `~/Library/Rime`。
3. 在鼠须管菜单里“重新部署”，再到方案选单选“晨星键道”。

</details>

<details>
<summary><b>🐧 Fcitx5 for macOS + Rime</b></summary>


1. 安装 [Fcitx5 for macOS](https://github.com/fcitx/fcitx5-macos)，在“系统设置 → 键盘 → 输入法”里加上小企鹅输入法，确认菜单栏能切到 Fcitx5。
2. 打开 Fcitx5 的 Plugin Manager，安装 **Rime** 插件。这个插件已经带了 librime 和 `librime-lua`。只装主程序的话，列表里不会出现“中州韵／Rime”。
3. 在“输入法 → 添加输入法”里先加一次“中州韵／Rime”，让它建好用户目录。
4. 下载 [`eosphoros-fcitx5-macos-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-rime-full.zip)（或其他档位）。在“高级 → 数据管理”里打开 Rime 用户目录 `~/.local/share/fcitx5/rime/`，把包里的东西复制进去。复制完应该能直接看到 `eosphoros.schema.yaml` 和三个 `eosphoros` 目录，中间不要多出一层文件夹。
5. 以前用过晨星的话，覆盖前先备份 `dicts/eosphoros/eosphoros.user.dict.yaml`、`dicts/eosphoros/eosphoros.zzc.dict.yaml`、`zzc_state/` 和自己的 `*.custom.yaml`。`build/` 目录是编译产物，不算备份。
6. 在数据管理里“重新部署”（默认快捷键 <kbd>Ctrl</kbd>+<kbd>Option</kbd>+<kbd>`</kbd>），然后在方案选单选“晨星键道”。
7. 试一下 `ihello`、`=1+1` 或造词。普通中文能打而这些不行，多半是 Rime 插件没装好或 `lua/eosphoros/` 不完整。
8. 不要改共享目录 `~/Library/fcitx5/share/rime-data`，也不要把用户目录链接到鼠须管的 `~/Library/Rime`。两个前端同时读写同一个用户词库可能会把它弄坏。
9. 排错时可以看 `/tmp/Fcitx5.log`，搜 `rime`、`lua`、`deploy` 或 `error`。更详细的目录说明见 [Fcitx5 macOS 的中州韵文档](https://fcitx-contrib.github.io/docs/im/rime.html)。

</details>

<details>
<summary><b>🐧 Fcitx5 for macOS 原生 Table</b></summary>


1. 安装 [Fcitx5 for macOS](https://github.com/fcitx-contrib/fcitx5-macos-installer/blob/master/README.zh-CN.md)，在 Plugin Manager 里装 Chinese Addons。这个版本不需要 Rime 插件。
2. 解压 [`eosphoros-fcitx5-macos-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-full.zip)（或其他档位）。
3. 打开“输入法 → 添加输入法 → 导入码表”，同时选中根目录的 `eosphoros.conf` 和 `eosphoros.txt`。只选一个、文件还在压缩包里，或者拿了带 `-rime` 的包，导入都会失败。
4. 重启 Fcitx5，添加“晨星键道”。`themes/` 里是 macOS 用的主题，可以在主题编辑器里另外导入。
5. 更新时重新导入同一档位的这两个文件。原生 Table 不读 Rime 用户目录，也没有 Lua、OpenCC、反查注释和自造词。

</details>

### 🤖 Android

<details>
<summary><b>🤖 同文输入法 Trime</b></summary>


1. 安装[同文输入法](https://github.com/osfans/trime/releases/latest)，在“配置管理 → 用户文件夹”里先选好或初始化默认目录。
2. 把 [`eosphoros-trime-android-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-trime-android-full.zip)（或其他档位）的全部内容放进 `/storage/emulated/0/rime/`。主题文件已经在包的根目录，不用另外下载。
3. 回到配置管理执行部署，先选晨星键道方案，再在主题设置里选“晨星键道·格调”。这个主题基于 mytrime 的“格调”布局，默认跟随系统切换黎明和夜色配色，也可以手动选黑白极简。

</details>

<details>
<summary><b>🐧 Fcitx5 for Android + Rime</b></summary>


1. 主程序和 [Rime 插件](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android-plugin-rime/)要从同一个渠道安装，比如都从 [Jenkins](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android/) 下载，版本也尽量一致。签名或版本对不上时，系统可能拒装插件，或者 Fcitx5 加载不了它。想自动检查更新可以再装一个[更新器](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android-updater/)。
2. 在系统设置里启用“小企鹅输入法5”，打开应用完成初始化，然后在“输入法 → 添加输入法”里加上“中州韵／Rime”。列表里没有 Rime，说明插件没装上、被停用了，或者和主程序不匹配。
3. 加过 Rime 之后才会出现用户目录 `/storage/emulated/0/Android/data/org.fcitx.fcitx5.android/files/data/rime/`。目录不存在时别手动建，先回到上一步把 Rime 加好。
4. 下载 [`eosphoros-fcitx5-android-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-rime-full.zip)（或其他档位），先在“下载”目录里解压。
5. 用系统自带的文件管理器（DocumentsUI）复制文件：在侧边栏选“小企鹅输入法5”，进到 `data/rime/`，把解压出的内容放进去。这样不需要第三方文件管理器、ADB 或 root。目标目录里应该直接是 `eosphoros.schema.yaml` 和三个 `eosphoros` 目录。
6. 已经有个人数据的话，先备份 `eosphoros.user.dict.yaml`、`eosphoros.zzc.dict.yaml`、`zzc_state/` 和 `*.custom.yaml`。不要清除整个应用数据，那会把插件配置和剪贴板也一起清掉。
7. 回到“输入法 → 中州韵／Rime → 数据管理”重新部署，再选“晨星键道”。以后更新就是“备份、覆盖、重新部署”。
8. 主题和方案分开装：下载 [`eosphoros-fcitx5-android-themes.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-themes.zip)，解开外层压缩包，再在“主题 → 导入主题”里逐个选里面的 ZIP，内层的 ZIP 不要再解压。Rime 包里的 `themes/` 也是同样的文件。
9. 部署后还是旧词库，先在应用设置里重启 Fcitx5 再部署一次。只有普通候选、`ihello` 和计算器都没反应，就检查 `lua/eosphoros/` 是否完整。Android 受限目录的操作可以参考 [Mintimate/oh-my-rime#96](https://github.com/Mintimate/oh-my-rime/issues/96)。

</details>

<details>
<summary><b>🐧 Fcitx5 for Android 原生 Table</b></summary>


1. 只需要安装 [Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android) 主程序，码表功能是内置的，不用 Rime 插件。
2. 下载 [`eosphoros-fcitx5-android-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-full.zip)（或其他档位），在“输入法 → 码表管理 → 导入码表 → 从 ZIP 导入”里直接选这个文件，然后添加“晨星键道”。
3. 这个 ZIP 故意不带主题，免得导入码表时出错。主题请另外下载 [`eosphoros-fcitx5-android-themes.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-themes.zip)，解开外层后在“主题 → 导入主题”里逐个导入 `eosphoros-dawn.zip`、`eosphoros-night.zip` 或 `eosphoros-mono.zip`。
4. 更新时在码表管理里重新导入同一档位就行，不涉及 Rime 目录和重新部署。

</details>

<details>
<summary><b>📦 小小输入法 Yong</b></summary>


1. 从[官方下载页](https://yongim.ysepan.com/)或[测试版帖子](https://yong.dgod.net/read.php?fid=2&tid=2)安装 Android 版。
2. 下载 [`eosphoros-yong-android-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-android-full.zip)（或其他档位）。这个包只有晨星的配置、码表和两套键盘皮肤，不含 APK。
3. 解压后把 `yong` 文件夹合并到手机存储里的同名目录，确认 `/storage/emulated/0/yong/.yong/yong.ini` 和 `/storage/emulated/0/yong/.yong/mb/eosphoros/eosphoros.txt` 都在。覆盖前记得备份自己的配置。
4. 切到别的输入法再切回来，或者在设置里重载配置。
5. 在皮肤设置里直接选“晨星·黎明”或“晨星·夜色”。皮肤文件已经放在 `yong/.yong/android/`，不要解压，也不要把 Windows 的 `skin/` 当成手机皮肤用。这两套皮肤以小小官方的 Android 键盘为底，候选展开、长按、Emoji、语音、编辑面板和剪贴板都保留，晨星只改了工具栏、名字和配色。

> [!NOTE]
> 本仓库不打包“晨星键道 APK”。公开的 [`dgod/yong`](https://github.com/dgod/yong) 仓库里没有能复现当前 APK 的构建工程和签名流程，重新签名的 APK 也会失去官方更新。单独发配置包，既能继续用官方 APK 更新，每次 Release 又能带上最新码表。

</details>

### 📱 iOS

<details>
<summary><b>📱 元书输入法</b></summary>


1. 在“输入方案”里选“下载方案”，填下面任一地址：
   - <https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-full.zip>
   - 国内网络可以用代理地址：<https://gh-proxy.com/https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-full.zip>
2. 下载完成后进“方案目录切换”，在 `RimeUserData` 里选刚导入的目录，点右上角“打开”。
3. 更新时重新下载，再回到“方案目录切换”选新目录并重新部署。
4. 键盘皮肤在包里的 `skins/` 下，要另外导入：解压后在元书里导入 `.cskin` 文件，不要把整个方案包当皮肤导入。
5. 想用 iCloud 同步自造词，请看[自造词使用教程](zzc/自造词使用教程.md)。

</details>

<details>
<summary><b>🐹 仓输入法</b></summary>


1. 安装[仓输入法](https://apps.apple.com/app/id6446617683)。
2. 用浏览器下载 [`eosphoros-hamster-ios-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-hamster-ios-rime-full.zip)（或其他档位），存到“文件”应用里。仓输入法不能直接从在线地址下载这个方案。
3. 在仓输入法里用本地导入选择这个 ZIP，或者在“文件”里通过共享菜单交给仓输入法打开。包里的词典、Lua、OpenCC 目录不要删。
4. 导入后重新部署，切换到晨星键道。
5. 需要皮肤的话，先解压，再通过共享菜单逐个打开 `skins/` 里的 `.hskin`。

</details>

### 🐧 Linux

<details>
<summary><b>🐧 Fcitx5 + Rime</b></summary>


1. 先确认桌面用的是 Fcitx5，而不是 Fcitx4 或 IBus。运行 `fcitx5-diagnose`，能看到 Fcitx5 进程和配置目录才算正常。如果 Fcitx5 本身还不能用，先看下面折叠的桌面环境设置。
2. 安装 [`fcitx5-rime`](https://github.com/fcitx/fcitx5-rime) 和 librime 的 Lua 插件。常见的包名：

   | 发行版 | 安装 |
   | --- | --- |
   | Arch / Manjaro / EndeavourOS | `fcitx5-rime`、`librime`，以及仓库或 AUR 里的 librime Lua 插件 |
   | Ubuntu / Debian / Linux Mint | `sudo apt install fcitx5-rime librime-plugin-lua` |
   | Fedora | `sudo dnf install fcitx5-rime librime-lua`，装完确认插件目录能被加载 |
   | 其他 | 安装对应的 Fcitx5 Rime 前端、librime 和 librime-lua |

3. 在 Fcitx5 配置工具里添加“中州韵／Rime”并切换一次，让它建好用户目录 `~/.local/share/fcitx5/rime/`（设置了 `XDG_DATA_HOME` 时在 `$XDG_DATA_HOME/fcitx5/rime/`）。
4. 下载 [`eosphoros-fcitx5-linux-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-rime-full.zip)（或其他档位），把内容复制到用户目录。已有晨星数据的话先备份 `eosphoros.user.dict.yaml`、`eosphoros.zzc.dict.yaml`、`zzc_state/` 和 `*.custom.yaml`。不要往 `/usr/share/rime-data/` 里放文件，那是包管理器管的。
5. 重启 Fcitx5，重新部署，选“晨星键道”。以后升级、换档位或改 YAML 都要重新部署。
6. 试 `ihello`、`=1+1` 或造词。只有普通候选的话，通常是 librime-lua 没装、插件目录没被加载，或者 `lua/eosphoros/` 不完整。排错时保存一份 `fcitx5-diagnose` 的输出，在日志里搜 `rime`、`lua_translator`、`plugin` 和 `error`。发行版的包没加载插件目录时，应该向发行版反馈，不要把插件文件手动塞进用户目录。

用户目录的标准位置也可以在 [Rime 用户文件夹说明](https://github.com/rime/home/wiki/UserData)里核对。

</details>

<details>
<summary><b>🐧 Fcitx5 原生 Table</b></summary>


这个版本不需要 Rime，只要 Fcitx5、配置工具和 `fcitx5-chinese-addons`：

| 发行版 | 安装 |
| --- | --- |
| Arch / Manjaro / EndeavourOS | `sudo pacman -S fcitx5-im fcitx5-chinese-addons fcitx5-configtool` |
| Ubuntu / Debian / Linux Mint | `sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-config-qt` |
| Fedora | `sudo dnf install fcitx5 fcitx5-chinese-addons fcitx5-configtool` |
| RHEL / AlmaLinux / Rocky Linux | 先启用 EPEL／CRB，再安装 Fcitx5 Chinese Addons |
| Deepin / UOS | 还在用 Fcitx4 的话先卸掉，再装 Fcitx5 和 Chinese Addons |

1. 解压 [`eosphoros-fcitx5-linux-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-full.zip)（或其他档位）。
2. 把 `inputmethod/eosphoros.conf`、`table/eosphoros.main.dict` 和需要的 `themes/` 复制到 `~/.local/share/fcitx5/` 下的同名目录。
3. 重启 Fcitx5，在配置工具里添加“晨星键道”。不能输入时用 `fcitx5-diagnose` 确认 Chinese Addons 已加载。
4. 更新时覆盖这三个目录里的晨星文件，再重启 Fcitx5。

原生 Table 版有完整的 1 到 6 码中文码表，候选顺序固定，无匹配或满码时自动上屏。它关闭了学习和自动造词，`i/u/v/o` 四个入口在第一个键就分开，不会和普通编码混在一起。Fcitx5 自带的标点、快捷短语、简繁转换、Emoji 和 Unicode 输入照常可用。

</details>

<details>
<summary><b>📦 小小输入法 Yong</b></summary>


1. 下载 [`eosphoros-yong-linux-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-linux-full.zip)（或其他档位），里面已经有小小的 Linux 程序。
2. 解压后进入 `yong/`，按[官方说明](https://yong.dgod.net/read.php?fid=7&tid=6)运行 `sudo ./yong-tool.sh --install`，再用 `./yong-tool.sh --select` 为当前用户选择输入法。
3. 包里有“晨星·极简／黎明／石墨”三套纯色皮肤，默认是黑白极简。装完重载或重启小小输入法。
4. GNOME 下建议通过 IBus 添加 Yong；KDE Plasma Wayland 在“系统设置 → 键盘 → 虚拟键盘”里选 Yong Wayland；wlroots 桌面可以按官方说明用 `yong --wayland`。XIM、IBus 和 Wayland 的环境变量不要全部叠在一起。

</details>

<details>
<summary><b>🖥️ Linux 桌面环境与应用兼容设置</b></summary>

上面的步骤做完能正常打字的话，这一节可以跳过。下面几套配置按桌面环境选一套，不要全部叠加。Fcitx5 官方也说过，没有一套变量能适合所有 X11 和 Wayland 环境，详见[设置 Fcitx5](https://fcitx-im.org/wiki/Setup_Fcitx_5) 和[在 Wayland 上使用 Fcitx5](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland)。

**KDE Plasma / Wayland**

1. 打开“系统设置 → 虚拟键盘”，选 Fcitx 5。
2. 为了兼容 XWayland 程序，在 `/etc/environment` 或 `~/.config/environment.d/im.conf` 里只设置：

   ```text
   XMODIFIERS=@im=fcitx
   ```

3. Plasma 5.27 以后一般不要全局设置 `GTK_IM_MODULE`、`QT_IM_MODULE`、`SDL_IM_MODULE`，否则候选窗可能会闪。某个旧的 X11 程序不能输入时，只给那个程序单独设置。
4. 由 KWin 虚拟键盘启动的 Fcitx5 不要从托盘菜单“重启”，新进程拿不到 KWin 传进来的 Wayland 连接。改完设置请注销重新登录。

**GNOME / Budgie**

1. Debian、Ubuntu、Linux Mint 可以运行 `im-config -n fcitx5`；Fedora 用 `im-chooser` 选 Fcitx5。之后注销重新登录。
2. Wayland 下至少给 XWayland 程序设置 `XMODIFIERS=@im=fcitx`。Qt 5 程序可以加 `QT_IM_MODULE=fcitx`，Qt 6.8.2 以后可以用 `QT_IM_MODULES="wayland;fcitx"`。
3. Chrome/Chromium 跑在 XWayland 时可以单独设置 `GTK_IM_MODULE=fcitx`。GNOME Shell 自己的界面里候选窗位置不对，可以试试 Fcitx5 文档里提到的 Kimpanel 扩展。
4. 只有旧版 GNOME/Budgie 没把 GTK 输入模块写对时，才需要这条命令：

   ```bash
   gsettings set org.gnome.settings-daemon.plugins.xsettings overrides "{'Gtk/IMModule':<'fcitx'>}"
   ```

**Deepin / UOS（DDE）**

1. 运行 `im-config -n fcitx5`，注销重新登录。
2. 如果启动的还是旧输入法，检查会话自启动里是不是 Fcitx4 和 Fcitx5 都在，只留 Fcitx5。
3. 只有 X11 程序不能输入时，才补上 `GTK_IM_MODULE=fcitx`、`QT_IM_MODULE=fcitx` 和 `XMODIFIERS=@im=fcitx`。Wayland 会话不要照搬这几项。

**Xfce / LXQt / LXDE / MATE 等 X11 桌面**

1. 确认 Fcitx5 会随会话启动。LXQt 在“会话设置 → 自动启动”里添加，其他桌面在“会话和启动”里添加 `fcitx5`。
2. 在 `~/.xprofile`（只对 X11 有效）或登录环境配置里加：

   ```bash
   export XMODIFIERS=@im=fcitx
   export GTK_IM_MODULE=fcitx
   export QT_IM_MODULE=fcitx
   export SDL_IM_MODULE=fcitx
   ```

   写在 shell 文件里要带 `export`，写在 `/etc/environment` 或 `environment.d` 里不要带。

**i3wm / awesome / bspwm 等平铺窗口管理器**

在 `~/.xprofile` 里加上和上面一样的四个变量，再让窗口管理器启动 Fcitx5：

| 窗口管理器 | 配置 |
| --- | --- |
| i3wm | `~/.config/i3/config` 里加 `exec --no-startup-id fcitx5 -d` |
| awesome | `~/.config/awesome/rc.lua` 里加 `awful.spawn.with_shell("fcitx5 -d")` |
| bspwm | `~/.config/bspwm/bspwmrc` 里加 `fcitx5 -d &` |

**Sway / Hyprland 等 wlroots 合成器**

- Sway 1.10 以后支持 text-input-v3。XWayland 程序设置 `XMODIFIERS=@im=fcitx`，Qt 5 按需设置 `QT_IM_MODULE=fcitx`，新版 Qt 6 用 `QT_IM_MODULES="wayland;fcitx"`。
- 自启动写在合成器的配置里，比如 Sway 用 `exec_always --no-startup-id fcitx5 -d`。其他合成器对输入法协议的支持不一样，请同时看它们的文档。
- kitty 需要特殊变量时用 `GLFW_IM_MODULE=ibus`，不是 `fcitx`。

**Electron / Chrome / VS Code**

- 走 XWayland 一般最稳：让程序读到 `GTK_IM_MODULE=fcitx` 或 `XMODIFIERS=@im=fcitx`。
- 一定要原生 Wayland 的话，KDE 下可以试：

  ```text
  --enable-features=UseOzonePlatform --ozone-platform=wayland --enable-wayland-ime --wayland-text-input-version=1
  ```

- GNOME、Sway 1.10 以后等支持 text-input-v3 的环境，把最后一项换成 `--wayland-text-input-version=3`。Chromium 和 Electron 在这方面的行为随版本变化，候选窗错位或打不了字时，先退回 XWayland。

</details>

### ❓ 常见问题

| 现象 | 先检查 |
| --- | --- |
| 方案选单里没有晨星键道 | `eosphoros.schema.yaml` 是否在前端实际使用的用户目录里，有没有重新部署 |
| 中文能打，顶功、造词、计算器不行 | `lua/eosphoros/` 是否完整，前端有没有 `librime-lua` |
| 没有 Emoji、简繁或火星文 | `opencc/eosphoros/` 是否完整，对应开关是否打开，有没有重新部署 |
| 更新后还是旧候选 | 是不是放进了另一个用户目录；重新部署，不行就退出前端再开 |
| 个人词或设置被覆盖了 | 个人内容应该放在 `eosphoros.user.dict.yaml` 和 `*.custom.yaml`，不要直接改生成出来的词典 |

<a id="-各平台皮肤与样式"></a>

## 🎨 皮肤与主题

皮肤是由各个前端自己画的，不是 Rime 方案的一部分，所以同一份配色文件没法在不同平台之间直接通用。下面是每个平台包里带的东西：

| 平台与前端 | 包里有什么 | 怎么用 |
| --- | --- | --- |
| Windows 小狼毫 | 晨星·黎明／夜色／极简，默认用 `EosphorosLight` / `EosphorosDark` 跟随系统明暗 | 想固定黑白极简，在 `weasel.custom.yaml` 里把 `style/color_scheme` 设为 `EosphorosMono` |
| macOS 鼠须管 | 同一套黎明／夜色／极简配色，用鼠须管 1.x 的新布局字段 | 在 `squirrel.custom.yaml` 里把 `style/color_scheme` 设为 `EosphorosMono` 可固定黑白极简 |
| Windows / Linux 小小输入法 | 晨星·极简、黎明、石墨，便携版默认极简；两边共用纯色 `skin.ini` | 放进程序目录的 `skin/` 或 `.yong/skin/`，再改 `[IM]/skin`；Windows 的 VBS 换肤脚本在 Linux 上不能用 |
| macOS Fcitx5 | 晨星自动明暗主题、黑白极简主题，以及其他桌面配色的 `.conf` | 从包里的 `themes/` 取：自动明暗用 `eosphoros-auto.conf`，极简用 `eosphoros-mono.conf` |
| iOS 元书 | 自动明暗和黑白极简两个 `.cskin`，以 ResourceforHamster 的完整万象布局为底，横竖屏、符号面板、候选展开、剪贴板、常用语、Emoji、方案切换和快捷手势都在 | 导入 `skins/eosphoros.cskin`，要纯黑白就用 `eosphoros-mono.cskin`。格式见[元书皮肤结构](https://ihsiao.com/apps/hamster/v3/docs/guides/skins/structure/) |
| iOS 仓输入法 | 自动明暗和黑白极简两个 `.hskin`，保留横竖屏、iPad、浮动和单手布局 | 通过共享菜单导入 `skins/eosphoros.hskin` 或 `eosphoros-mono.hskin`。格式见[仓皮肤指南](https://ihsiao.com/apps/hamster/docs/guides/keyboard_skins/) |
| Android 同文 | 基于 mytrime 3.3.10“格调”的完整 `eosphoros.trime.yaml`，三套晨星配色 | 放进同文用户目录，部署后选“晨星键道·格调” |
| Android Fcitx5 | 三个主题格式 2.1 的 ZIP | 解开外层包，逐个导入里面的 ZIP |
| Android 小小输入法 | 晨星·黎明／夜色，以官方 Android 键盘为底 | 在皮肤设置里直接选 |
| Linux Fcitx5 | 晨星日间／夜间／极简主题和其他桌面配色 | 把 `themes/` 解压到 `~/.local/share/fcitx5/themes/`，再选主题 |

> [!NOTE]
> `Hamster.yaml` 只管元书和仓输入法里自造词文件的同步规则，不是皮肤。元书的 `.cskin`、仓的 `.hskin` 和同文的主题 YAML 互不兼容，改扩展名也没用。

<details>
<summary><b>🐧 小企鹅主题怎么装</b></summary>

Fcitx5 的主题颜色是从 `weasel.yaml` 和 `squirrel.yaml` 自动转换来的：Rime 的 BGR／AABBGGRR 色值转成 Fcitx 的 RGBA，候选、首选、序号、注释、预编辑、背景和边框都分别对应。两份配置里同名的配色以鼠须管为准，小狼毫独有的也都保留。改了桌面配色后运行 `python tools/build_fcitx5_themes.py` 重新生成，CI 会拦下过期的主题。

**macOS**：打开“主题编辑器 → 基础 → 选择／导入主题”，推荐导入 `eosphoros-auto.conf`，浅色用黎明、深色用夜色。单独的 `eosphoros-主题名.conf` 在明暗模式下颜色不变。macOS 26 开着液态玻璃时，系统会根据候选窗下面的内容调整外观，这是系统行为，不是主题坏了。导入方法见 [Fcitx5 macOS 文档](https://fcitx-contrib.github.io/docs/theme/import.html)。

**Linux**：把压缩包里的 `themes/` 解压到 `~/.local/share/fcitx5/themes/`，应该能看到 `eosphoros-light/theme.conf` 这样的目录。在 `fcitx5-configtool` 的“附加组件 → 经典用户界面”里，亮色选 `eosphoros-light`，暗色选 `eosphoros-dark`，然后重启 Fcitx5。主题只用纯色字段，不依赖 SVG，避开了一些 Wayland/GTK 渲染器的兼容问题。格式见 [Fcitx5 主题文档](https://fcitx-im.org/wiki/Fcitx_5_Theme)。

</details>

<details>
<summary><b>🧩 其他皮肤资源</b></summary>

元书和仓的皮肤用的是 [ResourceforHamster](https://github.com/BlackCCCat/ResourceforHamster) 的完整布局（MIT 许可），晨星只改了名字、配色、圆角和少量细节。元书包里保留了可编辑的 Jsonnet 源码，构建时重新编译，并固定来源版本和校验值。[hamster-skin-skill](https://github.com/imfuxiao/hamster-skin-skill) 只用来参考格式和校验规则。

如果想换别的皮肤，可以看看这些地方。它们都不随本仓库分发，兼容性和授权请以作者说明为准：

| 前端 | 资源 | 说明 |
| --- | --- | --- |
| 元书 | [ResourceforHamster](https://github.com/BlackCCCat/ResourceforHamster)、[空山素影](https://github.com/luozikuan/kongshan-suying) | 选明确支持当前元书版本的 `.cskin`，或按项目说明导入编译 Jsonnet，方法以[元书官方文档](https://ihsiao.com/apps/hamster/v3/docs/guides/skins/structure/)为准。ResourceforHamster 里“仓”的旧皮肤已经不维护了，别拿来当新版元书皮肤 |
| 仓输入法 | [仓／元书皮肤交流频道](https://t.me/s/hamster_skins) | 只选 `.hskin` 且注明兼容当前版本的文件，格式见[仓官方皮肤指南](https://ihsiao.com/apps/hamster/docs/guides/keyboard_skins/)。社区文件没有经过本仓库审核 |
| 同文 | [mytrime 3.3.10“格调”](https://github.com/chwt163/mytrime/tree/main/3.3.10)、[rime-pure 的同文主题](https://github.com/SivanLaai/rime-pure)、[Trime 官方仓库](https://github.com/osfans/trime) | 晨星内置的是 GPL-3.0-or-later 授权的“格调”适配版；其他资源不要整体覆盖晨星的方案文件 |
| 小企鹅 Android | [tankb52/fcitx5-andoird-themes](https://github.com/tankb52/fcitx5-andoird-themes)、[官方在线主题设计器](https://fcitx5-android.github.io/theme-designer/) | 主题合集的 `themes/` 里有能直接导入的 ZIP。作者说过部分配色移植自其他主题，可能有版权问题，所以这里只放链接。也可以用官方设计器自己做一个 |
| 小小输入法 Android | [官方皮肤版块](https://yong.dgod.net/index.php?c=thread&fid=6)、[Android 皮肤制作参考](https://yong.dgod.net/read.php?tid=5022)、[新版兼容性讨论](https://yong.dgod.net/read.php?fid=6&tid=4977) | 优先用注明兼容当前 Android 版的皮肤。官方维护者建议从当前 APK 的默认皮肤改起 |
| 小小输入法 Windows / Linux | [皮肤格式说明与在线编辑器](https://yong.dgod.net/read.php?fid=7&tid=5)、[官方皮肤版块](https://yong.dgod.net/index.php?c=thread&fid=6)、[Pithiness / FreshX 等桌面皮肤](https://yong.dgod.net/read.php?tid=4338)、[Default5 SVG 多配色](https://yong.dgod.net/read.php?fid=6&tid=5267) | 基础 `skin.ini` 和 PNG/ZIP 皮肤两边都能用。Linux 的缩放通常更好，Windows 对复杂 SVG 支持有限。Default5 附带的 VBS 切换脚本只能在 Windows 上用 |

> [!WARNING]
> 导入第三方皮肤前先备份现有配置。如果某个皮肤要求替换词典、`eosphoros.schema.yaml`、`lua/eosphoros/` 或 `opencc/eosphoros/`，不要照做，否则晨星的编码、Emoji 或 Lua 功能会坏掉。

</details>

<details>
<summary><b>🌱 用东风破（plum）安装</b></summary>

`recipe/eosphoros/` 里有按平台和档位生成的配方，一共 30 份，和 Release 用的是同一份档位定义。命令是这样：

```bash
curl -fsSL https://raw.githubusercontent.com/rime/plum/master/rime-install | bash -s -- \
  0x696c757a696f/eosphoros-keytao:recipe/eosphoros/weasel-windows-rime-standard
```

Windows 也可以在小狼毫菜单的“输入法设定／获取更多输入方案”里填：

```text
0x696c757a696f/eosphoros-keytao:recipe/eosphoros/weasel-windows-rime-standard
```

配方名是“平台名 + 档位后缀”。平台名有 `rime`（通用）、`weasel-windows-rime`、`rabbit-windows-rime`、`squirrel-macos-rime`、`fcitx5-macos-rime`、`trime-android`、`fcitx5-android-rime`、`yuanshu-ios-rime`、`hamster-ios-rime`、`fcitx5-linux-rime`；后缀是 `-full`、`-standard` 或 `-lite`。比如 `recipe/eosphoros/trime-android-lite`。

东风破只管 Rime 用户目录。Fcitx5 原生 Table、小小输入法，以及要装到前端专用目录的主题和皮肤，还是用 Release 包。

</details>

<details>
<summary><b>🔧 中州韵助手（rimetool）兼容性</b></summary>

方案已经补齐了[中州韵助手](https://gitee.com/wubi98/rimetool)识别方案需要的结构：`default.yaml` 和 `default.custom.yaml` 都列出了 `eosphoros`，schema 里有方案名、开关状态和显式 `reset`、快捷键和 `menu/page_size`。它会按 `translator/dictionary` 找到当前档位的词库索引，索引的第一项是 `dicts/eosphoros/eosphoros.user`，薄荷模板可以据此找到个人词库。

在 rimetool 里可以选“薄荷解析模板”。模板要的 `transcription`、`emoji`、`ascii_punct` 和 `melt_eng` 都有：`transcription` 和原来的 `jffh` 都能触发简繁转换，`emoji` 和 `emoji_cn` 都能触发表情，`melt_eng/prefix` 实际参与 `i` 英文入口的识别，`ascii_punct` 和 `full_shape` 是 Rime 原生开关。

> [!WARNING]
> 宗派词库和几个大词库的正文里保留了分类注释，方便人工审阅。rimetool 不建议正文带注释，所以请不要在 rimetool 里对这些大码表做“全库重写”。正常浏览、编译和打字不受影响。

</details>

<a id="键道6编码概要"></a>

## ⌨️ 键道6编码概要

键道6的思路是：双拼定音，笔画和字根选字，下一个编码把上一个字顶上屏。单字先打两码音码，需要时再补最多四码形码；词组从每个字的音码里取码，碰到重码再补首笔。完整的键位图和历史规则可以看[键道图谱](https://pingshunhuangalex.gitbook.io/rime-xkjd/learn-xkjd/layouts)、[音码规则](https://pingshunhuangalex.gitbook.io/rime-xkjd/learn-xkjd/phonetics-rules)、[单字规则](https://pingshunhuangalex.gitbook.io/rime-xkjd/start-xkjd/characters)和[顶功说明](https://pingshunhuangalex.gitbook.io/rime-xkjd/advance-in-xkjd/top-up)。实际编码以本仓库的单字表、生成器和 schema 为准。

### 🔊 音码

每个字的读音用两个键表示：声母一个，韵母一个。和普通双拼思路一样，但只用 21 个键，`a`、`i`、`o`、`u`、`v` 留给形码，所以不能套用别的双拼键位。

- 零声母的 `a`、`e`、`o` 开头音节用 `x` 引导，例如 `安 → xf`、`爱 → xh`、`欧 → xd`。
- `j`、`q`、`x`、`y` 和 `ü` 系韵母按键道的拼合规则输入，例如 `居 → jl`、`去 → ql`。
- 有些声母或韵母可以用两个键之一（飞键），用来让左右手更顺，也能分散重码：

| 音 | 可用键 | 例子 |
| --- | --- | --- |
| `ch` | `j` / `w` | `超 → jz` 或 `wz` |
| `zh` | `f` / `q` | `找 → fz` 或 `qz` |
| `uang` | `m` / `x` | `爽 → emv` 或 `exv` |

飞键能和哪些韵母搭配是固定的，不是随便换。刚开始不用背，看候选就行。

<details>
<summary><b>✍️ 形码与拆字规则</b></summary>

两码音码后面可以接形码，用来在同音字里挑字。五个基本笔画对应五个键：

| 笔画 | 横 | 竖 | 撇 | 点／捺 | 折 |
| --- | --- | --- | --- | --- | --- |
| 键 | `v` | `i` | `u` | `o` | `a` |

单字最长六码，即两码音码加最多四码形码。平时多数字补一两码就能排到第一。拆字时：

1. 按规范笔顺取形，不能只看左右上下的位置。
2. 二分时尽量让两部分都是组字能力强的部件，大致按“独立汉字 → 常用字形 → 键道字根 → 偏旁部首”的顺序判断。
3. 部件尽量取大，但不能跨过笔画的断开或交叉处；实在拆不稳就按笔顺取笔画。
4. 有些字根是两码，两码合起来算一个字根；形码不满四码时按规则重复末码补齐。

</details>

### 🧱 词组

词组规则由 `eosphoros.full.dict.yaml` 里的 encoder 和本仓库的生成器共同决定：

| 词长 | 基础码 | 有重码时 |
| --- | --- | --- |
| 两字 | 两个字各取两码音码，共四码 | 依次补第一、第二个字的首笔，最长六码 |
| 三字 | 三个字各取音码的第一键，共三码 | 依次补三个字的首笔，最长六码 |
| 四字及以上 | 第一、二、三和最后一个字各取音码第一键，共四码 | 依次补第一、第二个字的首笔，最长六码 |

常用词先占短码，优先级低的词依次往后补首笔。如果六码都被别的词占了，自动导入的词会被跳过。

```text
爱德        xhde      两字词：xh + de
慕道班      mdb       三字词基础码
赞主曲      zqq → zqqu → zqquo → zqquoi
婚姻圣召    hyef → hyefa → hyefaa
```

### ⚡ 顶功

普通双拼要按空格确认，键道靠音码键和形码键的交替来判断一个字在哪里结束。当前首选已经是一个合法的 4 到 6 码编码时，继续打下一个字，前面的字就会自动上屏。

- 音码键：`b c d e f g h j k l m n p q r s t w x y z`
- 形码和触发键：`a v u i o ;`
- 中文顶功最长六码。`i`（英文）、`u`（全拼）、`v`（二分）和 `o`（GBK）开头的输入不走中文顶功。
- 拿不准时照样可以按空格或数字选字。开启整句模式后，中文顶功会自动关闭。

<details>
<summary><b>🎯 学习顺序建议</b></summary>

1. 先熟悉两码音码和常见的零声母，暂时用空格上屏。
2. 再记五个笔画，候选不在第一位时补一两码。
3. 熟悉两字、三字、四字以上词组的取码。
4. 最后练顶功和飞键。飞键只是让手感更顺，不会也能打字。

`i` 既是“竖”的形码，也是英文入口：只有在输入开头时才进英文。配合[练习页](https://keytao.rea.ink/practice)慢慢来就好，不用一次全记住。

</details>

## 🚀 日常使用

### 🔎 输入入口

| 想做什么 | 怎么输 | 说明 |
| --- | --- | --- |
| 打中文 | 直接输入键道编码 | 空格上屏首选，数字选对应候选，满足条件时自动顶屏 |
| 打英文 | <kbd>i</kbd> + 单词 | `ihello` 显示和输出的都是 `hello`，从第二个键起入口 `i` 会隐藏 |
| 用全拼查编码 | <kbd>u</kbd> + 全拼 | 知道读音但忘了编码时用，注释里显示键道码 |
| 查不会读的字 | <kbd>v</kbd> + 二分编码 | 按字形拆成两部分查字，同时显示键道码 |
| 繁体和生僻字 | <kbd>o</kbd> + 编码 | 进入 GBK 和扩展单字词典，这里不追加 Emoji |
| 快符 | <kbd>;</kbd> + 字母 | “快符开”时可用，具体行为可以在 custom 文件里调 |
| 计算器 | <kbd>=</kbd> + 算式 | 没有候选时输入，如 `=1+2*3`；有候选时 `=` 是下一页 |
| 打字统计 | `=tj` | 本机累计字数和速度 |
| 日期时间 | `rq` 等 | 由 Lua 生成日期和时间候选 |
| 自造词 | <kbd>\</kbd> 进入指令模式 | 见下面的速查和[自造词使用教程](zzc/自造词使用教程.md) |

`u`、`v`、`o` 只用来反查，不会出 Emoji。打字统计保存在 `zzc_state/eosphoros_typing_stats.tsv`，第一次运行时会读取旧的根目录 `typing_stats.txt` 并迁移过来，旧文件不会自动删除。手机上只把本机的统计写回应用目录，不会用 iCloud 上的统计覆盖另一台设备。

### ⏩ 按键

| 按键 | 什么时候 | 作用 |
| --- | --- | --- |
| <kbd>Space</kbd> | 有候选 | 上屏当前候选 |
| <kbd>1</kbd>～<kbd>5</kbd> | 有候选 | 选本页对应候选，每页默认 5 个 |
| <kbd>Tab</kbd> | 有候选 | 选第二个候选 |
| <kbd>-</kbd> / <kbd>=</kbd> | 有候选 | 上一页 / 下一页 |
| <kbd>F6</kbd> | 任何时候 | 切到下一个输入方案 |
| <kbd>F7</kbd> | 任何时候 | 切换简体和繁体输出 |
| <kbd>Ctrl</kbd> + <kbd>\</kbd> | 任何时候 | 打开或关闭 Emoji 候选 |

<details>
<summary><b>🎛️ 功能开关和默认值</b></summary>

开关的默认值写在 [`eosphoros.custom.yaml`](eosphoros.custom.yaml) 里，重新部署后生效：

| 开关 | 默认 | 作用 |
| --- | :---: | --- |
| 中文/英文 | 中文 | 整体 ASCII 模式。平时打英文用 `i` 就行，不用切 |
| 简体/繁體 | 简体 | OpenCC 简繁转换，也可以按 <kbd>F7</kbd> |
| 简约/逐码展示 | 逐码展示 | 是否显示逐码补全候选 |
| 简约/表情展示 | 表情展示 | 是否给中文候选加 Emoji |
| 快符关/快符开 | 快符开 | 是否启用 `;` 快符 |
| `;` 次选 | 关 | 是否把分号当作次选键 |
| 计算关/计算开 | 计算开 | 是否启用 `=` 计算器 |
| 空顶关/空顶开 | 关 | 是否启用空码顶功 |
| 简约/630提示 | 630提示 | 是否显示 630 规则提示 |
| 地球文/火星文 | 地球文 | 是否转成火星文 |
| 半角/全角 | 半角 | 标点和字符宽度 |

Emoji 是按需加载的，在原来 txjx 的映射之外，又从雾凇拼音补了约 2,500 个不重复的关键词，多了很多情绪、手势、人物、动物、食物、交通、旗帜和新版 Emoji。看不到 Emoji 时，依次检查“表情展示”是否开着、打的是不是普通中文编码（不是 `u/v/o` 反查）、`opencc/eosphoros/` 是否完整，然后重新部署。

</details>

<details>
<summary><b>📝 自造词指令速查</b></summary>

| 指令 | 作用 |
| --- | --- |
| `编码\自造词\` | 空码时新增；已有首选时替换首选，原来的词顺延到更长的编码 |
| `\自造词3`～`\自造词6` | 指定 3 到 6 码造词，码长够了自动结束 |
| `编码\+自造词\` | 作为这个编码的重码候选追加 |
| `编码\-数字\` | 删掉指定序号的候选，不写数字就删首选 |
| `编码\数字\` | 把指定候选置顶或前移 |
| `编码\<\` | 把当前候选提前一码，被占的编码依次整理 |
| `编码\++数字\` | 从可恢复列表里恢复指定项 |
| `\--\` | 撤回最近一次还没合并的操作 |
| `\!!!\` | 清空所有还没合并的操作 |

造的词会在会话结束时追加到 `dicts/eosphoros/eosphoros.zzc.dict.yaml`。想正式并入词库，运行 `zzc/` 里对应平台的合并脚本。完整流程（保存、跨设备同步、合并、撤回）见[自造词使用教程](zzc/自造词使用教程.md)和[合并脚本说明](zzc/README.md)。

Windows 上可以在仓库根目录运行：

```powershell
python .\zzc\Windows_词库合并.py
```

没装 Python 的话，直接双击 `zzc/Win_词库合并.exe`，撤回最近一次合并用 `zzc/Win_撤回合并.exe`。这两个 EXE 只在发布 Release 时在 Windows 上重新构建，构建后会实际跑一遍合并和撤回测试。构建方法见[合并脚本说明](zzc/README.md#重新构建-windows-exe)。

</details>

<details>
<summary><b>🔤 英文输入细节</b></summary>

英文词典直接并在主词典里，不需要单独的英文方案，也不用切换：

```text
输入：ihello
显示：hello
输出：hello
```

- 只按一个 `i` 时还会显示这个字母，继续打才隐藏。
- 英文不会触发中文的 4 到 6 码顶功。
- 大小写都能输出，常见技术词有别名，比如 `C++ → icpp`、`C# → icsharp`、`.NET → idotnet`。
- 英文编码都是 `i` 加小写字母，和中文编码冲突的条目在生成时就去掉了。

</details>

<details>
<summary><b>🌊 开启整句输入</b></summary>

默认是键道的顶功模式。想用整句输入，可以在 `eosphoros.custom.yaml` 里打开：

```yaml
patch:
  translator/enable_sentence: true
  translator/enable_user_dict: true
```

打开后中文顶功会自动停用，分号和单引号改作分隔符。相关的按键调整在 `eosphoros.custom.yaml` 的注释里有说明。

</details>

<a id="词库组成"></a>

## 📚 词库

下面是当前提交里各词库的记录数，不含自造词和个人词库。这张表由脚本生成，每次词库变动后自动更新。

<!-- dictionary-file-stats:start -->
| 词库 | 记录数 | 用途 |
| --- | ---: | --- |
| `dicts/eosphoros/eosphoros.danzi.dict.yaml` | 36,292 | 单字表，原样取自 rime-jiandao |
| `dicts/eosphoros/eosphoros.cizu.dict.yaml` | 190,589 | 基础词组，源自 xmjd6-rere，本仓库维护 |
| `dicts/eosphoros/eosphoros.catholicism.dict.yaml` | 3,131 | 天主教、礼仪、神学与东方礼词汇 |
| `dicts/eosphoros/eosphoros.protestantism.dict.yaml` | 541 | 传统新教宗派、信条、人物、日常教会用语及《和合本》词汇 |
| `dicts/eosphoros/eosphoros.orthodoxy.dict.yaml` | 88 | 东正教礼仪、圣像、灵修与教会制度专有词汇 |
| `dicts/eosphoros/eosphoros.oriental.dict.yaml` | 68 | 东方正统教会、合性论传统与成员教会专有词汇 |
| `dicts/eosphoros/eosphoros.assyrian.dict.yaml` | 71 | 东方亚述教会、东叙利亚礼与景教史专有词汇 |
| `dicts/eosphoros/eosphoros.core.dict.yaml` | 901 | 630 规则、快符和核心候选 |
| `dicts/eosphoros/eosphoros.fjcy.dict.yaml` | 514,010 | 长尾扩展词组，源自 xmjd6-rere，仅 Full |
| `dicts/eosphoros/eosphoros.ice.dict.yaml` | 360,404 | 雾凇拼音中文词，重新编码后的补充库 |
| `dicts/eosphoros/eosphoros.wanxiang.*.dict.yaml` | 46,561 | 万象七类专业与常识词，重新编码 |
| `dicts/eosphoros/eosphoros.rere.cizu.dict.yaml` | 386 | xmjd6-rere 近期新增的基础词，只占空闲码位 |
| `dicts/eosphoros/eosphoros.rere.fjcy.dict.yaml` | 103 | xmjd6-rere 近期新增的扩展词，只占空闲码位，仅 Full |
| `dicts/eosphoros/eosphoros.en.dict.yaml` | 23,648 | 雾凇拼音英文词，`i` 开头输入 |
| **合计** | **1,176,793** | 不含动态自造词和个人词库 |
<!-- dictionary-file-stats:end -->

<details>
<summary><b>🗂️ 每个词库是怎么来的</b></summary>

每个词库是怎么来的：

- **单字表 `danzi`**：原样取自 [rime-jiandao](https://github.com/amorphobia/rime-jiandao) 的 `dicts/01.danzi.txt`，本仓库不手工修改。其他所有词的编码都从这张单字表推出来。
- **基础词组 `cizu` 和扩展词组 `fjcy`**：最早来自 [xmjd6-rere](https://github.com/hugh7007/xmjd6-rere)，之后在本仓库里独立整理，修正过错码、去掉了重复和不合规的条目。`fjcy` 很大，只放在 Full 里。
- **xmjd6-rere 新增词 `rere.cizu`、`rere.fjcy`**：xmjd6-rere 之后陆续加的新词，会自动同步过来，但只收本方案还没有的词，按本地单字表重新编码，而且只用没人占的编码，所以不会挤掉任何现有候选。
- **核心短码 `core`**：630 规则、快符和最常用的短码。
- **雾凇补充词 `ice`**：取自 [rime-ice](https://github.com/iDvel/rime-ice) 的 `base`、`ext`、`others`。拼音会转换成键道编码，本地已有的词去掉，再过滤掉低频长尾、数字年份模板、8 字以上的 `ext` 整句、12 字以上的超长词，以及审过的古文整句、口号和法律条文片段。药名例外：片剂、胶囊、注射液、口服液这类剂型词不会因为低频或太长被过滤。编码时短词先占基础码，长词和低频同码词尽量往后补笔画；新加的词在同一个编码下最多 8 个候选，合并后的重码率不会高于同步前。
- **万象专业词 `wanxiang.*`**：取自 [rime-wanxiang](https://github.com/amzxyz/rime-wanxiang)，只要药品、医学、化学、地名、名人、台风名和一小部分高频基础词，拼音重新编码成键道码，不收联想句、普通人名、纠错、英文、单字和方言。本地已有的词先去掉，所有合法编码都被占的就跳过，所以不会新增异词同码。其中药品、医学、化学和台风四类上游已经删除了，本仓库保留最后一次同步的结果，不再更新；地名、名人和基础词仍然每周同步。
- **宗派专题词**：天主教、新教、东正教、东方正统教会和东方亚述教会各一个词库，都是人工审核后生成的，见下一段。
- **英文 `en`**：取自 rime-ice 的 `en` 和 `en_ext`，加上 `i` 前缀后并入主词典。

</details>

<details>
<summary><b>⛪ 宗派词库的收词原则</b></summary>

宗派词库以有宗派辨识度的信条、礼仪、制度、正式教会名称和历史术语为主，也收了信徒平时常打的崇拜、团契、查经、祷告、服事用语，但不会把“宗派名＋通用活动”硬拼成长词凑数。`protestantism` 另外收了审核过的《和合本》书卷名、人名、地名和固定译名，统一用和合本的译法（“马太”“约翰”“使徒行传”“启示录”），不混入思高本译名。新教部分覆盖信义宗、改革宗／长老宗、公理宗、圣公宗、浸信宗、循道卫理宗、再洗礼派／门诺会、贵格会、摩拉维亚弟兄会、弟兄会和救世军。东正教、东方正统教会、东方亚述教会和东方礼天主教会分开维护，免得把相近的叙利亚礼、圣像或牧首制度词放错地方；东方正统教会部分不用“一性论”这种不准确的说法。多段人名用间隔号，例如“马丁·路德”，编码时不算间隔号。

天主教新增词的审核清单是 [`tools/catholicism_expansion_2026.txt`](tools/catholicism_expansion_2026.txt)，另外四个宗派的是 [`tools/christian_traditions_2026.txt`](tools/christian_traditions_2026.txt)，核对来源和授权边界见 [`tools/christian_traditions_sources.md`](tools/christian_traditions_sources.md)。生成器依次尝试基础码和首笔辅助码，没有空闲编码的词一般不收。只有三个《和合本》书名例外：“哥林多后书”“帖撒罗尼迦后书”在标准规则下和各自的“前书”所有候选码完全相同，“雅各书”的所有候选码都已被旧词占用，所以人工审核后用了最终六码。除此之外，四个非天主教宗派词库没有新增异词同码。

</details>

### 📑 加载顺序

[`eosphoros.full.dict.yaml`](eosphoros.full.dict.yaml) 是完整的词库索引，Standard 和 Lite 的索引都从它自动生成。词库都不带权重，候选顺序就是加载顺序：

```text
user → zzc → danzi → cizu → core → ice → 宗派专题 → wanxiang → fjcy → rere.cizu → rere.fjcy → en
```

个人词和基础常用词排在最前，自动生成的 ICE 在它们之后，宗派专题和其他扩展再往后。xmjd6-rere 的新增词排在中文词库的最后。

<details>
<summary><b>👤 个人词库怎么加词</b></summary>

[`dicts/eosphoros/eosphoros.user.dict.yaml`](dicts/eosphoros/eosphoros.user.dict.yaml) 是留给你自己的词库，三个档位都有，而且最先加载。姓名、地址、专业术语、常用短语都适合放这里，但不建议塞大量公共词条。

在文件头部的 `...` 后面一行一条，词和编码之间用 **Tab** 分隔，`#` 开头的是注释。可以把文件里的示例去掉 `#` 直接改：

```text
词组<Tab>bmmso
单字<Tab>bb
```

`<Tab>` 指的是真正的 Tab 键，不是空格。改完要重新部署。文件头的 `name: eosphoros.user`、YAML 分隔符和 UTF-8 编码请保留，覆盖升级前最好单独备份这个文件。

Rime 系的前端（小狼毫、鼠须管、同文、玉兔毫、元书、仓、Fcitx5 + Rime）都会直接读这个文件。Fcitx5 原生 Table 和小小输入法用的是发布时生成的静态码表，改这个 YAML 对它们不起作用，要等下一个 Release 或者自己重新构建。

</details>

## ⚙️ 配置文件

<details>
<summary><b>📄 各配置文件的作用</b></summary>

| 文件 | 作用 |
| --- | --- |
| `eosphoros.schema.yaml` | 主方案：引擎、翻译器、反查和快捷键 |
| `eosphoros.custom.yaml` | 推荐修改的地方：开关、候选数、整句模式 |
| `eosphoros.{full,standard,lite}.dict.yaml` | 三个档位的词库加载顺序 |
| `default.custom.yaml` | 方案列表和全局选项 |
| `weasel.yaml` / `weasel.custom.yaml` | 小狼毫的候选窗样式和配色 |
| `squirrel.yaml` / `squirrel.custom.yaml` | 鼠须管的候选窗样式和配色 |
| `fcitx5/macos/themes/` | macOS Fcitx5 主题，`eosphoros-auto.conf` 自动切换明暗 |
| `fcitx5/linux/themes/` | Linux Fcitx5 经典界面主题 |
| `fcitx5/themes.yaml` | 小企鹅主题的来源清单，由脚本维护 |
| `mobile_themes/` | Fcitx5 Android 和同文的主题，以及移动端共用色板；元书和仓的皮肤在打包时生成 |
| `Hamster.yaml` | 元书和仓输入法的自造词同步规则，不是皮肤 |
| `eosphoros.symbols.yaml` | 标点和符号 |
| `dicts/eosphoros/eosphoros.core.dict.yaml` | 630、快符和核心短码 |
| `dicts/eosphoros/eosphoros.user.dict.yaml` | 个人词库 |
| `lua/eosphoros/` | Lua 模块 |
| `opencc/eosphoros/` | 简繁、Emoji、火星文数据 |

改了 YAML 要重新部署。个人配置尽量写在 `*.custom.yaml` 和个人词库里。`danzi`、`ice`、`wanxiang.*`、`rere.*` 和 `en` 是自动生成的，直接改会在下次同步时被覆盖。

</details>

<a id="上游来源与自动同步"></a>

## 🔄 来源与自动更新

### 🔗 词库来源

每个上游都锁定在 [`tools/upstream_dictionaries.lock.json`](tools/upstream_dictionaries.lock.json) 里的一个具体 commit，生成结果也记录了 SHA-256。所以任何时候都能从锁定的上游原样重建出当前的词库，CI 每次都会这样重建一遍来核对。

| 上游 | 取用的文件 | 生成的词库 | 现状 |
| --- | --- | --- | --- |
| [amorphobia/rime-jiandao](https://github.com/amorphobia/rime-jiandao) | `dicts/01.danzi.txt` | `eosphoros.danzi` | 每周同步 |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `cn_dicts/base`、`ext`、`others` | `eosphoros.ice` | 每周同步 |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `en_dicts/en`、`en_ext` | `eosphoros.en` | 每周同步 |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `opencc/emoji.txt` | `opencc/eosphoros/eosphoros_emoji_extra_*` | 每周同步 |
| [amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang/tree/wanxiang/dicts) | `diming`、`mingren`、`jichu` | `eosphoros.wanxiang.{diming,mingren,jichu}` | 每周同步 |
| [amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang/tree/wanxiang/dicts) | `yaopin`、`yixue`、`huaxue`、`taifeng`（上游已删除） | `eosphoros.wanxiang.{yaopin,yixue,huaxue,taifeng}` | 保留最后一版，不再变化 |
| [hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere) | `xmjd6.cizu`、`xmjd6.fjcy` 里 `baseline_commit` 之后新增的词 | `eosphoros.rere.{cizu,fjcy}` | 每周同步 |

本地的 `cizu`、`fjcy` 最早也来自 xmjd6-rere，但两边已经各自整理了很多年，所以不会整体覆盖，只按上面说的方式补新词。上游如果删掉了某个文件（就像万象那四类），同步时会自动把它从锁文件里移除，对应的词库保留最后一版，它的词和编码照样会被其他词库避让。

同步器不会去追上游分支的浮动内容。它比较“上次锁定的 commit”和“当前 HEAD”，只有用到的文件变了才按最新的完整快照重建，不会一点点叠补丁导致越走越偏。

### 🤖 哪些是自动的

| 内容 | 怎么更新 | 需要人管吗 |
| --- | --- | --- |
| 上游词库 | 每周一 04:17 UTC 检查，有变化就重建、跑完整检查，通过后自动合并 | 不需要 |
| 开发依赖（Pixi 锁文件） | 每周日刷新，跑完整检查，通过后自动合并 | 不需要 |
| GitHub Actions 和 pip 依赖 | Dependabot 每天／每周开 PR，CI 会跑 | 合并 Dependabot 的 PR |
| OpenCC 补充数据 | 每周一检查新的发布附件，校验后自动合并 | 不需要 |
| README 里的词库统计 | 每次推送都重新计算 | 不需要 |
| Release | 每月 1 日和 15 日检查，有新提交才验证、打包、发布 | 不需要 |
| rime-txjx 的 Lua 实现 | 每周三方合并，没有冲突就开 PR，有冲突就开 Issue | 合并 PR 或处理 Issue |
| xmjd6-rere 的方案代码 | 每周检查，有变化就开审校 Issue | 人工判断要不要移植 |
| 宗派词库的来源链接 | 每月联网检查一次 | 链接失效时处理 |
| 本地词库的错码 | 每次推送都检查，新的错码会让 CI 失败 | 只在改词库时 |

自动合并的那几项（词库、Pixi 依赖、OpenCC）都用固定的分支名：新一轮检查会直接替换上一轮还没合并的 PR，不会堆一串过期又互相冲突的 PR。合并前工作流自己已经在这个提交上跑过全部检查。如果想改回手动审核，在仓库的 **Settings → Secrets and variables → Actions → Variables** 里新建变量 `AUTOMATION_AUTO_MERGE`，值设为 `false`。这些工作流要能开 PR，需要在 **Settings → Actions → General → Workflow permissions** 里允许 GitHub Actions 创建 Pull Request。

需要人来判断的只剩两类：上游的代码改动（Lua 和方案逻辑），以及涉及编码取舍的词库调整。前者由工作流开 PR 或 Issue 提醒，后者在本地改完由 CI 把关。

<details>
<summary><b>🛠️ 手动同步词库</b></summary>

Windows 推荐用 PowerShell 7：

```powershell
pwsh -File .\tools\update_upstream_dictionaries.ps1
pwsh -File .\tools\update_upstream_dictionaries.ps1 -CheckOnly
pwsh -File .\tools\update_upstream_dictionaries.ps1 -Python .\.venv\Scripts\python.exe
```

也可以直接用 Python：

```powershell
python .\tools\sync_upstream_dictionaries.py --check
python .\tools\sync_upstream_dictionaries.py --refresh --write
```

</details>

<details>
<summary><b>🧬 Lua 与方案代码的上游</b></summary>

Lua 和自造词的实现参考了 [wzxmer/rime-txjx](https://github.com/wzxmer/rime-txjx)，已整合到 `a8769140`，记录在 [`tools/upstream_code.lock.json`](tools/upstream_code.lock.json)。[`tools/adapt_txjx_upstream.py`](tools/adapt_txjx_upstream.py) 按 [`tools/txjx_adaptation_manifest.json`](tools/txjx_adaptation_manifest.json) 里登记的“上游路径 → 本地路径”，把 `txjx` 的模块名和方案名换成 `eosphoros`，再以锁定的 commit 为共同祖先做三方合并。所以两边文件名可以不同，本地的修改也不会被整个覆盖：

```powershell
# 只预览差异、映射和冲突
python .\tools\adapt_txjx_upstream.py --json

# 全部映射都能安全合并时才写入，并更新锁
python .\tools\adapt_txjx_upstream.py --write --update-lock --json
```

对应的 `.github/workflows/check-txjx-upstream.yml` 每周跑一次。没有冲突的改动会推到固定分支并开 PR；本地和上游改了同一处、上游加了没登记的源码、删了已映射的文件，或者需要重新构建 Windows EXE 时，工作流不改任何文件，只开一个审校 Issue。

直接上游 xmjd6-rere 的方案代码另外在 [`tools/legacy_upstream.lock.json`](tools/legacy_upstream.lock.json) 里记录人工审校点，目前审到 `2c28424`。已经移植了节气的每日和每年计算缓存、`/jq` 的简体节气名称；本地保留更精确的天文节气算法、命名空间化的 Emoji 流程，不引入按平均日期算的倒计时和旧的 `xmjd6` 路径。`.github/workflows/check-reference-upstreams.yml` 每周检查这个上游、每月检查宗派词库的来源链接，发现变化只开 Issue，不会自动改目录、Lua、schema 或词库。

第三方来源、固定版本和许可证见 [`THIRD_PARTY.md`](THIRD_PARTY.md) 和 [`licenses/`](licenses/)。

</details>

### 🏷️ 发布

Release 工作流每月 1 日和 15 日的 04:17 UTC 检查一次。上次发布之后有新提交，才会继续验证、构建 Windows EXE、用真实的 librime 做部署测试、打包各平台并发布；没有新提交就直接结束，不会发空版本。每次发布都附带 `SHA256SUMS`，可以用来核对下载的文件。也可以手动运行 `Create Release with Zipped Branch Assets and Date` 强制发布。

## 🛠️ 维护与验证

Python 工具需要 3.11 或更新。推荐装 [Pixi](https://pixi.sh/)，用仓库锁定的环境：`pixi.lock` 固定了 Python、PyYAML、Pillow、Lua 和 PyInstaller 的版本，本机和 CI 的结果才一致。已经有 Python 环境的话，也可以直接跑下面这些命令。

<details>
<summary><b>🧪 完整的检查与维护命令</b></summary>

在仓库根目录执行：

```powershell
# 推荐：用锁定环境跑完整检查
pixi run check

# 从锁定的上游完整重建所有生成文件并比对（改了生成算法或输入时用）
pixi run generated

# 分项检查
python -m unittest discover -s tests -p 'test_*.py' -v
python .\tools\validate_repo.py
python .\tools\clean_dictionary_quality.py --check
python .\tools\audit_long_dictionary_entries.py --check
python .\tools\check_christian_sources.py --check
python .\tools\sync_upstream_dictionaries.py --check
python .\tools\check_legacy_upstream.py
python .\tools\check_txjx_upstream.py
python .\tools\adapt_txjx_upstream.py --json
python .\tools\build_platform_packages.py --check
python .\tools\build_fcitx5_table.py --check
python .\tools\build_fcitx5_themes.py --check
python .\tools\build_mobile_themes.py --check
git diff --check
```

`pixi run check` 先跑全部回归测试，再把生成文件和锁定的 SHA-256 逐一比对。

常用的维护命令：

```powershell
# 把 VERSION 和各 YAML 的 version 改成指定日期
python .\tools\update_versions.py 2026-08-10

# 去掉完全相同的词典记录
python .\tools\dedupe_dictionaries.py

# 检查词库质量（单字表不在范围内）
python .\tools\clean_dictionary_quality.py --check

# 删掉“同一个词已经有合法编码”的错码，并稳妥地迁移低优先级的本地重码
python .\tools\clean_invalid_duplicate_codes.py --check
python .\tools\optimize_local_collisions.py --check

# 检查全库的异常长词，确实要保留的固定术语写进白名单
python .\tools\audit_long_dictionary_entries.py --check

# 重新生成天主教扩展并整理分区
python .\tools\build_catholicism_expansion.py --write
python .\tools\organize_catholicism_legacy.py

# 重建四个宗派词库，再重建 ICE 让它避开新占的编码
python .\tools\build_christian_traditions.py --write
python .\tools\sync_upstream_dictionaries.py --write
```

测试覆盖了词组编码、飞键、天主教分类、四个宗派词库及其零重码、长词审计、词库质量、上游去重、重码上限、英文 `i` 前缀、各平台安装包的内容和自动同步工作流。Ubuntu 上的 CI 还会用 `rime_deployer` 编译一个临时用户目录，确认真实的 librime 能生成主方案、棱镜和主词典，并用 Mira 跑一遍实际的输入行为测试。

</details>

## 🗂️ 项目结构

<details>
<summary><b>🌳 展开目录结构</b></summary>

```text
.
├─ eosphoros.schema.yaml                     主方案
├─ eosphoros.{full,standard,lite}.dict.yaml  三个档位的词库索引（没有词条正文）
├─ dicts/eosphoros/                          所有词库：本地维护的、上游生成的和个人的
├─ lua/eosphoros/                            Lua 处理器、翻译器和过滤器
│  ├─ input/                                 按键、顶功、标点和快符处理
│  └─ zzc/                                   自造词的运行时、候选和操作链
├─ opencc/eosphoros/                         OpenCC 数据
├─ recipe/eosphoros/                         东风破配方（10 个平台 × 3 个档位）
├─ tools/                                    生成、同步、清理和验证工具
├─ tests/                                    Python 和 Lua 回归测试
├─ licenses/                                 第三方许可证
├─ THIRD_PARTY.md                            第三方来源说明
└─ .github/workflows/                        发布和定期同步工作流
```

</details>

## 🙏 致谢与授权

晨星键道的来路是“星空键道 6.2 → 星猫键道 6 → 晨星键道”。最该感谢的是吅吅大山、Proud丶Cat、热热、浮生、千年蟲和历代方案与词库的维护者。没有他们多年整理编码、词库和使用经验，就不会有这个方案。

### 🌱 引擎与方案

| 项目 | 在本仓库里的作用 |
| --- | --- |
| [librime](https://github.com/rime/librime)、[librime-lua](https://github.com/hchunhui/librime-lua) | Rime 输入法核心，以及方案用到的 Lua 扩展 |
| [OpenCC](https://github.com/BYVoid/OpenCC) | 简繁和地区用字转换 |
| [xkinput/Rime_JD](https://github.com/xkinput/Rime_JD) | 键道 Rime 方案的结构和历史实现 |
| [hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere) | 直接上游：方案、`cizu`／`fjcy` 词库的来源，以及小小输入法打包素材 |
| [wzxmer/rime-txjx](https://github.com/wzxmer/rime-txjx) | 模块化 Lua、Emoji 查询优化、自造词操作链、合并脚本和测试思路 |

### 📖 词典与资料

| 项目或资料 | 在本仓库里的作用 |
| --- | --- |
| [amorphobia/rime-jiandao](https://github.com/amorphobia/rime-jiandao) | 单字表和 `make_dicts.sh` 的生成规则 |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | 中文补充词、英文词和 Emoji 数据 |
| [amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang) | 药品、医学、化学、地名、名人、台风名和高频基础词，本仓库重新编码、去重并过滤 |
| [amorphobia/opencc-tonggui](https://github.com/amorphobia/opencc-tonggui) | 发布时下载并校验的 OpenCC 补充数据 |
| [SCIM Tables](https://github.com/scim-im/scim-tables) 与 LiangFen 作者 TianHeng | `liangfen` 二分反查的历史数据 |
| [AOSP PinyinIME](https://android.googlesource.com/platform/packages/inputmethods/PinyinIME.git) | `pinyin_simp` 拼音反查的历史数据 |
| [CrossWire SWORD `ChiUns`](https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=ChiUns)、[Digital Bible Society](https://bibles.dbs.org/CMNUNVS/pdf/CMNUNVS.pdf) 和[各教会的官方资料](tools/christian_traditions_sources.md) | 《和合本》书卷、人名、地名和宗派术语的人工核对来源；不转载释义或受版权保护的正文 |

<details>
<summary><b>🧰 前端、工具、皮肤资源和构建环境</b></summary>

| 项目 | 在本仓库里的作用 |
| --- | --- |
| [小狼毫](https://github.com/rime/weasel)、[鼠须管](https://github.com/rime/squirrel) | Windows 和 macOS 的 Rime 前端，以及桌面配色格式 |
| [Techince/weasel](https://github.com/Techince/weasel) | Windows 水龙月 Fork |
| [Fcitx5 macOS](https://github.com/fcitx-contrib/fcitx5-macos-installer)、[Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android)、[Fcitx5](https://github.com/fcitx/fcitx5) | 三个平台的小企鹅前端、安装说明和主题格式 |
| [同文 Trime](https://github.com/osfans/trime)、[chwt163/mytrime](https://github.com/chwt163/mytrime/tree/main/3.3.10) | Android Rime 前端；mytrime 以 GPL-3.0-or-later 提供了晨星同文主题所用的“格调”布局 |
| [仓输入法](https://apps.apple.com/app/id6446617683)、[元书输入法](https://apps.apple.com/app/id6744464701)及其[文档](https://ihsiao.com/apps/hamster/) | iOS Rime 前端，方案导入、自造词同步和皮肤格式 |
| [小小输入法 Yong](https://yong.dgod.net/)（[dgod/yong](https://github.com/dgod/yong)） | Windows、Linux 和 Android 的输入法平台；桌面端提供整合便携包，Android 只提供配置包 |
| [rimeinn/rabbit](https://github.com/rimeinn/rabbit) | 玉兔毫和它的便携包 |
| [rimeinn/mira](https://github.com/rimeinn/mira) | CI 里的真实输入行为测试 |
| [东风破 plum](https://github.com/rime/plum) | 配方的安装和更新机制 |
| [中州韵助手 rimetool](https://gitee.com/wubi98/rimetool)及其[文档](https://github.com/yanhuacuo/rimetool/wiki) | Rime 方案管理工具和“薄荷解析模板”的兼容结构 |
| [薄荷输入法（Mintimate/oh-my-rime）](https://github.com/Mintimate/oh-my-rime) | 薄荷模板的结构和开关命名，以及 Android DocumentsUI 的操作说明 |
| [ResourceforHamster](https://github.com/BlackCCCat/ResourceforHamster)、[hamster-skin-skill](https://github.com/imfuxiao/hamster-skin-skill)、[空山素影](https://github.com/luozikuan/kongshan-suying) | ResourceforHamster 以 MIT 许可提供了元书和仓皮肤的底稿；hamster-skin-skill 用来参考格式和校验规则；空山素影是仍在维护的元书外部皮肤 |
| [rime-pure](https://github.com/SivanLaai/rime-pure) | 同文外部主题参考，只放链接 |
| [tankb52/fcitx5-andoird-themes](https://github.com/tankb52/fcitx5-andoird-themes)、[Fcitx5 Android 主题设计器](https://fcitx5-android.github.io/theme-designer/) | 小企鹅安卓版的外部主题和官方主题工具，第三方主题不随仓库分发 |
| [仓／元书皮肤交流频道](https://t.me/s/hamster_skins) | 仓输入法第三方皮肤，内容和兼容性由发布者负责 |
| [Python](https://www.python.org/)、[PyInstaller](https://github.com/pyinstaller/pyinstaller)、[PyYAML](https://github.com/yaml/pyyaml) | 词库同步、质量检查、主题生成和 Windows 词库工具的构建环境 |

</details>

### ⚖️ 授权

> [!IMPORTANT]
> 致谢只表示来源、依赖或参考，不代表这些作者和项目为晨星键道提供官方支持，也不改变任何上游的许可证。放了链接不等于取得了皮肤、词典、软件或文章的再分发授权。

| 内容 | 本仓库怎么处理 | 许可 |
| --- | --- | --- |
| rime-jiandao 单字数据 | 锁定上游 commit，按本方案格式原样生成 | AGPL-3.0-or-later |
| rime-ice 中文、英文和 Emoji 数据 | 去重、转换编码，锁定生成文件的校验值 | GPL-3.0 |
| rime-wanxiang 分类词 | 重新编码、过滤和去重，只取词条不取编码和权重 | CC-BY-4.0 |
| rime-txjx 参考实现 | 人工审查后适配进 `lua/eosphoros/` 和 `opencc/eosphoros/` | MIT |
| mytrime 3.3.10“格调”主题 | 锁定上游文件，修正严格 YAML 解析问题，加入晨星名称和配色 | GPL-3.0-or-later |
| CrossWire `ChiUns`《和合本》 | 只选取并人工复核书卷名、人名、地名和固定译名 | 上游标注 Public Domain |
| 在线神学、教会和圣经资料 | 只用来人工核对词条，不批量抓取释义或正文 | 权利归各提供者，来源和取词原则另有记录 |
| 其他移动端第三方皮肤 | 只放外部链接，不复制、不修改、不放进仓库或 Release | 以皮肤作者的说明和许可证为准 |
| 小小输入法、玉兔毫等便携包 | 在上游程序或发行包的基础上加入晨星配置 | 程序本身的权利和许可仍归各自上游 |

仓库是分层授权的，没有一个许可证能覆盖所有历史词库和第三方数据，总的说明见 [`LICENSE.md`](LICENSE.md)。第三方来源、固定 commit、生成文件的 SHA-256 和许可证副本在 [`THIRD_PARTY.md`](THIRD_PARTY.md)、[`licenses/`](licenses/)、[`tools/upstream_dictionaries.lock.json`](tools/upstream_dictionaries.lock.json) 和 [`tools/upstream_code.lock.json`](tools/upstream_code.lock.json) 里。宗派词库的核对来源和取词边界见 [`tools/christian_traditions_sources.md`](tools/christian_traditions_sources.md)，机器可读的索引是 [`tools/christian_sources.json`](tools/christian_sources.json)。没有特别标注的文件，不要因为出现在致谢里就推定它们用同样的许可证；复用或再分发前请先看对应文件和仓库的授权说明。贡献规则和统一的检查命令见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

<p align="right"><a href="#top">⬆️ 返回顶部</a></p>
