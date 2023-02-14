# 插件作者：05007
# 该页代码完全开源，允许应用到你的其他项目，但请注明出处
import mc
import landAPI as lapi
import json
import os
import sqlite3 as sq
import random


logger = mc.Logger(__name__)


debug_pc = {}  # 修复pc端多次打开表单
onlinePlayerList = []  # 在线玩家列表
NULL_SIGN = "无"
Bottom_information = "§e[landop]§b %player:§a %message\n§e[landname]§d %displayname"
# ===============================================================================


def loadsdata():
    global landconfig
    global scoreboard
    global land_world_open
    global land_nether_open
    global land_ender_open
    global land_2D_open
    global land_3D_open
    global land_2D_buy_money
    global land_2D_sell_money
    global land_3D_buy_money
    global land_3D_sell_money
    global land_maxnum
    global land_2D_maxsize
    global land_3D_maxsize
    global menu_itemname
    global playerbuyland
    global mobile_listener
    global around_place
    global land_teleport
    global Bottom_information
    global NULL_SIGN
    landconfig = lapi.getconfig()  # 获取领地的配置文件信息
    scoreboard = landconfig["scoreboard"]
    land_maxnum = landconfig["land_maxnum"]
    land_world_open = landconfig["land_world_open"]
    land_nether_open = landconfig["land_nether_open"]
    land_ender_open = landconfig["land_ender_open"]
    land_2D_open = landconfig["land_2D_open"]
    land_3D_open = landconfig["land_3D_open"]
    land_2D_buy_money = landconfig["land_2D_buy_money"]
    land_2D_sell_money = landconfig["land_2D_sell_money"]
    land_3D_buy_money = landconfig["land_3D_buy_money"]
    land_3D_sell_money = landconfig["land_3D_sell_money"]
    land_2D_maxsize = landconfig["land_2D_maxsize"]
    land_3D_maxsize = landconfig["land_3D_maxsize"]
    menu_itemname = landconfig["menu_itemname"]
    playerbuyland = landconfig["playerbuyland"]
    mobile_listener = landconfig["mobile_listener"]
    around_place = landconfig['around_place']
    land_teleport = landconfig['land_teleport']
    NULL_SIGN = lapi.get_null()
    Bottom_information = lapi.get_Bottom_information()


def landstart():
    lapi.landapistart()  # 启动领地核心引擎，必要！
    loadsdata()
    mc.setListener("onServerStarted", onServerStarted)
    mc.setListener('onFormSelected', onSelectForm)  # 统一的表单处理接口，勿修改
    mc.setListener('onJoin', onPlayerJoin)
    mc.setListener('onLeft', onPlayerLeft)
    mc.setListener('onConsoleCmd', onControlCmd)  # 使用控制台命令
    mc.setListener('onChangeDim', onChangeDim)  # 维度切换
    mc.setListener('onUseItem', onUseItem)  # 使用物品
    mc.setListener('onBlockInteracted', onBlockInteracted)  # 方块交互
    mc.setListener('onPlaceBlock', onPutBlock)  # 放置方块
    mc.setListener('onDestroyBlock', onDestroyBlock)  # 破坏方块
    mc.setListener('onMobHurt', onActorJury)  # 受伤
    mc.setListener('onPlayerAttack', onPlayerAttack)  # 攻击
    mc.setListener('onOpenContainer', onChestOpen)  # 开箱
    # mc.setListener('onOpenBarrel', onChestOpen) #开木桶
    mc.setListener('onLevelExplode', onWorldBoom)  # 爆炸
    mc.setListener('onFarmLandDecay', onFarmDestroy)  # 耕地
    mc.setListener('onUseRespawnAnchor', useRespawnAnchorBlock)  # 使用重生锚
    mc.setListener('onUseFrameBlock', onUseFrameBlock)  # 物品展示框
    mc.setListener('onMove', onPlayerMobile)
    mc.setCommandDescription(
        'pland', lapi.get_command_description("pland"), landhelp)
    mc.setCommandDescription(
        'pland q', lapi.get_command_description("pland q"), pland_q)
    mc.setCommandDescription(
        'pland 2a', lapi.get_command_description("pland 2a"), pland_2a)
    mc.setCommandDescription(
        'pland 2b', lapi.get_command_description("pland 2b"), pland_2b)
    mc.setCommandDescription(
        'pland 3a', lapi.get_command_description("pland 3a"), pland_3a)
    mc.setCommandDescription(
        'pland 3b', lapi.get_command_description("pland 3b"), pland_3b)
    mc.setCommandDescription(
        'plandremove', lapi.get_command_description("plandremove"), plandremove)
# =============语言工具====================================


def land_message(messagename):
    return lapi.get_message(messagename)


def gui_text(guiname):
    return lapi.get_gui_text(guiname)


def gui_image(guiname):
    return lapi.get_gui_image(guiname)


# =================表单工具==========================================================================
Formid = {}
Formdata = {}
# 将字符串转化为json对象


def stringtojson(data):
    jsondata = json.loads(data)
    return jsondata
# json对象转字符串


def jsontostring(data):
    data2 = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return data2


def addFormid(formid, BackFun, formdata):
    Formid[formid] = BackFun
    Formdata[formid] = formdata


def getFormid(formid, e):
    if e['formid'] in Formid:
        select = getselect(formid, e["selected"].replace('\n', ''))
        Formid[formid](e["player"], select["chooseid"], select["choosedata"])
        del Formid[formid]
# 发送表单,参数：玩家指针-json数据-返回时调用函数


def sendForm(player, jsondata, BackFun):
    formid = player.sendCustomForm(jsontostring(jsondata["form"]))
    if BackFun != "":
        addFormid(formid, BackFun, jsondata["formdata"])


def onSelectForm(e):
    debug_pc[e['player'].xuid] = True
    if e["selected"] != "null" and e["selected"] != "null\n":
        getFormid(e["formid"], e)
# 处理表单返回值


def getselect(formid, select2):
    try:
        formdata = Formdata[formid]
        del Formdata[formid]
    except:
        try:
            formdata = [[0] * int(select2)]
        except:
            formdata = [
                [0] * len(stringtojson("{\"select\":" + select2 + "}")["select"])]
    select = {}
    select["chooseid"] = []  # 选择的序号
    select["choosedata"] = []  # 选择的数据
    try:
        id = int(select2)
        select["chooseid"] = [id]
        select["choosedata"] = [formdata[id]]
    except:
        a = "{\"select\":" + select2 + "}"
        id = stringtojson(a)["select"]
        select["chooseid"] = id
        for i in range(len(stringtojson("{\"select\":" + select2 + "}")["select"])):
            try:
                select["choosedata"].append(formdata[i][id[i]])
            except:
                select["choosedata"].append(id[i])
    return select
