<a id="top"></a>

# 🌟 晨星键道 · Eosphoros KeyTao

> Repository: `eosphoros-keytao` · Rime schema ID: `eosphoros`

<p align="center">
  <a href="https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/0x696c757a696f/eosphoros-keytao?display_name=tag"></a>
  <a href="https://github.com/0x696c757a696f/eosphoros-keytao/actions/workflows/package-master.yml"><img alt="Build and test" src="https://github.com/0x696c757a696f/eosphoros-keytao/actions/workflows/package-master.yml/badge.svg"></a>
  <img alt="librime 1.9.0 or newer" src="https://img.shields.io/badge/librime-%E2%89%A5%201.9.0-476b9e">
  <img alt="UTF-8" src="https://img.shields.io/badge/encoding-UTF--8-2ea44f">
</p>

<p align="center">
  <a href="#适合怎样的使用者">💡 适合人群</a> ·
  <a href="https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rime-full.zip">⬇️ 下载方案</a> ·
  <a href="#如何使用">🚀 如何使用</a> ·
  <a href="#键道6编码概要">⌨️ 编码规则</a> ·
  <a href="#词库组成">📚 词库说明</a>
</p>

晨星键道是一款为「键道」输入方案打造的中文输入法。

“晨星”取黎明将至、星光引路之意。文字从指间落下，如循微光而行；每一次击键，都让所思所想渐次成形。

名字亦有一层来自《默示录》的含义。在《默示录》22:16 中，耶稣以“明亮的晨星”自称。因此，“晨星”既是自然的文学意象，也寄寓光明、指引与盼望。它并不改变键道作为高效中文输入方案的本质，只为这个名字留下更深的一层来处。

“键道”则承自原有的输入方案名称。键为所用，道为所行。借由顶功、音形结合与简洁的编码规则，让文字沿着熟悉的按键自然流出。

晨星未必照亮整片长夜，却足以指明将明的方向。

循星而行，以键成文。

晨星键道继承自星猫键道，并沿袭星空键道6.2以来的编码体系继续整理和维护。本仓库主要尝试在保留原有键道手感的同时，改善词库组织、跨平台部署和后续维护；其中大量编码、词条和使用经验都来自历代维护者，并非从零创造。本方案已获得相关授权，适用于 Windows、macOS、Android、iOS 和 Linux 上支持 Rime/Lua 的输入法前端。方案 ID、文件名和本地命名空间统一使用 `eosphoros`，GitHub 仓库名使用 `eosphoros-keytao`。

