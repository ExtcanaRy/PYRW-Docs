import mc
import time

logger = mc.Logger(__name__)
conf_mgr = mc.ConfigManager(__name__)

banData = {}


def init():
    global banData
    conf_mgr.make()
    banData = conf_mgr.read()


def onPlayerJoin(player):
    if player.name.lower() in str(banData.keys()).lower() or player.xuid in str(banData.values()):
        bannedTime = banData[player.name.lower()]["info"][-1].split()[0]
        banTime = banData[player.name.lower()]["info"][-1].split()[1]
        if not compareTime(bannedTime, banTime):
            if "." in banTime:
                msg = f"until {banTime}"
            elif banTime == "forever":
                msg = "forever"
            else:
                msg = f"for {banTime} seconds"
            player.disconnect(
                f"You are banned {msg}!\nBanned time: {bannedTime}\nReason: {banData[player.name.lower()]['info'][-1].split()[-1]}")


def onPlayerCmd(data):
    cmd = data['cmd'].split()
    admin = data['player']
    playerXuid = "unknown"
    playerIP = "unknown"
    if cmd[0] == "/ban" or cmd[0] == "/unban":
        if admin.perm < 2 and admin.name != cmd[1]:
            admin.sendTextPacket("你不是管理员！")
            return False
        if len(cmd) == 1:
            if cmd[0] == "/unban":
                admin.sendTextPacket("用法: /unban <玩家名>")
            elif cmd[0] == "/ban":
                admin.sendTextPacket(
                    "用法: /ban <玩家名> <时间: 秒数或形如2022.04.01-11.45.14的具体时间, 不填为永久> <原因:选填>")
            return False
        cmd[1] = cmd[1].replace("\"","")
        for player in mc.getPlayerList():
            if player.name == cmd[1]:
                playerXuid = player.xuid
                playerIP = player.IP
                player.disconnect("")
        if cmd[0] == "/unban":
            addBanPlayer(cmd[1], playerXuid, playerIP, time="unban")
            saveBanList()
            admin.sendTextPacket("已解封")
            return False
        elif len(cmd) == 2:
            addBanPlayer(cmd[1], playerXuid, playerIP)
        elif len(cmd) == 3:
            addBanPlayer(cmd[1], playerXuid, playerIP, cmd[2])
        elif len(cmd) == 4:
            addBanPlayer(cmd[1], playerXuid, playerIP, cmd[2], cmd[3])
        saveBanList()
        admin.sendTextPacket("玩家已被封禁")
        return False


def onConsoleCmd(data):
    if len(data) == 0:
        return True
    cmd = data.split()
    playerXuid = "unknown"
    playerIP = "unknown"
    if cmd[0] == "ban" or cmd[0] == "unban":
        if len(cmd) == 1:
            if cmd[0] == "unban":
                logger.error("用法: unban <玩家名>")
            if cmd[0] == "ban":
                logger.error("用法: ban <玩家名> <时间: 秒数或形如2022.04.01-11.45.14的具体时间, 不填为永久> <原因:选填>")
            return False
        cmd[1] = cmd[1].replace("\"","")
        for player in mc.getPlayerList():
            if player.name == cmd[1]:
                playerXuid = player.xuid
                playerIP = player.IP
                player.disconnect("")
        if cmd[0] == "unban":
            addBanPlayer(cmd[1], playerXuid, playerIP, time="unban")
            saveBanList()
            logger.info("已解封")
            return False
        elif len(cmd) == 2:
            addBanPlayer(cmd[1], playerXuid, playerIP)
        elif len(cmd) == 3:
            addBanPlayer(cmd[1], playerXuid, playerIP, cmd[2])
        elif len(cmd) == 4:
            addBanPlayer(cmd[1], playerXuid, playerIP, cmd[2], cmd[3])
        saveBanList()
        logger.info("玩家已被封禁")
        return False


def addBanPlayer(playerName, xuid="unknown", IP="unknown", time="forever", reason="unknown"):
    global banData
    if playerName.lower() in banData:
        banData[playerName.lower()]["info"].append(
            f'{getTime()} {time} {IP} {reason}')
    else:
        banData.update({playerName.lower(): {'info': [
                       f'{getTime()} {time} {IP} {reason}'], 'name': playerName, 'xuid': xuid}})


def saveBanList():
    conf_mgr.save(banData)


def compareTime(bannedTime, banTime: int):
    if banTime == "unban":
        return True
    if banTime == "forever":
        return False
    nowTime = getTime()
    if "." in banTime:
        nowTime = nowTime.replace(".", "").replace("-", "")
        banTime = banTime.replace(".", "").replace("-", "")
        for i in range(len(banTime)):
            if int(nowTime[i]) < int(banTime[i]):
                return False
    else:
        if toSecond(nowTime) - toSecond(bannedTime) < int(banTime):
            return False
    return True


def toSecond(banTime):
    banTime = banTime.replace("-", ".").split(".")
    intBanTime = []
    for i in banTime:
        intBanTime.append(int(i))
    seconds = intBanTime[0] * 365 * 24 * 60 * 60 + intBanTime[1] * 30 * 24 * 60 * 60 + \
        intBanTime[2] * 24 * 60 * 60 + intBanTime[3] * \
        60 * 60 + intBanTime[4] * 60 + intBanTime[5]
    return seconds


def getTime():
    return time.strftime('%Y.%m.%d-%H.%M.%S')


init()

mc.setListener('onPlayerJoin', onPlayerJoin)
mc.setListener('onPlayerCmd', onPlayerCmd)
mc.setListener('onConsoleCmd', onConsoleCmd)
mc.setCommandDescription(
    'ban', '/ban <玩家名> <时间: 秒数或形如2022.04.01-11.45.14的具体时间, 不填为永久> <原因:选填>')
mc.setCommandDescription('unban', '/unban <玩家名>')