# 创建简单表单


def createSmileForm(title, content):
    jv = {}
    jv["form"] = {}
    jv["form"]["type"] = "form"
    jv["form"]["title"] = title
    jv["form"]["content"] = content
    jv["form"]["buttons"] = []
    jv["formdata"] = []
    return jv
# 向简单表单添加按钮


def addbuttons(jv, buttonsname, image):
    jv2 = {}
    jv2["text"] = buttonsname
    if image != "":
        jv2["image"] = {}
        jv2["image"]["type"] = "path"
        jv2["image"]["data"] = image
    jv["form"]["buttons"].append(jv2)
    jv["formdata"].append(buttonsname)
    return jv
# 创建复杂表单


def createForm(title):
    jv = {}
    jv["form"] = {}
    jv["form"]["type"] = "custom_form"
    jv["form"]["title"] = title
    jv["form"]["content"] = []
    jv["formdata"] = []
    return jv
# 向表单添加下拉框options列表


def addDropdown(jv, title, options):
    jv2 = {}
    jv2["type"] = "dropdown"
    jv2["text"] = title
    if options == []:
        options = [NULL_SIGN]
    jv2["options"] = options
    jv["form"]["content"].append(jv2)
    jv["formdata"].append(options)
    return jv
# 添加一个开关


def addToggl(jv, title, default):
    jv2 = {}
    jv2["type"] = "toggle"
    jv2["text"] = title
    jv2["default"] = default
    jv["form"]["content"].append(jv2)
    jv["formdata"].append(title)
    return jv
# 添加一个滑块


def addSlider(jv, title, pmin, pmax, step, default):
    jv2 = {}
    jv2["type"] = "slider"
    jv2["text"] = title
    jv2["min"] = pmin
    jv2["max"] = pmax
    jv2["step"] = step
    jv2["default"] = default
    jv["form"]["content"].append(jv2)
    jv["formdata"].append(title)
    return jv
# 添加一个label


def addLabel(jv, text):
    jv2 = {}
    jv2["type"] = "label"
    jv2["text"] = text
    jv["form"]["content"].append(jv2)
    jv["formdata"].append(text)
    return jv
# 添加输入信息文本


def addInput(jv, title):
    jv2 = {}
    jv2["type"] = "input"
    jv2["text"] = title
    jv["form"]["content"].append(jv2)
    jv["formdata"].append(title)
    return jv
# 向表单添加在线玩家列表组件、显示玩家名称，返回是玩家指针


def addOnlinePlayerList(jv, title):
    c = []
    jv2 = {}
    jv2["type"] = "dropdown"
    jv2["text"] = title
    options = []
    for p in onlinePlayerList:
        try:
            options.append(p.name)
            c.append(p)
        except:
            pass
    if options == []:
        options = [NULL_SIGN]
    jv2["options"] = options
    jv["form"]["content"].append(jv2)
    jv["formdata"].append(c)
    return jv


def addPlayerLandList(jv, title, player):
    playerxuid = player.xuid
    playerworld = getplayerworld(player)
    playerlandall = lapi.getplayerland(playerxuid)
    c = []
    jv2 = {}
    jv2["type"] = "dropdown"
    jv2["text"] = title
    options = []
    for a in playerlandall[playerworld]:
        try:
            displayname = getland_displayname(a)
            options.append(displayname)
            c.append(a)
        except:
            pass
    if options == []:
        options = [NULL_SIGN]
        c = [NULL_SIGN]
    jv2["options"] = options
    jv["form"]["content"].append(jv2)
    jv["formdata"].append(c)
    return jv
# ====================经济部分===========================================
# ++++++++++++++++++++感谢huohua+++++++++++++++++++++++++++++++++++++++++++++++++
# 查询LLMoney玩家金钱


def Query_Money(Plxuid):
    conn = sq.connect('plugins/LLMoney/money.db',
                      timeout=5, check_same_thread=False)
    c = conn.cursor()
    cursor = c.execute("SELECT XUID, Money  from money")
    result = cursor.fetchall()
    rejson = {'code': 1, 'msg': 'Not found Player'}
    for i in result:
        if int.from_bytes(i[0], 'little') == int(Plxuid):
            rejson = {'code': 0, 'money': i[1]}
    return rejson
# ++++++++++++++++++++感谢huohua++++++++++++++++++++++++++++++++++++++++++++++


def getmoney(player):
    if scoreboard == "LLMoney":
        Player_Money_Dict = Query_Money(player.xuid)
        if Player_Money_Dict['code'] == 0:
            return Player_Money_Dict['money']
        elif Player_Money_Dict['code'] == 1:
            mc.runcmd('money set "'+player.name+'" 0')
            return 0
    else:
        return player.getScore(scoreboard)


def addmoney(player, num):
    if scoreboard == "LLMoney":
        mc.runcmd('money add "'+player.name+'" '+str(num))
    else:
        player.modifyScore(scoreboard, num, 1)


def removemoney(player, num):
    if getmoney(player) < num:
        return False
    if scoreboard == "LLMoney":
        mc.runcmd('money reduce "'+player.name+'" '+str(num))
    else:
        player.modifyScore(scoreboard, num, 2)
    return True
# ===================调用函数=============================================================
# 将世界ID转化为英文名称


def getworldname(worldid):
    if worldid == 1:
        worldname = "nether"
    elif worldid == 2:
        worldname = "ender"
    else:
        worldname = "world"
    return worldname


def getplayerworld(player):
    worldid = player.did
    return getworldname(worldid)
# 计算购买领地所需要的钱


def getneedbuymoney(pointA, pointB, Dim):
    global land_2D_buy_money
    global land_3D_buy_money
    x1 = pointA[0]
    y1 = pointA[1]
    z1 = pointA[2]
    x2 = pointB[0]
    y2 = pointB[1]
    z2 = pointB[2]
    if Dim == "3D":
        landsize = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1) * (abs(z1 - z2) + 1)
        if landsize <= land_3D_maxsize:
            money = landsize * land_3D_buy_money
        else:
            money = -1
    else:
        landsize = (abs(x1 - x2) + 1) * (abs(z1 - z2) + 1)
        if landsize <= land_2D_maxsize:
            money = landsize * land_2D_buy_money
        else:
            money = -1
    return [money, landsize]
# 计算出售领地所获得的钱


def getneedsellmoney(pointA, pointB, Dim):
    global land_2D_sell_money
    global land_3D_sell_money
    x1 = pointA[0]
    y1 = pointA[1]
    z1 = pointA[2]
    x2 = pointB[0]
    y2 = pointB[1]
    z2 = pointB[2]
    if Dim == "3D":
        money = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1) * \
            (abs(z1 - z2) + 1) * land_3D_sell_money
    else:
        money = (abs(x1 - x2) + 1) * (abs(z1 - z2) + 1) * land_2D_sell_money
    return money