- 当前维护仓库：[0x696c757a696f/eosphoros-keytao](https://github.com/0x696c757a696f/eosphoros-keytao)
- 发行包：[Releases](https://github.com/0x696c757a696f/eosphoros-keytao/releases/)
- 上游方案：[hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere)
- 历史使用资料：[星猫键道6飞书笔记](https://hu0w1jn4xq.feishu.cn/docx/ZgQ8deGPlozhWCxOyeucBvHJnPe)（由原方案维护者整理，并非本仓库文档）
- 键道6练习：[直连网站](https://keytao.rea.ink/practice) · [Vercel 网站（需梯子）](https://keytao.vercel.app/practice)

<a id="适合怎样的使用者"></a>

## 💡 适合怎样的使用者

键道6以双拼音码为基础，再用少量字根和笔画形码筛选同音候选。它适合已经熟悉拼音、愿意学习一套双拼键位，并希望通过顶功减少空格和数字选重的用户；遇到不会读的字时，也可以使用二分或 GBK 入口反查。

晨星键道尤其适合希望离线使用、重视编码可解释性、愿意维护个人词库，或者需要在多个 Rime 前端之间迁移配置的用户。它不依赖云端大模型，也不以长句预测为主要方向；这带来隐私、稳定和可维护方面的便利，也意味着它不会在所有整句输入场景中胜过现代云拼音。

如果只想沿用全拼、不愿学习顶功和笔画辅助码，或者主要依赖云端整句预测，建议先体验练习页再决定是否长期使用。仓库会尽量保留既有键道规则、控制明显重码并改善跨平台部署，但实际体验仍取决于个人词频、客户端实现和使用习惯。

## ✨ 方案侧重与取舍

晨星键道不以“功能最多”或“词条最多”为目标，当前维护更看重编码可解释、常用输入稳定和更新过程可复查。以下是它相对侧重的方面，不代表一定比其他键道分支或输入方案更适合所有人：

- 继承键道6的短码、顶功、飞键和首笔辅助码规则，尽量不改变已有用户的基本手感。
- 约 117 万条内置码表记录，覆盖单字、常用词、专业补充、基督宗派词汇和英文；词库会主动舍弃一部分低频长句、模板词和重码收益较低的内容，因此记录数可能少于某些上游版本。
- `i` 键可直接进入英文输入；`u`、`v`、`o` 分别用于全拼、二分和 GBK／生僻字反查，减少临时切换方案的需要。
- 提供自造词、逐码补全、630 提示、计算器、日期时间、打字统计、Emoji、简繁和火星文等日常辅助功能；部分上游实验性工具没有照单全收。
- 词典、Lua 和 OpenCC 数据分别集中在 `dicts/eosphoros/`、`lua/eosphoros/` 与 `opencc/eosphoros/`，方便检查来源、替换生成文件和排查部署问题。
- 上游词库以 Git commit 和生成文件校验值记录来源，自动化负责发现变化和重复劳动，涉及编码取舍的内容仍尽量保留人工审查。
- Release 按输入法前端拆包，并提供东风破配方、桌面主题和部分移动端皮肤；受不同客户端能力限制，各平台体验仍不可能完全一致。

> [!NOTE]
> 本方案依赖 `librime-lua`，安装体积和配置复杂度高于精简码表；顶功、飞键和辅助码也需要一定学习。如果更重视零学习成本、云端整句预测，或只需要一个很小的基础词库，纯拼音或更精简的键道配置可能更合适。

第一次安装请直接阅读[“如何使用”](#如何使用)。其中保留了 Windows、macOS、Android、iOS 和 Linux 各客户端的用户目录、导入步骤和重新部署方法；较少使用的 Linux 内容统一放在各平台说明末尾，并按桌面环境列出 Wayland、X11、平铺窗口管理器及 Electron 应用的特殊设置。

| 阅读入口 | 适合内容 |
| --- | --- |
| [快速安装](#快速安装) | 下载方案、东风破部署、便携包与桌面主题 |
| [如何使用](#如何使用) | 各客户端导入、按键、功能开关与自造词 |
| [键道6编码概要](#键道6编码概要) | 飞键、首笔辅助码与词组编码规则 |
| [词库组成](#词库组成) | 各词典定位、记录数、优先级与去重原则 |
| [上游来源与自动同步](#上游来源与自动同步) | 锁定 commit、自动更新及维护方法 |

<a id="快速安装"></a>

## 📦 快速安装

### 📥 选择适合前端的方案包

1. 按下表下载适合当前输入法前端的压缩包；不确定时使用完整通用包 [`eosphoros-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rime-full.zip)。
2. 解压到 Rime 用户文件夹；保留压缩包内的目录结构。
3. 重新部署 Rime。
4. 在方案选单中选择“晨星键道”。

本方案包含 Lua 处理器，所用 Rime 前端需要带有 `librime-lua` 支持。建议使用 librime 1.9.0 或更新版本。

> [!IMPORTANT]
> 请完整保留压缩包中的 `dicts/eosphoros/`、`lua/eosphoros/` 与 `opencc/eosphoros/` 目录。只复制根目录 YAML 会导致词库、顶功、自造词、英文、Emoji 或简繁转换不完整。

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

> **Fcitx5 应该下载哪一个？** 不带 `-rime` 的包使用官方 Table／libime，安装最简单，
> 不需要 Rime；带 `-rime` 的包保留原有完整 Rime 功能，需要对应平台的 Rime 插件
> （Linux 还需要 librime-lua）。两者择一安装，不要放入同一个数据目录。
> 原生 Table 也包含 `i` 英文、`u` 连写全拼、`v` 二分和 `o` 单字编码四个静态入口；
> 例如 `ihello`、`uhao`。Rime 版则另外提供模糊音、反查注释、Lua、OpenCC 与 ZZC。

Fcitx5 Android 原生 Table 需要另行导入 [晨星主题包](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-themes.zip)。小小输入法 Windows／Linux 平台包已经集成桌面皮肤，同时另提供[独立皮肤包](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-desktop-skins.zip)，方便只更新皮肤；其余主题或皮肤均随对应平台包提供。

所有平台都提供相同的三个词库档位，输入逻辑、编码、Lua、OpenCC、自造词工具和主题保持一致，仅预置词库体量不同：

- **Full 完整版**：包含全部本地、`fjcy`、ICE、万象专业和宗派专题词库，适合桌面与存储充足设备。
- **Standard 标准版**：仅省略约 51 万行的 `fjcy`，保留 ICE 与专业词库，兼顾覆盖率和部署速度。
- **Lite 精简版**：保留基础单字、常用词组、核心词和英文入口，省略大型及专题扩展，适合低内存移动设备。

不确定时选择 **Full**；同一设备只安装一个档位，切换档位后需重新部署或重新导入码表。

| 平台 | 常见前端 | 默认用户目录 |
| --- | --- | --- |
| Windows | [小狼毫 Weasel](https://github.com/rime/weasel/releases/latest) | `%APPDATA%\Rime` |
| macOS | [鼠须管 Squirrel](https://github.com/rime/squirrel/releases/latest) | `~/Library/Rime` |
| macOS | [Fcitx5 for macOS + Rime](https://fcitx-contrib.github.io/docs/im/rime.html) | `~/.local/share/fcitx5/rime/` |
| macOS | [Fcitx5 for macOS 原生 Table](https://github.com/fcitx/fcitx5-macos) | 应用内导入码表 |
| Android | [同文 Trime](https://github.com/osfans/trime/releases/latest) | `/storage/emulated/0/rime/` |
| Android | [Fcitx5 for Android + Rime](https://github.com/fcitx5-android/fcitx5-android) | `/storage/emulated/0/Android/data/org.fcitx.fcitx5.android/files/data/rime/` |
| Android | [Fcitx5 for Android 原生 Table](https://github.com/fcitx5-android/fcitx5-android) | 应用内“输入法 → 码表管理”直接导入 ZIP |
| Android | [小小输入法 Yong](https://yong.dgod.net/read.php?fid=2&tid=1) | `/storage/emulated/0/yong/.yong/` |
| iOS | [仓输入法](https://apps.apple.com/app/id6446617683)、[元书输入法](https://apps.apple.com/app/id6744464701) | 下载对应平台包后，通过应用的本地导入功能安装；仓输入法不支持在线方案下载 |
| Linux | [Fcitx5 + Rime](https://github.com/fcitx/fcitx5-rime) | `~/.local/share/fcitx5/rime/` |
| Linux | [Fcitx5 原生 Table](https://github.com/fcitx/fcitx5-chinese-addons) | `~/.local/share/fcitx5/` |
| Linux | [小小输入法 Yong](https://yong.dgod.net/read.php?fid=7&tid=6) | `~/.yong/` 或 `$XDG_CONFIG_HOME/yong/` |

部署失败或更新后仍显示旧候选时，请先确认文件放在正确的用户目录，再从输入法菜单执行一次“重新部署”。

### 🎨 各平台皮肤与样式

皮肤由输入法前端绘制，并不是 Rime 方案本身的通用能力；因此同一套配色文件不能直接跨平台复用：

| 平台与前端 | 本仓库状态 | 配置方式 |
| --- | --- | --- |
| Windows 小狼毫 | 内置原创“晨星·黎明／夜色／极简”；默认由 `EosphorosLight` / `EosphorosDark` 自动跟随系统明暗模式 | 在 `weasel.custom.yaml` 中将 `style/color_scheme` 设为 `EosphorosMono` 可固定使用黑白极简 |
| macOS 鼠须管 | 内置同一套晨星黎明／夜色／极简配色，使用鼠须管 1.x 的新布局字段 | 在 `squirrel.custom.yaml` 中将 `style/color_scheme` 设为 `EosphorosMono` 可固定使用黑白极简 |
| Windows / Linux 小小输入法 | 内置“晨星·极简”“晨星·黎明”“晨星·石墨”，便携版默认启用黑白极简；两端共用纯色 `skin.ini` | 皮肤放入程序目录的 `skin/` 或用户目录的 `.yong/skin/`，再修改 `[IM]/skin`；复杂 Windows VBS 换肤脚本不能直接用于 Linux |
| macOS Fcitx5 | 平台包内置晨星专属自动明暗主题和黑白极简主题，并保留其余可导入 `.conf` | 从 `eosphoros-fcitx5-macos-full.zip` 的 `themes/` 取用；自动明暗用 `eosphoros-auto.conf`，极简用 `eosphoros-mono.conf` |
| iOS 元书输入法 | 平台包内置自动明暗与黑白极简两个 `.cskin`；以 ResourceforHamster 的完整万象键盘布局为底稿，保留横竖屏、数字／符号面板、候选展开、剪贴板、常用语、Emoji、脚本、键盘菜单、方案切换及快捷手势；标准皮肤日间使用黎明配色，系统进入黑暗模式后自动切换夜色配色 | 解压 `eosphoros-yuanshu-ios-rime-full.zip` 后，在元书中导入 `skins/eosphoros.cskin`；需要纯黑白外观时改用 `eosphoros-mono.cskin`。格式参见[元书皮肤结构](https://ihsiao.com/apps/hamster/v3/docs/guides/skins/structure/) |
| iOS 仓输入法 | 平台包内置自动明暗与黑白极简两个 `.hskin`；沿用成熟方案的横竖屏、iPad、浮动与单手布局；标准皮肤日间使用黎明配色，系统进入黑暗模式后自动切换夜色配色 | 解压 `eosphoros-hamster-ios-rime-full.zip` 后，通过系统共享菜单导入 `skins/eosphoros.hskin`；需要纯黑白外观时改用 `eosphoros-mono.hskin`。格式参见[仓皮肤指南](https://ihsiao.com/apps/hamster/docs/guides/keyboard_skins/) |
| Android 同文输入法 | Release 提供基于 mytrime 3.3.10 `style.trime.yaml`“格调”版的完整 `eosphoros.trime.yaml`，保留工具栏、符号、编辑和液态键盘，并内含三套晨星配色 | 把主题文件放入同文用户目录，重新部署后选择“晨星键道·格调”主题 |
| Android Fcitx5 | Release 提供三个符合主题格式 2.1 的可导入 ZIP | 解压外层包后，在主题管理中逐个导入内部 ZIP；不能直接导入外层合集 |
| Android 小小输入法 | 附带“晨星·黎明／夜色”皮肤；以小小官方完整 Android 键盘为兼容底稿，仅维护晨星工具栏、名称和配色覆盖 | 保留官方候选展开、按键提示、长按、Emoji、语音、编辑面板和剪贴板历史，并增加切换输入法的直接入口 |
| Linux Fcitx5 | 平台包内置晨星日间／夜间／极简专属主题，并保留其余桌面配色 | 从 `eosphoros-fcitx5-linux-full.zip` 的 `themes/` 解压到 `~/.local/share/fcitx5/themes/`，再选择相应主题 |

> [!NOTE]
> `Hamster.yaml` 只负责元书/仓输入法中的自造词文件同步规则，不是键盘皮肤。元书的 `.cskin`、仓的 `.hskin` 与同文的 Trime YAML 主题互不兼容，不能通过改文件名或扩展名混用。

#### 📱 移动端外部皮肤资源

Release 中的元书 `.cskin` 与仓 `.hskin` 都以 [ResourceforHamster](https://github.com/BlackCCCat/ResourceforHamster) 的成熟完整布局为底稿，在 MIT 许可下保留原有功能与多设备布局，仅修改晨星名称、自动明暗／黑白极简配色、圆角及少量界面细节。元书包保留可编辑 Jsonnet 源码并在构建时重新编译；构建脚本会固定来源版本、校验值和许可证。[hamster-skin-skill](https://github.com/imfuxiao/hamster-skin-skill) 仅作为格式与校验规则参考，不再作为简化皮肤底稿。下面同时列出其他可选资源。

| 客户端 | 外部资源 | 使用建议 |
| --- | --- | --- |
| 元书输入法 | [ResourceforHamster](https://github.com/BlackCCCat/ResourceforHamster)（综合资源）、[空山素影](https://github.com/luozikuan/kongshan-suying)（独立维护的元书皮肤） | 优先下载明确标注支持当前元书版本的 `.cskin`，或按项目说明在元书中导入并编译 Jsonnet；导入方法和结构以[元书官方文档](https://ihsiao.com/apps/hamster/v3/docs/guides/skins/structure/)为准。ResourceforHamster 中“仓”的旧皮肤已停止维护，不要当作最新版元书皮肤使用。 |
| 仓输入法 | [仓／元书皮肤交流频道](https://t.me/s/hamster_skins)（第三方社区资源） | 只选择扩展名为 `.hskin` 且作者明确标注兼容当前仓版本的文件，通过系统共享菜单导入；格式及操作以[仓官方皮肤指南](https://ihsiao.com/apps/hamster/docs/guides/keyboard_skins/)为准。社区文件未经本仓库审核，请自行确认来源、版本和授权。 |
| 同文输入法 Trime | [mytrime 3.3.10“格调”布局](https://github.com/chwt163/mytrime/tree/main/3.3.10)、[rime-pure 的同文主题](https://github.com/SivanLaai/rime-pure)、[Trime 官方仓库](https://github.com/osfans/trime) | Release 内置的是经 GPL-3.0-or-later 授权的 `style.trime.yaml` 晨星适配版；其他资源只作为外部选择，不要整体覆盖晨星键道。 |
| 小企鹅输入法 Android | [tankb52/fcitx5-andoird-themes](https://github.com/tankb52/fcitx5-andoird-themes)（第三方主题合集）、[官方在线主题设计器](https://fcitx5-android.github.io/theme-designer/) | 主题合集的 `themes/` 目录提供可直接导入的 ZIP，也附有 JSON 和预览图；作者明确说明部分配色移植自其他主题且可能存在版权争议，因此这里只作为外部发现入口、不随仓库分发。也可用官方设计器自行生成来源明确的主题。 |
| 小小输入法 Android | [官方皮肤版块](https://yong.dgod.net/index.php?c=thread&fid=6)、[Android 皮肤制作参考](https://yong.dgod.net/read.php?tid=5022)、[新版兼容性讨论](https://yong.dgod.net/read.php?fid=6&tid=4977) | 优先使用明确标注兼容当前 Android 版的皮肤；官方维护者建议从当前 APK 默认皮肤修改。第三方皮肤不随本仓库分发。 |
| 小小输入法 Windows / Linux | [官方皮肤格式说明与在线编辑器](https://yong.dgod.net/read.php?fid=7&tid=5)、[官方皮肤版块](https://yong.dgod.net/index.php?c=thread&fid=6)、[Pithiness / FreshX 等桌面皮肤](https://yong.dgod.net/read.php?tid=4338)、[Default5 SVG 多配色](https://yong.dgod.net/read.php?fid=6&tid=5267) | 基础 `skin.ini` 与 PNG/ZIP 皮肤可供 Windows、Linux 使用；Linux 系统缩放通常更好，Windows 对复杂 SVG 的兼容性有限。Default5 附带的 VBS 快速切换脚本仅适用于 Windows，Linux 只取皮肤资源并手动选择。 |

> [!WARNING]
> 导入前请备份客户端现有皮肤和配置。第三方资源可能随客户端升级改变格式；下载时应查看其最新 Release、README 和许可证。若皮肤要求替换方案词典、`eosphoros.schema.yaml`、`lua/eosphoros/` 或 `opencc/eosphoros/`，不要直接覆盖，以免破坏晨星键道的编码、Emoji 或 Lua 功能。

#### 🐧 小企鹅主题安装

主题颜色由 `weasel.yaml` 与 `squirrel.yaml` 自动生成，不是手工近似。转换程序会把 Rime 的 BGR／AABBGGRR 色值转换成 Fcitx 使用的 RGBA，并分别映射普通候选、首选、序号、注释、预编辑、背景和边框。两份桌面配置同名时采用鼠须管的当前定义，小狼毫独有的配色也会全部保留。

**macOS 小企鹅**

1. 主题直接取自 `eosphoros-fcitx5-macos-full.zip` 内的 `themes/`。
2. 打开“主题编辑器 → 基础 → 选择／导入主题”。推荐导入 `eosphoros-auto.conf`：浅色使用“晨星·黎明”，深色使用“晨星·夜色”，可跟随系统外观。
3. 需要其他桌面主题时，导入对应的 `eosphoros-主题名.conf`；单主题文件会在系统明暗模式下保持同一套颜色。
4. macOS 26 启用液态玻璃时，系统可能根据候选窗下方内容调整外观，这是小企鹅的系统级行为，不是主题颜色丢失。导入规则参见 [Fcitx5 macOS 官方文档](https://fcitx-contrib.github.io/docs/theme/import.html)。

**Linux 小企鹅**

1. 主题直接取自 `eosphoros-fcitx5-linux-full.zip` 内的 `themes/`。
2. 将压缩包直接解压到 `~/.local/share/fcitx5/themes/`；解压后应看到 `eosphoros-light/theme.conf` 等目录，不要再多套一层目录。
3. 打开 `fcitx5-configtool`，进入“附加组件 → 经典用户界面”。亮色主题选择 `eosphoros-light`，暗色主题选择 `eosphoros-dark`；也可以选择压缩包内其他桌面配色。
4. 应用设置后重启 Fcitx5。主题只使用官方支持的纯色字段，不依赖 SVG，避免不同 Wayland/GTK 渲染器加载 SVG 时出现兼容问题。格式参见 [Fcitx5 官方主题文档](https://fcitx-im.org/wiki/Fcitx_5_Theme)。

维护者修改桌面配色后，运行 `python tools/build_fcitx5_themes.py` 即可重新生成两端主题；CI 会用 `--check` 阻止过期主题进入 Release。

### 🌱 东风破（plum）安装与更新

仓库根目录提供通用配方和各前端配方，可由东风破直接安装或更新。macOS、Linux 以及其他带 Bash 的环境可执行：

```bash
curl -fsSL https://raw.githubusercontent.com/rime/plum/master/rime-install | bash -s -- 0x696c757a696f/eosphoros-keytao
```

Windows 可从小狼毫菜单打开“输入法设定／获取更多输入方案”，输入：

```text
0x696c757a696f/eosphoros-keytao:weasel
```

也可以在已经安装东风破的命令行中按前端选择：

```bash
rime-install 0x696c757a696f/eosphoros-keytao:weasel
rime-install 0x696c757a696f/eosphoros-keytao:rabbit
rime-install 0x696c757a696f/eosphoros-keytao:squirrel
rime-install 0x696c757a696f/eosphoros-keytao:mobile
```

不带后缀的命令安装通用 Rime 核心。东风破只部署 Rime 方案，因此不再提供
Fcitx5 配方；Fcitx5 用户应直接使用对应系统的官方 Table Release 包。其余配方会
复制对应前端所需 YAML、Lua、OpenCC 和 ZZZC 工具，并安全加入晨星方案列表。

### 🔧 中州韵助手（rimetool）兼容性

本方案已补齐[中州韵助手 rimetool](https://gitee.com/wubi98/rimetool)用于识别和编辑方案的主要结构：`default.yaml` 与 `default.custom.yaml` 都列出 `eosphoros`，schema 内有方案名、完整开关状态及显式 `reset`、本方案快捷键和 `menu/page_size`；根目录保留 RimeTool 会按固定路径查找的 `eosphoros.extended.dict.yaml` 兼容索引，实际词条统一位于 `dicts/eosphoros/`。索引首项为 `dicts/eosphoros/eosphoros.user`，可供薄荷模板定位个人主词库。

可在 rimetool 选择“薄荷解析模板”。模板要求的 `transcription`、`emoji`、`ascii_punct` 和 `melt_eng` 都已提供：`transcription` 与原有 `jffh` 都会触发简繁转换，`emoji` 与原有 `emoji_cn` 都会触发表情候选，`melt_eng/prefix` 实际参与 `i` 英文入口的识别，`ascii_punct` 与 `full_shape` 则使用 Rime 原生开关。

> [!WARNING]
> 为了让宗派词库及大型词库仍可人工审阅，部分码表正文保留了分类注释。中州韵助手的兼容约定不建议正文注释，因此不建议在其中对这些大型码表执行“全库重写”。正常浏览、Rime 编译和输入不受影响。`custom_phrase` 是雾凇方案专用的节点，本方案不添加无效的同名占位配置。

### 💾 便携与主题发行包

- Windows 小小输入法完整便携版：[eosphoros-yong-windows-full.zip](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-windows-full.zip)
- Windows / Linux 小小输入法原创皮肤：[eosphoros-yong-desktop-skins.zip](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-desktop-skins.zip)
- Linux 小小输入法完整便携版：[eosphoros-yong-linux-full.zip](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-linux-full.zip)
- Android 小小输入法晨星配置：[eosphoros-yong-android-full.zip](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-android-full.zip)
- 玉兔毫：[eosphoros-rabbit-windows-rime-full.zip](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rabbit-windows-rime-full.zip)
- macOS 小企鹅方案与主题：[eosphoros-fcitx5-macos-full.zip](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-full.zip)
- Linux 小企鹅方案与主题：[eosphoros-fcitx5-linux-full.zip](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-full.zip)

玉兔毫便携版建议解压到不含空格的路径。小小输入法版默认使用 `Ctrl + Space` 激活；请解压到当前用户可写的普通目录（如 `D:\Apps\Yong`），不要放入受权限保护的 `Program Files`，否则设置界面无法保存皮肤等配置。

<a id="键道6编码概要"></a>

## ⌨️ 键道6编码概要

键道6是一套“**双拼音码定音、字根与笔画形码选重、后续按键顶功上屏**”的音形码方案。普通单字先输入两位音码，再按需要追加最多四位形码；词组根据词长抽取各字音码，并在发生占码或重码时追加首笔辅助码。完整键位图和历史规则可参考[键道图谱](https://pingshunhuangalex.gitbook.io/rime-xkjd/learn-xkjd/layouts)、[键道音码](https://pingshunhuangalex.gitbook.io/rime-xkjd/learn-xkjd/phonetics-rules)、[单字规则](https://pingshunhuangalex.gitbook.io/rime-xkjd/start-xkjd/characters)与[顶功说明](https://pingshunhuangalex.gitbook.io/rime-xkjd/advance-in-xkjd/top-up)。本仓库实际编码以当前单字表、生成器和 Schema 为准。

### 1. 两码音码

每个汉字的读音固定由两键表示：第一键表示声母，第二键表示韵母。它与普通双拼的思路相同，但只使用 21 个音码键，`a`、`i`、`o`、`u`、`v` 留给形码，因此不能直接套用其他双拼方案的键位。

- `a`、`e`、`o` 开头的零声母音节使用 `x` 引导，例如 `安 → xf`、`爱 → xh`、`欧 → xd`。
- `j`、`q`、`x`、`y` 与 `ü` 系韵母按键道拼合规则输入，例如 `居 → jl`、`去 → ql`。
- 飞键允许部分声母或韵母使用两个键位，以改善左右手节奏并分散重码。

| 飞键音码 | 可用键位 | 示例 |
| --- | --- | --- |
| `ch` | `j` / `w` | `超 → jz` 或 `wz` |
| `zh` | `f` / `q` | `找 → fz` 或 `qz` |
| `uang` | `m` / `x` | `爽 → emv` 或 `exv` |

`ch`、`zh` 与不同韵母存在固定拼合范围，并非所有组合都能任意互换；初学时以码表候选和键位图为准，不必先死记全部飞键。

### 2. 单字形码

两位音码后可以继续输入形码筛选同音字。形码由五种基本笔画和少量字根组成，五个主笔画键如下：

| 笔画 | 横 | 竖 | 撇 | 捺/点 | 折/钩 |
| --- | --- | --- | --- | --- | --- |
| 按键 | `v` | `i` | `u` | `o` | `a` |

单字全码最长六码，即“**两位音码 + 最多四位形码**”。日常输入通常追加一两位形码即可定位，不需要每次打满。拆字时遵循以下原则：

1. 按规范书写顺序取形，不能只按视觉上的左右或上下位置拆分。
2. 二分时优先让两个部件都具有较强组字能力，通常按“独立汉字 → 常用字形 → 键道字根 → 偏旁部首”判断。
3. 部件尽量取大，但不能跨越书写中断或笔画交错；不能稳定拆分时按笔顺直接取基本笔画。
4. 部分字根使用双编码，两码视为一个完整字根；不足四位形码时可按规则重复末码补足。

### 3. 词组取码

词组编码规则由 `eosphoros.extended.dict.yaml` 的 encoder 与本仓库生成器共同约束。`A1/A2` 表示某字音码的第一、第二键，`a` 表示该字单字全码中的首个形码：

| 词长 | 基础音码 | 需要避重时追加 |
| --- | --- | --- |
| 两字词 | 第一字两位音码 + 第二字两位音码，共四码 | 依次追加第一、第二字首形码，最长六码 |
| 三字词 | 三个字各取音码第一键，共三码 | 依次追加三个字首形码，最长六码 |
| 四字及以上 | 取第一、第二、第三和末字的音码第一键，共四码 | 依次追加第一、第二字首形码，最长六码 |

候选分配遵循本地词库优先级和来源词频：常用词先占短码，较低优先级词依次尝试首形码扩展；所有合法六码都被其他词占用时，自动导入词会被跳过或受重码预算限制。

```text
爱德        xhde      两字词：xh + de
慕道班      mdb       三字词基础码
赞主曲      zqq → zqqu → zqquo → zqquoi
婚姻圣召    hyef → hyefa → hyefaa
```

### 4. 顶功与上屏

传统双拼通常需要空格确认候选；键道顶功会利用“音码键”和“形码键”的交替关系判断编码边界。当当前首选已经形成合法的 4～6 码中文编码，继续输入下一段编码时，前一个字词可以自动上屏，从而连续输入而少按空格。当前配置的主要范围是：

- 音码键：`b c d e f g h j k l m n p q r s t w x y z`
- 形码／触发键：`a v u i o ;`
- 中文顶功最长六码；英文 `i...`、全拼 `u...`、二分 `v...` 和 GBK `o...` 入口不套用普通中文顶功规则。
- 不确定候选时仍可按空格确认首选，或使用数字选择其他候选；启用流式整句输入后，中文顶功会自动停用。

### 5. 反查与特殊入口

| 入口 | 用途 | 示例或说明 |
| --- | --- | --- |
| `i` | 英文词典 | `ihello → hello`；继续输入后隐藏开头的 `i` |
| `u` | 连写全拼反查 | 输入普通全拼，并查看对应键道编码 |
| `v` | 二分拆字反查 | 不会读但知道字形时使用 |
| `o` | GBK／生僻字编码入口 | 查询单字及其键道码 |
| 反引号（&#96;） | 反查分隔 | 用于 Schema 中的反查组合 |

### 6. 推荐学习顺序

1. 先熟悉两码音码和常用零声母音节，暂时用空格上屏。
2. 再记五个基本笔画，只在候选不是首位时追加一两笔。
3. 熟悉两字、三字和四字以上词组的取码规律。
4. 最后练习顶功和飞键；飞键属于手感优化，不是开始输入的前置条件。

这里的 `i` 同时也是“竖”的形码；只有位于输入开头并进入英文模式时，才作为英文入口。可配合[键道6练习页](https://keytao.rea.ink/practice)逐步熟悉，而不必一次记住全部规则。

<a id="如何使用"></a>

## 🚀 如何使用

### 📋 各客户端安装、导入与更新

方案运行核心在各压缩包中一致；建议按前端下载对应包，以免携带无关平台配置：

| 平台 | 推荐客户端 | 安装方式 | 更新后必须做的操作 |
| --- | --- | --- | --- |
| Windows | [小狼毫](https://github.com/rime/weasel/releases/latest)、[水龙月 Fork](https://github.com/Techince/weasel/releases/latest)、[玉兔毫 Rabbit](https://github.com/rimeinn/rabbit/releases/latest)、[小小输入法 Yong](https://yong.dgod.net/) | 解压到用户目录，或下载对应便携包 | 重新部署；便携版按说明启动 |
| macOS | [鼠须管 Squirrel](https://github.com/rime/squirrel/releases/latest) | 解压 Rime 平台包到 `~/Library/Rime` | 重新部署 Rime |
| macOS | [Fcitx5 for macOS + Rime](https://github.com/fcitx/fcitx5-macos) | 安装 Rime 插件，导入带 `-rime` 的平台包 | 重新部署 Rime |
| macOS | [Fcitx5 for macOS 原生 Table](https://github.com/fcitx-contrib/fcitx5-macos-installer/blob/master/README.zh-CN.md) | 不安装 Rime 插件，在应用内导入原生 Table 包 | 重启 Fcitx5 |
| Android | [同文 Trime](https://github.com/osfans/trime/releases/latest) | 导入同文平台包 | 部署同文 |
| Android | [Fcitx5 for Android + Rime](https://github.com/fcitx5-android/fcitx5-android/releases/latest) | 安装官方 Rime 插件，导入带 `-rime` 的平台包 | 重新部署 Rime |
| Android | [Fcitx5 for Android 原生 Table](https://github.com/fcitx5-android/fcitx5-android) | 不安装 Rime 插件，在码表管理导入原生 Table 包 | 添加晨星 Table |
| Android | [小小输入法 Yong](https://yong.dgod.net/read.php?fid=2&tid=1) | 导入晨星配置包 | 重启 Yong |
| iOS | [元书](https://apps.apple.com/app/id6744464701)、[仓输入法](https://apps.apple.com/app/id6446617683) | 手动下载对应平台包，再通过应用的本地导入功能安装；仓输入法不能在线下载方案 | 切换到新方案目录并重新部署 |
| Linux | [Fcitx5 + Rime](https://github.com/fcitx/fcitx5-rime) | 安装 `fcitx5-rime` 与 `librime-lua`，部署带 `-rime` 的平台包 | 重新部署 Rime |
| Linux | [Fcitx5 原生 Table](https://github.com/fcitx/fcitx5-chinese-addons) | 安装 Chinese Addons，复制原生 Table 包文件 | 重启 Fcitx5 |
| Linux | [小小输入法 Yong](https://yong.dgod.net/read.php?fid=7&tid=6) | 使用 Yong 便携包 | 重启 Yong |

Rime 客户端不要只复制根目录 YAML，需保留 `dicts/eosphoros/`、`lua/eosphoros/`、
`opencc/eosphoros/`。Fcitx5 平台包是独立的官方 Table 码表，不使用这些 Rime 目录。

#### 🖥️ Windows

**小狼毫 Weasel**

1. 安装[小狼毫正式版](https://github.com/rime/weasel/releases/latest)或[小狼毫测试版](https://github.com/rime/weasel/releases/tag/latest)。也可使用[水龙月 Fork 版](https://github.com/Techince/weasel/releases/latest)；从原版切换到 Fork 版时，建议先卸载原版并重启系统。
2. 从 Release 下载 `eosphoros-weasel-windows-rime-full.zip`（或所需档位），解压后把压缩包内的文件和目录复制到 `%APPDATA%\Rime`。
3. 在小狼毫菜单中执行“重新部署”。
4. 打开方案选单，选择“晨星键道”。
5. 更新方案时覆盖同名方案文件即可；个人词汇应放在 `dicts/eosphoros/eosphoros.user.dict.yaml`，个人配置写在 `*.custom.yaml`，然后重新部署。

**小小输入法便携版**

1. 输入法本体由[小小输入法 Yong](https://yong.dgod.net/)提供；本仓库的完整晨星键道 Windows 便携版可下载 [`eosphoros-yong-windows-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-windows-full.zip)。
2. 解压后运行包内的小小输入法，不需要另外导入 Rime 方案。
3. 默认使用 `Ctrl + Space` 激活输入法。
4. `eosphoros-yong-windows-{full,standard,lite}.zip` 均包含 Windows 小小输入法程序、配置和对应档位码表；Release 不再提供配置-only 包。
5. 包内附带“晨星·极简”“晨星·黎明”“晨星·石墨”三套原创桌面皮肤，但保留小小默认皮肤作为初始选择。可在设置界面选择，或把 `[IM]/skin` 改成 `skin/Eosphoros-Mono`、`skin/Eosphoros-Dawn`、`skin/Eosphoros-Graphite` 后重载。

**玉兔毫 Rabbit**

1. 玉兔毫项目见 [amorphobia/rabbit](https://github.com/amorphobia/rabbit)；直接使用本方案可下载 [`eosphoros-rabbit-windows-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-rabbit-windows-rime-full.zip)（或所需档位）。
2. 解压到路径中不含空格的目录。
3. 运行玉兔毫并选择晨星键道；该包已经带入方案文件，不需要再复制 `eosphoros-rime-full.zip`。
4. 包内 `rabbit.yaml` 已合入 `weasel.yaml` 的主题和兼容样式，`rabbit.custom.yaml` 默认启用“晨星·黎明”，并随 Windows 黑暗模式自动切换“晨星·夜色”。候选序号使用 Rabbit 所需的 AutoHotkey v2 格式 `{:s}. `。
5. Rabbit 包只保留程序本体、运行晨星键道所需的词典／Lua／OpenCC 文件和少量用户配置，不包含东风破配方、其他平台皮肤、开发工具及仓库文档。
6. 输入 `\` 可直接使用方案内自造词；需要永久整理词库时双击包根目录的 `ZZZC-Merge.cmd`，撤回最近一次合并时运行 `ZZZC-Rollback.cmd`。两个入口会自动处理 Rabbit 的 `Data/` 与 `Rime/` 双目录，不需要手工移动词库。

#### 🍎 macOS

**鼠须管 Squirrel**

1. 安装[鼠须管正式版](https://github.com/rime/squirrel/releases/latest)或[测试版](https://github.com/rime/squirrel/releases/tag/latest)。
2. 下载并解压 `eosphoros-squirrel-macos-rime-full.zip`（或所需档位），把全部内容复制到 `~/Library/Rime`。
3. 从鼠须管菜单执行“重新部署”，再在方案选单中选择“晨星键道”。

**Fcitx5 for macOS + Rime**

1. 从 [Fcitx5 for macOS](https://github.com/fcitx/fcitx5-macos) 安装当前版本，并在 macOS“系统设置 → 键盘 → 输入法”中添加小企鹅输入法。首次启动后先确认菜单栏能够切换到 Fcitx5。
2. 打开 Fcitx5 的 Plugin Manager，安装 **Rime** 插件。当前官方插件集合中的 Rime 包同时带有 librime、`librime-lua` 等运行组件；只安装主程序时不会出现“中州韵／Rime”。
3. 在“输入法 → 添加输入法”中先添加“中州韵／Rime”，让 Fcitx5 初始化用户目录和部署环境。
4. 下载 [`eosphoros-fcitx5-macos-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-rime-full.zip)（或所需档位）。Full、Standard、Lite 只改变预置词库体量，安装方式相同。
5. Rime 用户目录为 `~/.local/share/fcitx5/rime/`。在“高级 → 数据管理”中打开 Rime 用户目录，解压平台包并把包内文件复制进去；复制后应直接看到 `eosphoros.schema.yaml`、`dicts/eosphoros/`、`lua/eosphoros/` 和 `opencc/eosphoros/`，不要额外套一层压缩包文件夹。
6. 已经使用过晨星键道时，覆盖前先备份 `dicts/eosphoros/eosphoros.user.dict.yaml`、`dicts/eosphoros/eosphoros.zzc.dict.yaml`、`zzc_state/` 与个人 `*.custom.yaml`。不要把 `build/` 目录当成个人数据备份。
7. 在数据管理中执行“重新部署”，或使用默认快捷键 <kbd>Ctrl</kbd>+<kbd>Option</kbd>+<kbd>`</kbd>。部署完成后在 Rime 的方案选单中选择“晨星键道”。
8. 验证 Lua 是否可用：确认方案能正常产生候选，再测试 `ihello` 英文入口、`=1+1` 计算器或方案内自造词功能。普通中文可输入但这些功能失效时，优先检查 Rime 插件和 `lua/eosphoros/` 是否完整。
9. 不要修改共享目录 `~/Library/fcitx5/share/rime-data`，也不要把用户目录链接到鼠须管的 `~/Library/Rime`；两个前端同时访问同一 LevelDB 用户词库可能造成损坏。
10. 更新 Fcitx5 或插件可使用“关于 Fcitx5 macOS”中的更新功能；更新方案包后仍需重新部署。排错时可查看 `/tmp/Fcitx5.log`，搜索 `rime`、`lua`、`deploy` 或 `error`。

该版本保留拼音模糊音、反查注释、Lua、OpenCC 与 ZZC。不要再导入同名原生 Table 包，两种实现择一安装。

详细目录与部署方法见 [Fcitx5 macOS 的中州韵文档](https://fcitx-contrib.github.io/docs/im/rime.html)。

**Fcitx5 for macOS 原生 Table**

1. 安装 [Fcitx5 for macOS](https://github.com/fcitx-contrib/fcitx5-macos-installer/blob/master/README.zh-CN.md)，再从 Plugin Manager 安装 Chinese Addons；不要安装或启用 Rime 插件中的同名晨星方案。
2. 下载并解压 [`eosphoros-fcitx5-macos-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-macos-full.zip)（或所需档位）。
3. 打开“输入法 → 添加输入法 → 导入码表”，同时选择根目录的 `eosphoros.conf` 与 `eosphoros.txt`。客户端会使用内置 libime 完成转换。
4. 导入成功后，确认输入法列表出现“晨星键道”；如果只选择了其中一个文件、文件仍在压缩包内或使用了带 `-rime` 的包，导入会失败。
5. `themes/` 内是 macOS 专用主题，可在主题编辑器中另行导入；重启 Fcitx5 后添加“晨星键道”。
6. 更新码表时重新导入对应档位的 `eosphoros.conf` 与 `eosphoros.txt`。原生 Table 不读取 Rime 用户目录，也不支持晨星的 Lua、OpenCC、反查注释或 ZZC。

#### 🤖 Android

**小小输入法 Yong**

1. 从[小小输入法官方下载页](https://yongim.ysepan.com/)或[官方测试版本帖](https://yong.dgod.net/read.php?fid=2&tid=2)安装当前 Android APK。
2. 下载 [`eosphoros-yong-android-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-android-full.zip)（或所需档位）。该文件包含晨星键道配置、码表和两套可直接使用的键盘皮肤，不包含也不修改 APK。
3. 解压后把包内 `yong` 文件夹合并到手机存储中的同名目录，确认存在 `/storage/emulated/0/yong/.yong/yong.ini` 和 `/storage/emulated/0/yong/.yong/mb/eosphoros/eosphoros.txt`。
4. 切换到其他输入法再切回小小输入法，或从设置中重载配置。覆盖前请备份个人配置和用户数据。
5. 包内已经放好 `yong/.yong/android/Eosphoros-Dawn.zip` 和 `Eosphoros-Night.zip`。在小小输入法的皮肤设置中直接选择“晨星·黎明”或“晨星·夜色”即可；不要解压这两个 ZIP，也不要把 Windows 的 `skin/` 皮肤当成 Android 键盘皮肤。两套皮肤以小小官方完整 Android 键盘为兼容底稿，保留横竖屏、候选展开、长按、离线 Emoji、语音、完整编辑面板、剪贴板历史、切换输入法和收起键盘；晨星键道只维护工具栏入口、名称与昼夜配色，不加入多配色合集、游戏或联网功能。

> [!NOTE]
> 本仓库不自动编译“晨星键道 APK”。当前公开的 [`dgod/yong`](https://github.com/dgod/yong) 仓库没有可直接复现当前 Android APK 的 Gradle 工程、应用签名及发布流程；二次签名 APK 还会失去官方升级链。自动生成独立配置包能保留官方 APK 更新与签名验证，同时让每次 Release 自动更新晨星码表。

**同文输入法 Trime**

1. 安装[同文输入法](https://github.com/osfans/trime/releases/latest)。
2. 在应用设置中打开“配置管理 → 用户文件夹”。
3. 先选择或初始化默认用户文件夹，再把 [`eosphoros-trime-android-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-trime-android-full.zip)（或所需档位）的完整内容导入 `/storage/emulated/0/rime/`；主题文件已经位于包的根目录。
4. 不需要另下主题包；重新部署后即可在主题设置中选择“晨星键道·格调”。该文件完整采用 mytrime 的“格调”键盘布局，不依赖同文官方默认皮肤。
5. 返回配置管理执行部署，先选择晨星键道输入方案，再在主题设置中选择“晨星键道·格调”。主题默认以黎明／夜色跟随系统，也可在主题配色中选用黑白极简。

**Fcitx5 for Android + Rime**

1. 项目主页为[小企鹅输入法 Android 版](https://github.com/fcitx5-android/fcitx5-android)。从同一发布渠道安装相互匹配的[主程序](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android/)和[Rime 插件](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android-plugin-rime/)；需要自动检查 Jenkins 更新时可另装[更新器](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android-updater/)。主程序和插件应来自同一签名渠道并尽量使用同一批次版本，否则 Android 可能拒绝安装插件或 Fcitx5 无法加载它。
2. 在 Android 系统设置中启用“小企鹅输入法5”，打开应用并完成首次初始化。此时只有主程序内置的输入法，尚未添加 Rime 时不会创建晨星需要的用户目录。
3. 打开“小企鹅输入法5 → 输入法 → 添加输入法”，添加“中州韵／Rime”。如果列表中没有 Rime，说明插件尚未安装、被系统停用，或与主程序版本／签名不匹配。
4. 首次添加 Rime 后会建立默认用户目录：`/storage/emulated/0/Android/data/org.fcitx.fcitx5.android/files/data/rime/`。目录不存在时不要手工猜路径，应先返回上一步成功添加 Rime。
5. 下载 [`eosphoros-fcitx5-android-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-rime-full.zip)（或所需档位），先在普通“下载”目录解压。复制目标应直接包含 `eosphoros.schema.yaml`、`dicts/eosphoros/`、`lua/eosphoros/` 与 `opencc/eosphoros/`，不能变成 `rime/eosphoros-fcitx5-android-rime-full/...` 的多余嵌套。
6. 推荐使用 Android 系统 DocumentsUI 管理文件：打开系统内置文件管理器，在侧边栏选择“小企鹅输入法5”，进入 `data/rime/` 后复制文件。该入口可以直接访问 `/sdcard/Android/data/org.fcitx.fcitx5.android/files/`，不需要第三方文件管理器、ADB 或 root。
7. 已有个人数据时，覆盖前先备份 `eosphoros.user.dict.yaml`、`eosphoros.zzc.dict.yaml`、`zzc_state/` 和个人 `*.custom.yaml`；不要删除整个应用数据，否则插件配置、剪贴板和其他输入法设置也会被清空。
8. 复制完成后返回“小企鹅输入法5 → 输入法 → 中州韵／Rime → 数据管理”，执行重新部署，再进入 Rime 方案选单选择“晨星键道”。更新平台包时重复“备份 → 覆盖 → 重新部署”即可。
9. 键盘主题与 Rime 方案分开管理。下载 [`eosphoros-fcitx5-android-themes.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-themes.zip)，解压最外层聚合包，再在“小企鹅输入法5 → 主题 → 导入主题”中逐个选择里面的主题 ZIP；内层 ZIP 不要再次解压。Rime 平台包的 `themes/` 也提供相同文件，已经下载平台包时可直接使用，无需重复下载独立主题包。
10. 验证 `ihello`、计算器或自造词等 Lua 功能。如果只有普通候选而 Lua 功能失效，检查 `lua/eosphoros/` 是否复制完整，并确认安装的是官方 Rime 插件而不是原生 Table 方案。
11. 部署后仍显示旧词库时，先从应用设置重启 Fcitx5 实例，再重新部署；仍失败时检查主程序与插件版本、目录层级以及文件访问是否被 DocumentsUI 中断。

该版本保留 Lua、OpenCC、反查注释和 ZZC；不要同时导入同名原生 Table 包。Android 受限目录的操作背景可参考 [Mintimate/oh-my-rime#96](https://github.com/Mintimate/oh-my-rime/issues/96)。

**Fcitx5 for Android 原生 Table**

1. 安装 [Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android) 主程序；自定义码表由本体内置 Chinese Addons／Table 提供，不需要 Rime 插件。剪贴板、符号／Emoji 选择器等客户端自带功能不受影响。
2. 下载 [`eosphoros-fcitx5-android-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-full.zip)（或所需档位）。
3. 打开“小企鹅输入法 → 输入法 → 码表管理 → 导入码表 → 从 ZIP 导入”，直接选择整个平台包。根目录中的 `eosphoros.conf` 与 `eosphoros.txt` 会由应用内置 libime 转换并安装。
4. 在输入法列表添加“晨星键道”。这个码表 ZIP 特意不含 `themes/`，避免 Android 码表导入失败。
5. 另行下载 [`eosphoros-fcitx5-android-themes.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-android-themes.zip)，先解压最外层聚合包，再在“小企鹅输入法5 → 主题 → 导入主题”中逐个选择其中的 `eosphoros-dawn.zip`、`eosphoros-night.zip` 或 `eosphoros-mono.zip`。三个内层主题 ZIP 不要再次解压，也不要从“码表管理”导入。
6. 更新时在码表管理中重新导入同一档位即可；主题只有在主题包更新时才需重新导入。原生 Table 不创建也不读取 `data/rime/`，因此不需要 Rime 插件、DocumentsUI 文件复制或重新部署 Rime。

#### 📱 iOS

**元书输入法**

1. 在“输入方案”中选择“下载方案”。
2. 使用以下任一地址：

   - 原始地址：<https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-full.zip>
   - 国内网络可用代理地址：<https://gh-proxy.com/https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yuanshu-ios-rime-full.zip>

3. 下载完成后进入“方案目录切换”，在 `RimeUserData` 中选择刚导入的方案目录，点击右上角“打开”。
4. 后续更新时重新下载方案，再回到“方案目录切换”选择更新后的目录并重新部署。
5. 使用 iCloud 联动和自造词合并时，继续阅读[自造词使用教程](zzc/自造词使用教程.md)。
6. 键盘皮肤已经放在平台包的 `skins/` 中，但仍需与输入方案分开安装：解压后在元书中逐个导入所需的 `.cskin`，不要把整个平台包当作皮肤导入。

**仓输入法**

1. 安装[仓输入法](https://apps.apple.com/app/id6446617683)。
2. 在浏览器中手动下载 [`eosphoros-hamster-ios-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-hamster-ios-rime-full.zip)（或所需档位），并把文件保存到 iOS“文件”应用；仓输入法不支持通过在线方案地址直接下载晨星键道。
3. 在仓输入法中使用本地方案导入功能选择刚下载的 ZIP；也可以从“文件”应用通过系统共享菜单交给仓输入法打开。不要先删除包内的词典、Lua 或 OpenCC 目录。
4. 导入或更新后重新部署，并在应用中切换到晨星键道。
5. 如需晨星键盘皮肤，先解压平台包，再通过系统共享菜单逐个打开 `skins/` 中所需的 `.hskin`；皮肤和输入方案需要分别导入。

#### 🐧 Linux

**小小输入法 Yong**

1. 下载 [`eosphoros-yong-linux-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-yong-linux-full.zip)（或所需档位）。它在当前小小 Linux 发行包基础上整合，不必另下程序本体。
2. 解压后进入 `yong/`，按[官方 Linux 安装说明](https://yong.dgod.net/read.php?fid=7&tid=6)执行 `sudo ./yong-tool.sh --install`；在当前用户下选择输入法可运行 `./yong-tool.sh --select`。
3. 完整包内含晨星码表和“晨星·极简／黎明／石墨”三套纯色皮肤，默认启用极简黑白。安装后重载或重启小小输入法。
4. GNOME 推荐通过 IBus 添加 Yong；KDE Plasma Wayland 可在“系统设置 → 键盘 → 虚拟键盘”选择 Yong Wayland；wlroots 桌面可按官方说明使用 `yong --wayland`。不要把 XIM、IBus 与 Wayland 的环境变量配置全部叠加。
5. 小小程序本体来自上游 `yong-lin.7z`，晨星只替换配置、码表和新增皮肤；上游重新上传同名附件后，下一次 Release 会直接使用新附件构建。

**Fcitx5 + Rime**

1. 先确认当前桌面会话已经使用 Fcitx5，而不是 Fcitx4 或 IBus。运行 `fcitx5-diagnose`，应能看到 Fcitx5 进程、配置目录和当前前端；如果基础 Fcitx5 尚未工作，先完成下方展开区域中的桌面环境设置。
2. 安装发行版提供的 [`fcitx5-rime`](https://github.com/fcitx/fcitx5-rime) 和 librime Lua 插件。常见包名如下；发行版拆包方式不同，安装后应再次使用 `fcitx5-diagnose` 确认 Rime 与 Lua 插件均已加载。

   | 发行版 | 安装命令或说明 |
   | --- | --- |
   | Arch / Manjaro / EndeavourOS | 安装 `fcitx5-rime`、`librime` 和仓库／AUR 提供的 librime Lua 插件包 |
   | Ubuntu / Debian / Linux Mint | `sudo apt install fcitx5-rime librime-plugin-lua` |
   | Fedora | `sudo dnf install fcitx5-rime librime-lua`，并检查当前软件包是否能正确加载插件目录 |
   | 其他发行版 | 安装等价的 Fcitx5 Rime 前端、librime 与 librime-lua 软件包 |

3. 在 Fcitx5 配置工具中添加“中州韵／Rime”并切换一次，让前端建立用户目录。默认目录是 `~/.local/share/fcitx5/rime/`；设置了 `XDG_DATA_HOME` 时则位于 `$XDG_DATA_HOME/fcitx5/rime/`。
4. 下载 [`eosphoros-fcitx5-linux-rime-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-rime-full.zip)（或所需档位），解压后把包内全部内容复制到 Rime 用户目录。目标目录应直接包含 `eosphoros.schema.yaml`、`dicts/eosphoros/`、`lua/eosphoros/` 与 `opencc/eosphoros/`，不要多套一层文件夹。
5. 已有晨星数据时先备份 `dicts/eosphoros/eosphoros.user.dict.yaml`、`dicts/eosphoros/eosphoros.zzc.dict.yaml`、`zzc_state/` 和个人 `*.custom.yaml`。系统共享目录 `/usr/share/rime-data/` 由软件包管理器维护，不应复制或修改晨星文件。
6. 重启 Fcitx5，在状态菜单或 Rime 配置入口执行重新部署，再从 Rime 方案选单选择“晨星键道”。升级晨星平台包、切换 Full／Standard／Lite 或修改 YAML 后都必须重新部署。
7. 验证普通中文候选后，再测试 `ihello`、`=1+1` 或自造词功能。只有普通 Rime 候选而这些功能失效，通常表示 librime-lua 未安装、插件目录没有被前端加载，或 `lua/eosphoros/` 不完整。
8. 排错时先保存 `fcitx5-diagnose` 输出，并查看当前会话启动 Fcitx5 的终端／systemd 日志，搜索 `rime`、`lua_translator`、`lua_filter`、`plugin` 和 `error`。若发行版的 `fcitx5-rime` 没有加载 librime 插件目录，应优先使用发行版修复包或向其维护者报告，而不是把插件文件随意复制到用户目录。
9. 该版本保留模糊音、反查注释、Lua、OpenCC 和 ZZC。不要再安装同名原生 Table 方案，两种实现择一使用。

Fcitx5 Rime 的标准用户目录也可在 [Rime 用户文件夹说明](https://github.com/rime/home/wiki/UserData)中核对。

**Fcitx5 原生 Table**

晨星 Fcitx5 版不使用 Rime。只需安装发行版提供的 Fcitx5、配置工具和
`fcitx5-chinese-addons`（其中含官方 Table 引擎与 libime）。

| 发行版 | 安装命令或说明 |
| --- | --- |
| Arch / Manjaro / EndeavourOS | `sudo pacman -S fcitx5-im fcitx5-chinese-addons fcitx5-configtool` |
| Ubuntu / Debian / Linux Mint | `sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-config-qt` |
| Fedora | `sudo dnf install fcitx5 fcitx5-chinese-addons fcitx5-configtool` |
| RHEL / AlmaLinux / Rocky Linux | 先启用 EPEL／CRB，再安装仓库提供的 Fcitx5 Chinese Addons |
| Deepin / UOS | 如仍使用 Fcitx4，先卸载旧组件，再安装 Fcitx5 与 Chinese Addons |

不同发行版拆包名称可能略有差异；配置工具中能看到“码表／Table”即满足运行条件。

安装方案：

1. 下载并解压 [`eosphoros-fcitx5-linux-full.zip`](https://github.com/0x696c757a696f/eosphoros-keytao/releases/latest/download/eosphoros-fcitx5-linux-full.zip)（或所需档位）。
2. 把 `inputmethod/eosphoros.conf`、`table/eosphoros.main.dict` 和所需 `themes/`
   分别复制到 `~/.local/share/fcitx5/` 下的同名目录。
3. 重启 Fcitx5，在配置工具中添加“晨星键道”。
4. 若仍不能输入，运行 `fcitx5-diagnose`，确认 Table／Chinese Addons 已加载。
5. 更新时覆盖上述三个目录中的晨星文件并重启 Fcitx5。原生 Table 不读取 `~/.local/share/fcitx5/rime/`，也不需要执行 Rime 重新部署。

这个纯 Table 版本保留完整 1～6 键普通中文码表、稳定候选顺序以及无匹配／满码
自动上屏。主表关闭学习与自动造词，短码按词典固定顺序；`i/u/v/o` 在首键处分流，
不会挂到其他普通编码的前缀子树。Fcitx5 官方标点、快捷短语、简繁转换、Emoji 与
Unicode 可照常使用；Rime 专属的模糊音、反查注释、Lua 和 ZZC 不会混进原生 Table。

<details>
<summary><strong>🧰 展开 Linux 桌面环境与应用兼容设置</strong></summary>

> [!TIP]
> 下面的配置按桌面环境互斥选择。普通用户完成上面的五步后能够正常输入，就不需要继续设置环境变量。

桌面环境配置必须按实际会话选择，不要把下面几套变量全部叠加。Fcitx5 官方也明确说明不存在适合所有 X11/Wayland 环境的一套全局配置；完整背景可参考[设置 Fcitx5](https://fcitx-im.org/wiki/Setup_Fcitx_5)和[在 Wayland 上使用 Fcitx5](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland)。

**KDE Plasma / Wayland**

1. 打开“系统设置 → 虚拟键盘”，选择 Fcitx 5。
2. 为兼容 XWayland 程序，只需在 `/etc/environment` 或 `~/.config/environment.d/im.conf` 中设置：

   ```text
   XMODIFIERS=@im=fcitx
   ```

3. Plasma 5.27 及更新版本通常不要全局设置 `GTK_IM_MODULE`、`QT_IM_MODULE`、`SDL_IM_MODULE`，否则候选窗可能闪烁；仅在某个旧 X11 应用不能输入时，给那个应用单独设置。
4. 由 KWin“虚拟键盘”启动的 Fcitx5 不要从托盘菜单执行“重启”，因为 KWin 传入的 Wayland socket 不能被新进程复用。修改设置后应注销并重新登录。

**GNOME / Budgie**

1. Debian、Ubuntu、Linux Mint 等系统登录图形界面后运行 `im-config`，在向导中选择 `fcitx5`；也可直接运行 `im-config -n fcitx5`。Fedora 可运行 `im-chooser`，选择 Fcitx5 后注销并重新登录。
2. Wayland 下建议至少为 XWayland 程序设置 `XMODIFIERS=@im=fcitx`；Qt 5 程序可按需设置 `QT_IM_MODULE=fcitx`。Qt 6.8.2 及更新版本需要回退顺序时可使用 `QT_IM_MODULES="wayland;fcitx"`。
3. Chrome/Chromium 走 XWayland 时可为该应用设置 `GTK_IM_MODULE=fcitx`。GNOME Shell 内部界面无法正常定位候选窗时，可考虑 Fcitx5 官方文档提到的 Kimpanel 扩展。
4. 只有旧版 GNOME/Budgie 的 GTK 输入模块没有被桌面配置正确写入时，才尝试下面的兼容命令；它不是所有 GNOME 系统都必须执行的步骤：

   ```bash
   gsettings set org.gnome.settings-daemon.plugins.xsettings overrides "{'Gtk/IMModule':<'fcitx'>}"
   ```

**Deepin / UOS（DDE）**

1. 运行 `im-config -n fcitx5`，然后注销并重新登录。
2. 若 DDE 仍启动旧输入法，检查会话自启动项中是否同时存在 Fcitx4 与 Fcitx5，只保留 Fcitx5。
3. 只有 X11 应用不能输入时才补充 `GTK_IM_MODULE=fcitx`、`QT_IM_MODULE=fcitx` 和 `XMODIFIERS=@im=fcitx`；不要在 Wayland 会话中无条件套用 X11 的全量变量。

**Xfce / LXQt / LXDE / MATE 等 X11 桌面**

1. 确认 Fcitx5 随桌面会话自动启动；LXQt 可在“会话设置 → 自动启动”中添加，其他桌面可在“会话和启动”中添加 `fcitx5`。
2. 可在用户级 `~/.xprofile`（仅适合 X11）或系统支持的登录环境配置中加入：

   ```bash
   export XMODIFIERS=@im=fcitx
   export GTK_IM_MODULE=fcitx
   export QT_IM_MODULE=fcitx
   export SDL_IM_MODULE=fcitx
   ```

   写进 shell 文件时四项都应带 `export`；写进 `/etc/environment` 或 `environment.d` 时不要写 `export`。`~/.xprofile` 不适用于原生 Wayland 会话。

**i3wm / awesome / bspwm 等平铺窗口管理器**

X11 平铺窗口管理器可在 `~/.xprofile` 中加入：

```bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export SDL_IM_MODULE=fcitx
```

然后为窗口管理器添加自动启动：

| 窗口管理器 | 配置示例 |
| --- | --- |
| i3wm | 在 `~/.config/i3/config` 加入 `exec --no-startup-id fcitx5 -d` |
| awesome | 在 `~/.config/awesome/rc.lua` 加入 `awful.spawn.with_shell("fcitx5 -d")` |
| bspwm | 在 `~/.config/bspwm/bspwmrc` 加入 `fcitx5 -d &` |

**Sway / Hyprland 等 wlroots Wayland 合成器**

- Sway 1.10 及更新版本可使用 text-input-v3；为 XWayland 程序设置 `XMODIFIERS=@im=fcitx`，Qt 5 可按需设置 `QT_IM_MODULE=fcitx`，新 Qt 6 可使用 `QT_IM_MODULES="wayland;fcitx"`。
- 自动启动方式写在合成器自身配置中，例如 Sway 使用 `exec_always --no-startup-id fcitx5 -d`。其他 wlroots 合成器对输入法协议的支持程度不同，应同时查阅对应合成器文档。
- kitty 需要特殊变量时使用 `GLFW_IM_MODULE=ibus`，不是 `fcitx`。

**Electron / Chrome / VS Code**

- XWayland 模式通常最稳：安装 GTK 输入模块并让应用读取 `GTK_IM_MODULE=fcitx` 或 `XMODIFIERS=@im=fcitx`。
- 必须使用原生 Wayland 时，KDE/KWin 可尝试：

  ```text
  --enable-features=UseOzonePlatform --ozone-platform=wayland --enable-wayland-ime --wayland-text-input-version=1
  ```

- GNOME、Sway 1.10+ 或其他支持 text-input-v3 的环境可尝试将最后一项改成 `--wayland-text-input-version=3`。Chromium 和 Electron 对 Wayland 输入协议的行为会随版本变化，遇到候选窗错位或不能输入时优先退回 XWayland。

</details>

#### ❓ 客户端更新与排错

| 现象 | 优先检查 |
| --- | --- |
| 方案选单里没有晨星键道 | `eosphoros.schema.yaml` 是否位于当前客户端真正使用的 Rime 用户目录；是否执行重新部署 |
| 中文能输入，但顶功、自造词或计算器失效 | `lua/eosphoros/` 是否完整，客户端是否带 `librime-lua` |
| 没有 Emoji、简繁或火星文 | `opencc/eosphoros/` 是否完整，功能开关是否开启，是否重新部署 |
| 更新后仍出现旧候选 | 确认没有导入到另一个用户目录；重新部署，必要时退出并重启客户端 |
| 个人词或设置被覆盖 | 个人内容应写入 `dicts/eosphoros/eosphoros.user.dict.yaml` 和 `*.custom.yaml`，不要直接改自动生成词典 |

### 🔎 基础输入与反查入口

| 想做什么 | 输入方式 | 示例或说明 |
| --- | --- | --- |
| 输入中文 | 直接输入键道6编码 | 空格上屏首选，数字选择对应候选；达到顶功条件时自动上屏 |
| 输入英文 | <kbd>i</kbd> + 英文字母 | `ihello` 的预编辑和候选均显示 `hello`，第二键开始隐藏入口 `i` |
| 用全拼查键道码 | <kbd>u</kbd> + 全拼 | 适合知道读音、忘记键道编码时使用；候选注释显示键道码 |
| 拆字查不会读的字 | <kbd>v</kbd> + 二分编码 | 使用二分反查定位汉字，并显示键道码 |
| 查繁体和生僻字 | <kbd>o</kbd> + 编码 | 进入 GBK/扩展单字词典；此入口不追加 Emoji |
| 输入快符 | <kbd>;</kbd> + 字母编码 | 开启“快符开”后使用；叶节点可直接上屏，行为可在 custom 文件中调整 |
| 使用计算器 | <kbd>=</kbd> + 表达式 | 未显示候选菜单时输入，例如 `=1+2*3`；有候选菜单时 `=` 是下一页 |
| 查看打字统计 | `=tj` | 显示累计字数、速度等本地统计信息 |
| 输入日期时间 | 输入 `rq` 等日期码 | 日期、时间候选由 Lua 动态生成 |
| 使用自造词 | <kbd>\</kbd> 进入指令模式 | 详见[自造词使用教程](zzc/自造词使用教程.md) |

`u`、`v`、`o` 是反查专用入口，不参与 Emoji 转换；普通中文编码才会在开启 Emoji 后附加表情候选。`i` 只有位于输入开头时才是英文入口，在中文编码的第 2～6 位仍按“竖”笔画码处理。

打字统计现在按 eosphoros 命名保存在 `zzc_state/eosphoros_typing_stats.tsv`。首次运行会兼容读取旧的根目录 `typing_stats.txt`，随后写入新文件；旧文件暂不自动删除，便于确认迁移结果或手工备份。移动端规则只把本机统计回传到应用目录，不用 iCloud 统计覆盖另一台设备。

### ⏩ 候选、翻页和方案切换

| 按键 | 条件 | 行为 |
| --- | --- | --- |
| <kbd>Space</kbd> | 有候选 | 上屏当前选中候选 |
| <kbd>1</kbd>～<kbd>5</kbd> | 有候选 | 选择本页对应序号；候选页大小默认是 5 |
| <kbd>Tab</kbd> | 有候选 | 选择第 2 个候选 |
| <kbd>-</kbd> | 有候选 | 上一页 |
| <kbd>=</kbd> | 有候选 | 下一页；没有候选时可作为计算器入口 |
| <kbd>F6</kbd> | 任意状态 | 切换到下一个输入方案 |
| <kbd>F7</kbd> | 任意状态 | 切换简体/繁体输出 |
| <kbd>Ctrl</kbd> + <kbd>\</kbd> | 任意状态 | 开启或关闭 Emoji 候选 |

### 🎛️ 功能开关和默认状态

重新部署后，方案选单中的开关状态由 [`eosphoros.custom.yaml`](eosphoros.custom.yaml) 控制：

| 开关 | 默认 | 作用 |
| --- | :---: | --- |
| 中文/英文 | 中文 | 整体 ASCII 模式；平时输英文无需切换，直接使用 `i` 入口 |
| 简体/繁體 | 简体 | OpenCC 简繁转换，也可按 <kbd>F7</kbd> 切换 |
| 简约/逐码展示 | 逐码展示 | 是否显示逐码补全候选 |
| 简约/表情展示 | 表情展示 | 是否给普通中文候选追加 Emoji |
| 快符关/快符开 | 快符开 | 是否启用 `;` 快符入口 |
| `;` 次选 | 关闭 | 是否把分号用作次选键；与快符习惯有关 |
| 计算关/计算开 | 计算开 | 是否启用 `=` 计算器和工具入口 |
| 空顶关/空顶开 | 关闭 | 是否启用空码顶功 |
| 简约/630提示 | 630提示 | 是否显示 630 规则辅助提示 |
| 地球文/火星文 | 地球文 | 是否启用火星文转换 |
| 半角/全角 | 半角 | 标点和字符宽度 |

默认启用键道顶功、逐码补全、Emoji、快符、计算器和 630 提示，默认关闭流式整句输入。Emoji 使用 Lua 懒加载：保留原有 txjx 映射，并追加 2,516 个来自 Rime-Ice 的不重复关键词，涵盖更多情绪别名、手势、人物、动物、食物、交通、旗帜和新版 Emoji。若 Emoji 没出现，依次确认“表情展示”已开启、输入的是普通中文编码而不是 `u/v/o` 反查、文件已完整复制到 `opencc/eosphoros/`，然后重新部署。

### ✍️ 自造词指令速查

| 指令 | 作用 |
| --- | --- |
| `编码\自造词\` | 空码时新增；已有首选时替换首选，并把原词递归顺延到更长编码 |
| `\自造词3`～`\自造词6` | 指定 3～6 码造词，达到码长后自动结束 |
| `编码\+自造词\` | 追加为当前编码的重码候选 |
| `编码\-数字\` | 删除指定序号候选；省略数字时删除首选 |
| `编码\数字\` | 将指定序号候选置顶或前移 |
| `编码\<\` | 把当前候选前移一码，并递归整理被占用的编码 |
| `编码\++数字\` | 从可恢复候选列表恢复指定项 |
| `\--\` | 撤回最近一次尚未合并的自造词操作 |
| `\!!!\` | 清空全部尚未合并的自造词操作 |

输入法会在会话结束时把运行时操作安全追加到 `dicts/eosphoros/eosphoros.zzc.dict.yaml`；要永久整理进正式词库，再运行 `zzc/` 中对应平台的合并脚本。完整的保存、跨设备同步、合并和撤回流程见[自造词使用教程](zzc/自造词使用教程.md)和[合并脚本说明](zzc/README.md)。

Windows 用户可以在仓库根目录运行：

```powershell
python .\zzc\Windows_词库合并.py
```

没有 Python 时可以直接双击 `zzc/Win_词库合并.exe`，需要撤回最近一次合并时双击 `zzc/Win_撤回合并.exe`。两个 EXE 均由当前 eosphoros 共享 Python 核心构建；正式 Release 会在 Windows Runner 上使用 Python 3.14 的最新补丁版和 `requirements-build.txt` 锁定的 PyInstaller 重新构建，并实际执行合并、撤回测试，再把通过测试的 CI 产物交给最终发布。普通推送和 PR 的 `package-main` 只验证源码、词库与已提交文件，不重复编译 EXE。构建和校验方法见[合并脚本说明](zzc/README.md#重新构建-windows-exe)。

## 🔤 英文输入

英文词典直接导入主词典，不需要 `eosphoros.en.schema.yaml`，也不需要切换方案。

```text
实际输入：ihello
预编辑区：hello
候选输出：hello
```

- 单独按下 `i` 时仍显示入口字符；继续输入后才隐藏开头的 `i`。
- 英文长码不会触发中文的 4～6 码顶功。
- 支持大小写输出和常见技术词别名，例如 `C++ → icpp`、`C# → icsharp`、`.NET → idotnet`。
- 英文编码统一为 `i[a-z]+`，生成时会排除与现有中文码冲突的条目。
- 英文词库来自 Rime-Ice 的 `en.dict.yaml` 与 `en_ext.dict.yaml`，当前生成 23,610 条记录。

<a id="词库组成"></a>

## 📚 词库组成

以下为 2026-08-10 版本的内置记录数；自造词和个人用户词库不计入统计。

| 词库 | 记录数 | 用途 |
| --- | ---: | --- |
| `dicts/eosphoros/eosphoros.danzi.dict.yaml` | 36,214 | 上游键道单字表 |
| `dicts/eosphoros/eosphoros.cizu.dict.yaml` | 191,002 | 本地基础词组 |
| `dicts/eosphoros/eosphoros.catholicism.dict.yaml` | 3,514 | 天主教、礼仪、神学与东方礼词汇 |
| `dicts/eosphoros/eosphoros.protestantism.dict.yaml` | 433 | 传统新教宗派、信条、人物、日常教会用语及《和合本》词汇 |
| `dicts/eosphoros/eosphoros.orthodoxy.dict.yaml` | 88 | 东正教礼仪、圣像、灵修与教会制度专有词汇 |
| `dicts/eosphoros/eosphoros.oriental.dict.yaml` | 68 | 东方正统教会、合性论传统与成员教会专有词汇 |
| `dicts/eosphoros/eosphoros.assyrian.dict.yaml` | 71 | 东方亚述教会、东叙利亚礼与景教史专有词汇 |
| `dicts/eosphoros/eosphoros.core.dict.yaml` | 920 | 630 规则、快符和核心候选 |
| `dicts/eosphoros/eosphoros.fjcy.dict.yaml` | 514,033 | 附加扩展词组 |
| `dicts/eosphoros/eosphoros.ice.dict.yaml` | 362,647 | Rime-Ice 中文精简补充词库 |
| `dicts/eosphoros/eosphoros.wanxiang.*.dict.yaml` | 40,561 | 七个万象分类补充词库 |
| `dicts/eosphoros/eosphoros.en.dict.yaml` | 23,610 | Rime-Ice 英文词库 |
| **合计** | **1,173,161** | 不含动态自造词和个人词库 |

四个非天主教传统词库以具有宗派辨识度的信条、礼仪、制度、正式教会名称和历史术语为主体，并补充基督徒实际常打的崇拜、团契、查经、祷告和服事用语；不把“宗派名＋通用活动”机械拼成长词凑量。`eosphoros.protestantism` 另收经审核的《和合本》书卷名、人地名和固定译语，以《和合本》的“马太、约翰、使徒行传、启示录”等新教译名为准，不混入《思高本》译名；传统宗派部分覆盖信义宗、改革宗／长老宗、公理宗、圣公宗、浸信宗、循道卫理宗、再洗礼派／门诺会、贵格会、摩拉维亚弟兄会、弟兄会和救世军，五旬节派保留既有条目但不是本轮扩建重点。东正教、东方正统教会、东方亚述教会和东方礼天主教会分别维护，避免把相近的叙利亚礼、圣像或牧首制度词汇混错归属；东方正统部分不用不准确的“一性论”作为自称。多段人名使用间隔号显示，例如“马丁·路德”，编码时不计间隔号。核对来源和授权边界见 [`tools/christian_traditions_sources.md`](tools/christian_traditions_sources.md)。

天主教新增词由 [`tools/catholicism_expansion_2026.txt`](tools/catholicism_expansion_2026.txt) 审核；四个非天主教专题词库由 [`tools/christian_traditions_2026.txt`](tools/christian_traditions_2026.txt) 审核。生成器依次尝试键道六码的基础码和首笔辅助码。固定本地词典没有空闲合法码时通常不收录；专题词确定后再重建低优先级 `eosphoros.ice`，让 ICE 词移到更长的合法码或按既有重码预算淘汰。唯一例外是“哥林多后书”“帖撒罗尼迦后书”“雅各书”三卷《和合本》正式书名：前两组的前书与后书在标准规则下拥有完全相同的全部候选，后一卷的全部候选已被固定旧词占用，因此人工审核后使用最终六码并保持专题词优先。除此三项外，四个非天主教专题词库没有新增异词同码。

`eosphoros.ice` 定位为本地词库之后的精简补充库。同步过滤器不会直接删除 2～3 字词；它会排除上游低权重长尾、批量数字/年份模板、8 字以上 `ext` 整句、12 字以上普通超长词，以及已审核的古文整句、口号和法律句式片段。药品名称是例外：片、胶囊、颗粒、注射液、口服液、滴眼液、喷雾剂等剂型词不会因词频低或名称过长被过滤，并在重码预算中优先保留。编码时短词优先占用基础码，长词和低频同码词尽量追加笔画码；随后再按照 `base → ext → others` 和上游权重排序。低优先级重码词会被删减，合并后的中文重码率不会高于同步前的本地基准；新增词在同一码下最多保留 8 个候选。这些过滤规则写在同步器中，因此以后拉取上游时不会重新混入。

`eosphoros.wanxiang` 不直接导入万象的拼音码和词频，只吸收药品 9,367 条、医学 12,441 条、化学 10,892 条、地名 5,281 条、名人 2,239 条、台风名 190 条和高频基础词 151 条。联想句、批量普通人名、错音/多音纠错、英文、单字和方言库均不导入。带声调拼音先规范化（保留 `ü → v`），再按键道6飞键和首笔规则重新编码；本地已有词先去重，所有合法码都冲突的条目直接跳过。通过筛选的码会先受保护，再重建低优先级 ICE，因此不会新增异词同码。

### 📑 词库加载顺序

[`eosphoros.extended.dict.yaml`](eosphoros.extended.dict.yaml) 控制词库导入。当前主要顺序为：

```text
user → zzc → danzi → cizu → catholicism → protestantism → orthodoxy → oriental → assyrian → core → fjcy → ice → wanxiang → en
```

本地词库优先于自动生成的上游词库。`dicts/eosphoros/eosphoros.user.dict.yaml` 权限最高，适合保存个人常用词；加入大量通用词前应优先考虑对应的专题或基础词库。

### 👤 个人用户词库

[`dicts/eosphoros/eosphoros.user.dict.yaml`](dicts/eosphoros/eosphoros.user.dict.yaml) 是专门保留给用户维护的高优先级 Rime 词库，Full、Standard 和 Lite 三个档位都会包含。它在扩展词库中最先加载，因此适合添加姓名、地址、专业术语和个人常用短语，不建议放入大量公共词条。

词条写在文件头部的 `...` 之后，每行使用一个 **Tab 制表符** 分隔词条与键道编码；以 `#` 开头的行是注释。可以复制文件内示例并删除开头的 `#`：

```text
词组<Tab>bmmso
单字<Tab>bb
```

其中 `<Tab>` 表示真实的 Tab 键，不是空格或文字本身。修改后需要在输入法中执行“重新部署”才能生效。请保留文件头部的 `name: eosphoros.user`、YAML 分隔符和 UTF-8 编码；升级或覆盖方案前建议单独备份此文件。

该文件由 Rime、Weasel、Squirrel、Trime、Rabbit、元书、仓输入法及 Fcitx5 + Rime 包直接读取。Fcitx5 原生 Table 与 Yong 使用发布时生成的静态码表，安装后修改此 YAML 不会自动更新它们，需要等待新 Release 或自行重新构建对应码表。

## ⚙️ 配置文件

| 文件 | 作用 |
| --- | --- |
| `eosphoros.schema.yaml` | 主方案、引擎、翻译器、反查和快捷键 |
| `eosphoros.custom.yaml` | 用户推荐修改的开关、候选数和流式输入配置 |
| `eosphoros.extended.dict.yaml` | 词库导入顺序与开关 |
| `default.custom.yaml` | 默认方案列表及全局选项 |
| `weasel.yaml` / `weasel.custom.yaml` | Windows 小狼毫候选窗样式与明暗配色 |
| `squirrel.yaml` / `squirrel.custom.yaml` | macOS 鼠须管候选窗样式与明暗配色 |
| `fcitx5/macos/themes/` | macOS Fcitx5 可导入主题；`eosphoros-auto.conf` 自动切换 Cat 明暗配色 |
| `fcitx5/linux/themes/` | Linux Fcitx5 Classic UI 桌面配色复刻主题 |
| `fcitx5/themes.yaml` | 小企鹅主题来源清单，由生成脚本维护 |
| `mobile_themes/` | Fcitx5 Android、Trime 的原生主题和跨移动端统一色板；元书／仓导入包在 Release 阶段生成 |
| `Hamster.yaml` | iOS 客户端自造词文件同步规则，不是元书键盘皮肤 |
| `eosphoros.symbols.yaml` | 标点与符号 |
| `dicts/eosphoros/eosphoros.core.dict.yaml` | 630、快符和核心码表 |
| `dicts/eosphoros/eosphoros.user.dict.yaml` | 个人高优先级补充词库 |
| `lua/eosphoros/` | 方案 Lua 模块 |
| `opencc/eosphoros/` | 简繁、Emoji、火星文数据 |

修改 YAML 后必须重新部署。升级仓库时，个人配置尽量写入 `*.custom.yaml` 或 `dicts/eosphoros/eosphoros.user.dict.yaml`，不要直接修改自动生成的 `eosphoros.danzi`、`eosphoros.ice`、`eosphoros.wanxiang.*` 和 `eosphoros.en`。

### 🌊 流式输入

默认使用键道顶功。需要整句流式输入时，可在 `eosphoros.custom.yaml` 中启用：

```yaml
patch:
  translator/enable_sentence: true
  translator/enable_user_dict: true
```

启用 `enable_sentence` 后，中文顶功会自动停用，分号和单引号改作分隔符。详细说明和相关按键覆盖已写在 `eosphoros.custom.yaml` 的注释中。

<a id="上游来源与自动同步"></a>

## 🔄 上游来源与自动同步

生成文件和来源 commit 记录在 [`tools/upstream_dictionaries.lock.json`](tools/upstream_dictionaries.lock.json)：

| 上游 | 源文件 | 生成文件 |
| --- | --- | --- |
| [amorphobia/rime-jiandao](https://github.com/amorphobia/rime-jiandao) | `dicts/01.danzi.txt` | `dicts/eosphoros/eosphoros.danzi.dict.yaml` |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `cn_dicts/base`、`ext`、`others` | `dicts/eosphoros/eosphoros.ice.dict.yaml` |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `en_dicts/en`、`en_ext` | `dicts/eosphoros/eosphoros.en.dict.yaml` |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `opencc/emoji.txt` | `opencc/eosphoros/eosphoros_emoji_extra_*` |
| [amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang/tree/wanxiang/dicts) | `yaopin`、`yixue`、`huaxue`、`diming`、`mingren`、`taifeng`、`jichu` | `dicts/eosphoros/eosphoros.wanxiang.*.dict.yaml` |

同步器不会盲目追踪浮动的 `main`/`master` 内容。锁文件保存已经整合的 Git commit 和生成文件 SHA-256；更新器比较“上次 commit → 当前 HEAD”，只有目标源文件变化时才按最新完整快照重建，避免长期累积补丁造成漂移。

Windows 下推荐使用 PowerShell 7：

```powershell
pwsh -File .\tools\update_upstream_dictionaries.ps1
```

脚本默认使用当前 `PATH` 中的 Python；也可以通过 `-Python` 传入自己的解释器。只验证锁定内容、不刷新上游：

```powershell
pwsh -File .\tools\update_upstream_dictionaries.ps1 -CheckOnly
pwsh -File .\tools\update_upstream_dictionaries.ps1 -Python .\.venv\Scripts\python.exe
```

也可以直接使用 Python：

```powershell
python .\tools\sync_upstream_dictionaries.py --check
python .\tools\sync_upstream_dictionaries.py --refresh --write
```

`.github/workflows/sync-upstream-dictionaries.yml` 每周一 04:17 UTC 自动检查，有变化时运行测试并创建 PR。首次启用自动 PR 前，需要在仓库的 **Settings → Actions → General → Workflow permissions** 中允许 GitHub Actions 创建 Pull Request。

Lua 与自造词实现参考 [wzxmer/rime-txjx](https://github.com/wzxmer/rime-txjx)，已整合的 commit、完整 `lua/`、`zzc/`、`zzc_state/` 审查范围和明确排除项记录在 [`tools/upstream_code.lock.json`](tools/upstream_code.lock.json)。当前审查点为 `377001a70e73727b4e3d8cb7b6de9ee401ab3a98`：已适配打字统计的 `zzc_state` 命名空间、iCloud 安全的逻辑空状态、计算器等号防按键重复，以及 Fcitx5 Linux/macOS Python 入口；保留 eosphoros 的命名空间、英文 `i` 入口、键道6顶功规则和防重复追加状态。

[`tools/adapt_txjx_upstream.py`](tools/adapt_txjx_upstream.py) 会先读取 [`tools/txjx_adaptation_manifest.json`](tools/txjx_adaptation_manifest.json) 中逐文件登记的“上游路径 → 本地路径”，把 `txjx` 模块名和方案名转换为 `eosphoros`，再以锁定 commit 为共同祖先进行三方合并。因此上游文件与本地文件可以继续使用不同名字，本地独有修改也不会被整文件覆盖：

```powershell
# 只预览上游差异、映射结果和冲突
python .\tools\adapt_txjx_upstream.py --json

# 仅在全部映射都可安全合并时写入，并推进 commit 锁
python .\tools\adapt_txjx_upstream.py --write --update-lock --json
```

对应工作流 `.github/workflows/check-txjx-upstream.yml` 每周执行：已登记且无冲突的修改会进入固定的自动化分支并创建或更新 PR；若同一区域被本地和上游同时修改、上游新增未登记源码、删除已映射文件，或变更会要求重建 Windows EXE，则不改本地文件、不推进锁，只创建或更新人工审查 Issue。Windows EXE 仍只在 Release 工作流编译。工作流不包含任何本机绝对仓库路径，在 GitHub Actions 的 checkout 目录中运行。

直接上游 [hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere) 另用 [`tools/legacy_upstream.lock.json`](tools/legacy_upstream.lock.json) 记录人工审校点。当前已审校至 `6cbc3620f7c6046dd0f646c1265329c701e81664`：日期不补月／日虚位与 `eo` 时间候选在本地已有对应实现；词库更新只择取固定术语，并按本地单字表重新计算合法飞键、检查全库占码。`.github/workflows/check-reference-upstreams.yml` 把旧上游周检与基督教术语来源月检合并管理；旧上游仍只创建审校 Issue，不自动覆盖已更名的目录、Lua、Schema 或本地词库。

第三方来源、固定版本和许可证见 [`THIRD_PARTY.md`](THIRD_PARTY.md) 与 [`licenses/`](licenses/)。

Release 工作流会在每月 1 日和 15 日的 04:17 UTC 自动检查。只有最新 Release 之后出现新提交时，才会继续验证、编译 Windows EXE、执行真实 librime 部署冒烟测试、构建各平台压缩包并发布；没有新提交时会直接结束，不生成空 Release。每次发布同时生成 `SHA256SUMS`，可用于核对所有下载产物是否完整。手动运行 `Create Release with Zipped Branch Assets and Date` 仍可强制重新发布。

## 🛠️ 维护与验证

本项目的 Python 工具需要 Python 3.11 或更新版本。推荐安装 [Pixi](https://pixi.sh/) 后使用仓库锁定的跨平台环境；`pixi.lock` 固定 Python、PyYAML、Pillow、Lua 和 PyInstaller 版本，避免本机与 CI 行为漂移。已有 Python 环境仍可直接运行下面的等价命令。

依赖更新采用自动 PR 而非直接写入主分支：Dependabot 每周检查 GitHub Actions 与 `requirements-*.txt` 中的 pip、PyYAML、Pillow、PyInstaller；Python Actions 跟随 3.14 的最新补丁版。依赖 PR 合并后，`sync-development-dependencies.yml` 会把标准 requirements 版本同步到 `pixi.toml`、刷新四个平台的 `pixi.lock`、运行完整测试并再开一个锁文件 PR。定时任务也会每周刷新 Python、Lua 和间接依赖；无人审查时不会自动合并。

<details>
<summary><strong>🧪 展开维护与完整验证命令</strong></summary>

先激活相应环境，再在仓库根目录执行：

```powershell
# 推荐：创建锁定环境并执行完整检查
pixi run check

# 强制重新计算全部上游生成词库（修改生成算法或输入后使用）
pixi run generated

# 等价的分项检查
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

`pixi run check` 会先运行全部回归测试，再通过生成器代码、本地输入、上游 commit、
Unicode 数据版本和生成物哈希组成的内容指纹验证上游词库。输入未变化时无需重复处理
数百万条上游记录；指纹变化会立即失败，此时运行 `pixi run generated` 强制完整重算。

主要维护命令：

```powershell
# 将 VERSION 和 YAML version 更新到指定日期
python .\tools\update_versions.py 2026-08-10

# 清理完全相同的词典记录
python .\tools\dedupe_dictionaries.py

# 检查或修复词库质量（单字表不在清理范围内）
python .\tools\clean_dictionary_quality.py --check

# 审计全库异常长词；确需保留的固定术语写入专用白名单
python .\tools\audit_long_dictionary_entries.py --check

# 校验基督宗派词库来源索引；联网月检由 GitHub Actions 自动执行
python .\tools\check_christian_sources.py --check

# 重新生成天主教扩展并整理分区
python .\tools\build_catholicism_expansion.py --write
python .\tools\organize_catholicism_legacy.py

# 重建四个基督宗派专题词库；随后重建 ICE 以重新避让本地码位
python .\tools\build_christian_traditions.py --write
python .\tools\sync_upstream_dictionaries.py --write
```

仓库验证会检查 YAML、JSON、TOML、Lua、生成文件哈希、目录命名空间和关键配置。当前测试同时覆盖键道6词组编码、飞键规则、天主教分类、四个基督宗派专题词库、专题词跨库零重码、全库长词审计、词库质量、上游去重、重码上限、英文 `i` 命名空间、平台包内容及自动同步工作流。Ubuntu CI 还会用 `rime_deployer` 编译临时用户目录，确认主方案、棱镜和主词典能由真实 librime 生成。

</details>

## 🗂️ 项目结构

```text
.
├─ eosphoros.schema.yaml                 主方案
├─ eosphoros.extended.dict.yaml          RimeTool 兼容词库索引（无词条正文）
├─ dicts/eosphoros/                      本地、上游生成和个人词条数据
│  └─ eosphoros.wanxiang.*.dict.yaml     万象七个分类词库
├─ lua/eosphoros/                        Lua 处理器、翻译器和过滤器
│  ├─ input/                         模块化按键、顶功、标点和快符处理
│  └─ zzc/                           自造词运行时、候选和操作链
├─ opencc/eosphoros/                     OpenCC 命名空间数据
├─ *.recipe.yaml                     各桌面前端与移动端东风破配方
├─ tools/                             生成、同步、清理和验证工具
├─ tests/                             Python 与 Lua 回归测试
├─ licenses/                          第三方许可证副本
├─ THIRD_PARTY.md                    第三方来源说明
└─ .github/workflows/                发布和定期同步工作流
```

## 🙏 致谢与授权

本方案的演进关系为“星空键道6.2 → 星猫键道6 → 晨星键道”。首先感谢吅吅大山、Proud丶Cat、热热、浮生、千年蟲等历代方案和词库维护者。没有他们长期整理编码、词库与使用经验，就没有今天的晨星键道。

### 🌱 核心引擎与方案传承

| 项目或贡献者 | 本仓库中的作用 |
| --- | --- |
| [librime（Rime 核心引擎）](https://github.com/rime/librime)、[librime-lua](https://github.com/hchunhui/librime-lua) | 提供 Rime 输入法核心及本方案处理器、翻译器和过滤器所需的 Lua 扩展能力 |
| [OpenCC](https://github.com/BYVoid/OpenCC) | 简繁转换与地区用字转换的基础设施 |
| [xkinput/Rime_JD](https://github.com/xkinput/Rime_JD) | 键道 Rime 方案结构与历史实现参考 |
| [hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere) | 本方案的直接上游、历史配置及小小输入法打包素材来源 |
| [wzxmer/rime-txjx](https://github.com/wzxmer/rime-txjx) | 模块化 Lua、Emoji 查询优化、自造词操作链、合并脚本及测试思路参考 |

### 📖 词典、数据与核对资料

| 项目或资料 | 本仓库中的作用 |
| --- | --- |
| [amorphobia/rime-jiandao](https://github.com/amorphobia/rime-jiandao) | 单字表和 `make_dicts.sh` 生成规则来源 |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | 中文补充词库、英文词库及 Emoji 上游数据 |
| [amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang) | 药品、医学、化学、地名、名人、台风名及高频基础词的筛选来源；本仓库重新编码、去重并过滤长尾内容 |
| [amorphobia/opencc-tonggui](https://github.com/amorphobia/opencc-tonggui) | Release 构建时下载并校验的 OpenCC 补充数据 |
| [SCIM Tables](https://github.com/scim-im/scim-tables)与 LiangFen 作者 TianHeng | `liangfen` 两分反查的历史数据来源 |
| [AOSP PinyinIME](https://android.googlesource.com/platform/packages/inputmethods/PinyinIME.git) | `pinyin_simp` 拼音反查的历史数据来源 |
| [CrossWire SWORD `ChiUns`](https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=ChiUns)、[Digital Bible Society](https://bibles.dbs.org/CMNUNVS/pdf/CMNUNVS.pdf)及[各教会官方资料](tools/christian_traditions_sources.md) | 《和合本》书卷、人名、地名及基督宗派专题术语的人工核对来源；不转载词典释义或受版权保护的正文 |

<details>
<summary><strong>客户端、部署工具、皮肤资源与构建工具</strong></summary>

| 项目 | 本仓库中的作用 |
| --- | --- |
| [小狼毫](https://github.com/rime/weasel)、[鼠须管](https://github.com/rime/squirrel) | Windows、macOS 官方 Rime 前端及桌面配色格式 |
| [Techince/weasel](https://github.com/Techince/weasel) | Windows 水龙月 Fork 客户端 |
| [Fcitx5 macOS](https://github.com/fcitx-contrib/fcitx5-macos-installer)、[Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android)、[Fcitx5](https://github.com/fcitx/fcitx5) | macOS、Android、Linux 的小企鹅前端、安装说明与主题格式 |
| [同文输入法 Trime](https://github.com/osfans/trime)、[chwt163/mytrime](https://github.com/chwt163/mytrime/tree/main/3.3.10) | Android Rime 前端；mytrime 在 GPL-3.0-or-later 下提供晨星同文皮肤采用的“格调”完整布局母版 |
| [仓输入法](https://apps.apple.com/app/id6446617683)、[元书输入法](https://apps.apple.com/app/id6744464701)及其[官方文档](https://ihsiao.com/apps/hamster/) | iOS Rime 前端、方案导入、自造词同步和键盘皮肤格式支持 |
| [小小输入法 Yong](https://yong.dgod.net/)（[dgod/yong 源码](https://github.com/dgod/yong)） | Windows、Linux 与 Android 输入平台；本仓库为桌面端提供便携整合包，为 Android 提供不含程序本体、但内置可直接选择皮肤的晨星配置包 |
| [rimeinn/rabbit](https://github.com/rimeinn/rabbit)、[amorphobia/rabbit](https://github.com/amorphobia/rabbit) | 玉兔毫运行环境、便携包及相关实现 |
| [东风破 plum](https://github.com/rime/plum) | `recipe.yaml` 安装与更新机制 |
| [中州韵助手 rimetool](https://gitee.com/wubi98/rimetool)及其[使用文档](https://github.com/yanhuacuo/rimetool/wiki) | Rime 方案管理工具及“薄荷解析模板”兼容结构参考 |
| [薄荷输入法（Mintimate/oh-my-rime）](https://github.com/Mintimate/oh-my-rime) | 薄荷解析模板的方案结构与开关命名，以及 Android DocumentsUI 操作说明参考 |
| [ResourceforHamster](https://github.com/BlackCCCat/ResourceforHamster)、[hamster-skin-skill](https://github.com/imfuxiao/hamster-skin-skill)、[空山素影](https://github.com/luozikuan/kongshan-suying) | ResourceforHamster 在 MIT 许可下提供晨星元书与仓皮肤采用的成熟完整底稿；hamster-skin-skill 提供格式与校验规则参考；空山素影作为仍在维护的元书外部皮肤参考 |
| [rime-pure](https://github.com/SivanLaai/rime-pure) | 同文输入法外部主题参考；本仓库仅提供链接，不复制其方案文件 |
| [tankb52/fcitx5-andoird-themes](https://github.com/tankb52/fcitx5-andoird-themes)、[Fcitx5 Android 主题设计器](https://fcitx5-android.github.io/theme-designer/) | 小企鹅输入法安卓版外部主题发现入口与官方主题生成工具；第三方主题不随仓库分发 |
| [仓／元书皮肤交流频道](https://t.me/s/hamster_skins) | 仓输入法第三方皮肤发现入口；内容与兼容性由发布者负责 |
| [Python](https://www.python.org/)、[PyInstaller](https://github.com/pyinstaller/pyinstaller)、[PyYAML](https://github.com/yaml/pyyaml) | 词典同步、质量检查、主题生成和 Windows 词库工具的构建环境 |

</details>

### ⚖️ 授权与再分发边界

> [!IMPORTANT]
> 致谢表示来源、依赖或技术参考，不代表相关作者和项目为晨星键道（`eosphoros-keytao`）提供官方支持，也不改变任何上游许可证。引用链接不等于取得皮肤、词典、软件或文章的再分发授权。

| 内容 | 本仓库的处理方式 | 许可证或边界 |
| --- | --- | --- |
| Rime-Jiandao 单字数据 | 锁定上游 commit，按本方案格式确定性生成 | AGPL-3.0-or-later |
| Rime-Ice 中文、英文与 Emoji 数据 | 去重、转换编码并锁定生成文件校验值 | GPL-3.0 |
| rime-txjx 参考实现 | 经人工审查后适配到 `lua/eosphoros/` 与 `opencc/eosphoros/` 命名空间 | MIT |
| mytrime 3.3.10“格调”皮肤 | 锁定上游 `style.trime.yaml`，修正严格 YAML 解析问题并注入晨星名称与昼夜配色 | GPL-3.0-or-later |
| CrossWire `ChiUns`《和合本》 | 仅选取并人工复核书卷名、人名、地名和固定译语 | 上游标注 Public Domain |
| 在线神学、教会与圣经资料 | 只用于人工核对词目，不批量抓取释义或正文 | 权利归各资料提供者；来源与取词原则单独记录 |
| 其他移动端第三方皮肤 | README 只提供外部入口，不复制、不修改、不放入仓库或 Release | 下载、导入和再分发须遵守皮肤作者的说明与许可证 |
| 小小输入法、玉兔毫等便携包 | 在相应上游程序或发行包基础上整合 eosphoros 配置，并在 CI 中校验来源与文件哈希 | 客户端程序的权利与许可仍归各自上游；eosphoros 不改变其许可条件 |

仓库采用分层授权，不能用一个许可证覆盖所有历史词库和第三方数据；总说明见 [`LICENSE.md`](LICENSE.md)。第三方来源、固定 commit、生成文件 SHA-256 和许可证副本集中记录在 [`THIRD_PARTY.md`](THIRD_PARTY.md)、[`licenses/`](licenses/)、[`tools/upstream_dictionaries.lock.json`](tools/upstream_dictionaries.lock.json)及[`tools/upstream_code.lock.json`](tools/upstream_code.lock.json)。宗派词库的在线核对来源与取词边界见 [`tools/christian_traditions_sources.md`](tools/christian_traditions_sources.md)，机器可读索引见 [`tools/christian_sources.json`](tools/christian_sources.json)。除上述明确标注的内容外，不应仅凭本节致谢推定其他文件采用相同许可证；复用或再分发前请先核对相应文件及仓库的授权声明。贡献规则与统一 Pixi 检查命令见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

<p align="right"><a href="#top">⬆️ 返回顶部</a></p>
