# BDSpyrunnerW(Lightweight Python plugin platform)

![Liscense](https://img.shields.io/github/license/WillowSauceR/BDSpyrunnerW?style=for-the-badge)
[![Downloads](https://img.shields.io/github/downloads/WillowSauceR/BDSpyrunnerW/total?style=for-the-badge)](https://github.com/WillowSauceR/BDSpyrunnerW/releases/latest)
[![DwonloadsLatest](https://img.shields.io/github/downloads/WillowSauceR/BDSpyrunnerW/latest/total?label=DOWNLOAD@LATEST&style=for-the-badge)](https://github.com/WillowSauceR/BDSpyrunnerW/releases/latest)
[![BDS](https://img.shields.io/badge/BDS-1.19.61.01-blue?style=for-the-badge)](https://www.minecraft.net/download/server/bedrock)

[简体中文](https://pyr.jfishing.love/zh_Hans/) | [English](/)

Here is the official website of [BDSpyrunnerW](https://github.com/WillowSauceR/BDSpyrunnerW/ "Github page"), BDSpyrunnerW is a branch of BDSpyrunner, because the original project chose to rely on the richer API of LL and gave up independent development, the positioning of this branch is lightweight, to meet the requirements of the survival suit micro-change (play recommended to [addons](https://mcpedl.com/ "find addons"), to maintain the independence of the project to continue to maintain the branch The API is not much, but we will try to ensure the high performance and stability of the plug-in. We add ``W`` after the original name ``BDSpyrunner`` to distinguish the main branch version using [LiteLoaderAPI](https://github.com/LiteLDev/LiteLoaderBDS/). This branch version is based on the main branch [Release1.8.7](https://github.com/twoone-3/BDSpyrunner/tree/f7645c3e69bf505d4207f76932c28665fff576fe "Github page"), which was the last commit version of BDSpyrunner before it switched to using ``LiteLoaderAPI``. This branch focuses on stability, so the API and listeners are not as rich as the main branch, so please pay attention to the listener and API versions used by your plugin when using it

## How to use

1. Download ``BDSpyrunnerW.dll``, ``mc.py`` and ``BDSpyrunnerW.pdb`` from [Release](https://github.com/WillowSauceR/BDSpyrunnerW/releases/latest). pdb files are not required, but are useful for feedback in case of crashes.
2. Make sure you have [LiteLoader](https://github.com/LiteLDev/LiteLoaderBDS) or [BDXCore](https://github.com/jfishing/BDXCore) installed. Alternatively, you can use [Xenos](https://github.com/DarthTon/Xenos/releases/latest) to inject this plugin into BDS for loading, ``Type`` select ``New``, ``Process`` select ``bedrock_server. exe``, click the ``Add`` button and select ``BDSpyrunnerW.dll``, finally click the ``Inject`` button for start server and load plugin.
3. (Method 1) (Recommended) Download the one-click installation environment package from [here](https://pyr.jfishing.love/plugins/setup_pyrw_runtime.zip), unzip it to the server folder after downloading, your server folder should look roughly like this after the unzip is complete.
   ```Folder Structure
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
   Then double-click ``install_py_env.bat`` to install it. When the message ``Successfully install the Python runtime environment`` appears in the console, the environment has been installed. If not, please contact us and give us feedback on the problem.
   (Method 2) Download and install [Python 3.9.13](https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe), and check ``Add Python to Path`` when installing.
4. Put ``BDSpyrunnerW.dll`` and ``BDSpyrunnerW.pdb`` into the folder you use to store plugins, such as ``plugins``, ``bdxcore_mod``
5. Put ``mc.py`` into the ``plugins/py`` folder

### Available commands

* ``pyreload <module>``: hot reload (all) plugins

## Plugin list

[co↑co↓](plugins/README.md "here")

## Development Documentation

[Start reading](docs/README.md)
