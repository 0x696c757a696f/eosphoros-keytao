晨星键道 · 小小输入法 Android 配置包
=====================================

本压缩包不是 APK。请先从小小输入法官网安装 Android 版，再把压缩包内
yong 文件夹合并到手机存储中的 yong 文件夹，使最终路径类似：

  /storage/emulated/0/yong/.yong/yong.ini
  /storage/emulated/0/yong/.yong/mb/eosphoros/eosphoros.txt
  /storage/emulated/0/yong/.yong/android/Eosphoros-Dawn.zip
  /storage/emulated/0/yong/.yong/android/Eosphoros-Night.zip

覆盖前请备份自己修改过的 yong.ini 和用户数据。复制完成后，切换到其他
输入法再切回小小输入法，或者在小小输入法设置中重载配置。

本包已直接包含“晨星·黎明”和“晨星·夜色”两套完整 Android 键盘皮肤，
不需要准备基础皮肤，也不需要运行 Python。复制完成后，在小小输入法的
皮肤设置中选择 Eosphoros-Dawn.zip 或 Eosphoros-Night.zip 即可。不要解压
这两个皮肤 ZIP，也不要把 ZIP 内的零散文件直接放到 android 目录。

两套皮肤使用晨星键道自行维护的四行 QWERTY 布局，按键比例和错位方式参考
Gboard 的常见全键盘结构，配色和图标由本项目独立设计。皮肤保留候选展开、
长按符号、删除连发、双击 Shift、空格滑动光标、离线 Emoji、语音、粘贴、
方向键、切换输入法和收起键盘；不含旧“彩”皮肤的多配色、游戏或联网功能。

码表包含 i + 英文、u + 连写全拼、v + 二分、o + 键道单字码四个静态入口，
例如 ihello 和 uhao。普通词库没有删减，配置使用后台线程加载大码表。

小小输入法官网：https://yong.dgod.net/
官方下载页：https://yongim.ysepan.com/
晨星键道：https://github.com/0x696c757a696f/eosphoros-keytao