# ====================表单部分=========================================================
playerbuy_2Dlandopen = {}
playerbuy_3Dlandopen = {}
playerchoosepointA = {}
playerbuylanddata = {}
setsharelandplayer = {}
setpowerlandplayer = {}
isonlineplayer = {}


def isonlineplayers(player):
    try:
        return isonlineplayer[player]
    except:
        return False


def getland_displayname(landname):
    displayname = lapi.getlandsign(landname, "displayname")
    if displayname == {}:
        return landname
    return displayname


def getland_leave_message(landname):
    message = lapi.getlandsign(landname, "message")
    if message == {}:
        return ""
    return message


def landsignhelpback(player, chooseid, choosedata):
    if choosedata[1] == NULL_SIGN:
        player.sendTextPacket(land_message("请先购买领地"))
        return
    if chooseid[0] == 0:
        displayname = str(chooseid[2])
        if displayname == "":
            player.sendTextPacket(land_message("请输入标识"))
            return
        if len(displayname) > 10:
            player.sendTextPacket(land_message("名称过长"))
        landname = choosedata[1]
        lapi.addlandsign(landname, "displayname", displayname)
        player.sendTextPacket(land_message("设置成功"))
    elif chooseid[0] == 1:
        landname = choosedata[1]
        if lapi.removelandsign(landname, "displayname"):
            player.sendTextPacket(land_message("移除成功"))
        else:
            player.sendTextPacket(land_message("移除失败"))
    elif chooseid[0] == 2:
        message = str(chooseid[2])
        if message == "":
            player.sendTextPacket(land_message("请输入标识"))
            return
        if len(message) > 20:
            player.sendTextPacket(land_message("留言过长"))
        landname = choosedata[1]
        lapi.addlandsign(landname, "message", message)
        player.sendTextPacket(land_message("设置成功"))
    elif chooseid[0] == 3:
        landname = choosedata[1]
        if lapi.removelandsign(landname, "message"):
            player.sendTextPacket(land_message("移除成功"))
        else:
            player.sendTextPacket(land_message("移除失败"))


def landsignhelp(player):
    jv = createForm(gui_text("设置标识"))
    addDropdown(jv, gui_text("选项"), [gui_text("设置展示名称"), gui_text(
        "移除展示名称"), gui_text("设置领地留言"), gui_text("移除领地留言")])
    playerworld = getplayerworld(player)
    addPlayerLandList(jv, gui_text("选择当前世界(%playerworld)的领地").replace(
        "%playerworld", playerworld), player)
    addInput(jv, gui_text("输入标识"))
    sendForm(player, jv, landsignhelpback)


def landhelpback(player, chooseid, choosedata):
    if chooseid[0] == 0:
        landbuyhelp(player)
    elif chooseid[0] == 1:
        mylandhelp(player)
    elif chooseid[0] == 2:
        sharelandhelp(player)
    elif chooseid[0] == 3:
        landsignhelp(player)
    elif chooseid[0] == 4:
        querylandhelp(player)


def landbuyhelpback(player, chooseid, choosedata):
    playerxuid = player.xuid
    if not playerbuyland and not lapi.islandop(playerxuid):
        player.sendTextPacket(land_message("只能由管理员购买领地"))
        return
    worldid = player.did
    if worldid == 1:
        if not land_nether_open:
            player.sendTextPacket(land_message("地狱未开启领地功能"))
            return
    elif worldid == 2:
        if not land_ender_open:
            player.sendTextPacket(land_message("末地未开启领地功能"))
            return
    else:
        if not land_world_open:
            player.sendTextPacket(land_message("主世界未开启领地功能"))
            return
    if chooseid[0] == 0:
        if land_2D_open:
            if land_3D_open:
                playerbuy_3Dlandopen[playerxuid] = False
            playerbuy_2Dlandopen[playerxuid] = True
            playerchoosepointA[playerxuid] = []
            player.sendTextPacket(land_message("开启二维领地购买功能"))
            player.sendTextPacket(land_message("放置方块选择点A"))
            player.sendTextPacket(land_message("破坏方块选择点B"))
            player.sendTextPacket(land_message("空手点击地面或使用命令/pland q退出领地选择模式"))
        else:
            player.sendTextPacket(land_message("未开启二维领地功能"))
    elif chooseid[0] == 1:
        if land_3D_open:
            if land_2D_open:
                playerbuy_2Dlandopen[playerxuid] = False
            playerbuy_3Dlandopen[playerxuid] = True
            playerchoosepointA[playerxuid] = []
            player.sendTextPacket(land_message("开启三维领地购买功能"))
            player.sendTextPacket(land_message("放置方块选择点A"))
            player.sendTextPacket(land_message("破坏方块选择点B"))
            player.sendTextPacket(land_message("空手点击地面或使用命令/pland q退出领地选择模式"))
        else:
            player.sendTextPacket(land_message("未开启三维领地功能"))


def landbuyhelp(player):
    jv = createSmileForm(gui_text("领地购买"), gui_text("选项"))
    addbuttons(jv, gui_text("购买二维领地"), gui_image("购买二维领地"))
    addbuttons(jv, gui_text("购买三维领地"), gui_image("购买三维领地"))
    sendForm(player, jv, landbuyhelpback)


def delshareplayer(player, chooseid, choosedata):
    playerxuid = player.xuid
    landname = setsharelandplayer[playerxuid]
    del setsharelandplayer[playerxuid]
    if choosedata[0] == NULL_SIGN or choosedata[0] == "":
        return
    shareplayerxuid = choosedata[0]
    shareplayername = lapi.getshareplayername(shareplayerxuid)
    lapi.setshareplayer(shareplayerxuid, shareplayername, landname, "del")
    player.sendTextPacket(land_message("取消分享") + shareplayername)


def setlandplayerpower(player, chooseid, choosedata):
    playerxuid = player.xuid
    landname = setpowerlandplayer[playerxuid]
    del setpowerlandplayer[playerxuid]
    lapi.setlandpower(landname, "attack", chooseid[0])
    lapi.setlandpower(landname, "share_attack", chooseid[1])
    lapi.setlandpower(landname, "useitem", chooseid[2])
    lapi.setlandpower(landname, "share_useitem", chooseid[3])
    lapi.setlandpower(landname, "openchest", chooseid[4])
    lapi.setlandpower(landname, "share_openchest", chooseid[5])
    lapi.setlandpower(landname, "putblock", chooseid[6])
    lapi.setlandpower(landname, "share_putblock", chooseid[7])
    lapi.setlandpower(landname, "destroyblock", chooseid[8])
    lapi.setlandpower(landname, "share_destroyblock", chooseid[9])
    player.sendTextPacket(land_message("设置成功"))


