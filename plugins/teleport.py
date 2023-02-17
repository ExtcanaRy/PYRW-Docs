# -*- coding: utf-8 -*-
from cmath import exp, log
from webbrowser import get
import mc
import json
import time
import random
import threading


logger = mc.Logger(__name__)
conf_mgr = mc.ConfigManager(__name__)


home = {}  # key = xuid
warp = {}  # key = warpname
FormFn = {}  # 表单函数
FormIDs = []
tmp = {}  # key = player
tpaPlayerList = {"tpa": {"player1": "player2"}, "tpah": {"player1": "player2"}}
playerNameListForm = []  # 玩家列表(表单用)
playerList = []  # 玩家列表
MAX_HOME = 10
WAIT_TIME = 30
# tpr
LOCK_TIME = 300
TP_RANGE = 100000
PROCESS_TIME = 5
TP_HEIGH = 500
STEP_LENTH = 10
lockList = []  # tpr 锁定玩家列表


# 读取配置文件
def init():
    global home
    global warp
    global maxHome
    global waitTime
    # tpr
    global lockTime
    global tpRange
    global processTime
    global tpHeight
    global stepLenth

    j = {"config": {"maxHome": MAX_HOME, "waitTime": WAIT_TIME, "lockTime": LOCK_TIME, "tpRange": TP_RANGE, "processTime": PROCESS_TIME, "tpHeight": TP_HEIGH, "stepLenth": STEP_LENTH},
         "home": home, "warp": warp}
    conf_mgr.make(j)
    j = conf_mgr.read()
    home = j['home']
    warp = j['warp']
    maxHome = j['config']['maxHome']
    waitTime = j['config']['waitTime']
    # tpr
    lockTime = j['config']['lockTime']
    tpRange = j['config']['tpRange']
    processTime = j['config']['processTime']
    tpHeight = j['config']['tpHeight']
    stepLenth = j['config']['stepLenth']


def save():
    j = {"config": {"maxHome": maxHome, "waitTime": waitTime, "lockTime": lockTime, "tpRange": tpRange, "processTime": processTime, "tpHeight": tpHeight, "stepLenth": stepLenth},
         "home": home, "warp": warp}
    conf_mgr.save(j)


def reset(player_name):
    global tpaPlayerList
    # logger.info("")
    # try:
    if True:
        # logger.info(str(tpaPlayerList.items()))
        # logger.info(player.name)
        if player_name in str(tpaPlayerList.items()):
            if player_name in tpaPlayerList["tpa"]:
                # logger.info("0")
                del(tpaPlayerList["tpa"][player_name])
            elif player_name in tpaPlayerList["tpah"]:
                # logger.info("1")
                del(tpaPlayerList["tpah"][player_name])
            else:
                try:
                    del(tpaPlayerList["tpa"][get_keys(
                        tpaPlayerList["tpa"], player_name)[0]])
                except:
                    del(tpaPlayerList["tpah"][get_keys(
                        tpaPlayerList["tpah"], player_name)[0]])
            # logger.info(str(tpaPlayerList.items()))


# 传送
def tp(n1, n2):
    player1 = getPlayer(n1)
    player2 = getPlayer(n2)
    p2 = player2.pos
    did2 = player2.did
    player1.teleport(p2[0], p2[1]-1.62, p2[2], did2)


# tpa回调
def tpafn(player, selected, id):
    global tpaPlayerList
    global FormIDs
    player2 = playerList[int(selected)]
    # if player == player2:
    #	player.sendTextPacket('§c不能选择自己!')
    #	return False
    tpaPlayerList["tpa"][player.name] = player2.name  # player to player2
    player.sendTextPacket(f'§e你 向 {player2.name} 发起了一个tpa请求')
    player2.sendTextPacket(
        f'§e {player.name} 向 你 发起了一个tpa请求。使用 /tpac 接受，/tpad 拒绝')
    formid = player2.sendModalForm(
        "传送", f' {player.name} 向 你 发起了一个tpa请求', "同意", "拒绝")
    FormIDs.append(formid)
    #t1 = threading.Timer(30, timeout1)
    t1 = threading.Thread(target=timeout, args=(player,))
    t1.setDaemon(True)
    t1.start()


# tpahere回调
def tpaherefn(player, selected, id):
    global tpaPlayerList
    global FormIDs
    player2 = playerList[int(selected)]
    # if player == player2:
    #	player.sendTextPacket('§c不能选择自己!')
    #	return False
    tpaPlayerList["tpah"][player2.name] = player.name  # player to player2
    player.sendTextPacket(f'§e你 向 {player2.name} 发起了一个tpahere请求')
    player2.sendTextPacket(
        f'§e {player.name} 向 你 发起了一个tpahere请求。使用 /tpac 接受，/tpad 拒绝')
    formid = player2.sendModalForm(
        "传送", f' {player.name} 向 你 发起了一个tpahere请求', "同意", "拒绝")
    FormIDs.append(formid)
    t2 = threading.Thread(target=timeout, args=(player,))
    t2.setDaemon(True)
    t2.start()


