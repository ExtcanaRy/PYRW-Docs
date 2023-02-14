import json
import os
import mc

VERSION = '1.2.0'
isstart = False
config = {}
landdata = {}
landdata['landdata'] = {}
landdata['po'] = []
landdata['player'] = {}
landindex = {}
landindex['2D'] = {}
landindex['3D'] = {}
landindex['2D']['world'] = {}
landindex['2D']['nether'] = {}
landindex['2D']['ender'] = {}
landindex['3D']['world'] = {}
landindex['3D']['nether'] = {}
landindex['3D']['ender'] = {}
accuracy = 10
scoreboard = 'money'
land_world_open = True
land_nether_open = True
land_ender_open = True
land_2D_open = True
land_3D_open = True
land_maxnum = 5
land_2D_buy_money = 100
land_2D_sell_money = 100
land_3D_buy_money = 10
land_3D_sell_money = 10
land_2D_maxsize = 10000
land_3D_maxsize = 100000
menu_itemname = 'compass'
playerbuyland = True
mobile_listener = True
around_place = True


logger = mc.Logger(__name__)


def stringtojson(data):
    jsondata = json.loads(data)
    return jsondata


def jsontostring(data):
    data2 = json.dumps(data, sort_keys=True, indent=4,
                       separators=(',', ': '), ensure_ascii=False)
    return data2


def createpath(path):
    a = os.path.exists(os.getcwd() + '/' + path)
    if a != True:
        os.makedirs(os.getcwd() + '/' + path, exist_ok=True)


def havefp(path2):
    a = os.path.exists(os.getcwd() + '/plugins/py/pland/' + path2)
    if a:
        return True
    return False


def readlandfp(path2):
    path = './plugins/py/pland/' + path2
    try:
        f1 = open(path, 'r', encoding='UTF-8')
        data = f1.read()
    finally:
        if f1:
            f1.close()

    return data


def writelandfp(path2, data):
    path = 'plugins/py/pland/' + path2
    try:
        f2 = open(path, 'w', encoding='UTF-8')
        f2.write(data)
    finally:
        if f2:
            f2.close()


def getworldname(worldid):
    if worldid == 1:
        worldname = 'nether'
    else:
        if worldid == 2:
            worldname = 'ender'
        else:
            worldname = 'world'
    return worldname


config['scoreboard'] = 'money'
config['version'] = VERSION
config['accuracy'] = 10
config['land_maxnum'] = 5
config['land_world_open'] = True
config['land_nether_open'] = True
config['land_ender_open'] = True
config['land_2D_open'] = True
config['land_3D_open'] = True
config['land_2D_buy_money'] = 100
config['land_2D_sell_money'] = 100
config['land_3D_buy_money'] = 10
config['land_3D_sell_money'] = 10
config['land_2D_maxsize'] = 10000
config['land_3D_maxsize'] = 100000
config['menu_itemname'] = 'compass'
config['landop_xuid'] = ['xuid1', 'xuid2']
config['playerbuyland'] = True
config['mobile_listener'] = True
config['around_place'] = True
config['land_teleport'] = True
config['pistonBlock_listener'] = True


def createconfig():
    global config
    writelandfp('config.json', jsontostring(config))


