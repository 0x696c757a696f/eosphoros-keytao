<a id="top"></a>

# 星猫键道6（xmjd6-0x69）

<p align="center">
  <a href="https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/0x696c757a696f/xmjd6-0x69?display_name=tag"></a>
  <a href="https://github.com/0x696c757a696f/xmjd6-0x69/actions/workflows/package-master.yml"><img alt="Build and test" src="https://github.com/0x696c757a696f/xmjd6-0x69/actions/workflows/package-master.yml/badge.svg"></a>
  <img alt="librime 1.9.0 or newer" src="https://img.shields.io/badge/librime-%E2%89%A5%201.9.0-476b9e">
  <img alt="UTF-8" src="https://img.shields.io/badge/encoding-UTF--8-2ea44f">
</p>

<p align="center">
  <a href="https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/xmjd6.zip">⬇️ 下载方案</a> ·
  <a href="#如何使用">🚀 如何使用</a> ·
  <a href="#键道6编码概要">⌨️ 编码规则</a> ·
  <a href="#词库组成">📚 词库说明</a>
</p>

星猫键道6是基于星空键道6.2持续整理和扩展的 Rime 音形输入方案，兼顾常用词短码、单字精确定位、生僻字反查和可维护的大型词库。本方案已获得相关授权，适用于 Windows、macOS、Android、iOS 和 Linux 上支持 Rime/Lua 的输入法前端。