# 通过字典的 值 返回 键
def get_keys(dict, value):
    #print([key for key,v in dict.items() if v == value])
    return [key for key, v in dict.items() if v == value]


# tpa/tpah超时
def timeout(player):
    player_name = player.name
    time.sleep(waitTime)
    if is_online(player_name):
        if player_name in str(tpaPlayerList.items()):
            reset(player_name)
            player.sendTextPacket('§c请求超时')
    else:
        reset(player_name)


# home tp and home del回调
def homefn(player, selected, id):
    xuid = player.xuid
    x = eval(selected)
    hname = list(home[xuid])[x[0]]
    mode = x[1]
    if hname == '':
        player.sendTextPacket('§c名字不能为空!')
        return False
    if mode == 0:  # 传送
        if not hname in home[xuid]:
            player.sendTextPacket('§c没有这个家!')
            reset(player.name)
            return False
        pos = home[xuid][hname]
        t5 = threading.Thread(target=tpdim, args=(player, pos))
        t5.setDaemon(True)
        t5.start()
        player.sendTextPacket('§a已传送到 ' + hname)
        reset(player.name)
    elif mode == 1:  # 删除
        if not hname in home[xuid]:
            player.sendTextPacket('§c没有这个家!')
            reset(player.name)
            return False
        del home[xuid][hname]
        player.sendTextPacket('§a删除家 ' + hname + ' 成功')
        reset(player.name)
        save()
    return False

# home del 回调


def homeNew(player, selected, id):
    xuid = player.xuid
    x = eval(selected)
    hname = x[0]
    if len(home[xuid]) >= maxHome:
        player.sendTextPacket('§c家的数量已达到上限!最多为' + str(maxHome) + "!")
        reset(player.name)
        return False
    if hname in home[xuid]:
        player.sendTextPacket('§c已经有这个家!')
        reset(player.name)
        return False
    x = player.pos[0]
    y = player.pos[1]
    z = player.pos[2]
    d = player.did
    home[xuid][hname] = [x, y, z, d]
    player.sendTextPacket('§a创建家 ' + hname + ' 成功')
    reset(player.name)
    save()

# warp回调


def warpfn(player, selected, id):
    x = eval(selected)
    wname = x[0]
    mode = x[1]
    if wname == '':
        player.sendTextPacket('§c名字不能为空!')
        return False
    if mode == 0:  # 传送
        if not wname in warp:
            player.sendTextPacket('§c没有这个传送点!')
            reset(player.name)
            return False
        pos = warp[wname]
        t6 = threading.Thread(target=tpdim, args=(player, pos))
        t6.setDaemon(True)
        t6.start()
        player.sendTextPacket('§a已传送到 ' + wname)
        reset(player.name)
    elif mode == 1:  # 创建
        if wname in warp:
            player.sendTextPacket('§c已经有这个传送点!')
            reset(player.name)
            return False
        if player.perm == 0:
            player.sendTextPacket('§c你没有权限操作!')
            reset(player.name)
            return False
        x = player.pos[0]
        y = player.pos[1]
        z = player.pos[2]
        d = player.did
        warp[wname] = [x, y, z, d]
        player.sendTextPacket('§a创建传送点 ' + wname + ' 成功')
        reset(player.name)
        save()
    elif mode == 2:  # 删除
        if not wname in warp:
            player.sendTextPacket('§c没有这个家!')
            reset(player.name)
            return False
        if player.perm == 0:
            player.sendTextPacket('§c你没有权限操作!')
            reset(player.name)
            return False
        del warp[wname]
        player.sendTextPacket('§a删除传送点 ' + wname + ' 成功')
        reset(player.name)
        save()
    return False

# 在tpr中延时移除玩家的锁


def rmLock():
    time.sleep(lockTime)
    lockList.remove(lockList[0])

# 在tpr中计算地面最高点并tp


def tpToLand(x, z, did, player):
    time.sleep(processTime)
    # stepLenth为步长，也就是每隔【stepLenth - 1】个方块检测一次，从200格向下遍历方块，直到获取的方块不是空气是将玩家传送到该方块+stepLenth格处
    for y in range(200, -1, -stepLenth):
        player.teleport(x, 256, z, did)
        if mc.getBlock(x, y, z, did)['blockname'][10:] != "air":
            player.teleport(x, y + stepLenth, z, did)
            player.sendTextPacket("§a已将您传送至:" + str(x) +
                                  ", " + str(y + stepLenth) + ", " + str(z))
            break