def createlanddata(playerxuid, x1, y1, z1, x2, y2, z2, worldid, Dim):
    global landdata
    if worldid != 0:
        if worldid != 1:
            if worldid != 2:
                logger.warn(f"参数[worldid={worldid}有误, 无法创建领地")
                return ['False']
    if Dim != '2D':
        if Dim != '3D':
            logger.warn(f"参数[Dim={Dim}]有误！无法创建领地")
            return ['False']
    landall = {}
    landall['2D'] = getland_area(x1, y1, z1, x2, y2, z2, worldid, '2D')
    if Dim == '2D':
        landall['3D'] = getland_area(x1, -256, z1, x2, 256, z2, worldid, '3D')
    else:
        landall['3D'] = getland_area(x1, y1, z1, x2, y2, z2, worldid, '3D')
    if landall['2D'] != [] or landall['3D'] != []:
        return landall
    landname = f"{Dim}:{x1}.{y1}.{z1}:{x2}.{y2}.{z2}:{worldid}"
    worldname = getworldname(worldid)
    if landname not in landdata['landdata']:
        landdata['landdata'][landname] = {}
    landdata['landdata'][landname]['playerxuid'] = playerxuid
    landdata['landdata'][landname]['x1'] = x1
    landdata['landdata'][landname]['y1'] = y1
    landdata['landdata'][landname]['z1'] = z1
    landdata['landdata'][landname]['x2'] = x2
    landdata['landdata'][landname]['y2'] = y2
    landdata['landdata'][landname]['z2'] = z2
    landdata['landdata'][landname]['worldid'] = worldid
    landdata['landdata'][landname]['Dim'] = Dim
    landdata['landdata'][landname]['putblock'] = False
    landdata['landdata'][landname]['destroyblock'] = False
    landdata['landdata'][landname]['useitem'] = False
    landdata['landdata'][landname]['openchest'] = False
    landdata['landdata'][landname]['attack'] = False
    landdata['landdata'][landname]['share_putblock'] = True
    landdata['landdata'][landname]['share_destroyblock'] = True
    landdata['landdata'][landname]['share_useitem'] = True
    landdata['landdata'][landname]['share_openchest'] = True
    landdata['landdata'][landname]['share_attack'] = True
    landdata['landdata'][landname]['shareplayer'] = []
    landdata['landdata'][landname]['sign'] = {}
    if landname not in landdata['po']:
        landdata['po'].append(landname)
    if playerxuid not in landdata['player']:
        landdata['player'][playerxuid] = {}
    if worldname + 'land' not in landdata['player'][playerxuid]:
        landdata['player'][playerxuid][worldname + 'land'] = []
    if landname not in landdata['player'][playerxuid][worldname + 'land']:
        landdata['player'][playerxuid][worldname + 'land'].append(landname)
    addlandindex(x1, y1, z1, x2, y2, z2, worldid, Dim)
    writelandfp('land.json', jsontostring(landdata))
    return landall


def removelanddata(landname):
    land = getlandinfo(landname)
    if land == {}:
        return False
    removelandindex(landname)
    playerxuid = land['playerxuid']
    worldid = land['worldid']
    worldname = getworldname(worldid)
    landdata['po'].remove(landname)
    landdata['player'][playerxuid][worldname + 'land'].remove(landname)
    del landdata['landdata'][landname]
    writelandfp('land.json', jsontostring(landdata))
    return True


def getconfig():
    return config


def getlanddata():
    return landdata


def setlandop(playerxuid, mode):
    if mode == 'add':
        if playerxuid not in config['landop_xuid']:
            config['landop_xuid'].append(playerxuid)
            print('添加成功:' + playerxuid)
            writelandfp('config.json', jsontostring(config))
            return True
        print(playerxuid + '已经是管理员了')
    else:
        if mode == 'del':
            if playerxuid in config['landop_xuid']:
                config['landop_xuid'].remove(playerxuid)
                print('删除成功:' + playerxuid)
                writelandfp('config.json', jsontostring(config))
                return True
            print(playerxuid + '不是管理员, 无法删除')
        else:
            logger.warn(f"参数[mode={mode}]有误, 无法设置领地管理员")
    return False


def islandop(playerxuid):
    if playerxuid in config['landop_xuid']:
        return True
    return False


