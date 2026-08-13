# 晨星键道：Fcitx5 原生码表

这里不是晨星自制插件，也不使用 Rime。发布包只依赖各平台 Fcitx5 客户端
提供的官方组件：`fcitx5-chinese-addons` Table 引擎、libime、标点、快捷短语、
简繁转换以及客户端已有的 Emoji／Unicode 功能；不要求安装晨星 `.so` 或第三方插件。

- Linux：将 `inputmethod/eosphoros.conf` 和 `table/eosphoros.main.dict`
  分别复制到 `~/.local/share/fcitx5/` 下的同名目录，然后重启 Fcitx5。
- macOS：在 Fcitx5 的“输入法 → 导入码表”中同时选择 ZIP 内的
  `eosphoros.conf` 与 `eosphoros.txt`。
- Android：在“小企鹅输入法 → 输入法 → 码表管理”中直接导入平台 ZIP；
  应用会用内置 libime 将文本码表转换为二进制码表。Android 码表 ZIP 只含
  `eosphoros.conf` 与 `eosphoros.txt`；主题必须单独导入。

普通中文主表保留 1～6 键编码、候选顺序和无匹配／满码自动上屏。Android 与
macOS 客户端通常已经包含 Chinese Addons；Linux 发行版常将其拆为
`fcitx5-chinese-addons` 软件包。这些都是 Fcitx5 官方组件，不是晨星插件。
Rime 的 Lua 命令、反查模式、英文前缀、OpenCC 候选过滤和自造词脚本不属于
这个原生 Table 版本。某一平台若没有随客户端提供 `fcitx5-lua`，晨星也不会把
它列为基本依赖。