# 获取玩家列表
def getPlayerNameList():
    global playerNameListForm
    global playerList
    playerNameListForm = []
    playerList = []
    for i in mc.getPlayerList():
        playerNameListForm.append({'text': i.name})
        playerList.append(i)


# 根据名字获取玩家指针
def getPlayer(playerName: str):
    for player in mc.getPlayerList():
        if player.name == playerName:
            return player


def is_online(player_name: str):
    if getPlayer(player_name):
        return True
    else:
        return False


# 输入命令
def command(e):
    global isTpaLock
    global tpaPlayerList
    player = e['player']
    xuid = player.xuid
    # tpa
    if e['cmd'] == '/tpa' or e['cmd'] == "/me tpa":
        if player.name in tpaPlayerList["tpa"]:
            player.sendTextPacket('§c你已经有一个待处理的传送请求')
            return False
        getPlayerNameList()
        formid = player.sendSimpleForm('tpa', '', json.dumps(
            playerNameListForm, ensure_ascii=False))
        FormFn[formid] = tpafn
        return False
    # tpahere
    elif e['cmd'] == '/tpah' or e['cmd'] == "/me tpah":
        if player.name in str(tpaPlayerList["tpah"].values()):
            player.sendTextPacket('§c你已经有一个待处理的传送请求')
            return False
        getPlayerNameList()
        formid = player.sendSimpleForm('tpahere', '', json.dumps(
            playerNameListForm, ensure_ascii=False))
        FormFn[formid] = tpaherefn
        return False
    # 同意
    # elif e['cmd'] == '/tpaccept':
    elif e['cmd'] == '/tpac':
        tpacFn(player)
        return False
    # 拒绝
    # elif e['cmd'] == '/tpdeny':
    elif e['cmd'] == '/tpad':
        tpadFn(player)
        return False

    # home new
    elif e['cmd'] == '/homenew':
        if tmp[player.name][1] == 'home':
            player.sendTextPacket('§c错误!没有清除数据!')
            return False
        if not xuid in home:
            home[xuid] = {}
        homes = []
        for n in home[xuid]:
            homes.append(n)
        formid = player.sendCustomForm('{"content":[{"placeholder":"家的名字","default":"","type":"input","text":"' + '你目前的家:' + str(
            homes) + '"}], "type":"custom_form","title":"home"}')
        FormFn[formid] = homeNew
        return False
    # home tp and home del
    elif e['cmd'] == '/home':
        if tmp[player.name][1] == 'home':
            player.sendTextPacket('§c错误!没有清除数据!')
            return False
        if not xuid in home:
            home[xuid] = {}
        homes = []
        for n in home[xuid]:
            homes.append(n)
        if homes == []:
            player.sendTextPacket('§c您没有家，请使用指令 “/homenew” 创建一个!')
        else:
            formid = player.sendCustomForm('{"content": [{"default": 0,"options":' + json.dumps(
                homes) + ',"type": "dropdown","text": "请选择您的家"},{"default": 0,"options": ["§e传送","§c删除"],"type": "dropdown","text": "模式"}],"type": "custom_form","title": "home"}')
            FormFn[formid] = homefn
        return False
    # warp
    elif e['cmd'] == '/warp':
        if tmp[player.name][1] == 'warp':
            player.sendTextPacket('§c错误!没有清除数据!')
            return False
        warps = []
        for n in warp:
            warps.append(n)
        formid = player.sendCustomForm('{"content":[{"placeholder":"传送点的名字","default":"","type":"input","text":"' + '可用的传送点:' + str(
            warps) + '"},{"default":0,"options":["§e传送","§a创建","§c删除"],"type":"dropdown","text":"mode"}], "type":"custom_form","title":"warp"}')
        FormFn[formid] = warpfn
        return False
    # back
    elif e['cmd'] == '/back':
        if 'die' in tmp[player.name]:
            pos = tmp[player.name]['die']
            t7 = threading.Thread(target=tpdim, args=(player, pos))
            t7.setDaemon(True)
            t7.start()
            del tmp[player.name]['die']
            player.sendTextPacket('§a传送成功')
        else:
            player.sendTextPacket('§c没有可用的死亡点')
        return False

    # tpr
    elif e['cmd'] == "/tpr":
        player = e['player']
        did = player.did
        if did != 0:
            player.sendTextPacket("§c 您只能在主世界使用此命令")
            return False
        for name in lockList:
            if player.name == name:
                player.sendTextPacket("§c 命令冷却中，请等待" + str(lockTime) + "秒再试")
                return False
    # 给玩家加锁，防止短时间内重复执行卡服
        lockList.append(player.name)
        x = random.randint(-tpRange, tpRange)
        z = random.randint(-tpRange, tpRange)
        player.teleport(x, tpHeight, z, did)
    # 设置多线程进一步处理传送
        t3 = threading.Thread(target=tpToLand, args=(x, z, did, player))
        t3.setDaemon(True)
        t3.start()
    # 延时删除对玩家添加的锁
        t4 = threading.Thread(target=rmLock)
        t4.setDaemon(True)
        t4.start()
        return False