def setshareplayer(playerxuid, playername, landname, mode):
    try:
        if mode == 'add':
            if playerxuid not in landdata['landdata'][landname]['shareplayer']:
                landdata['landdata'][landname]['shareplayer'].append(playerxuid)
                if playerxuid not in landdata['player']:
                    landdata['player'][playerxuid] = {}
                landdata['player'][playerxuid]['playername'] = playername
                writelandfp('land.json', jsontostring(landdata))
                return True
        else:
            if mode == 'del':
                if playerxuid in landdata['landdata'][landname]['shareplayer']:
                    landdata['landdata'][landname]['shareplayer'].remove(playerxuid)
                    if playerxuid not in landdata['player']:
                        landdata['player'][playerxuid] = {}
                    landdata['player'][playerxuid]['playername'] = playername
                    writelandfp('land.json', jsontostring(landdata))
                    return True
            else:
                logger.warn(f"参数[mode={mode}]有误, 无法设置领地共享")
                return False
    except:
        return False


def addplayername(playerxuid, playername):
    try:
        if landdata['player'][playerxuid]['playername'] != playername:
            if playerxuid not in landdata['player']:
                landdata['player'][playerxuid] = {}
            landdata['player'][playerxuid]['playername'] = playername
            writelandfp('land.json', jsontostring(landdata))
    except:
        if playerxuid not in landdata['player']:
            landdata['player'][playerxuid] = {}
        else:
            landdata['player'][playerxuid]['playername'] = playername
            writelandfp('land.json', jsontostring(landdata))


def getshareplayername(playerxuid):
    try:
        playername = landdata['player'][playerxuid]['playername']
    except:
        playername = ''

    return playername


def setlandplayer(playerxuid, landname):
    try:
        landdata['landdata'][landname]['playerxuid'] = playerxuid
        return True
    except:
        return False


def getlandplayer(landname):
    try:
        return landdata['landdata'][landname]['playerxuid']
    except:
        return False


def setlandpower(landname, adminname, pbool):
    if pbool != False:
        pbool = True
    try:
        landdata['landdata'][landname][adminname] = pbool
        writelandfp('land.json', jsontostring(landdata))
    except:
        return False
    else:
        return True


def getlandpower(landname, adminname):
    try:
        return landdata['landdata'][landname][adminname]
    except:
        return False
        return False


def addlandsign(landname, signname, data):
    try:
        landdata['landdata'][landname]['sign'][signname] = data
    except:
        landdata['landdata'][landname]['sign'][signname] = {}
        landdata['landdata'][landname]['sign'][signname] = data

    writelandfp('land.json', jsontostring(landdata))


def removelandsign(landname, signname):
    try:
        del landdata['landdata'][landname]['sign'][signname]
    except:
        return False
    else:
        writelandfp('land.json', jsontostring(landdata))
        return True


def getlandsign(landname, signname):
    data = {}
    try:
        data = landdata['landdata'][landname]['sign'][signname]
    except:
        return data
    else:
        return data


def islandshareplayer(playerxuid, landname):
    try:
        if playerxuid in landdata['landdata'][landname]['shareplayer']:
            return True
    except:
        return False
    else:
        return False


def getlandinfo(landname):
    try:
        return landdata['landdata'][landname]
    except:
        return {}


def createlandindex():
    global accuracy
    global landindex
    for landname in landdata['po']:
        land = getlandinfo(landname)
        x1, z1, x2, z2 = land['x1'], land['z1'], land['x2'], land['z2']
        startx, endx = int(min([x1, x2]) / accuracy), int(max([x1, x2]) / accuracy)
        startz, endz = int(min([z1, z2]) / accuracy), int(max([z1, z2]) / accuracy)
        worldid, Dim = land['worldid'], land['Dim']
        worldname = getworldname(worldid)
        for i in range(endx - startx + 1):
            p = startx + i
            for j in range(endz - startz + 1):
                q = startz + j
                aindex = f"{p}:{q}"
                if aindex in landindex[Dim][worldname]:
                    landindex[Dim][worldname][aindex].append(landname)
                else:
                    landindex[Dim][worldname][aindex] = [landname]
    return landindex