def mylandhelpback(player, chooseid, choosedata):
    #logger.info(choosedata[1])
    #logger.info(NULL_SIGN)
    if choosedata[1] == NULL_SIGN or choosedata[1] == "":
        return
    landname = choosedata[1]
    land = lapi.getlandinfo(landname)
    playerxuid = player.xuid
    if chooseid[0] == 0:
        shareplayerall = ""
        for shareplayerxuid in land["shareplayer"]:
            shareplayername = lapi.getshareplayername(shareplayerxuid)
            shareplayerall += "§3[" + shareplayername + "]"
        displayname = getland_displayname(landname)
        message = getland_leave_message(landname)
        player.sendTextPacket(land_message("领地名称") + displayname)
        player.sendTextPacket(land_message("领地范围") + landname)
        player.sendTextPacket(land_message("领地主人") +
                              lapi.getshareplayername(land["playerxuid"]))
        player.sendTextPacket(land_message("共享玩家") + shareplayerall)
        player.sendTextPacket(land_message("领地留言") + message)
    elif chooseid[0] == 1:
        if not land_teleport:
            player.sendTextPacket(land_message("没有开启领地传送功能"))
            return
        x = (land["x1"] + land["x2"]) / 2
        y = (land["y1"] + land["y2"]) / 2
        z = (land["z1"] + land["z2"]) / 2
        worldid = land["worldid"]
        player.teleport(x, y, z, worldid)
        player.sendTextPacket(land_message("传送成功"))
    elif chooseid[0] == 2:
        jv = createForm(gui_text("设置领地权限"))
        addToggl(jv, gui_text("攻击权限"), land["attack"])
        addToggl(jv, gui_text("攻击权限(共享玩家)"), land["share_attack"])
        addToggl(jv, gui_text("使用物品权限"), land["useitem"])
        addToggl(jv, gui_text("使用物品权限(共享玩家)"), land["share_useitem"])
        addToggl(jv, gui_text("开箱权限"), land["openchest"])
        addToggl(jv, gui_text("开箱权限(共享玩家)"), land["share_openchest"])
        addToggl(jv, gui_text("放置方块权限"), land["putblock"])
        addToggl(jv, gui_text("放置方块权限(共享玩家)"), land["share_putblock"])
        addToggl(jv, gui_text("破坏方块权限"), land["destroyblock"])
        addToggl(jv, gui_text("破坏方块权限(共享玩家)"), land["share_destroyblock"])
        setpowerlandplayer[playerxuid] = landname
        sendForm(player, jv, setlandplayerpower)
    elif chooseid[0] == 3:
        jv = createForm(gui_text("取消领地分享"))
        c = []
        jv2 = {}
        jv2["type"] = "dropdown"
        jv2["text"] = gui_text("选择已分享的玩家")
        options = []
        for shareplayerxuid in land["shareplayer"]:
            shareplayername = lapi.getshareplayername(shareplayerxuid)
            options.append(shareplayername)
            c.append(shareplayerxuid)
        if options == []:
            options = [NULL_SIGN]
        if c == []:
            c = [NULL_SIGN]
        jv2["options"] = options
        jv["form"]["content"].append(jv2)
        jv["formdata"].append(c)
        setsharelandplayer[playerxuid] = landname
        sendForm(player, jv, delshareplayer)
    elif chooseid[0] == 4:
        moneysell = getneedsellmoney([land["x1"], land["y1"], land["z1"]], [
                                     land["x2"], land["y2"], land["z2"]], land["Dim"])
        if lapi.removelanddata(landname):
            addmoney(player, moneysell)
            player.sendTextPacket(land_message("出售成功,获得金币") + str(moneysell))
        else:
            player.sendTextPacket(land_message("出售失败"))


def mylandhelp(player):
    jv = createForm(gui_text("我的领地"))
    addDropdown(jv, gui_text("选项"), [gui_text("领地信息"), gui_text(
        "传送至领地"), gui_text("设置领地权限"), gui_text("取消领地分享"), gui_text("出售领地")])
    playerworld = getplayerworld(player)
    addPlayerLandList(jv, gui_text("选择当前世界(%playerworld)的领地").replace(
        "%playerworld", playerworld), player)
    sendForm(player, jv, mylandhelpback)


def sharelandhelpback(player, chooseid, choosedata):
    if choosedata[2] == NULL_SIGN or choosedata[2] == "":
        return
    landname = choosedata[2]
    shareplayername = choosedata[1].name
    if chooseid[0] == 0:
        lapi.setshareplayer(choosedata[1].xuid,
                            shareplayername, landname, "add")
        player.sendTextPacket(land_message("成功将领地(%land),分享给玩家").replace(
            "%land", landname) + shareplayername)
    if chooseid[0] == 1:
        land = lapi.getlandinfo(landname)
        playerxuid = land["playerxuid"]
        x1 = land["x1"]
        y1 = land["y1"]
        z1 = land["z1"]
        x2 = land["x2"]
        y2 = land["y2"]
        z2 = land["z2"]
        worldid = land["worldid"]
        Dim = land["Dim"]
        lapi.removelanddata(landname)
        lapi.createlanddata(choosedata[1].xuid,
                            x1, y1, z1, x2, y2, z2, worldid, Dim)
        player.sendTextPacket(land_message("成功将领地(%land),赠送给玩家").replace(
            "%land", landname) + shareplayername)


def sharelandhelp(player):
    jv = createForm(gui_text("领地共享"))
    addDropdown(jv, gui_text("选项"), [gui_text("分享领地"), gui_text("赠送领地")])
    addOnlinePlayerList(jv, "选择玩家")
    playerworld = getplayerworld(player)
    addPlayerLandList(jv, gui_text("选择当前世界(%playerworld)的领地").replace(
        "%playerworld", playerworld), player)
    sendForm(player, jv, sharelandhelpback)


def querylandhelpback(player, chooseid, choosedata):
    #playerinfo = mc.getPlayerInfo(player)
    XYZ = player.pos
    if chooseid[0] == 0:
        landall = lapi.island(int(XYZ[0]), int(
            XYZ[1]), int(XYZ[2]), player.did)
        if landall == "noland":
            player.sendTextPacket(land_message("你脚下没有领地"))
            return
        else:
            land = lapi.getlandinfo(landall)
            shareplayerall = ""
            for shareplayerxuid in land["shareplayer"]:
                shareplayername = lapi.getshareplayername(shareplayerxuid)
                shareplayerall += "§3[" + shareplayername + "]"
            displaynamed = getland_displayname(landall)
            message = getland_leave_message(landall)
            player.sendTextPacket(land_message("领地名称") + displaynamed)
            player.sendTextPacket(land_message("领地范围") + landall)
            player.sendTextPacket(land_message(
                "领地主人") + lapi.getshareplayername(land["playerxuid"]))
            player.sendTextPacket(land_message("共享玩家") + shareplayerall)
            player.sendTextPacket(land_message("领地留言") + message)
    if chooseid[0] == 1:
        land_2D = lapi.getland_point(int(XYZ[0]), int(
            XYZ[1]), int(XYZ[2]), player.did, "2D")
        land_3D = lapi.getland_point(int(XYZ[0]), int(
            XYZ[1]), int(XYZ[2]), player.did, "3D")
        if land_2D == [] and land_3D == []:
            player.sendTextPacket(land_message("周围没有领地"))
            return
        player.sendTextPacket(land_message("获取周围领地"))
        for a in land_2D:
            player.sendTextPacket(land_message("二维领地") + a)
        for b in land_3D:
            player.sendTextPacket(land_message("三维领地") + b)


