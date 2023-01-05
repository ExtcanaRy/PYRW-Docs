# chatlog

# 简介

隐藏离线玩家计分板的插件

# 下载

[这里](https://pyr.jfishing.love/plugins/BestScoreboard.py "点我下载")

# 配置文件

配置文件位于`plugins/py/BestScoreboard/Config.json`
'''json
{
    "Money": "money",    // 经济计分板
    "DisplayerScore": "displayermoney",        // 显示计分板名称
    "DisplayerName": "\u91d1\u5e01\u6392\u884c\u699c",         // 游戏内显示计分板名称
    "ScoreboardSet": true,            // 启动服务器时，显示本插件设置
    "Scoreboardsidebar": true,        // 为 右侧计分板
    "Scoreboardlist": true,           // 为 游戏暂停界面计分板
    "ScoreboardBelowname": true,     // 为 玩家头顶显示计分板
    "ScoreboardLog":true              // 控制台输出日志
    }
    // 由于 Pyr 中的 Json 文件不允许有注释
    // 请不要直接复制本描述代码
    // 配置文件会在第一次启动时生成
'''