def addlandindex(x1, y1, z1, x2, y2, z2, worldid, Dim):
    landname = f"{Dim}:{x1}.{y1}.{z1}:{x2}.{y2}.{z2}:{worldid}"
    worldname = getworldname(worldid)
    startx, endx = int(min([x1, x2]) / accuracy), int(max([x1, x2]) / accuracy)
    startz, endz = int(min([z1, z2]) / accuracy), int(max([z1, z2]) / accuracy)
    for i in range(endx - startx + 1):
        p = startx + i
        for j in range(endz - startz + 1):
            q = startz + j
            aindex = f"{p}:{q}"
            if aindex in landindex[Dim][worldname]:
                landindex[Dim][worldname][aindex].append(landname)
            else:
                landindex[Dim][worldname][aindex] = [landname]
    return landindex



def removelandindex(landname):
    land = getlandinfo(landname)
    if land == {}:
        return

    x1, z1, x2, z2 = land['x1'], land['z1'], land['x2'], land['z2']
    startx, endx = int(min([x1, x2]) / accuracy), int(max([x1, x2]) / accuracy)
    startz, endz = int(min([z1, z2]) / accuracy), int(max([z1, z2]) / accuracy)
    Dim, worldid = land['Dim'], land['worldid']
    worldname = getworldname(worldid)

    for i in range(endx - startx + 1):
        p = startx + i
        for j in range(endz - startz + 1):
            q = startz + j
            aindex = f"{p}:{q}"
            try:
                landindex[Dim][worldname][aindex].remove(landname)
            except:
                continue

    return landindex


def island2(x, y, z, worldid, LandDim):
    worldname = getworldname(worldid)
    if LandDim not in ["2D", "3D"]:
        return 'noland'

    try:
        xa, za = int(x / accuracy), int(z / accuracy)
        aindex = f"{xa}:{za}"
        aland = landindex[LandDim][worldname][aindex]

        for landname in aland:
            land = getlandinfo(landname)
            x1, z1, x2, z2 = land['x1'], land['z1'], land['x2'], land['z2']
            if min([x1, x2]) <= x <= max([x1, x2]) and min([z1, z2]) <= z <= max([z1, z2]):
                if LandDim == "3D":
                    y1, y2 = land['y1'], land['y2']
                    if min([y1, y2]) <= y <= max([y1, y2]):
                        return landname
                else:
                    return landname
        return 'noland'
    except:
        return 'noland'


def island(x, y, z, worldid):
    global land_2D_open
    global land_3D_open
    landname = 'noland'
    if land_2D_open:
        landname = island2(x, y, z, worldid, '2D')
    if landname == 'noland':
        if land_3D_open:
            landname = island2(x, y, z, worldid, '3D')
    return landname


def islandplayer(playerxuid, x, y, z, worldid, adminname):
    global land_ender_open
    global land_nether_open
    global land_world_open
    if worldid == 0 and not land_world_open:
        return True
    if worldid == 1 and not land_nether_open:
        return True
    if worldid == 2 and not land_ender_open:
        return True

    if islandop(playerxuid):
        return True
    landname = island(x, y, z, worldid)
    if landname == 'noland':
        return True
    land = getlandinfo(landname)
    if playerxuid == land['playerxuid']:
        return True
    if islandshareplayer(playerxuid, landname) and getlandpower(landname, 'share_' + adminname):
        return True
    elif getlandpower(landname, adminname):
        return True
    return False


def is_inside_rectangle(land, rect):
    return (land['x1'] >= rect['x1'] and land['x1'] <= rect['x2'] and
            land['x2'] >= rect['x1'] and land['x2'] <= rect['x2'] and
            land['z1'] >= rect['z1'] and land['z1'] <= rect['z2'] and
            land['z2'] >= rect['z1'] and land['z2'] <= rect['z2'])