def querylandhelp(player):
    jv = createSmileForm(gui_text("领地查询"), gui_text("选项"))
    addbuttons(jv, gui_text("查询脚下领地"), gui_image("查询脚下领地"))
    addbuttons(jv, gui_text("查询周围领地"), gui_image("查询周围领地"))
    sendForm(player, jv, querylandhelpback)


def buylandback(player, chooseid, choosedata):
    playerxuid = player.xuid
    buylanddata = playerbuylanddata[playerxuid]
    del playerbuylanddata[playerxuid]
    if chooseid[0] == 0:
        needmoney = buylanddata["needmoney"]
        Dim = buylanddata["Dim"]
        if needmoney == -1:
            player.sendTextPacket(land_message("领地面积超出最大尺寸"))
            return
        if lapi.getplayerlandnum(playerxuid) >= land_maxnum:
            player.sendTextPacket(land_message("你拥有的领地已达最大值"))
            return
        playermoney = getmoney(player)
        if playermoney < needmoney:
            player.sendTextPacket(land_message("余额不足，购买失败"))
            return
        pointA = buylanddata["pointA"]
        pointB = buylanddata["pointB"]
        worldid = buylanddata["worldid"]
        x1 = pointA[0]
        y1 = pointA[1]
        z1 = pointA[2]
        x2 = pointB[0]
        y2 = pointB[1]
        z2 = pointB[2]
        landall = lapi.createlanddata(
            playerxuid, x1, y1, z1, x2, y2, z2, worldid, Dim)
        if landall["2D"] == [] and landall["3D"] == []:
            removemoney(player, needmoney)
            try:
                if playerbuy_2Dlandopen[playerxuid]:
                    playerbuy_2Dlandopen[playerxuid] = False
                    del playerchoosepointA[playerxuid]
            except:
                pass
            try:
                if playerbuy_3Dlandopen[playerxuid]:
                    playerbuy_3Dlandopen[playerxuid] = False
                    del playerchoosepointA[playerxuid]
            except:
                pass
            player.sendTextPacket(land_message("领地购买成功,花费") + str(needmoney))
        else:
            landall_2D = gui_text("重叠二维领地")
            landall_3D = gui_text("重叠三维领地")
            for a in landall["2D"]:
                landall_2D += f"§3{a}\n"
            for b in landall["3D"]:
                landall_3D += f"§3{b}\n"
            msg = gui_text("购买失败，领地重叠").replace(
                "%landall_2D", landall_2D).replace("%landall_3D", landall_3D)
            # "§9结果：§c购买失败，领地重叠。\n \n"+landall_2D+"\n \n"+landall_3D+"\n \n \n
            # \n"
            jv = createSmileForm(gui_text("领地购买"), msg)
            jv = addbuttons(jv, gui_text("确定"), gui_image("确定"))
            sendForm(player, jv, "")


def buyland(player, pointA, pointB, worldid, Dim):
    ab = getneedbuymoney(pointA, pointB, Dim)
    needmony = ab[0]
    playermoney = getmoney(player)
    playerxuid = player.xuid
    playerbuylanddata[playerxuid] = {}
    playerbuylanddata[playerxuid]["pointA"] = pointA
    playerbuylanddata[playerxuid]["pointB"] = pointB
    playerbuylanddata[playerxuid]["worldid"] = worldid
    playerbuylanddata[playerxuid]["Dim"] = Dim
    playerbuylanddata[playerxuid]["needmoney"] = needmony
    x1 = pointA[0]
    y1 = pointA[1]
    z1 = pointA[2]
    x2 = pointB[0]
    y2 = pointB[1]
    z2 = pointB[2]
    landname = f"{Dim}:{x1}.{y1}.{z1}:{x2}.{y2}.{z2}:{worldid}"
    msg = gui_text("购买领地信息提示").replace("%playermoney", str(playermoney)).replace(
        "%needmony", str(needmony)).replace("%landname", landname).replace("%ab", str(ab[1]))
    # "§9我的金币： §3"+str(playermoney)+"\n \n"+"§9购买领地需要金币：§3"+str(needmony)+"\n
    # \n"+"§9领地范围：§3"+landname+"\n \n"+"§9领地尺寸：§3"+str(ab[1])+"\n \n \n \n"
    jv = createSmileForm(gui_text("是否购买领地"), msg)
    jv = addbuttons(jv, gui_text("确定"), gui_image("确定"))
    jv = addbuttons(jv, gui_text("取消"), gui_image("取消"))
    sendForm(player, jv, buylandback)
# ==========================监听函数=========================================


