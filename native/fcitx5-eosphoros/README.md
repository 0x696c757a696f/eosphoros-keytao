# 晨星键道原生 Fcitx5 引擎（第一阶段）

这是与仓库现有 Rime 方案并行的实验性原生实现。它直接实现
`InputMethodEngineV2`，运行时不加载 `fcitx5-rime`、`librime`、
`librime-lua`、Rime schema 或 YAML 词典。

当前第一阶段只实现普通键道模式：原生二进制词典查询、候选窗、空格和
数字选词、退格、Escape、Enter 编码直出、上下/翻页选择，以及与现有
`eosphoros_topup.lua` 固定规则一致的基础顶功。英文和三种反查模式只在
状态枚举中预留，尚未启用；OpenCC、Lua 扩展、用户词典和词频学习也不在
本阶段范围内。

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
`EOSPHOROS_NATIVE_DICTIONARY=/path/to/eosphoros-native.dict` 临时覆盖词典。

默认构建小型确定性测试词典。要编译真实词典，可按导入优先级传入多个
Rime 词典；源文件顺序和每个文件的行顺序都会保留：

```bash
cmake -S native/fcitx5-eosphoros -B build/native \
  -DEOSPHOROS_DICTIONARY_INPUTS="dicts/eosphoros/eosphoros.core.dict.yaml;dicts/eosphoros/eosphoros.ext.dict.yaml"
```

只验证不依赖 Fcitx 的核心逻辑时，可添加 `-DBUILD_FCITX_ADDON=OFF`。

## 运行时依赖边界

原生插件只链接 Fcitx5 Core 和系统 C++ 运行库。发布前应检查：

```bash
ldd build/native/eosphoros-native.so
```

输出不得包含 `rime`、`librime`、`lua` 或 `opencc`。当前使用自有只读词典
和上下文状态机，没有使用 libime `TableContext`，原因见 [AUDIT.md](AUDIT.md)。
