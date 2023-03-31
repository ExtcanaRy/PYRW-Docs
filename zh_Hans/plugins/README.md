# 插件列表

这里收录了已适配 `BDSpyrunnerW` 的插件，所有的插件都应该放入`plugins/py/`文件夹进行加载

# 安装插件依赖

插件介绍页面中提到的依赖请您按照以下步骤安装：

注意：如果您使用教程中提到的方法一安装 Python 运行时环境，您应该在服务端目录下的`plugins/py/env/`文件夹打开终端，或保证工作目录位于此处。

1.打开您喜爱的终端，如 cmd 或 Powershell

2.[可选/一次性] 在国内使用 pip 官方源非常慢，这里推荐使用清华源来提升下载速度，键入

```shell
python.exe -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

3.[可选/一次性] 要升级您的 pip，键入

```shell
python.exe -m pip install --upgrade pip
```

4.安装依赖模块，键入 `python.exe -m pip install <依赖>`，如我要安装 `numpy`和 `chardet`依赖，则使用命令 `python.exe -m pip install numpy chardet`

# 下载插件

如果在点击下载链接后您的浏览器直接打开了该文件而不是下载。您可以在打开文件的页面`右键`，点击`另存为`来保存文件

# 插件列表

| 名称            | 描述                                         | 原作者  | 作者         | 详情                                  |
| --------------- | -------------------------------------------- | ------- | ------------ | ------------------------------------- |
| teleport        | 传送插件                                     | twoone3 | wsr          | [查看详情](teleport.md '这里')        |
| Backups         | 地图备份插件                                 | /       | wsr          | [查看详情](Backups.md '这里')         |
| Blockstatistics | 挖掘统计插件                                 | twoone3 | wsr          | [查看详情](Blockstatistics.md '这里') |
| ban             | 黑名单插件                                   | /       | wsr          | [查看详情](ban.md '这里')             |
| BehaviorLog     | 行为日志插件                                 | /       | wsr          | [查看详情](BehaviorLog.md '这里')     |
| pland           | 领地插件                                     | /       | 05007        | [查看详情](pland.md '这里')           |
| votekick        | 投票踢出插件                                 | /       | wsr          | [查看详情](votekick.md '这里')        |
| chatlog         | 行为日志简化版，仅控制台输出玩家聊天、指令等 | /       | wsr          | [查看详情](chatlog.md '这里')         |
| BestScoreBoard  | 隐藏离线玩家计分板的插件                     | /       | Moxiner      | [查看详情](BestScoreboard.md '这里')  |
| PyrWNbsPlayer   | 简易 NBS 音乐播放器                          | /       | student_2333 | [查看详情](pyrw-nbsplayer.md '这里')  |
