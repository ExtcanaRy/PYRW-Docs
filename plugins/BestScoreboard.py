# 此插件是实现去除离线玩家排行榜，感谢柳姐姐（@WillowSauceR）的帮助与指导！版本： 1.2（正式版）
import mc
import os

# ===================================配置文件构成=====================================================
# 如果您需要更改配置，请到配置文件里更改！
# 配置文件在 ./plugins/py/BestScoreboard 中
ConfigName = "BestScoreboard"
Version = "1.4"
Config = {}
Config['Money'] = "money"
Config["DisplayerName"] = "金币排行榜"
Config['DisplayerScore'] = "displaymoney"
Config['ScoreboardSet'] = True
Config['Scoreboardsidebar'] = True
Config['Scoreboardlist'] = True
Config['ScoreboardBelowname'] = True
Config["ScoreboardLog"]  = True



# ====================================代码部分======================================================
# 以下内容为代码部分，萌新切勿修改
# 插件主要类
class Log:
    def logout(*content, name: str = __name__, level: str = "INFO", info: str = ""):
        mc.log(content, name=name, level=level, info=info)

class master:
    def CreateScroe(e):
        '''
        创建必要计分板
        e:MC类属性
        '''
        mc.runcmd(
            f"scoreboard objectives add {Config['Money']} dummy {Config['DisplayerName']}")
        mc.runcmd(
            f"scoreboard objectives add {Config['DisplayerScore']} dummy {Config['DisplayerName']}")
        master.SetDisplay()

    def SetDisplay():
        '''设置显示计分板模式'''
        if Config['Scoreboardsidebar']:
            mc.runcmd(
                f"scoreboard objectives setdisplay sidebar {Config['DisplayerScore']}")
            if Config['ScoreboardSet']:
                Log.logout("右侧计分板 [开启]")
        else:
            mc.runcmd(f"scoreboard objectives setdisplay sidebar")
            if Config['ScoreboardSet']:
                Log.logout("右侧计分板 [关闭]")
        if Config['Scoreboardlist']:
            mc.runcmd(
                f"scoreboard objectives setdisplay list {Config['DisplayerScore']}")
            if Config['ScoreboardSet']:
                Log.logout("暂停界面计分板 [开启]")
        else:
            mc.runcmd(f"scoreboard objectives setdisplay list")
            if Config['ScoreboardSet']:
                Log.logout("暂停界面计分板 [关闭]")
        if Config['ScoreboardBelowname']:
            mc.runcmd(
                f"scoreboard objectives setdisplay belowname {Config['DisplayerScore']}")
            if Config['ScoreboardSet']:
                Log.logout("人物头部计分板 [开启]")
        else:
            mc.runcmd(f"scoreboard objectives setdisplay belowname")
            if Config['ScoreboardSet']:
                Log.logout("人物头部计分板 [关闭]")
        if Config["ScoreboardLog"]:
            Log.logout("BestScoreBord控制台日志输出 [开启]")
        else:
            Log.logout("BestScoreBord控制台日志输出 [关闭]")



    def ChangeScore(e):
        '''
        刷新计分板
        e:MC类属性
        '''
        if e["objectivename"] == Config['Money']:
            mc.runcmd(f"scoreboard players operation @a {Config['DisplayerScore']} = @a {Config['Money']}")

    def DisplayerScore(e):
        '''
        显示计分板
        e:MC类属性
        '''
        player = e
        mc.runcmd(f"scoreboard players operation @a {Config['DisplayerScore']} = @a {Config['Money']}")
        if Config["ScoreboardLog"]:
            Log.logout(f"已显示玩家 {player.name} 的计分板")

    def HiddenScore(e):
        '''
        隐藏计分板
        e:MC类属性
        '''
        player = e
        mc.runcmd(
            f"scoreboard players reset {player} {Config['DisplayerScore']}")
        if Config["ScoreboardLog"]:
            Log.logout(f"已隐藏玩家 {player} 的计分板")

    def HiddenConsoleLog(e):
        '''
        拦截不必要控制台输出
        e:MC类属性 
        '''
        RestNote = "Reset score displaymoney of player"
        SetNote = "Set [displaymoney]" 
        output = e[:-1]
        if output == f"Set the display objective in slot 'sidebar' to '{Config['DisplayerScore']}'":
            return False
        elif output == f"Set the display objective in slot 'belowname' to '{Config['DisplayerScore']}'":
            return False
        elif output == f"Set the display objective in slot 'list' to '{Config['DisplayerScore']}'":
            return False
        elif output == f"An objective with the name '{Config['Money']}' already exists":
            return False
        elif output == f"An objective with the name '{Config['DisplayerScore']}' already exists":
            return False
        elif output[:len(f"Reset score {Config['DisplayerScore']} of player")] == f"Reset score {Config['DisplayerScore']} of player":
            return False
        elif e[:len(RestNote)] == RestNote :
            return False
        elif e[:len(SetNote)] == SetNote :
            return False
        elif e[:27] == "No targets matched selector":
            return False
        elif e[:22] == "has no scores recorded":
            return False

# 初始化配置文件
if not os.path.exists(f"./plugins/py/{ConfigName}"):
    mc.make_conf(ConfigName, "Config.json", Config)
    Log.logout("未检测到配置文件，已重新生成" ,level="WARN")
config = mc.read_conf(ConfigName, "Config.json")

# 一堆监听器
mc.setListener("onScoreChanged", master.ChangeScore)
mc.setListener("onServerStarted", master.CreateScroe)
mc.setListener("onJoin", master.DisplayerScore)
mc.setListener("onLeft", master.HiddenScore)
mc.setListener("onConsoleOutput", master.HiddenConsoleLog)
# 控制台输出
Log.logout(f"已加载  {Version}")
Log.logout("作者：莫欣儿（Moxiner）")