def onUseItem(e):
    player = e["player"]
    playerxuid = player.xuid
    playerXYZ = e["position"]
    worldid = player.did
    itemname = e["itemname"]
    if itemname == menu_itemname and menu_itemname != "":
        if debug_pc[playerxuid]:
            landhelp(e["player"])
            debug_pc[playerxuid] = False
    if e["itemid"] == 0:
        if playerbuy_2Dlandopen[playerxuid]:
            playerbuy_2Dlandopen[playerxuid] = False
            playerchoosepointA[playerxuid] = []
            del playerchoosepointA[playerxuid]
            player.sendTextPacket(land_message("二维领地选择模式关闭"))
        if playerbuy_3Dlandopen[playerxuid]:
            playerbuy_3Dlandopen[playerxuid] = False
            playerchoosepointA[playerxuid] = []
            del playerchoosepointA[playerxuid]
            player.sendTextPacket(land_message("三维领地选择模式关闭"))
    if around_place:
        if itemname == "piston" or itemname == "sticky_piston":
            XYZ = player.pos
            x = int(XYZ[0])
            y = int(XYZ[1])
            z = int(XYZ[2])
            landall_2D = []
            landall_3D = []
            if land_2D_open:
                landall_2D = lapi.getland_point(x, y, z, worldid, "2D")
            if land_3D_open and landall_2D == []:
                landall_3D = lapi.getland_point(x, y, z, worldid, "3D")
            if landall_2D != [] or landall_3D != []:
                if lapi.island(int(playerXYZ[0]), int(playerXYZ[1]), int(playerXYZ[2]), worldid) == "noland":
                    for cc in landall_2D:
                        landinfo = lapi.getlandinfo(cc)
                        if playerxuid == landinfo["playerxuid"]:
                            return True
                    for dd in landall_3D:
                        landinfo = lapi.getlandinfo(dd)
                        if playerxuid == landinfo["playerxuid"]:
                            return True
                    player.sendTextPacket(land_message("领地周围禁止使用活塞"))
                    return False
        if itemname == "water_bucket" or itemname == "lava_bucket":
            XYZ = player.pos
            x = int(XYZ[0])
            y = int(XYZ[1])
            z = int(XYZ[2])
            landall_2D = []
            landall_3D = []
            if land_2D_open:
                landall_2D = lapi.getland_point(x, y, z, worldid, "2D")
            if land_3D_open and landall_2D == []:
                landall_3D = lapi.getland_point(x, y, z, worldid, "3D")
            if landall_2D != [] or landall_3D != []:
                if lapi.island(int(playerXYZ[0]), int(playerXYZ[1]), int(playerXYZ[2]), worldid) == "noland":
                    for cc in landall_2D:
                        landinfo = lapi.getlandinfo(cc)
                        if playerxuid == landinfo["playerxuid"]:
                            return True
                    for dd in landall_3D:
                        landinfo = lapi.getlandinfo(dd)
                        if playerxuid == landinfo["playerxuid"]:
                            return True
                    player.sendTextPacket(land_message("领地周围禁止使用水桶和岩浆"))
                    return False
    if not lapi.islandplayer(playerxuid, int(playerXYZ[0]), int(playerXYZ[1]), int(playerXYZ[2]), worldid, "useitem"):
        player.sendTextPacket(land_message("没有该领地使用物品权限"))
        return False
    return True


def onBlockInteracted(e):
    player = e["player"]
    playerxuid = player.xuid
    blockpos = e["blockpos"]
    x = int(blockpos[0])
    y = int(blockpos[1])
    z = int(blockpos[2])
    worldid = e["dimensionid"]
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "useitem"):
        player.sendTextPacket(land_message("没有该领地使用物品权限"))
        return False
    return True


def onPutBlock(e):
    player = e["player"]
    playerXYZ = e["position"]
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    playerxuid = player.xuid
    worldid = player.did
    try:
        if playerbuy_2Dlandopen[playerxuid]:
            pointA = [x, y, z]
            playerchoosepointA[playerxuid] = pointA
            player.sendTextPacket(land_message("成功选择点A") + f"{x}.{y}.{z}")
            player.sendTextPacket(land_message("破坏方块或使用命令/pland 2b选择点B"))
            player.sendTextPacket(land_message("空手点击地面或使用命令/pland q退出领地选择模式"))
            return False
    except:
        playerbuy_2Dlandopen[playerxuid] = False
    try:
        if playerbuy_3Dlandopen[playerxuid]:
            pointA = [x, y, z]
            playerchoosepointA[playerxuid] = pointA
            player.sendTextPacket(land_message("成功选择点A") + f"{x}.{y}.{z}")
            player.sendTextPacket(land_message("破坏方块或使用命令/pland 3b选择点B"))
            player.sendTextPacket(land_message("空手点击地面或使用命令/pland q退出领地选择模式"))
            return False
    except:
        playerbuy_3Dlandopen[playerxuid] = False
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "putblock"):
        player.sendTextPacket(land_message("没有该领地放置方块权限"))
        return False
    return True


def onDestroyBlock(e):
    player = e["player"]
    playerXYZ = e["position"]
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    playerxuid = player.xuid
    worldid = player.did
    try:
        if playerbuy_2Dlandopen[playerxuid]:
            pointB = [x, y, z]
            pointA = playerchoosepointA[playerxuid]
            if pointA == []:
                player.sendTextPacket("§e[land]§c请先选择点A")
                return False
            player.sendTextPacket(land_message("成功选择点B") + f"{x}.{y}.{z}")
            buyland(player, pointA, pointB, worldid, "2D")
            return False
    except:
        playerbuy_2Dlandopen[playerxuid] = False
    try:
        if playerbuy_3Dlandopen[playerxuid]:
            pointB = [x, y, z]
            pointA = playerchoosepointA[playerxuid]
            if pointA == []:
                player.sendTextPacket(land_message("请先选择点A"))
                return False
            player.sendTextPacket(land_message("成功选择点B") + f"{x}.{y}.{z}")
            buyland(player, pointA, pointB, worldid, "3D")
            return False
    except:
        playerbuy_3Dlandopen[playerxuid] = False
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "destroyblock"):
        player.sendTextPacket(land_message("没有该领地破坏方块权限"))
        return False
    return True


def onChestOpen(e):
    player = e["player"]
    playerxuid = player.xuid
    playerXYZ = e["position"]
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    worldid = player.did
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "openchest"):
        player.sendTextPacket(land_message("没有该领地打开容器权限"))
        return False
    return True


def onPlayerAttack(e):
    player = e["player"]
    playerxuid = player.xuid
    playerXYZ = e["actor"].pos
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    worldid = player.did
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "attack"):
        player.sendTextPacket(land_message("没有该领地攻击生物权限"))
        return False
    return True


def onActorJury(e):
    player = e["actor2"]
    if isonlineplayers(player):
        actor = e["actor1"]
        playerxuid = player.xuid
        playerXYZ = actor.pos
        x = int(playerXYZ[0])
        y = int(playerXYZ[1])
        z = int(playerXYZ[2])
        worldid = player.did
        if not lapi.islandplayer(playerxuid, x, y, z, worldid, "attack"):
            player.sendTextPacket(land_message("没有该领地攻击生物权限"))
            return False
    return True


def onUseFrameBlock(e):
    player = e["player"]
    playerxuid = player.xuid
    blockpos = e["blockpos"]
    x = int(blockpos[0])
    y = int(blockpos[1])
    z = int(blockpos[2])
    worldid = e["dimensionid"]
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "destroyblock"):
        player.sendTextPacket(land_message("没有该领地破坏方块权限"))
        return False
    return True


def onServerStarted(e):
    mc.runcmd("scoreboard objectives add money dummy money")


def onPlayerJoin(player):
    playerxuid = player.xuid
    playerbuy_2Dlandopen[playerxuid] = False
    playerbuy_3Dlandopen[playerxuid] = False
    playerchoosepointA[playerxuid] = []
    isonlineplayer[player] = True
    debug_pc[playerxuid] = True
    onlinePlayerList.append(player)
    lapi.addplayername(playerxuid, player.name)
    if scoreboard != "LLMoney":
        mc.runcmd(f"scoreboard players add {player.name} {scoreboard} 0")
    return True