def getland_area(x1, y1, z1, x2, y2, z2, worldid, Dim):
    rect = {'x1': x1, 'x2': x2, 'z1': z1, 'z2': z2}
    startx = int(min(x1, x2) / accuracy)
    endx = int(max(x1, x2) / accuracy)
    startz = int(min([z1, z2]) / accuracy)
    endz = int(max([z1, z2]) / accuracy)
    worldname = getworldname(worldid)
    landall = []
    for i in range(endx - startx + 1):
        p = startx + i
        for j in range(endz - startz + 1):
            q = startz + j
            aindex = f"{p}:{q}"
            try:
                aa = landindex[Dim][worldname][aindex]
                for landname in aa:
                    if landname not in landall:
                        land = getlandinfo(landname)
                        if Dim == '3D' and max([y1, y2]) >= min([land['y1'], land['y2']]) and min([y1, y2]) <= max([land['y1'], land['y2']]):
                            continue
                        if is_inside_rectangle(land, rect):
                            landall.append(landname)
            except:
                continue
    return landall


def getland_point(x, y, z, worldid, Dim):
    x1, z1 = x - accuracy, z - accuracy
    x2, z2 = x + accuracy, z + accuracy
    startx, endx = int(min(x1, x2) / accuracy), int(max(x1, x2) / accuracy)
    startz, endz = int(min(z1, z2) / accuracy), int(max(z1, z2) / accuracy)
    worldname = getworldname(worldid)
    landall = []
    for i in range(endx - startx + 1):
        p = startx + i
        for j in range(endz - startz + 1):
            q = startz + j
            aindex = f"{p}:{q}"
            aa = landindex.get(Dim, {}).get(worldname, {}).get(aindex, [])
            for landname in aa:
                if landname not in landall:
                    landall.append(landname)
    return landall



def getplayerland(playerxuid):
    landall = {}
    for dimension in ['worldland', 'netherland', 'enderland']:
        try:
            landall[dimension] = landdata['player'][playerxuid][dimension]
        except KeyError:
            landall[dimension] = []
    return landall



def getplayerlandnum(playerxuid):
    landnum = 0
    for dimension in ['worldland', 'netherland', 'enderland']:
        try:
            landnum += len(landdata['player'][playerxuid][dimension])
        except KeyError:
            pass
    return landnum


