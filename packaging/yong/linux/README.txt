晨星键道 · 小小输入法 Linux 配置包
===================================

本包不含小小输入法 Linux 程序。请先从小小输入法官方渠道下载当前 Linux
版本，按官方说明安装，再把本压缩包中的 .yong 目录合并到当前用户配置目录。

常见用户配置位置：

  ~/.yong/
  $XDG_CONFIG_HOME/yong/

若两个位置同时存在，以小小输入法当前实际读取的位置为准。复制后应能看到：

  yong.ini
  mb/eosphoros/eosphoros.txt
  skin/Eosphoros-Mono/skin.ini

包内默认启用“晨星·极简”皮肤；另附“晨星·黎明”和“晨星·石墨”。修改
yong.ini 的 [IM]/skin 后须重载或重启小小输入法。

安装程序通常可在解压目录中执行：

  sudo ./yong-tool.sh --install
  ./yong-tool.sh --select

Wayland、GNOME、KDE 和 wlroots 环境的接入方式不同，请以官方 Linux 安装
说明为准，不要同时叠加多套输入法环境变量。

官方 Linux 安装说明：https://yong.dgod.net/read.php?fid=7&tid=6
小小输入法官网：https://yong.dgod.net/
晨星键道：https://github.com/0x696c757a696f/eosphoros-keytao