def onPlayerLeft(player):
    try:
        playerxuid = player.xuid
        playerbuy_2Dlandopen[playerxuid] = False
        playerbuy_3Dlandopen[playerxuid] = False
        playerchoosepointA[playerxuid] = []
        debug_pc[playerxuid] = True
        del playerbuy_2Dlandopen[playerxuid]
        del playerbuy_3Dlandopen[playerxuid]
        del playerchoosepointA[playerxuid]
        del debug_pc[playerxuid]
        onlinePlayerList.remove(player)
    except:
        pass
    return True


def onChangeDim(player):
    playerxuid = player.xuid
    playerbuy_2Dlandopen[playerxuid] = False
    playerbuy_3Dlandopen[playerxuid] = False
    playerchoosepointA[playerxuid] = []
    del playerchoosepointA[playerxuid]
    return True


def onWorldBoom(e):
    XYZ = e["position"]
    worldid = e["dimensionid"]
    x = int(XYZ[0])
    y = int(XYZ[1])
    z = int(XYZ[2])
    landall_2D = []
    landall_3D = []
    if land_2D_open:
        landall_2D = lapi.getland_point(x, y, z, worldid, "2D")
    if land_3D_open and landall_2D == []:
        landall_3D = lapi.getland_point(x, y, z, worldid, "3D")
    if landall_2D != [] or landall_3D != []:
        return False
    return True


def onFarmDestroy(e):
    player = e["player"]
    playerxuid = e['player'].xuid
    XYZ = e["position"]
    x = int(XYZ[0])
    y = int(XYZ[1])
    z = int(XYZ[2])
    worldid = e["dimensionid"]
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "destroyblock"):
        player.sendTextPacket(land_message("没有该领地破坏方块权限"))
        return False
    return True


def useRespawnAnchorBlock(e):
    player = e["player"]
    playerxuid = e['player'].xuid
    XYZ = e["position"]
    worldid = e["dimensionid"]
    x = int(XYZ[0])
    y = int(XYZ[1])
    z = int(XYZ[2])
    landall_2D = []
    landall_3D = []
    if land_2D_open:
        landall_2D = lapi.getland_point(x, y, z, worldid, "2D")
    if land_3D_open and landall_2D == []:
        landall_3D = lapi.getland_point(x, y, z, worldid, "3D")
    if landall_2D != [] or landall_3D != []:
        if lapi.island(x, y, z, worldid) == "noland":
            for cc in landall_2D:
                landinfo = lapi.getlandinfo(cc)
                if playerxuid == landinfo["playerxuid"]:
                    return True
            for dd in landall_3D:
                landinfo = lapi.getlandinfo(dd)
                if playerxuid == landinfo["playerxuid"]:
                    return True
            player.sendTextPacket(land_message("领地周围禁止使用重生锚"))
            return False
    if not lapi.islandplayer(playerxuid, x, y, z, worldid, "useitem"):
        player.sendTextPacket(land_message("你没有该领地使用重生锚的权限"))
        return False
    return True


Mobiletick = {}


def onPlayerMobile(e):
    global mobile_listener
    if not mobile_listener:
        return True
    try:
        Mobiletick[e] += 1
        if Mobiletick[e] >= 25:
            pXYZ = e.pos
            x = int(pXYZ[0])
            y = int(pXYZ[1])
            z = int(pXYZ[2])
            worldid = e.did
            landname = lapi.island(x, y, z, worldid)
            if landname != "noland":
                landinfo = lapi.getlandinfo(landname)
                landplayer = lapi.getshareplayername(landinfo['playerxuid'])
                message = getland_leave_message(landname)
                displayname = getland_displayname(landname)
                msg = Bottom_information.replace("%player", landplayer).replace(
                    "%message", message).replace("%displayname", displayname)
                # msg="§e[landop]§b"+landplayer+":§a"+message+"\n§e[landname]§d"+displayname
                if random.randint(0, 1) == 0:
                    e.sendTextPacket(msg, 4)
            Mobiletick[e] = 0
    except:
        Mobiletick[e] = 0
    return True
# ======================================================================命令部分=============


def landhelp(player):
    worldid = player.did
    if worldid == 1:
        if not land_nether_open:
            player.sendTextPacket(land_message("地狱未开启领地功能"))
            return
    elif worldid == 2:
        if not land_ender_open:
            player.sendTextPacket(land_message("末地未开启领地功能"))
            return
    else:
        if not land_world_open:
            player.sendTextPacket(land_message("主世界未开启领地功能"))
            return
    jv = createSmileForm(gui_text("领地系统"), gui_text("选项"))
    addbuttons(jv, gui_text("购买领地"), gui_image("购买领地"))
    addbuttons(jv, gui_text("我的领地"), gui_image("我的领地"))
    addbuttons(jv, gui_text("领地共享"), gui_image("领地共享"))
    addbuttons(jv, gui_text("领地标识"), gui_image("领地标识"))
    addbuttons(jv, gui_text("领地查询"), gui_image("领地查询"))
    sendForm(player, jv, landhelpback)


def pland_2a(player):
    playerxuid = player.xuid
    playerXYZ = player.pos
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    if not playerbuyland and not lapi.islandop(playerxuid):
        player.sendTextPacket(land_message("只能由管理员购买领地"))
        return
    worldid = player.did
    if worldid == 1:
        if not land_nether_open:
            player.sendTextPacket(land_message("地狱未开启领地功能"))
            return
    elif worldid == 2:
        if not land_ender_open:
            player.sendTextPacket(land_message("末地未开启领地功能"))
            return
    else:
        if not land_world_open:
            player.sendTextPacket(land_message("主世界未开启领地功能"))
            return
    if playerbuy_3Dlandopen[playerxuid]:
        player.sendTextPacket(land_message("切换至二维领地选择模式"))
        playerbuy_3Dlandopen[playerxuid] = False
    playerbuy_2Dlandopen[playerxuid] = True
    pointA = [x, y, z]
    playerchoosepointA[playerxuid] = pointA
    player.sendTextPacket(land_message("成功选择点A") + f"{x}.{y}.{z}")
    player.sendTextPacket(land_message("破坏方块或使用/pland 2b选择点B"))
    player.sendTextPacket(land_message("空手点击地面或使用/pland q退出领地选择模式"))


