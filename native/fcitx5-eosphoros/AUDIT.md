# 现有晨星键道行为审计（2026.8.13）

## 审计范围与原则

本审计直接阅读了 `eosphoros.schema.yaml`、`eosphoros.extended.dict.yaml`、
`dicts/eosphoros/**`、`lua/eosphoros/**`、`opencc/eosphoros/**`、
`packaging/yong/**` 与现有测试。顶功结论以
`lua/eosphoros/eosphoros_processor.lua`、
`lua/eosphoros/input/eosphoros_topup.lua` 和
`lua/eosphoros/input/eosphoros_commit_guard.lua` 为准，不由 README 推测。

现有 Rime 与 Yong 实现继续保留；原生 Fcitx5 是并行输入法，不替换、修改
或打包进既有客户端方案。第一阶段只实现普通键道热路径，不提前移植
OpenCC、Lua 附加功能、用户词典、ZZZC 或词频学习。

## 1. 主编码查询与候选排序

- 主方案使用 `table_translator` 和 `eosphoros.extended`，字母表为
  `abcdefghijklmnopqrstuvwxyz;'`，`enable_completion: true`，关闭句子与用户词典。
- `eosphoros.extended.dict.yaml` 为 `sort: original`。候选静态优先级由
  `import_tables` 顺序及各源文件行序共同决定，而不是运行时 weight 重排。
- 原生构建器按显式输入文件顺序和行序生成确定性二进制词典；运行时只做
  exact/prefix lookup，不解析百万行 YAML。精确候选列在补全项之前，同文本去重；
  补全项标为 `completion`，不会被顶功自动提交。
- 已核对 libime 当前公开 API：`TableBasedDictionary` 提供二进制载入、
  `TableMatchMode::Exact/Prefix`、多候选回调和插入序号，具备后续承载完整大词典的
  基础能力；`TableContext` 同时带有自动选择、学习和组句状态，不适合作为晨星顶功
  状态机。第二阶段使用紧凑、稳定按编码排序的 `EOSDICT3` 数组，已经编译约 117 万条
  正式静态词条；它避免 `unordered_map` 在百万级数据上的节点内存膨胀，同时保留源文件
  优先级。命名空间字节隔离主码与 `i/u/v/o`，不依赖 libime-table。
- MVP 不实现用户学习，因此静态顺序不会被本地词频改变。

## 2. 短码

- 两码、三码等短码是正式 exact 候选；不会仅因“短”而自动上屏。
- Space、数字选词或后续满足顶功规则时才提交。golden trace 使用真实词条
  `不能 ba`、`棒不棒 bbb` 验证。

## 3. 顶功与连续顶功

schema 当前值为：

- `topup_this = bcdefghjklmnpqrstwxyz`
- `topup_with = avuio;`
- `min_length = 4`
- `max_length = 6`
- `auto_clear = true`
- `topup_command = false`
- `menu/page_size = 5`

这些值由 `build_dictionary.py --schema` 在构建期转换进 `EOSDICT3`，运行时
不读取或执行 schema。`TopupPolicy` 是不依赖 Fcitx 对象的纯逻辑。

`eosphoros_processor.lua` 的固定规则按当前顺序等价为：

1. 已有 6 码时，下一编码键触发；
2. 前一键属于 `topup_with`、下一键不属于时触发；
3. 已有至少 4 码，且前一键、下一键都不属于 `topup_with` 时触发；
4. `topup_command` 开启且首键属于顶功键时不触发（当前关闭）；
5. 分号快符前导输入在 direct-symbol 分支处理，不进入普通固定顶功。

触发后，只有当前选中的 exact 非 raw 候选可提交。成功提交后，新键由下一段
继续接收，从而支持连续顶功。

## 4. 空码顶功

这是原先 MVP 审计中的一处错误，现已纠正。`eosphoros_topup.exec()` 在没有
可提交候选且 `auto_clear=true` 时清空旧输入并报告状态已转换；processor 随后
返回 `kNoop`，让当前触发键继续交给 speller。因此真实行为是“清空旧码，触发键
成为下一段首码”，不是吞掉触发键。若 `auto_clear=false`，旧码保留并消费该键。

## 5. 飞键与首笔辅助码

- `layout/algebra` 用反引号派生展示编码中的声、笔位置；正式词典仍存最终键道码。
- 三字词第六位为第三字首笔，四字词编码按首字母位置组合；这些规则体现在生成词典
  而不是 native 运行时重新编码。