- 当前维护仓库：[0x696c757a696f/xmjd6-0x69](https://github.com/0x696c757a696f/xmjd6-0x69)
- 发行包：[Releases](https://github.com/0x696c757a696f/xmjd6-0x69/releases/)
- 上游方案：[hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere)
- 使用笔记：[星猫键道6飞书笔记](https://hu0w1jn4xq.feishu.cn/docx/ZgQ8deGPlozhWCxOyeucBvHJnPe)

## ✨ 主要特点

- 约 121 万条内置码表记录，覆盖单字、常用词、扩展词、Catholicism 专题词和英文词汇。
- 保留键道6的短码、顶功、飞键和首笔辅助码规则，常用词优先使用较短编码。
- `i` 键直接进入英文输入，不需要切换到单独的英文方案。
- `u`、`v`、`o` 分别提供全拼、二分和 GBK/生僻字入口。
- 支持自造词、逐码补全、630 提示、计算器、日期时间、打字统计、Emoji、简繁和火星文转换。
- Lua 文件集中在 `lua/xmjd6/`，OpenCC 数据集中在 `opencc/xmjd6/`，避免污染用户目录的公共命名空间。
- 上游词库使用 Git commit 锁定，可增量检测、确定性重建、定期验证并自动提交更新 PR。

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

### 标准 Rime 安装

1. 下载最新版 [`xmjd6.zip`](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/xmjd6.zip)。
2. 解压到 Rime 用户文件夹；保留压缩包内的目录结构。
3. 重新部署 Rime。
4. 在方案选单中选择“星猫键道”。

本方案包含 Lua 处理器，所用 Rime 前端需要带有 `librime-lua` 支持。建议使用 librime 1.9.0 或更新版本。

> [!IMPORTANT]
> 请完整保留压缩包中的 `lua/xmjd6/` 与 `opencc/xmjd6/` 目录。只复制根目录 YAML 会导致顶功、自造词、英文、Emoji 或简繁转换不完整。

| 平台 | 常见前端 | 默认用户目录 |
| --- | --- | --- |
| Windows | [小狼毫 Weasel](https://github.com/rime/weasel/releases/latest) | `%APPDATA%\Rime` |
| macOS | [鼠须管 Squirrel](https://github.com/rime/squirrel/releases/latest) | `~/Library/Rime` |
| Android | [同文 Trime](https://github.com/osfans/trime/releases/latest) | `/storage/emulated/0/rime/` |
| Android | [Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android) | 应用数据中的 `data/rime/` |
| iOS | [仓输入法](https://apps.apple.com/app/id6446617683)、[元书输入法](https://apps.apple.com/app/id6744464701) | 使用应用内方案导入功能 |
| Linux | [Fcitx5](https://github.com/fcitx/fcitx5) + `fcitx5-rime` + `librime-lua` | `~/.local/share/fcitx5/rime/` |

部署失败或更新后仍显示旧候选时，请先确认文件放在正确的用户目录，再从输入法菜单执行一次“重新部署”。

### 各平台皮肤与样式

皮肤由输入法前端绘制，并不是 Rime 方案本身的通用能力；因此同一套配色文件不能直接跨平台复用：

| 平台与前端 | 本仓库状态 | 配置方式 |
| --- | --- | --- |
| Windows 小狼毫 | 内置统一的 `CatLight` / `CatDark` 明暗配色 | `weasel.yaml` 与 `weasel.custom.yaml` |
| macOS 鼠须管 | 内置同名 `CatLight` / `CatDark` 配色，使用鼠须管 1.x 的新布局字段 | `squirrel.yaml` 与 `squirrel.custom.yaml` |
| macOS Fcitx5 | 已生成同一组可直接导入的 `.conf`；另有自动明暗主题 | 下载 `fcitx5-macos-xmjd6-themes.zip`，在“主题编辑器 → 基础 → 选择／导入主题”中导入 |
| iOS 元书输入法 | 支持独立的 `.cskin` 键盘皮肤；当前仓库只提供方案同步配置，没有附带元书皮肤包 | 皮肤使用 YAML/Jsonnet 描述并由元书单独导入，参见 [元书皮肤结构](https://ihsiao.com/apps/hamster/v3/docs/guides/skins/structure/) |
| Linux Fcitx5 | 已生成 95 套小狼毫／鼠须管桌面配色的 Classic UI 复刻主题 | 下载 `fcitx5-linux-xmjd6-themes.zip`，解压到 `~/.local/share/fcitx5/themes/` 后在经典用户界面中选择 |

> [!NOTE]
> `Hamster.yaml` 只负责元书/仓输入法中的自造词文件同步规则，不是键盘皮肤。元书的 `.cskin` 与旧版仓输入法的 `.hskin` 互不兼容，不能把现有仓皮肤直接改名使用。

#### 小企鹅主题安装

主题颜色由 `weasel.yaml` 与 `squirrel.yaml` 自动生成，不是手工近似。转换程序会把 Rime 的 BGR／AABBGGRR 色值转换成 Fcitx 使用的 RGBA，并分别映射普通候选、首选、序号、注释、预编辑、背景和边框。两份桌面配置同名时采用鼠须管的当前定义，小狼毫独有的配色也会全部保留。

**macOS 小企鹅**

1. 从 Release 下载并解压 `fcitx5-macos-xmjd6-themes.zip`。
2. 打开“主题编辑器 → 基础 → 选择／导入主题”。推荐导入 `xmjd6-auto.conf`：浅色使用 `CatLight`，深色使用 `CatDark`，可跟随系统外观。
3. 需要其他桌面主题时，导入对应的 `xmjd6-主题名.conf`；单主题文件会在系统明暗模式下保持同一套颜色。
4. macOS 26 启用液态玻璃时，系统可能根据候选窗下方内容调整外观，这是小企鹅的系统级行为，不是主题颜色丢失。导入规则参见 [Fcitx5 macOS 官方文档](https://fcitx-contrib.github.io/docs/theme/import.html)。

**Linux 小企鹅**

1. 从 Release 下载 `fcitx5-linux-xmjd6-themes.zip`。
2. 将压缩包直接解压到 `~/.local/share/fcitx5/themes/`；解压后应看到 `xmjd6-CatLight/theme.conf` 等目录，不要再多套一层目录。
3. 打开 `fcitx5-configtool`，进入“附加组件 → 经典用户界面”。亮色主题选择 `xmjd6-CatLight`，暗色主题选择 `xmjd6-CatDark`；也可以选择压缩包内其他桌面配色。
4. 应用设置后重启 Fcitx5。主题只使用官方支持的纯色字段，不依赖 SVG，避免不同 Wayland/GTK 渲染器加载 SVG 时出现兼容问题。格式参见 [Fcitx5 官方主题文档](https://fcitx-im.org/wiki/Fcitx_5_Theme)。

维护者修改桌面配色后，运行 `python tools/build_fcitx5_themes.py` 即可重新生成两端主题；CI 会用 `--check` 阻止过期主题进入 Release。

### 东风破（plum）安装与更新

仓库根目录提供了 `recipe.yaml`，可由东风破直接安装或更新。macOS、Linux 以及其他带 Bash 的环境可执行：

```bash
curl -fsSL https://raw.githubusercontent.com/rime/plum/master/rime-install | bash -s -- 0x696c757a696f/xmjd6-0x69
```

Windows 可从小狼毫菜单打开“输入法设定／获取更多输入方案”，输入：

```text
0x696c757a696f/xmjd6-0x69
```

也可以在已经安装东风破的命令行中运行 `rime-install 0x696c757a696f/xmjd6-0x69`。安装完成后仍需重新部署。配方只复制 Rime 运行所需的 YAML、`xmjd6.ico`、`lua/xmjd6/`、`opencc/xmjd6/` 和必要的自造词部件表；它通过东风破补丁把 `xmjd6` 安全加入现有方案列表，并把图标引用合并到 `xmjd6.custom.yaml`，不整份覆盖用户的 `*.custom.yaml`。仓库测试、构建脚本、EXE、`xmjd6_user.txt`、`*.userdb` 和自造词运行记录都不会被安装或覆盖。

### 中州韵助手（rimetool）兼容性

本方案已补齐中州韵助手用于识别和编辑方案的主要结构：`default.yaml` 与 `default.custom.yaml` 都列出 `xmjd6`，schema 内有方案名、完整开关状态及显式 `reset`、本方案快捷键和 `menu/page_size`；各词典也都有明确的 `text`、`code` 等列和实际编码。

可在 rimetool 选择“薄荷解析模板”。模板要求的 `transcription`、`emoji`、`ascii_punct` 和 `melt_eng` 都已提供：`transcription` 与原有 `jffh` 都会触发简繁转换，`emoji` 与原有 `emoji_cn` 都会触发表情候选，`melt_eng/prefix` 实际参与 `i` 英文入口的识别，`ascii_punct` 与 `full_shape` 则使用 Rime 原生开关。

> [!WARNING]
> 为了让宗派词库及大型词库仍可人工审阅，部分码表正文保留了分类注释。中州韵助手的兼容约定不建议正文注释，因此不建议在其中对这些大型码表执行“全库重写”。正常浏览、Rime 编译和输入不受影响。`custom_phrase` 是雾凇方案专用的节点，本方案不添加无效的同名占位配置。

### 便携与主题发行包

- Windows 小小输入法：[yong-xmjd6-full.zip](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/yong-xmjd6-full.zip)
- 玉兔毫：[Rabbit-xmjd6.zip](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/Rabbit-xmjd6.zip)
- macOS 小企鹅主题：[fcitx5-macos-xmjd6-themes.zip](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/fcitx5-macos-xmjd6-themes.zip)
- Linux 小企鹅主题：[fcitx5-linux-xmjd6-themes.zip](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/fcitx5-linux-xmjd6-themes.zip)

玉兔毫便携版建议解压到不含空格的路径。小小输入法版默认使用 `Ctrl + Space` 激活。

<a id="键道6编码概要"></a>

## ⌨️ 键道6编码概要

键道6以音码为主体，以首笔画作为辅助筛选码：

| 笔画 | 横 | 竖 | 撇 | 捺/点 | 折/钩 |
| --- | --- | --- | --- | --- | --- |
| 按键 | `v` | `i` | `u` | `o` | `a` |

词组编码规则以当前生成器和单字表为准：

- 两字词：两个字各取两位音码形成四码；需要区分时，第 5、6 位依次取第一、第二个字的首笔画。
- 三字词：三个字各取音码首键形成三码；第 4、5、6 位依次取三个字的首笔画。
- 四字及以上：取前三字和末字的音码首键形成四码；需要区分时再取前两个字的首笔画。
- 同音词按本地词库、来源优先级和词频排序；常用词先占短码，较低优先级词追加笔画码。

例如：

```text
赞主曲      zqquo
婚姻圣召    hyefa
```

这里的 `i` 同时也是“竖”的辅助码；只有当它位于输入开头时，才作为英文入口。

<a id="如何使用"></a>

## 🚀 如何使用

### 各客户端安装、导入与更新

所有标准 Rime 客户端都使用同一份 [`xmjd6.zip`](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/xmjd6.zip)。区别只在用户文件夹位置和客户端的导入方式：

| 平台 | 推荐客户端 | 安装方式 | 更新后必须做的操作 |
| --- | --- | --- | --- |
| Windows | [小狼毫](https://github.com/rime/weasel/releases/latest)、[水龙月 Fork](https://github.com/Techince/weasel/releases/latest)、玉兔毫、小小输入法 | 解压到用户目录，或下载对应便携包 | 重新部署；便携版按说明启动 |
| macOS | [鼠须管](https://github.com/rime/squirrel/releases/latest)、[Fcitx5 macOS](https://github.com/fcitx-contrib/fcitx5-macos-installer/blob/master/README.zh-CN.md) | 解压到对应 Rime 用户目录 | 重新部署 |
| Android | [同文](https://github.com/osfans/trime/releases/latest)、[Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android) | 通过应用配置管理或系统文件选择器导入 | 在应用内重新部署 |
| iOS | [元书](https://apps.apple.com/app/id6744464701)、[仓输入法](https://apps.apple.com/app/id6446617683) | 使用应用内下载方案或在线方案导入 | 切换到新方案目录并重新部署 |
| Linux | [Fcitx5](https://github.com/fcitx/fcitx5) + Rime + librime-lua | 安装组件后解压到 Fcitx5 Rime 目录 | 重启 Fcitx5 并重新部署 |

无论使用哪个客户端，都不要只复制根目录的 YAML 文件：`lua/xmjd6/` 和 `opencc/xmjd6/` 也必须保持原目录结构一起导入，否则顶功、自造词、英文、Emoji 和简繁转换可能不完整。

#### 🪟 Windows

**小狼毫 Weasel**

1. 安装[小狼毫正式版](https://github.com/rime/weasel/releases/latest)或[小狼毫测试版](https://github.com/rime/weasel/releases/tag/latest)。也可使用[水龙月 Fork 版](https://github.com/Techince/weasel/releases/latest)；从原版切换到 Fork 版时，建议先卸载原版并重启系统。
2. 从 Release 下载 `xmjd6.zip`，解压后把压缩包内的文件和目录复制到 `%APPDATA%\Rime`。
3. 在小狼毫菜单中执行“重新部署”。
4. 打开方案选单，选择“星猫键道”。
5. 更新方案时覆盖同名方案文件即可；个人词汇应放在 `xmjd6.user.dict.yaml`，个人配置写在 `*.custom.yaml`，然后重新部署。

**小小输入法便携版**

1. 下载 [`yong-xmjd6-full.zip`](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/yong-xmjd6-full.zip)。
2. 解压后运行包内的小小输入法，不需要另外导入 Rime 方案。
3. 默认使用 `Ctrl + Space` 激活输入法。
4. `yong-xmjd6.zip` 只包含配置和码表，适合已经安装小小输入法的用户；`yong-xmjd6-full.zip` 才包含完整便携程序。

**玉兔毫 Rabbit**

1. 玉兔毫项目见 [amorphobia/rabbit](https://github.com/amorphobia/rabbit)；直接使用本方案可下载 [`Rabbit-xmjd6.zip`](https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/Rabbit-xmjd6.zip)。
2. 解压到路径中不含空格的目录。
3. 运行玉兔毫并选择星猫键道；该包已经带入方案文件，不需要再复制 `xmjd6.zip`。

#### 🍎 macOS

**鼠须管 Squirrel**

1. 安装[鼠须管正式版](https://github.com/rime/squirrel/releases/latest)或[测试版](https://github.com/rime/squirrel/releases/tag/latest)。
2. 下载并解压 `xmjd6.zip`，把全部内容复制到 `~/Library/Rime`。
3. 从鼠须管菜单执行“重新部署”，再在方案选单中选择“星猫键道”。

**Fcitx5 macOS**

1. 安装[小企鹅输入法 macOS 版（中州韵版）](https://github.com/fcitx-contrib/fcitx5-macos-installer/blob/master/README.zh-CN.md)。
2. 把方案完整复制到 `~/.local/share/fcitx5/rime/`。
3. 重启 Fcitx5 或重新部署 Rime。

#### 🤖 Android

**同文输入法 Trime**

1. 安装[同文输入法](https://github.com/osfans/trime/releases/latest)。
2. 在应用设置中打开“配置管理 → 用户文件夹”。
3. 先选择或初始化默认用户文件夹，再把 `xmjd6.zip` 的完整内容导入 `/storage/emulated/0/rime/`。
4. 返回配置管理执行部署，然后选择星猫键道。

**Fcitx5 for Android**

1. 安装[Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android)及 Rime 插件；需要测试构建时可使用[主程序构建](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android/)、[Rime 插件构建](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android-plugin-rime/)和[更新器](https://jenkins.fcitx-im.org/job/android/job/fcitx5-android-updater/)。
2. 在小企鹅输入法中添加中州韵后，Rime 数据目录通常为 `/storage/emulated/0/Android/data/org.fcitx.fcitx5.android/files/data/rime/`。
3. 推荐通过 Android 系统 DocumentsUI 管理文件：打开系统文件选择器，在侧边栏选择“小企鹅输入法5”，即可访问其 `files/` 数据目录并复制完整方案，不需要第三方文件管理器、root 或 ADB。相关做法可参考 [Mintimate/oh-my-rime#96](https://github.com/Mintimate/oh-my-rime/issues/96)。
4. 返回应用重新部署 Rime。

#### 📱 iOS

**元书输入法**

1. 在“输入方案”中选择“下载方案”。
2. 使用以下任一地址：

   - 原始地址：<https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/xmjd6.zip>
   - 国内网络可用代理地址：<https://gh-proxy.com/https://github.com/0x696c757a696f/xmjd6-0x69/releases/latest/download/xmjd6.zip>

3. 下载完成后进入“方案目录切换”，在 `RimeUserData` 中选择刚导入的方案目录，点击右上角“打开”。
4. 后续更新时重新下载方案，再回到“方案目录切换”选择更新后的目录并重新部署。
5. 使用 iCloud 联动和自造词合并时，继续阅读[自造词使用教程](zzc/自造词使用教程.md)。

**仓输入法**

1. 安装[仓输入法](https://apps.apple.com/app/id6446617683)。
2. 使用应用内在线方案下载功能导入星猫键道。
3. 导入或更新后重新部署，并在应用中切换到对应方案。

#### 🐧 Linux：Fcitx5 + Rime

需要同时安装 Fcitx5、Rime 插件和 Lua 支持。不同发行版的软件包名称、拆包方式和仓库版本可能不同；如果命令提示找不到 `librime-lua`，请先查询本发行版是否已把 Lua 支持合并进 `librime`/`fcitx5-rime`，或按照该发行版的软件包说明安装对应组件。

| 发行版 | 安装命令或说明 |
| --- | --- |
| Arch / Manjaro / EndeavourOS | `sudo pacman -S fcitx5-im fcitx5-rime fcitx5-configtool librime-lua` |
| Ubuntu / Debian / Linux Mint | `sudo apt install fcitx5 fcitx5-rime librime-lua` |
| Fedora | `sudo dnf install fcitx5 fcitx5-rime librime-lua` |
| RHEL / AlmaLinux / Rocky Linux | 先启用 EPEL；RHEL/Rocky 9 再启用 CRB，然后安装 `fcitx5 fcitx5-rime librime-lua` |
| Deepin / UOS | 如仍使用 Fcitx4，先卸载旧组件，再安装 `fcitx5 fcitx5-rime librime-lua` |
| Flatpak | `flatpak install org.fcitx.Fcitx5 org.fcitx.Fcitx5.Addon.Rime` |

RHEL、AlmaLinux、Rocky Linux 可先运行 `sudo dnf install epel-release`；RHEL/Rocky 9 再运行 `sudo /usr/bin/crb enable` 后安装 Fcitx5。Deepin/UOS 如存在旧版 Fcitx4，可先运行 `sudo apt remove fcitx fcitx-bin fcitx-table-all`，再安装 Fcitx5 组件。

安装方案：

1. 将 `xmjd6.zip` 完整解压到 `~/.local/share/fcitx5/rime/`。
2. Flatpak 版通常使用 `~/.var/app/org.fcitx.Fcitx5/data/fcitx5/rime/`。
3. 打开 Fcitx5 配置工具，添加“中州韵”或 Rime 输入法。
4. 重启 Fcitx5，并从 Rime 菜单执行重新部署。
5. 若仍不能输入，先运行 `fcitx5-diagnose`，确认当前桌面会话、Fcitx5 自启动、Rime 插件和输入法环境变量是否被识别。

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

#### 客户端更新与排错

| 现象 | 优先检查 |
| --- | --- |
| 方案选单里没有星猫键道 | `xmjd6.schema.yaml` 是否位于当前客户端真正使用的 Rime 用户目录；是否执行重新部署 |
| 中文能输入，但顶功、自造词或计算器失效 | `lua/xmjd6/` 是否完整，客户端是否带 `librime-lua` |
| 没有 Emoji、简繁或火星文 | `opencc/xmjd6/` 是否完整，功能开关是否开启，是否重新部署 |
| 更新后仍出现旧候选 | 确认没有导入到另一个用户目录；重新部署，必要时退出并重启客户端 |
| 个人词或设置被覆盖 | 个人内容应写入 `xmjd6.user.dict.yaml` 和 `*.custom.yaml`，不要直接改自动生成词典 |

### 基础输入与反查入口

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

### 候选、翻页和方案切换

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

### 功能开关和默认状态

重新部署后，方案选单中的开关状态由 [`xmjd6.custom.yaml`](xmjd6.custom.yaml) 控制：

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

默认启用键道顶功、逐码补全、Emoji、快符、计算器和 630 提示，默认关闭流式整句输入。Emoji 使用 Lua 懒加载：保留原有 txjx 映射，并追加 2,516 个来自 Rime-Ice 的不重复关键词，涵盖更多情绪别名、手势、人物、动物、食物、交通、旗帜和新版 Emoji。若 Emoji 没出现，依次确认“表情展示”已开启、输入的是普通中文编码而不是 `u/v/o` 反查、文件已完整复制到 `opencc/xmjd6/`，然后重新部署。

### 自造词指令速查

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

输入法会在会话结束时把运行时操作安全追加到 `xmjd6.zzc.dict.yaml`；要永久整理进正式词库，再运行 `zzc/` 中对应平台的合并脚本。完整的保存、跨设备同步、合并和撤回流程见[自造词使用教程](zzc/自造词使用教程.md)和[合并脚本说明](zzc/README.md)。

Windows 用户可以在仓库根目录运行：

```powershell
python .\zzc\Windows_词库合并.py
```

没有 Python 时可以直接双击 `zzc/Win_词库合并.exe`，需要撤回最近一次合并时双击 `zzc/Win_撤回合并.exe`。两个 EXE 均由当前 xmjd6 共享 Python 核心构建；`package-main` 和正式 Release 会先在 Windows Runner 上使用 Python 3.14.6 + PyInstaller 6.21.0 重新构建并实际执行合并、撤回测试，再把通过测试的 CI 产物交给最终打包，避免发布旧版或损坏的可执行文件。构建和校验方法见[合并脚本说明](zzc/README.md#重新构建-windows-exe)。

## 🔤 英文输入

英文词典直接导入主词典，不需要 `xmjd6.en.schema.yaml`，也不需要切换方案。

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

以下为 2026-08-09 版本的内置记录数；自造词和个人用户词库不计入统计。

| 词库 | 记录数 | 用途 |
| --- | ---: | --- |
| `xmjd6.danzi.dict.yaml` | 36,214 | 上游键道单字表 |
| `xmjd6.cizu.dict.yaml` | 191,398 | 本地基础词组 |
| `xmjd6.catholicism.dict.yaml` | 3,514 | Catholicism、礼仪、神学与东方礼词汇 |
| `xmjd6.protestantism.dict.yaml` | 289 | 新教信条、循道卫理宗传统及《和合本》词汇 |
| `xmjd6.orthodoxy.dict.yaml` | 88 | 东正教礼仪、圣像、灵修与教会制度专有词汇 |
| `xmjd6.oriental.dict.yaml` | 68 | 东方正统教会、合性论传统与成员教会专有词汇 |
| `xmjd6.assyrian.dict.yaml` | 71 | 东方亚述教会、东叙利亚礼与景教史专有词汇 |
| `xmjd6.core.dict.yaml` | 921 | 630 规则、快符和核心候选 |
| `xmjd6.fjcy.dict.yaml` | 514,033 | 附加扩展词组 |
| `xmjd6.ice.dict.yaml` | 373,902 | Rime-Ice 中文精简补充词库 |
| `xmjd6.en.dict.yaml` | 23,610 | Rime-Ice 英文词库 |
| **合计** | **1,144,038** | 不含动态自造词和个人词库 |

四个非天主教传统词库以具有宗派辨识度的信条、礼仪、制度、正式教会名称和历史术语为主体，不靠“祷告”“教会”“基督徒”等泛用词凑量。`xmjd6.protestantism` 另收经审核的《和合本》书卷名、人地名和固定译语，以《和合本》的“马太、约翰、使徒行传、启示录”等新教译名为准，不混入《思高本》译名；循道卫理宗部分覆盖恩典与圣洁神学、班会与联结制度、议会体系、立约礼拜、亚德门传统、近代在华会名和代表人物。东正教、东方正统教会、东方亚述教会和东方礼天主教会分别维护，避免把相近的叙利亚礼、圣像或牧首制度词汇混错归属；东方正统部分不用不准确的“一性论”作为自称。多段人名使用间隔号显示，例如“马丁·路德”，编码时不计间隔号。核对来源和授权边界见 [`tools/christian_traditions_sources.md`](tools/christian_traditions_sources.md)。

这些专题词由 [`tools/christian_traditions_2026.txt`](tools/christian_traditions_2026.txt) 审核，生成器依次尝试键道六码的基础码和首笔辅助码。固定本地词典没有空闲合法码时通常不收录；专题词确定后再重建低优先级 `xmjd6.ice`，让 ICE 词移到更长的合法码或按既有重码预算淘汰。唯一例外是“哥林多后书”“帖撒罗尼迦后书”“雅各书”三卷《和合本》正式书名：前两组的前书与后书在标准规则下拥有完全相同的全部候选，后一卷的全部候选已被固定旧词占用，因此人工审核后使用最终六码并保持专题词优先。除此三项外，四个专题词库没有新增异词同码。

`xmjd6.ice` 定位为本地词库之后的精简补充库。同步过滤器不会直接删除 2～3 字词；它会排除上游低权重长尾、批量数字/年份模板、8 字以上 `ext` 整句及 12 字以上超长词，当前比未精简版本减少 71,144 条。药品名称是例外：片、胶囊、颗粒、注射液、口服液、滴眼液、喷雾剂等剂型词不会因词频低或名称过长被过滤，并在重码预算中优先保留。编码时短词优先占用基础码，长词和低频同码词尽量追加笔画码；随后再按照 `base → ext → others` 和上游权重排序。低优先级重码词会被删减，合并后的中文重码率不会高于同步前的本地基准；新增词在同一码下最多保留 8 个候选。这些过滤规则写在同步器中，因此以后拉取上游时不会重新混入。

### 词库加载顺序

[`xmjd6.extended.dict.yaml`](xmjd6.extended.dict.yaml) 控制词库导入。当前主要顺序为：

```text
user → zzc → danzi → cizu → catholicism → protestantism → orthodoxy → oriental → assyrian → core → fjcy → ice → en
```

本地词库优先于自动生成的上游词库。`xmjd6.user.dict.yaml` 权限最高，适合保存个人常用词；加入大量通用词前应优先考虑对应的专题或基础词库。

## ⚙️ 配置文件

| 文件 | 作用 |
| --- | --- |
| `xmjd6.schema.yaml` | 主方案、引擎、翻译器、反查和快捷键 |
| `xmjd6.custom.yaml` | 用户推荐修改的开关、候选数和流式输入配置 |
| `xmjd6.extended.dict.yaml` | 词库导入顺序与开关 |
| `default.custom.yaml` | 默认方案列表及全局选项 |
| `weasel.yaml` / `weasel.custom.yaml` | Windows 小狼毫候选窗样式与明暗配色 |
| `squirrel.yaml` / `squirrel.custom.yaml` | macOS 鼠须管候选窗样式与明暗配色 |
| `fcitx5/macos/themes/` | macOS Fcitx5 可导入主题；`xmjd6-auto.conf` 自动切换 Cat 明暗配色 |
| `fcitx5/linux/themes/` | Linux Fcitx5 Classic UI 桌面配色复刻主题 |
| `fcitx5/themes.yaml` | 小企鹅主题来源清单，由生成脚本维护 |
| `Hamster.yaml` | iOS 客户端自造词文件同步规则，不是元书键盘皮肤 |
| `xmjd6.symbols.yaml` | 标点与符号 |
| `xmjd6.core.dict.yaml` | 630、快符和核心码表 |
| `xmjd6.user.dict.yaml` | 个人高优先级补充词库 |
| `lua/xmjd6/` | 方案 Lua 模块 |
| `opencc/xmjd6/` | 简繁、Emoji、火星文数据 |

修改 YAML 后必须重新部署。升级仓库时，个人配置尽量写入 `*.custom.yaml` 或 `xmjd6.user.dict.yaml`，不要直接修改自动生成的 `xmjd6.danzi`、`xmjd6.ice` 和 `xmjd6.en`。

### 流式输入

默认使用键道顶功。需要整句流式输入时，可在 `xmjd6.custom.yaml` 中启用：

```yaml
patch:
  translator/enable_sentence: true
  translator/enable_user_dict: true
```

启用 `enable_sentence` 后，中文顶功会自动停用，分号和单引号改作分隔符。详细说明和相关按键覆盖已写在 `xmjd6.custom.yaml` 的注释中。

<a id="上游来源与自动同步"></a>

## 🔄 上游来源与自动同步

生成文件和来源 commit 记录在 [`tools/upstream_dictionaries.lock.json`](tools/upstream_dictionaries.lock.json)：

| 上游 | 源文件 | 生成文件 |
| --- | --- | --- |
| [amorphobia/rime-jiandao](https://github.com/amorphobia/rime-jiandao) | `dicts/01.danzi.txt` | `xmjd6.danzi.dict.yaml` |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `cn_dicts/base`、`ext`、`others` | `xmjd6.ice.dict.yaml` |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `en_dicts/en`、`en_ext` | `xmjd6.en.dict.yaml` |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | `opencc/emoji.txt` | `opencc/xmjd6/xmjd6_emoji_extra_*` |

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

Lua 与自造词实现参考 [wzxmer/rime-txjx](https://github.com/wzxmer/rime-txjx)，已整合的 commit、审查目录和明确排除项记录在 [`tools/upstream_code.lock.json`](tools/upstream_code.lock.json)。这部分不能像纯词库一样无损自动重建，因为必须保留 xmjd6 的命名空间、英文 `i` 入口和顶功差异；因此每周检查只会创建待审查 Issue，不会盲目覆盖本地代码：

```powershell
python .\tools\check_txjx_upstream.py
```

对应工作流是 `.github/workflows/check-txjx-upstream.yml`，不包含任何本机绝对仓库路径，在 GitHub Actions 的 checkout 目录中运行。

第三方来源、固定版本和许可证见 [`THIRD_PARTY.md`](THIRD_PARTY.md) 与 [`licenses/`](licenses/)。

## 🛠️ 维护与验证

本项目的 Python 工具需要 Python 3.11 或更新版本。可以使用系统 Python、虚拟环境或 Pixi。

<details>
<summary><strong>🧪 展开维护与完整验证命令</strong></summary>

先激活相应环境，再在仓库根目录执行：

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
python .\tools\validate_repo.py
python .\tools\clean_dictionary_quality.py --check
python .\tools\sync_upstream_dictionaries.py --check
python .\tools\check_txjx_upstream.py
git diff --check
```

主要维护命令：

```powershell
# 将 VERSION 和 YAML version 更新到指定日期
python .\tools\update_versions.py 2026-08-04

# 清理完全相同的词典记录
python .\tools\dedupe_dictionaries.py

# 检查或修复词库质量（单字表不在清理范围内）
python .\tools\clean_dictionary_quality.py --check

# 重新生成 Catholicism 扩展并整理分区
python .\tools\build_catholicism_expansion.py --write
python .\tools\organize_catholicism_legacy.py

# 重建四个基督宗派专题词库；随后重建 ICE 以重新避让本地码位
python .\tools\build_christian_traditions.py --write
python .\tools\sync_upstream_dictionaries.py --write
```

仓库验证会检查 YAML、Lua、生成文件哈希、目录命名空间和关键配置。当前测试同时覆盖键道6词组编码、飞键规则、Catholicism 分类、四个基督宗派专题词库、专题词跨库零重码、词库质量、上游去重、重码上限、英文 `i` 命名空间及自动同步工作流。

</details>

## 🗂️ 项目结构

```text
.
├─ xmjd6.schema.yaml                 主方案
├─ xmjd6.extended.dict.yaml          词库入口
├─ xmjd6.*.dict.yaml                 本地与生成词库
├─ lua/xmjd6/                        Lua 处理器、翻译器和过滤器
│  ├─ input/                         模块化按键、顶功、标点和快符处理
│  └─ zzc/                           自造词运行时、候选和操作链
├─ opencc/xmjd6/                     OpenCC 命名空间数据
├─ tools/                             生成、同步、清理和验证工具
├─ tests/                             Python 与 Lua 回归测试
├─ licenses/                          第三方许可证副本
├─ THIRD_PARTY.md                    第三方来源说明
└─ .github/workflows/                发布和定期同步工作流
```

## 💡 为什么选择键道6

键道6以音码提供低学习成本和词组输入效率，又通过首笔辅助码减少纯音码的重码。遇到不会读的字时，可使用二分或 GBK 扩展入口；遇到同音候选时，可继续补首笔精确定位。它不是依赖云端大模型的整句输入法，而是一套编码稳定、结果可解释、词库可以自行维护的本地方案。

本仓库的目标是在不破坏键道手感和飞键规则的前提下，持续改善词库质量、重码控制、跨平台可部署性和维护自动化。

## 🙏 致谢与授权

本方案的演进关系为“星空键道6.2 → 星猫键道6 → xmjd6-0x69”。感谢吅吅大山、Proud丶Cat、热热、浮生、千年蟲等方案和词库维护者，以及下列项目的作者与贡献者：

| 项目 | 本仓库中的用途或参考范围 |
| --- | --- |
| [Rime](https://github.com/rime/librime)、[小狼毫](https://github.com/rime/weasel)、[鼠须管](https://github.com/rime/squirrel) | 输入法引擎及 Windows、macOS 官方前端 |
| [东风破 plum](https://github.com/rime/plum) | `recipe.yaml` 安装与更新机制 |
| [xkinput/Rime_JD](https://github.com/xkinput/Rime_JD) | 键道 Rime 方案结构与历史实现参考 |
| [hugh7007/xmjd6-rere](https://github.com/hugh7007/xmjd6-rere) | 当前方案的直接上游、历史配置及小小输入法打包素材来源 |
| [amorphobia/rime-jiandao](https://github.com/amorphobia/rime-jiandao) | 单字表和 `make_dicts.sh` 生成规则来源 |
| [iDvel/rime-ice](https://github.com/iDvel/rime-ice) | 中文补充词库、英文词库及 Emoji 上游数据 |
| [wzxmer/rime-txjx](https://github.com/wzxmer/rime-txjx) | 模块化 Lua、Emoji 查询优化、自造词操作链及合并脚本参考 |
| [amorphobia/opencc-tonggui](https://github.com/amorphobia/opencc-tonggui) | Release 中补充下载的 OpenCC 数据 |
| [rimeinn/rabbit](https://github.com/rimeinn/rabbit)、[amorphobia/rabbit](https://github.com/amorphobia/rabbit) | 玉兔毫运行环境、便携包及相关实现 |
| [Techince/weasel](https://github.com/Techince/weasel) | Windows 水龙月 Fork 客户端 |
| [Fcitx5 macOS](https://github.com/fcitx-contrib/fcitx5-macos-installer)、[Fcitx5 for Android](https://github.com/fcitx5-android/fcitx5-android)、[Fcitx5](https://github.com/fcitx/fcitx5) | macOS、Android、Linux 的小企鹅前端、安装说明与主题格式 |
| [同文输入法 Trime](https://github.com/osfans/trime) | Android Rime 前端 |
| [Mintimate/oh-my-rime](https://github.com/Mintimate/oh-my-rime) | Android DocumentsUI 数据目录操作说明参考 |

上述列举表示来源或技术参考，不代表相关上游为本方案提供官方支持。仓库只分发经过适配和审核的内容：Rime-Jiandao 单字数据使用 AGPL-3.0-or-later，Rime-Ice 词库使用 GPL-3.0，rime-txjx 参考实现使用 MIT；《和合本》专有词审核来源、固定 commit、生成文件校验值和许可证副本见 [`THIRD_PARTY.md`](THIRD_PARTY.md)、[`tools/upstream_dictionaries.lock.json`](tools/upstream_dictionaries.lock.json)、[`tools/upstream_code.lock.json`](tools/upstream_code.lock.json)及[`tools/christian_traditions_sources.md`](tools/christian_traditions_sources.md)。

<p align="right"><a href="#top">⬆️ 返回顶部</a></p>
