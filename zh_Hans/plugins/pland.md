# pland

# 简介

1. 兼容旧版领地数据
2. 支持全部维度
3. 兼容二维领地和三维领地
4. 采用计分板经济
5. 添加设置领地默认权限、防止领地耕地破坏、领地内爆炸等
6. 丰富的拓展接口

# 下载

[主体](https://pyr.jfishing.love/plugins/pland.py "点我下载")

[子模块](https://pyr.jfishing.love/plugins/landAPI.py "点我下载")

# 配置文件

##### 1.文件夹

``plugins/py/pland``

##### 2.config.json

| 项目                 | 解释                                                 | 允许的值类型 |
| -------------------- | ---------------------------------------------------- | ------------ |
| accuracy             | 精度。建议10-500，值越小占用内存越大，但判断速度越快 | int          |
| around_place         | 是否允许在领地周围防止方块                           | bool         |
| land_2D_buy_money    | 二维领地购买价格                                     | int          |
| land_2D_maxsize      | 二维领地最大尺寸                                     | int          |
| land_2D_open         | 二维领地开关                                         | bool         |
| land_2D_sell_money   | 二维领地出售价格                                     | int          |
| land_3D_buy_money    | 三维领地购买价格                                     | int          |
| land_3D_maxsize      | 三维领地最大尺寸                                     | int          |
| land_3D_open         | 三维领地开关                                         | bool         |
| land_3D_sell_money   | 三维领地出售价格                                     | int          |
| land_ender_open      | 末地领地开关                                         | bool         |
| land_maxnum          | 玩家可拥有的最大领地数                               | int          |
| land_nether_open     | 地狱领地开关                                         | bool         |
| land_teleport        | 玩家是否可以传送到领地                               | bool         |
| land_world_open      | 主世界领地开关                                       | bool         |
| landop_xuid          | 领地管理员的xuid，填写格式为["xuid1","xuid2"]        | list         |
| menu_itemname        | 打开菜单的物品名称，如compass为指南针                | str       |
| mobile_listener      | 是否开启玩家移动监听，用于领地信息显示               | bool         |
| pistonBlock_listener | 是否开启活塞推拉监听                                 | bool         |
| scoreboard           | 经济采用的计分板名称                                 | str       |
| playerbuyland        | 设置玩家是否可以购买领地                             | bool         |
| version              | 版本                                                 | str       |

##### 3.config.json样例

```json
{
    "accuracy": 10,
    "around_place": false,
    "land_2D_buy_money": 0,
    "land_2D_maxsize": 10000,
    "land_2D_open": true,
    "land_2D_sell_money": 0,
    "land_3D_buy_money": 1,
    "land_3D_maxsize": 100000,
    "land_3D_open": true,
    "land_3D_sell_money": 1,
    "land_ender_open": true,
    "land_maxnum": 10,
    "land_nether_open": true,
    "land_teleport": true,
    "land_world_open": true,
    "landop_xuid": [
        "2535424098181234",
        "2535416022290000",
        "2535445654591145"
    ],
    "menu_itemname": "compass",
    "mobile_listener": true,
    "pistonBlock_listener": true,
    "playerbuyland": true,
    "scoreboard": "money",
    "version": "1.2.0"
}
```

##### 4.land.json

记录数据，勿随意修改！

# 可用命令

##### 1.游戏内

| 命令         | 解释                   |
| ------------ | ---------------------- |
| /pland       | 打开菜单               |
| /plandremove | 领地管理员强制移除领地 |

##### 2.服务器控制台

| 命令          | 解释                                                                         |
| ------------- | ---------------------------------------------------------------------------- |
| plandreload   | 重新加载配置文件                                                             |
| oldlandreload | 将旧版领地数据转化为新版，旧版领地为：land-g7.dll,转化时不要删除land文件夹。 |

# 调用接口

##### 1.调用领地菜单

```python
import pland
pland.landhelp(player)
# 参数：玩家指针
```

##### 2.核心功能接口

```python
import landAPI as lapi

lapi.island(x, y, z, worldid)
# 检查是否为领地，参数：(int)坐标-(int)世界id，返回值：(str)领地名称，不存在返回“noland”

lapi.islandplayer(playerxuid, x, y, z, worldid, powername)
# 检查玩家是否拥有领地某项权限，参数：(str)玩家xuid-(int)坐标-(int)世界id-(str)权限名称，返回值：bool
# powername值："useitem"|"putblock"|"destroyblock"|"openchest"|"attack"

lapi.getlandinfo(landname)
# 获取领地信息，参数：(str)领地名称，返回值：(dict)字典

lapi.getplayerland(playerxuid)
# 获取玩家拥有的领地，参数：(str)玩家xuid
# 返回值：(dict)字典，"world"-主世界领地，"nether"-地狱领地，"ender"-末地领地

lapi.getland_area(x1, y1, z1, x2, y2, z2, worldid, Dim)
# 获得一个区域内的全部领地
# Dim值："2D"|"3D"

lapi.getland_point(x, y, z, worldid, Dim)
# 获得一个点周围的领地
# Dim值："2D"|"3D"

lapi.createlanddata(playerxuid, x1, y1, z1, x2, y2, z2, worldid, Dim)
# 创建一个领地，参数：(str)玩家xuid-(int)坐标1-(int)坐标2-(int)世界id-(str)领地模式
# 返回值：(dict)字典，创建成功返回-{"2D":[],"3D":[]}，创建失败返回重叠领地的名称
# Dim值："2D"|"3D"

lapi.removelanddata(landname):
# 移除一个领地，参数：(str)领地名称，返回：bool

lapi.setlandop(playerxuid, mode)
# 设置领地管理员，参数：玩家xuid-模式，返回值：bool
# mode值："add"|"del"
```

##### 3.拓展功能接口

```python
lapi.addlandsign(landname, signname, data)
# 为领地添加一个标志，参数：(str)领地名称-(str)标志名称-(dict)字典，返回值：bool

lapi.removelandsign(landname, signname)
# 移除领地标志，参数：(str)领地名称-(str)标志名称，返回值：bool

lapi.getlandsign(landname, signname)
# 获取领地标志，参数：(str)领地名称-(str)标志名称，返回值 (dict)字典，不存在返回-{}
```