language = {}
language['sign'] = {}
language['sign']['Prefix'] = '§e[land]'
language['sign']['NULL_SIGN'] = '无'
language['sign']['Bottom_information'] = '§e[landop]§b %player:§a %message\n§e[landname]§d %displayname'
language['command'] = {}
language['command']['pland'] = '打开领地菜单'
language['command']['pland 2a'] = '设置二维领地点A'
language['command']['pland 2b'] = '设置二维领地点B'
language['command']['pland 3a'] = '设置三维领地点A'
language['command']['pland 3b'] = '设置三维领地点B'
language['command']['pland q'] = '退出领地选择'
language['command']['plandremove'] = '领地管理员移除领地'
language['message'] = {}
language['message']['请先购买领地'] = '§c请先购买领地'
language['message']['请输入标识'] = '§c请输入标识'
language['message']['名称过长'] = '§c名称过长'
language['message']['设置成功'] = '§a设置成功'
language['message']['移除成功'] = '§a移除成功'
language['message']['移除失败'] = '§c移除失败'
language['message']['留言过长'] = '§c留言过长'
language['message']['设置失败'] = '§a设置失败'
language['message']['地狱未开启领地功能'] = '§c地狱未开启领地功能'
language['message']['末地未开启领地功能'] = '§c末地未开启领地功能'
language['message']['主世界未开启领地功能'] = '§c主世界未开启领地功能'
language['message']['开启二维领地购买功能'] = '§c开启二维领地购买功能！'
language['message']['放置方块选择点A'] = '§b放置方块选择点A'
language['message']['破坏方块选择点B'] = '§b破坏方块选择点B'
language['message']['空手点击地面或使用命令/pland q退出领地选择模式'] = '§b空手点击地面或使用命令/pland q退出领地选择模式'
language['message']['未开启二维领地功能'] = '§c未开启二维领地功能'
language['message']['开启三维领地购买功能'] = '§b开启三维领地购买功能！'
language['message']['未开启三维领地功能'] = '§c未开启三维领地功能'
language['message']['取消分享'] = '§d取消分享:'
language['message']['领地名称'] = '§9领地名称: §3'
language['message']['领地范围'] = '§9领地范围: §3'
language['message']['领地主人'] = '§9领地主人: §3'
language['message']['共享玩家'] = '§9共享玩家: §3'
language['message']['领地留言'] = '§9领地留言: §3'
language['message']['没有开启领地传送功能'] = '§c没有开启领地传送功能'
language['message']['传送成功'] = '§a传送成功'
language['message']['传送失败'] = '§c传送失败'
language['message']['出售成功,获得金币'] = '§a出售成功,获得金币: '
language['message']['出售失败'] = '§c出售失败'
language['message']['成功将领地(%land),分享给玩家'] = '§d成功将领地(%land),分享给玩家'
language['message']['成功将领地(%land),赠送给玩家'] = '§d成功将领地(%land),赠送给玩家'
language['message']['你脚下没有领地'] = '§d你脚下没有领地！'
language['message']['周围没有领地'] = '§c周围没有领地'
language['message']['获取周围领地'] = '§a获取周围领地'
language['message']['二维领地'] = '§d二维领地: '
language['message']['三维领地'] = '§d三维领地: '
language['message']['领地面积超出最大尺寸'] = '§c领地面积超出最大尺寸！'
language['message']['你拥有的领地已达最大值'] = '§c你拥有的领地已达最大值！'
language['message']['余额不足, 购买失败'] = '§c余额不足, 购买失败！'
language['message']['领地购买成功,花费'] = '§a领地购买成功,花费: '
language['message']['二维领地选择模式关闭'] = '§c二维领地选择模式关闭'
language['message']['三维领地选择模式关闭'] = '§c三维领地选择模式关闭'
language['message']['领地周围禁止使用活塞'] = '§c领地周围禁止使用活塞'
language['message']['领地周围禁止使用水桶和岩浆'] = '§c领地周围禁止使用水桶和岩浆'
language['message']['没有该领地使用物品权限'] = '§c没有该领地使用物品权限'
language['message']['成功选择点A'] = '§a成功选择点A:'
language['message']['破坏方块或使用命令/pland 2b选择点B'] = '§b破坏方块或使用命令/pland 2b选择点B'
language['message']['破坏方块或使用命令/pland 3b选择点B'] = '§b破坏方块或使用命令/pland 3b选择点B'
language['message']['没有该领地放置方块权限'] = '§c没有该领地放置方块权限'
language['message']['请先选择点A'] = '§c请先选择点A'
language['message']['成功选择点B'] = '§a成功选择点B:'
language['message']['没有该领地破坏方块权限'] = '§c没有该领地破坏方块权限'
language['message']['没有该领地打开容器权限'] = '§c没有该领地打开容器权限'
language['message']['没有该领地攻击生物权限'] = '§c没有该领地攻击生物权限'
language['message']['切换至二维领地选择模式'] = '§d切换至二维领地选择模式'
language['message']['切换至三维领地选择模式'] = '§d切换至三维领地选择模式'
language['message']['命令使用成功'] = '§a命令使用成功'
language['message']['脚下没有领地'] = '§c脚下没有领地！'
language['message']['成功删除领地'] = '§a成功删除领地！'
language['message']['领地周围禁止使用重生锚'] = '§c领地周围禁止使用重生锚'
language['message']['你没有该领地使用重生锚的权限'] = '§c你没有该领地使用重生锚的权限'
language['gui'] = {}
language['gui']['领地系统'] = '领地系统'
language['gui']['选项'] = '§e选项'
language['gui']['设置标识'] = '设置标识'
language['gui']['设置展示名称'] = '设置展示名称'
language['gui']['移除展示名称'] = '移除展示名称'
language['gui']['设置领地留言'] = '设置领地留言'
language['gui']['移除领地留言'] = '移除领地留言'
language['gui']['选择当前世界(%playerworld)的领地'] = '选择当前世界(%playerworld)的领地'
language['gui']['购买领地'] = '购买领地'
language['gui']['我的领地'] = '我的领地'
language['gui']['领地共享'] = '领地共享'
language['gui']['领地标识'] = '领地标识'
language['gui']['领地查询'] = '领地查询'
language['gui']['领地购买'] = '领地购买'
language['gui']['购买二维领地'] = '购买二维领地'
language['gui']['购买三维领地'] = '购买三维领地'
language['gui']['设置领地权限'] = '设置领地权限'
language['gui']['攻击权限'] = '攻击权限'
language['gui']['攻击权限(共享玩家)'] = '攻击权限(共享玩家)'
language['gui']['使用物品权限'] = '使用物品权限'
language['gui']['使用物品权限(共享玩家)'] = '使用物品权限(共享玩家)'
language['gui']['开箱权限'] = '开箱权限'
language['gui']['开箱权限(共享玩家)'] = '开箱权限(共享玩家)'
language['gui']['放置方块权限'] = '放置方块权限'
language['gui']['放置方块权限(共享玩家)'] = '放置方块权限(共享玩家)'
language['gui']['破坏方块权限'] = '破坏方块权限'
language['gui']['破坏方块权限(共享玩家)'] = '破坏方块权限(共享玩家)'
language['gui']['取消领地分享'] = '取消领地分享'
language['gui']['选择已分享的玩家'] = '选择已分享的玩家'
language['gui']['领地信息'] = '领地信息'
language['gui']['传送至领地'] = '传送至领地'
language['gui']['设置领地权限'] = '设置领地权限'
language['gui']['分享领地'] = '分享领地'
language['gui']['赠送领地'] = '赠送领地'
language['gui']['选择玩家'] = '选择玩家'
language['gui']['查询脚下领地'] = '查询脚下领地'
language['gui']['查询周围领地'] = '查询周围领地'
language['gui']['重叠二维领地'] = '§9重叠二维领地: \n'
language['gui']['重叠三维领地'] = '§9重叠三维领地: \n'
language['gui']['购买失败, 领地重叠'] = '§9结果: §c购买失败, 领地重叠。\n \n%landall_2D\n \n%landall_3D\n \n \n \n'
language['gui']['确定'] = '确定'
language['gui']['取消'] = '取消'
language['gui']['购买领地信息提示'] = '§9我的金币: §3 %playermoney\n \n§9购买领地需要金币: §3 %needmony \n \n§9领地范围: §3 %landname\n \n§9领地尺寸: §3 %ab\n \n \n \n'
language['gui']['是否购买领地'] = '是否购买领地'
language['gui']['输入标识'] = '输入标识'
language['gui']['出售领地'] = '出售领地'
language['gui']['禁止活塞推动箱子'] = '禁止活塞推动箱子'
language['gui']['禁止活塞推动任何方块'] = '禁止活塞推动任何方块'
language['gui_image'] = {}
language['gui_image']['购买领地'] = ''
language['gui_image']['我的领地'] = ''
language['gui_image']['领地共享'] = ''
language['gui_image']['领地标识'] = ''
language['gui_image']['领地查询'] = ''
language['gui_image']['购买二维领地'] = ''
language['gui_image']['购买三维领地'] = ''
language['gui_image']['查询脚下领地'] = ''
language['gui_image']['查询周围领地'] = ''
language['gui_image']['确定'] = ''
language['gui_image']['取消'] = ''