def pland_2b(player):
    playerxuid = player.xuid
    playerXYZ = player.pos
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    worldid = player.did
    if not playerbuyland and not lapi.islandop(playerxuid):
        player.sendTextPacket(land_message("只能由管理员购买领地"))
        return
    if worldid == 1:
        if not land_nether_open:
            player.sendTextPacket(land_message("地狱未开启领地功能"))
            return
    elif worldid == 2:
        if not land_ender_open:
            player.sendTextPacket(land_message("末地未开启领地功能"))
            return
    else:
        if not land_world_open:
            player.sendTextPacket(land_message("主世界未开启领地功能"))
            return
    if playerbuy_3Dlandopen[playerxuid]:
        player.sendTextPacket(land_message("切换至二维领地选择模式"))
        playerbuy_3Dlandopen[playerxuid] = False
    playerbuy_2Dlandopen[playerxuid] = True
    pointB = [x, y, z]
    pointA = playerchoosepointA[playerxuid]
    if pointA == []:
        player.sendTextPacket(land_message("请先选择点A"))
        return False
    player.sendTextPacket(land_message("成功选择点B") + f"{x}.{y}.{z}")
    buyland(player, pointA, pointB, worldid, "2D")


def pland_3a(player):
    playerxuid = player.xuid
    playerXYZ = player.pos
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    worldid = player.did
    if not playerbuyland and not lapi.islandop(playerxuid):
        player.sendTextPacket(land_message("只能由管理员购买领地"))
        return
    if worldid == 1:
        if not land_nether_open:
            player.sendTextPacket(land_message("地狱未开启领地功能"))
            return
    elif worldid == 2:
        if not land_ender_open:
            player.sendTextPacket(land_message("末地未开启领地功能"))
            return
    else:
        if not land_world_open:
            player.sendTextPacket(land_message("主世界未开启领地功能"))
            return
    if playerbuy_2Dlandopen[playerxuid]:
        player.sendTextPacket(land_message("切换至三维领地选择模式"))
        playerbuy_2Dlandopen[playerxuid] = False
    playerbuy_3Dlandopen[playerxuid] = True
    pointA = [x, y, z]
    playerchoosepointA[playerxuid] = pointA
    player.sendTextPacket(land_message("成功选择点A") + f"{x}.{y}.{z}")
    player.sendTextPacket(land_message("破坏方块或使用/pland 3b选择点B"))
    player.sendTextPacket(land_message("空手点击地面或使用命令/pland q退出领地选择模式"))


def pland_3b(player):
    playerxuid = player.xuid
    playerXYZ = player.pos
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    worldid = player.did
    if not playerbuyland and not lapi.islandop(playerxuid):
        player.sendTextPacket(land_message("只能由管理员购买领地"))
        return
    if worldid == 1:
        if not land_nether_open:
            player.sendTextPacket(land_message("地狱未开启领地功能"))
            return
    elif worldid == 2:
        if not land_ender_open:
            player.sendTextPacket(land_message("末地未开启领地功能"))
            return
    else:
        if not land_world_open:
            player.sendTextPacket(land_message("主世界未开启领地功能"))
            return
    if playerbuy_2Dlandopen[playerxuid]:
        player.sendTextPacket(land_message("切换至三维领地选择模式"))
        playerbuy_2Dlandopen[playerxuid] = False
    playerbuy_3Dlandopen[playerxuid] = True
    pointB = [x, y, z]
    pointA = playerchoosepointA[playerxuid]
    if pointA == []:
        player.sendTextPacket(land_message("请先选择点A"))
        return False
    player.sendTextPacket("§e[land]§a成功选择点B:" + f"{x}.{y}.{z}")
    buyland(player, pointA, pointB, worldid, "3D")


def pland_q(player):
    playerxuid = player.xuid
    playerXYZ = player.pos
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    worldid = player.did
    if playerbuy_2Dlandopen[playerxuid]:
        playerbuy_2Dlandopen[playerxuid] = False
        playerchoosepointA[playerxuid] = []
        del playerchoosepointA[playerxuid]
        player.sendTextPacket(land_message("二维领地选择模式关闭"))
    if playerbuy_3Dlandopen[playerxuid]:
        playerbuy_3Dlandopen[playerxuid] = False
        playerchoosepointA[playerxuid] = []
        del playerchoosepointA[playerxuid]
        player.sendTextPacket(land_message("三维领地选择模式关闭"))
    player.sendTextPacket(land_message("命令使用成功"))


def plandremove(player):
    playerxuid = player.xuid
    playerXYZ = player.pos
    x = int(playerXYZ[0])
    y = int(playerXYZ[1])
    z = int(playerXYZ[2])
    worldid = player.did
    if lapi.islandop(playerxuid):
        landname = lapi.island(x, y, z, worldid)
        if landname == "noland":
            player.sendTextPacket(land_message("脚下没有领地"))
        else:
            lapi.removelanddata(landname)
            player.sendTextPacket(land_message("成功删除领地"))
    else:
        player.sendTextPacket(land_message("权限不足"))


def onControlCmd(e):
    if "plandreload" in e:
        lapi.loadsdata()
        loadsdata()
        return False
    if "oldlandreload" in e:
        landold_tolandnew()
        return False
    return True
# =======================================转化旧版领地数据组件=============


def getoldlandgetXYZ(a):
    b = a.index(":")
    c1 = a[:b]
    d1 = c1.index(".")
    d2 = c1[d1 + 1:]
    d3 = d2.index(".")
    x1 = c1[:d1]
    y1 = d2[:d3]
    z1 = d2[d3 + 1:]
    c2 = a[b + 1:]
    e1 = c2.index(".")
    e2 = c2[e1 + 1:]
    e3 = e2.index(".")
    x2 = c2[:e1]
    y2 = e2[:e3]
    z2 = e2[d3 + 1:]
    return [int(x1), int(y1), int(z1), int(x2), int(y2), int(z2)]
# 是否存在某个配置文件


def havelandoldfp(path2):
    a = os.path.exists(os.getcwd() + "\\land\\" + path2)
    if a:
        return True
    else:
        return False
# 读取领地文件


def readlandoldfp(path2):
    path = ".\\land\\" + path2
    try:
        f1 = open(path, 'r')
        data = f1.read()
    finally:
        if f1:
            f1.close()
    return data


def landold_tolandnew():
    landdata_old = {}
    if not havelandoldfp("land.json"):
        logger.error("未找到land.json无法完成转化")
        return
    landdata_old = stringtojson(readlandoldfp("land.json"))
    for landname_old in landdata_old["po"]:
        try:
            XYZ = getoldlandgetXYZ(landname_old)
            playerxuid = landdata_old["land"][landname_old]["xuid"]
            playername = landdata_old["land"][landname_old]["land_use"]
            lapi.createlanddata(
                playerxuid, XYZ[0], XYZ[1], XYZ[2], XYZ[3], XYZ[4], XYZ[5], 0, "2D")
            lapi.addplayername(playerxuid, playername)
        except:
            pass
    logger.info("旧版领地数据转化完成")

if __name__ == "pland":
    landstart()
