# Third-party sources

The generated dictionaries below retain their upstream provenance. Exact source
commits and generated-file checksums are recorded in
`tools/upstream_dictionaries.lock.json`.

## `dicts/eosphoros/eosphoros.protestantism.dict.yaml` Bible terminology

- Reference text: 1919 Chinese Union Version (`ChiUns`)
- Source information: <https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=ChiUns>
- Distribution status: Public Domain

Only reviewed book names, proper names, places, and fixed terminology are used;
the biblical text and dictionary definitions are not redistributed. Online
theological and Bible dictionaries whose redistribution terms are unclear are
manual verification sources only. The complete review policy and links are in
`tools/christian_traditions_sources.md`.

Additional short-term candidates were reviewed from the user-supplied iqt.ai
CSV archive and the Sogou/Baidu Christian dictionary category pages. Their
binary dictionaries, frequencies, definitions, scripture sentences, lyrics,
and long phrases are not redistributed. Temporary SCEL/BDICT conversions were
cross-checked with `studyzy/imewlconverter`; only independently reviewed lexical
items are retained, normalized to simplified Chinese, and deduplicated against
all local dictionaries.

## `dicts/eosphoros/eosphoros.danzi.dict.yaml`

- Upstream: <https://github.com/amorphobia/rime-jiandao>
- Source: `dicts/01.danzi.txt`
- Build-rule reference: `scripts/make_dicts.sh`
- License: GNU Affero General Public License 3.0 or later
- License copy: `licenses/rime-jiandao-AGPL-3.0.txt`

The local synchronization tool reproduces the relevant `make_dicts.sh`
behavior for this repository: it writes an eosphoros-specific Rime header and then
appends the upstream single-character rows unchanged.

## `dicts/eosphoros/eosphoros.ice.dict.yaml`

- Upstream: <https://github.com/iDvel/rime-ice>
- Sources: `cn_dicts/base.dict.yaml`, `cn_dicts/ext.dict.yaml`, and
  `cn_dicts/others.dict.yaml`
- License: GNU General Public License 3.0
- License copy: `licenses/rime-ice-GPL-3.0.txt`

Rime-Ice rows are converted from annotated full pinyin to JianDao 6 codes by
`tools/sync_upstream_dictionaries.py`. Existing local dictionaries take
precedence: duplicate text is excluded, then upstream duplicates are removed in
the order `base`, `ext`, `others`. Entries that cannot be aligned to a precise
upstream single-character reading are skipped rather than assigned a guessed
code. Within that source order, higher upstream weights receive shorter codes;
lower-priority homophones receive successive stroke suffixes. Remaining exact
full-code collisions are pruned against the existing local collision-rate
baseline, with no more than eight new combined candidates per code.

## `dicts/eosphoros/eosphoros.en.dict.yaml`

- Upstream: <https://github.com/iDvel/rime-ice>
- Sources: `en_dicts/en.dict.yaml` and `en_dicts/en_ext.dict.yaml`
- License: GNU General Public License 3.0
- License copy: `licenses/rime-ice-GPL-3.0.txt`

The two English sources are merged in main-then-extension order. Codes are
normalized to reachable lowercase letter sequences and prefixed with `i` before
the generated dictionary is imported into the main eosphoros table. This removes
the need for a separate auxiliary English schema while keeping English entries
isolated from JianDao 6 codes.

## `dicts/eosphoros/eosphoros.wanxiang.*.dict.yaml`

- Upstream: <https://github.com/amzxyz/rime-wanxiang/tree/wanxiang/dicts>
- Sources: `yaopin`, `yixue`, `huaxue`, `diming`, `mingren`, `taifeng`, and
  `jichu` dictionaries
- License: Creative Commons Attribution 4.0 International
- License text: <https://github.com/amzxyz/rime-wanxiang/blob/wanxiang/LICENSE>

These seven category files are an adapted and filtered vocabulary extract. Tone-marked pinyin is used
only to derive native JianDao 6 codes; upstream codes and final candidate
weights are not copied. Generic names, association sentences, correction
tables, single characters, English, and dialect sources are excluded. Local
vocabulary is deduplicated first, every accepted code is protected, and the
lower-priority Rime-Ice fallback is rebuilt around it so the addition does not
introduce new different-text/same-code collisions. Exact source commit,
generated checksum, filter statistics, and modification date are retained in
`tools/upstream_dictionaries.lock.json` and the generated dictionary header.

