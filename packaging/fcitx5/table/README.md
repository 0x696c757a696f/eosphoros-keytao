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

普通中文主表保留 1～6 键编码、候选顺序和无匹配／满码自动上屏，并在首键处分出
四个独立命名空间：`i` + 英文、`u` + 连写全拼、`v` + 二分编码、`o` + 键道单字码。
例如 `ihello` 可输入 `hello`，`uhao` 可查“好”。这四棵长码表不会挂到其他普通
编码的子树下；Table 同时关闭学习和自动造词，1～6 码保持词典固定顺序。生成检查
还会限制普通 1／2／3 码最大前缀规模，防止上游同步意外造成性能退化。

Android 与
macOS 客户端通常已经包含 Chinese Addons；Linux 发行版常将其拆为
`fcitx5-chinese-addons` 软件包。这些都是 Fcitx5 官方组件，不是晨星插件。
原生 Table 的四个入口使用静态精确码表，不包含 Rime 的拼音模糊音、反查注释；
Lua 命令、OpenCC 候选过滤和自造词脚本也不属于
这个原生 Table 版本。某一平台若没有随客户端提供 `fcitx5-lua`，晨星也不会把
它列为基本依赖。
