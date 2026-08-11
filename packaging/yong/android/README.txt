晨星键道 · 小小输入法 Android 配置包
=====================================

本压缩包不是 APK。请先从小小输入法官网安装 Android 版，再把压缩包内
yong 文件夹合并到手机存储中的 yong 文件夹，使最终路径类似：

  /storage/emulated/0/yong/.yong/yong.ini
  /storage/emulated/0/yong/.yong/mb/eosphoros/eosphoros.txt

覆盖前请备份自己修改过的 yong.ini 和用户数据。复制完成后，切换到其他
输入法再切回小小输入法，或者在小小输入法设置中重载配置。

本包不会强行覆盖 Android 键盘布局。theme-builder 中附带晨星·黎明和
晨星·夜色两套原创配色覆盖层，可将它们应用到与当前 APK 兼容的基础皮肤：

  python theme-builder/build_yong_android_skin.py 基础皮肤.zip --theme dawn --output 晨星-黎明.zip
  python theme-builder/build_yong_android_skin.py 基础皮肤.zip --theme night --output 晨星-夜色.zip

建议先从当前 APK 提取默认皮肤，或使用自己确认兼容且有权修改的皮肤作为
基础。构建器自身不会新增游戏、联网接口、字体或跟踪代码，但基础皮肤已有
的文件会原样保留，所以生成前仍要审查来源和内容。将结果放入
yong/.yong/android/，再按小小输入法的皮肤选择方式启用。脚本只改配色，
保留基础皮肤原有键位、手势和功能，因此基础皮肤仍须与当前 APK 兼容。

小小输入法官网：https://yong.dgod.net/
官方下载页：https://yongim.ysepan.com/
晨星键道：https://github.com/0x696c757a696f/eosphoros-keytao
