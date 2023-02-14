import json
import threading

import mc

logger = mc.Logger(__name__)

config = {}
config['tax'] = 1 / 3
config['reset_time'] = 300
config['ban_time'] = 600

mc.make_conf("votekick", "votekick.json", config)
config = mc.read_conf("votekick", "votekick.json")
# 此处可调节票数与在线总玩家的比率，1 / 3 表示三分之一，即表示某玩家被投的票数达到当前在线总人数的三分之一时会被踢出。参考量:2 / 3(三分之二)  1 / 2(二分之一)
tax = config['tax']

#每次投票持续的时间，超过此时间还没有踢出玩家则重置投票数据，单位:秒
resetTime = config['reset_time']

#被踢出玩家禁止再次进入服务器的时间，相当于ban一段时间，单位:秒
banTime = config['ban_time']

#以下数据请勿修改
formid = 0
reportedNameList = []
reporterNameList = []
banNameList = []
label = False
#获取玩家列表

def getPlayerNameList():
    global totalPlayer, playerNameList, playerList
    playerList = []
    playerNameList = []
    playerList = mc.getPlayerList()
    for i in playerList:
            playerNameList.append(i.name)
    totalPlayer = len(playerNameList)

def onCmd(e):
    global reporter,formid
    if e['cmd'] == "/vklist":
        e['player'].sendTextPacket("已被投票的玩家:" + json.dumps(reportedNameList))
        return False
    if e['cmd'] == "/vk":
        getPlayerNameList()
        reporter = e['player']
        for i in reporterNameList:
            if i == reporter.name:
                reporter.sendTextPacket("您已投票，请等待下一次投票！")
                return False
        formid = reporter.sendCustomForm('{"content":[{"default":0,"options":'+json.dumps(playerNameList)+',"type":"dropdown","text":"请选择要投票的玩家"}],"type":"custom_form","title":"投票踢出"}')
        return False

def onSelect(e):
    if formid != e['formid']:
        return False
    elif e['selected'] == "null":
        return False
    #提醒玩家已投票
    reporter.sendTextPacket("投票成功！")
    reporterNameList.append(reporter.name)
    reporter.sendTextPacket("已投票玩家:" + json.dumps(reporterNameList))
    #设置标识，只允许第一个投票的玩家创建投票
    global label
    if label:
        return False
    global resetTime
    reporter.sendTextPacket("您已创建投票踢出，有效时长" + str(resetTime / 60) + "分钟！" )
    label = True
    #使用多线程延迟重置投票数据
    t = threading.Timer(resetTime, reportOver)
    t.setDaemon(True)
    t.start()

    selected = int(e['selected'][1:-1])
    reportedNameList.append(playerNameList[selected])
    mostAppearPlayerName = max(set(reportedNameList), key=reportedNameList.count)
    mostAppearPlayerNum = reportedNameList.count(mostAppearPlayerName)
    if mostAppearPlayerNum >= totalPlayer * tax and mostAppearPlayerNum >= 3:
        mc.runcmd("kick " + mostAppearPlayerName + " 您已被投票踢出，请等待" + str(banTime / 60) + "分钟后再进入服务器")
        #不知道为什么，这里tellraw用不了中文
        mc.runcmd('tellraw @a {\"rawtext\":[{\"text\":' + '\"VOTEKICK:' + mostAppearPlayerName + ' has been kick by report，the number of report:' + str(mostAppearPlayerNum) + '\"}]}')
        logger.info(f"{mostAppearPlayerName} 已经被投票踢出，票数: {str(mostAppearPlayerNum)}")
        banNameList.append(mostAppearPlayerName)
        #使用多线程延迟重置封禁数据
        t = threading.Timer(banTime, banOver)
        t.setDaemon(True)
        t.start()
        reportOver()

def ban(e):
    for playerName in banNameList:
        if e.name == playerName:
            mc.runcmd(f"kick {playerName} 您已被投票踢出，请等待 {str(banTime / 60)} 分钟后再进入服务器")
mc.setListener('onJoin',ban)

def banOver():
    banNameList.remove(banNameList[0])

def reportOver():
    global label,reporterNameList,reportedNameList
    label = False
    reporterNameList = []
    reportedNameList = []
    mc.runcmd('tellraw @a {"rawtext":[{"text":"VOTEKICK：上一轮的投票已结束！"}]}')
mc.setListener('onPlayerCmd', onCmd)
mc.setListener('onFormSelected', onSelect)
mc.setCommandDescription('vk', f'投票踢出，票数到达在线人数的{str(tax * 100)[0:3]}%%时将会踢出')
mc.setCommandDescription('vklist','已被投票的玩家')
logger.info("Loaded! Author: WillowSauceR")