- MVP 的词典查询不会改写编码。golden 使用已人工确认的 `赞主曲 zqquo` 和单字
  辅助码 `毌 aaiv`，确保运行时保留现有飞键／首笔结果。测试夹具中的每一条
  `文本 + 编码` 都由仓库级测试反查正式 `core`、`cizu` 或 `catholicism` 词库；
  不再用为测试临时发明的词或编码证明顶功行为。

## 6. 第二候选快捷键与重码

- Rime `Tab` 通过 key binder 发送 `2`；`smarttwo` 开启时，分号提交候选索引 1，
  撇号提交索引 2。Yong 的 `select=; \'` 同样提供次选快捷键。
- 数字 1–9、鼠标、Tab，以及开启 smarttwo 时的分号／撇号候选选择均已实现。
- golden 使用真实冲突 `洪山 / 婚姻圣召 hyefa`、`散装酒 / 三钟经 sfj` 验证
  静态重码顺序和数字次选。

## 7. 基础编辑键

- Space：提交当前高亮 exact 候选；没有候选时清空组合。
- 1–9：按当前候选页选择；候选点击使用 Fcitx5 原生 `CandidateWord::select()`。
- Up/Down、PageUp/PageDown：改变全局候选光标，页面大小来自 schema 编译配置。
- Backspace：删除一码并刷新候选；Escape：清空组合。
- Enter：Yong 当前为 `enter=default`；MVP 采用原始编码直出，并在差异表明确记录。

## 8. 英文与反查入口

- `i`：`melt_eng/prefix` 与 `english/prefix` 均为 `i`，主词典预编辑规则在继续输入后
  隐藏入口字母；processor 遇到此前缀时让 Rime translator 接管。
- `u`：全拼反查 `pinyin_simp`；`v`：二分反查 `quanpinerfen`；`o`：GBK／生僻字
  反查 `eosphorosgbk`。
- 原生 `Mode` 已启用 `English`、`ReversePinyin`、`ReverseLiangfen`、
  `ReverseGBK`；构建期命名空间确保相同编码不会跨模式串候选。

## 9. Yong 非 Rime 参考

`packaging/yong/yong.ini` 使用同一晨星码表，候选数 5，`enter=default`、
`space=default`、`select=; \'`，关闭自动造词和自动调频。它证明晨星编码可以在
非 Rime 引擎运行，但 Yong 自身不定义 Lua 顶功细节，因此顶功仍以 Lua 源码为准。

## 10. OpenCC 与 Lua 附加功能（只审计，不迁移）

现有 OpenCC Lua 管线包含 replace、append、Emoji split 等候选操作，不能等同于
简单文字转换。计算器、日期、统计、火星文、Emoji、ZZZC、自造词和用户数据库均
明确留给后续阶段；正常 native 汉字输入路径不链接 Lua、OpenCC 或 librime。

## 第二阶段行为差异与未实现

- 已实现：小型原生词典、exact/prefix 候选、静态排序、独立输入上下文、原生候选窗、
  Space/数字/鼠标选词、方向与翻页、Backspace/Escape、Enter 原码、固定顶功、连续顶功、
  空码顶功、schema 构建期配置转换，以及 Shift 字母键规范化为小写编码。
- 新增：完整静态词典、自动回退、Tab/分号/撇号候选快捷键、基础中文标点和
  `i/u/v/o` 隔离入口。
- 与 Rime 差异：不学习词频；不实现分号快符、动态注音 comment、OpenCC 或 Lua
  候选过滤；反查只做静态候选，不组句。
- 未实现：OpenCC、Lua 附加功能、用户词典、ZZZC、自造词、动态词频及系统化性能
  benchmark。它们属于后续阶段，不冒充当前能力。

## 第一阶段验证门

- CMake 构建 `.so`，CTest 分别运行 Dictionary、TopupPolicy、golden Context 测试；
- 安装树包含 addon、输入法元数据、`eosphoros-native.dict` 与晨星图标；
- 元数据名称为“晨星键道（原生）”；
- CI 对 `.so` 执行 `ldd`，禁止 `librime`、`rime`、`lua`、`opencc`；
- 所有 Rime／客户端 Release 包和 Package Master 通用 artifact 禁止包含 `native/`。
