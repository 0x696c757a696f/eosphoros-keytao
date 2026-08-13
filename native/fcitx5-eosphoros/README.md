# 晨星键道原生 Fcitx5 引擎（第三阶段预览）

这是与仓库现有 Rime 方案并行的实验性原生实现。它直接实现
`InputMethodEngineV2`，运行时不加载 `fcitx5-rime`、`librime`、
`librime-lua`、Rime schema 或 YAML 词典。

当前实现会按 [production-dictionaries.tsv](data/production-dictionaries.tsv)
编译主方案约 117 万条静态词条，并提供候选窗、数字/鼠标/Tab/分号/撇号选词、
退格、Escape、Enter 编码直出、上下/翻页、中文标点、固定与连续顶功、空码顶功和
自动回退。`i` 英文、`u` 全拼、`v` 两分、`o` GBK 入口使用独立词典命名空间，继续
输入后预编辑会隐藏入口字母。构建时还会把反查注音、仓库已有 Emoji 与简繁映射、
ZZC 单字拆分编译成只读辅助索引；运行时仍不加载 Lua 或 OpenCC。支持 F7 简繁、
计算器与日期时间、候选词频学习和用户词持久化。按反斜杠进入原生 ZZC，依次输入并
选择组成词的各字，再按反斜杠结束，词会按键道 6 规则计算六码并保存。

## 构建

在安装了 Fcitx5 开发文件、Extra CMake Modules、CMake、C++17 编译器和
Python 3 的 Linux 上运行：

```bash
cmake -S native/fcitx5-eosphoros -B build/native -G Ninja \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build/native
ctest --test-dir build/native --output-on-failure
sudo cmake --install build/native
```

重新启动 Fcitx5 后，在配置工具中添加“晨星键道（原生）”。开发时可以用
`EOSPHOROS_NATIVE_DICTIONARY=/path/to/eosphoros-native.dict`、
`EOSPHOROS_NATIVE_AUXILIARY=/path/to/eosphoros-native.aux` 和
`EOSPHOROS_NATIVE_USER_DATA=/path/to/user-data.tsv` 临时覆盖相应路径。

默认构建正式词典，同时另建小型确定性词典供快速单元测试。正式来源清单保留
`eosphoros.extended` 的导入顺序和各文件行序；新增静态词典时需同步更新该清单，
仓库测试会检查遗漏：

```bash
cmake -S native/fcitx5-eosphoros -B build/native \
  -DEOSPHOROS_DICTIONARY_MANIFEST=/path/to/production-dictionaries.tsv
```

构建器同时通过 `-DEOSPHOROS_SCHEMA=eosphoros.schema.yaml` 把当前 schema 的
`topup` 与 `menu/page_size` 转换进原生二进制词典；插件运行时不读取或执行
schema，也不会把顶功阈值散落硬编码在按键路径中。

只验证不依赖 Fcitx 的核心逻辑时，可添加 `-DBUILD_FCITX_ADDON=OFF`。

## 运行时依赖边界

原生插件只链接 Fcitx5 Core 和系统 C++ 运行库。发布前应检查：

```bash
ldd build/native/libeosphoros-native.so
```

输出不得包含 `rime`、`librime`、`lua` 或 `opencc`。当前使用自有只读词典
和上下文状态机，没有使用 libime `TableContext`，原因见 [AUDIT.md](AUDIT.md)。

## 第三阶段测试

CTest 分别验证 Dictionary、纯 `TopupPolicy` 和基于来源标注 golden trace 的
`EosphorosContext`。trace 覆盖短码、二／三／四字词、首笔辅助码、确认过的飞键、
真实重码、Space／数字/快捷键选词、退格、Escape、固定／连续／空码顶功、自动回退、
中文标点和翻页选择。生产词典冒烟测试还会检查总条数及主码、英文、全拼、两分、
GBK 五种查询路径。
测试夹具不包含临时编造的词条；仓库级测试会逐项确认其文本和编码仍存在于正式
晨星词库，避免 golden 结果与实际方案脱节。
完整已实现、差异和未实现清单见 [AUDIT.md](AUDIT.md)。