def read_language():
    global language
    fplanguage = stringtojson(readlandfp('language.json'))
    for a in language:
        for key in language[a]:
            if a in fplanguage and key in fplanguage[a]:
                language[a][key] = fplanguage[a][key]
            else:
                if a not in fplanguage:
                    fplanguage[a] = {}
                fplanguage[a][key] = language[a][key]
                logger.warn(f"Missing language mapping <{a}|{key}>, successfully added.",
                       info="Language")

    writelandfp('language.json', jsontostring(fplanguage))


def get_null():
    try:
        return str(language['sign']['NULL_SIGN'])
    except:
        return '无'


def get_Bottom_information():
    try:
        return str(language['sign']['Bottom_information'])
    except:
        return '§e[landop]§b %player:§a %message\n§e[landname]§d %displayname'


def get_command_description(command):
    try:
        return str(language['command'][command])
    except:
        logger.error("at: " + command, info="Language")
        return command


def get_message(messagename):
    try:
        return str(language['sign']['Prefix']) + str(language['message'][messagename])
    except:
        logger.error("at: " + messagename, info="Language")
        return messagename


def get_gui_text(guiname):
    try:
        return str(language['gui'][guiname])
    except:
        logger.error("at: " + guiname, info="Language")
        return guiname


def get_gui_image(guiname):
    try:
        return str(language['gui_image'][guiname])
    except:
        logger.error("at: " + guiname, info="Language")
        return ''