## `opencc/eosphoros/eosphoros_emoji_extra_*`

- Upstream: <https://github.com/iDvel/rime-ice>
- Source: `opencc/emoji.txt`
- License: GNU General Public License 3.0
- License copy: `licenses/rime-ice-GPL-3.0.txt`

The synchronization tool excludes keys already present in the adapted TXJX
Emoji tables, then emits the remaining Rime-Ice mappings as an
eosphoros-namespaced Lua overlay. Single-character entries, a first-character
phrase index, and the phrase shard are generated separately so the existing
lazy OpenCC provider can load the data without replacing the original
mappings. No locally invented Emoji combinations are added.

## Lua input and ZZZC implementation

- Upstream: <https://github.com/wzxmer/rime-txjx>
- Integrated commit: `377001a70e73727b4e3d8cb7b6de9ee401ab3a98`
- Sources: modular input processor, ZZZC operation-chain implementation,
  completion/reverse-hint optimizations, OpenCC lookup optimizations, newline
  filter, merge scripts, documentation, and regression-test design
- License: MIT
- License copy: `licenses/rime-txjx-MIT.txt`
- Integration lock: `tools/upstream_code.lock.json`

The implementation is adapted rather than copied as a whole: module names are
kept below `lua/eosphoros/`, state keys use the eosphoros namespace, OpenCC assets stay
below `opencc/eosphoros/`, and the main processor preserves this repository's `i`
English prefix and JianDao 6 top-up behavior. TXJX dictionaries, schema files,
root-level OpenCC data, opaque platform binaries, and project-specific release
configuration are intentionally not imported.

## Android 同文输入法“格调”皮肤

- Upstream: <https://github.com/chwt163/mytrime/tree/main/3.3.10>
- Integrated commit: `419b31be726ba8c8277daf8913b84dee974e2048`
- Source: `3.3.10/style.trime.yaml`
- Original author: 风花絮 (`chwt163`)
- License: GNU General Public License 3.0 or later
- License copy: `licenses/mytrime-GPL-3.0.txt`

`tools/build_mobile_themes.py` keeps the complete 格调 keyboard, toolbar,
liquid keyboard and preset-key definitions. It repairs redundant flow-mapping
commas that strict YAML parsers reject, changes the displayed name, and injects
the Eosphoros dawn, night and monochrome color schemes. The generated
`mobile_themes/trime/eosphoros.trime.yaml` does not inherit Trime's built-in
default keyboard.

## 小小输入法桌面发行包

- Integration source: <https://github.com/hugh7007/xmjd6-rere/releases/tag/20231115>
- Windows asset: `yong-win.7z`
- Linux asset: `yong-lin.7z`
- Original project: <https://yong.dgod.net/>

Release 构建会下载当前发行附件，再加入晨星配置、码表、帮助和原创皮肤。
这些附件由同一维护者更新，允许在保留文件名的情况下重新上传；工作流不会进行
固定哈希比较。下载失败或附件无法解压时仍会中断。小小输入法程序本身仍遵循其
上游授权和分发条件，晨星键道不改变程序本体的许可证。

## 元书与仓输入法键盘布局模板

- Upstream: <https://github.com/BlackCCCat/ResourceforHamster>
- Integrated commit: `6c2b8d9a3c7116f41b77c32a662a7685770a5914`
- Sources: `Skin_Keyboard/万象-元书/WanxiangSkin` and
  `Skin_Keyboard/万象-仓/26键-万象`
- License: MIT
- Archive SHA-256:
  `fc2781f007b6d5c3f523400763208f1f8665e835e9b250bcaa92a344fd936559`

`tools/build_mobile_themes.py` downloads this exact archive only while building
Release assets, verifies the checksum, keeps the complete keyboard layouts, and
replaces their presentation with the repository's original Dawn, Night, and
Mono palettes and previews. The large template and generated `.cskin`/`.hskin`
files are not committed to the source tree; each generated skin contains its
own attribution notice.
