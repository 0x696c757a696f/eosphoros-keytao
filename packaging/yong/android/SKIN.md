# 晨星键道 Android 皮肤

本目录的 `skin/keyboard.html` 与 `skin/keyboard.css` 是晨星键道自行维护的小小输入法 Android 皮肤源文件。

- 键盘采用接近 Gboard 的四行 QWERTY 排列、第二行错位、圆角独立按键、左右功能键和长空格比例。
- 黎明与夜色配色由本项目独立设计；不复制 Gboard 的图像、商标或配色资源。
- 图标使用项目内联绘制的简单 SVG 路径，不依赖图片或字体文件。
- 皮肤不包含联网请求、游戏、天气、翻译、广告或第三方脚本。
- 保留候选展开、长按符号、删除连发、双击 Shift 锁定、空格滑动光标、离线 Emoji、语音、粘贴、方向键、切换输入法和收起键盘等实用功能。
- `tools/build_yong_android_skin.py` 将同一套布局分别与 `themes/dawn.css`、`themes/night.css` 合并，生成 Release 中可直接使用的两个 ZIP。
