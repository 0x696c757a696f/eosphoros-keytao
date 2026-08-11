晨星键道 · 小小输入法 Linux 完整包
=================================

本包在小小输入法 Linux 发行包基础上，内置晨星键道配置、码表和原创皮肤。
解压后可直接从 yong 目录运行安装工具，无需再单独下载程序本体。

常见用户配置位置：

  ~/.yong/
  $XDG_CONFIG_HOME/yong/

安装程序通常可在解压后的 yong 目录中执行：

  sudo ./yong-tool.sh --install
  ./yong-tool.sh --select

程序目录和 .yong 中均带有晨星配置入口；安装后若改用用户配置目录，应能看到：

  yong.ini
  mb/eosphoros/eosphoros.txt
  skin/Eosphoros-Mono/skin.ini

包内默认启用“晨星·极简”皮肤；另附“晨星·黎明”和“晨星·石墨”。修改
yong.ini 的 [IM]/skin 后须重载或重启小小输入法。

Wayland、GNOME、KDE 和 wlroots 环境的接入方式不同，请以官方 Linux 安装
说明为准，不要同时叠加多套输入法环境变量。

官方 Linux 安装说明：https://yong.dgod.net/read.php?fid=7&tid=6
小小输入法官网：https://yong.dgod.net/
晨星键道：https://github.com/0x696c757a696f/eosphoros-keytao