def loadsdata():
    global accuracy
    global around_place
    global config
    global land_2D_buy_money
    global land_2D_maxsize
    global land_2D_open
    global land_2D_sell_money
    global land_3D_buy_money
    global land_3D_maxsize
    global land_3D_open
    global land_3D_sell_money
    global land_ender_open
    global land_maxnum
    global land_nether_open
    global land_teleport
    global land_world_open
    global landdata
    global menu_itemname
    global mobile_listener
    global pistonBlock_listener
    global playerbuyland
    global scoreboard
    pfconfig = stringtojson(readlandfp('config.json'))
    try:
        accuracy = pfconfig['accuracy']
        scoreboard = pfconfig['scoreboard']
        land_world_open = pfconfig['land_world_open']
        land_nether_open = pfconfig['land_nether_open']
        land_ender_open = pfconfig['land_ender_open']
        land_2D_open = pfconfig['land_2D_open']
        land_3D_open = pfconfig['land_3D_open']
        land_maxnum = pfconfig['land_maxnum']
        land_2D_buy_money = pfconfig['land_2D_buy_money']
        land_2D_sell_money = pfconfig['land_2D_sell_money']
        land_3D_buy_money = pfconfig['land_3D_buy_money']
        land_3D_sell_money = pfconfig['land_3D_sell_money']
        land_2D_maxsize = pfconfig['land_2D_maxsize']
        land_3D_maxsize = pfconfig['land_3D_maxsize']
        menu_itemname = pfconfig['menu_itemname']
        playerbuyland = pfconfig['playerbuyland']
        mobile_listener = pfconfig['mobile_listener']
        around_place = pfconfig['around_place']
        land_teleport = pfconfig['land_teleport']
        pistonBlock_listener = pfconfig['pistonBlock_listener']
        config = pfconfig
    except:
        pfconfig = stringtojson(readlandfp('config.json'))
        for aa in config:
            try:
                config[aa] = pfconfig[aa]
            except:
                pfconfig[aa] = config[aa]
                logger.warn(f"Missing config.json: {aa}, successfully added.")

        pfconfig['version'] = VERSION
        writelandfp('config.json', jsontostring(pfconfig))
        loadsdata()
        return
    else:
        logger.info("Successfully read the config file: config.json")
        landdata = stringtojson(readlandfp('land.json'))
        createlandindex()
        logger.info("Successfully read the config file: land.json")
        read_language()
        logger.info("Successfully read the config file: language.json")


def landapistart():
    global isstart
    if not isstart:
        createpath('plugins/py/pland')
        logger.info(f"landAPI for BDSpyrunnerW loaded! Author: g05007, Version: {VERSION}")
        # logger.info("插件作者: g05007, bug反馈请加QQ: 654921949")
        # logger.info("本插件无需付费, 转载发布必须经作者授权!")
        if havefp('config.json') == False:
            createconfig()
            logger.info("Creating config file: config.json")
        if havefp('land.json') == False:
            writelandfp('land.json', jsontostring(landdata))
            logger.info("Creating config file: land.json")
        if havefp('language.json') == False:
            writelandfp('language.json', jsontostring(language))
            logger.info("Creating config file: language.json")
        loadsdata()
        isstart = True
