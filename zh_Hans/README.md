# BDSpyrunnerW(轻量级Python插件平台)

![Liscense](https://img.shields.io/github/license/WillowSauceR/BDSpyrunnerW?style=for-the-badge)
[![Downloads](https://img.shields.io/github/downloads/WillowSauceR/BDSpyrunnerW/total?style=for-the-badge)](https://github.com/WillowSauceR/BDSpyrunnerW/releases/latest)
[![DwonloadsLatest](https://img.shields.io/github/downloads/WillowSauceR/BDSpyrunnerW/latest/total?label=DOWNLOAD@LATEST&style=for-the-badge)](https://github.com/WillowSauceR/BDSpyrunnerW/releases/latest)
[![BDS](https://img.shields.io/badge/BDS-1.19.70.02-blue?style=for-the-badge)](https://www.minecraft.net/download/server/bedrock)

[简体中文](/) | [English](https://pyr.jfishing.love/en/)

这里是 [BDSpyrunnerW](https://github.com/WillowSauceR/BDSpyrunnerW/ "Github页面") 的官方网站，BDSpyrunnerW是BDSpyrunner的一个分支，因为原项目选择依赖LL的更加丰富API而放弃了自主独立开发，该分支的定位是轻量级，满足生存服微改要求（玩法建议以[addons](https://mcpedl.com/ "查找附加组件")为主），保持项目的独立继续维护的分支，API不多，但我们会尽量保证插件的高性能和稳定性。我们在原本名字``BDSpyrunner``后加上``W``以区分使用 [LiteLoaderAPI](https://github.com/LiteLDev/LiteLoaderBDS/) 的主分支版本。此分支版本基于主分支 [Release1.8.7](https://github.com/twoone-3/BDSpyrunner/tree/f7645c3e69bf505d4207f76932c28665fff576fe "Github页面") 开发而成，这是BDSpyrunner转为使用 ``LiteLoaderAPI``前的最后一个提交版本。本分支注重于稳定性，故API和监听器都没有主分支丰富，使用时请注意您的插件使用的监听器和API版本

## 如何使用

1. 下载 [Release](https://github.com/WillowSauceR/BDSpyrunnerW/releases/latest) 中的``BDSpyrunnerW.dll``、``mc.py``和``BDSpyrunnerW.pdb``，pdb文件不是必须的，但是在崩溃时用于反馈会给我们带来很大便利。如果你因为网络问题打不开Release页面，可以尝试由``fgit.ml``提供的加速镜像站（[链接](https://hub.fgit.ml/WillowSauceR/BDSpyrunnerW/releases/latest "点我转跳")），内容是一致的，感谢他们做出的贡献！
2. 确保您已经安装了[LiteLoader](https://github.com/LiteLDev/LiteLoaderBDS)或[BDXCore](https://github.com/jfishing/BDXCore)。或者，您也可以使用[Xenos](https://github.com/DarthTon/Xenos/releases/latest)将本插件注入到BDS进行加载，``Type``选择``New``，``Process``选择``bedrock_server.exe``，点击``Add``按钮并选择``BDSpyrunnerW.dll``，最后点击``Inject``按钮进行开服加载插件。
3. (方法一)(推荐) 在[此处](https://pyr.jfishing.love/plugins/setup_pyrw_runtime.zip)下载一键安装环境包，下载完成后解压到服务端文件夹，你的服务端文件夹在解压完成后应该大致是这样的：
   ```文件夹结构
   ├─behavior_packs
   ├─config
   ├─definitions
   ├─plugins
   ├─resource_packs
   ├─bedrock_server.exe
   ├─install_py_env.bat
   ├─python39._pth
   ├─server.properties
   ......
   ```
   然后双击``install_py_env.bat``进行安装，当控制台中出现``Successfully install the Python runtime environment``消息时，说明环境已完成安装。如果没有，请联系我们并反馈问题。
   (方法二) 下载安装[Python3.9.13](https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe)，安装时勾选 ``Add Python to Path``
4. 将``BDSpyrunnerW.dll``和``BDSpyrunnerW.pdb``放入您用于存放插件的文件夹，如``plugins``、``bdxcore_mod``
5. 将``mc.py``放入``plugins/py``文件夹

### 更新版本

更新到新版本前请手动将BDS目录中的``bedrock_server_sym.txt``和``bedrock_server_sym_cache.bin``删除

### 可用命令

* ``pyreload <module>``: 热重载(所有)插件

## 插件列表

[co↑co↓](plugins/README.md "这里")

## 开发文档

[开始阅读](docs/README.md)