def tpdim(player, pos):
    player.teleport(pos[0], 1000, pos[2], pos[3])
    time.sleep(5)
    return player.teleport(pos[0], pos[1], pos[2], pos[3])


def tpacFn(player):
    # 被tpa者同意{player: 请求者, player2: 接受者}
    if player.name in str(tpaPlayerList["tpa"].values()):
        player2 = getPlayer(get_keys(tpaPlayerList['tpa'], player.name)[0])
        tp(player2.name, player.name)
        player2.sendTextPacket('§a' + player.name + ' 同意了 你 的请求')
        player.sendTextPacket('§a你 同意了 ' + player2.name + ' 的请求')
        reset(player.name)
    # 被tpah者同意{player: 接受者, player2: 请求者}
    elif player.name in tpaPlayerList["tpah"]:
        player2 = getPlayer(tpaPlayerList['tpah'][player.name])
        tp(player.name, player2.name)
        player2.sendTextPacket('§a' + player.name + ' 同意了 你 的请求')
        player.sendTextPacket('§a你 同意了 ' + player2.name + ' 的请求')
        reset(player.name)
    else:
        player.sendTextPacket('§e你没有待处理的传送请求')


def tpadFn(player):
    # 被tpa者拒绝{player: 请求者, player2: 接受者}
    if player.name in str(tpaPlayerList["tpa"].values()):
        player2 = getPlayer(get_keys(tpaPlayerList['tpa'], player.name)[0])
        player2.sendTextPacket('§e' + player.name + ' 拒绝了 你 的请求')
        player.sendTextPacket('§e你 拒绝了 ' + player2.name + ' 的请求')
        reset(player.name)
    # 被tpah者拒绝{player: 接受者, player2: 请求者}
    elif player.name in tpaPlayerList["tpah"]:
        player2 = getPlayer(tpaPlayerList['tpah'][player.name])
        player2.sendTextPacket('§e' + player.name + ' 拒绝了 你 的请求')
        player.sendTextPacket('§e你 拒绝了 ' + player2.name + ' 的请求')
        reset(player.name)
    else:
        player.sendTextPacket('§e你没有待处理的传送请求')


mc.setListener('onInputCommand', command)


def selectForm(e):
    id = e['formid']
    if e['selected'] == 'null':
        return False
    if id in FormIDs and e['selected'] == "true":
        tpacFn(e["player"])
    elif id in FormIDs and e['selected'] == "false":
        tpadFn(e["player"])

    if id in FormFn:
        try:
            # FormFn[id](e['player'], e['selected'], id)
            FormFn[id](e['player'], e['selected'], id)
            del FormFn[id]
        except:
            FormFn[id](e['player'], e['selected'],  id)
            del FormFn[id]


mc.setListener('onSelectForm', selectForm)
# 后台输入


def cmdinput(e):
    if e == 'tpreload':
        init()
        return False
    return True


mc.setListener('onConsoleInput', cmdinput)


def join(e):
    getPlayerNameList()
    tmp[e.name] = {0: 0, 1: 0, 2: 0}


mc.setListener('onPlayerJoin', join)


def left(e):
    getPlayerNameList()
    try:
        del tmp[e.name]
    except:
        pass


mc.setListener('onPlayerLeft', left)


def mobdie(e):
    actor = e['actor1']
    if actor in mc.getPlayerList():
        pos = actor.pos
        tmp[actor.name]['die'] = [pos[0], pos[1], pos[2], actor.did]
        actor.sendTextPacket('§e输入/back即可返回重生点')


mc.setListener('onMobDie', mobdie)
mc.setCommandDescription('tpa', 'tpa界面')
mc.setCommandDescription('tpah', 'tpahere界面')
mc.setCommandDescription('tpac', '接受传送请求')
#mc.setCommandDescription('tpaccept', '接受传送请求')
mc.setCommandDescription('tpad', '拒绝传送请求')
#mc.setCommandDescription('tpdeny', '拒绝传送请求')
mc.setCommandDescription('home', 'home界面')
mc.setCommandDescription('homenew', '新建home界面')
# mc.setCommandDescription('homedel', '删除home界面')
mc.setCommandDescription('warp', 'warp界面')
mc.setCommandDescription('back', '返回上一次死亡点')
mc.setCommandDescription(
    'tpr', '随机传送 —— 目前该功能不稳定，可能会出现失败或崩服情况，使用前请练习落地水！失败后果自负！')
init()
logger.info("Loaded!")
