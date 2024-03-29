# API

## 函数描述格式

```format
函数原型
介绍
```

## mc

介绍：``mc``是BDSpyrunner的一个内置模块

### minVersionRequire(major:int, minor:int, micro:int) -> None

如果当前的BDSpyrunnerW版本不满足最低的传入函数的版本，则会抛出异常并终止加载当前插件

### getBDSVersion() -> str

获取BDS的版本号

### getServerProtocolVersion() -> int

获取BDS的通讯协议版本号

### logout(msg:str) -> None

标准输出流向控制台发送输出消息(可拦截)

### runcmd(cmd:str) -> None

执行一条控制台命令

### setListener(key:str, callback:function) -> None

将callback与key事件绑定，事件触发时callback将会被调用，
可用的key可在Listener界面查询

### removeListener(key:str, callback:function) -> None

将已设置的监听器移除，移除后事件发生时将不再会调用对应callback，填入的参数应当与设置时填写的一致

### reload(name:str)

将模块``name``进行热重载，由于无法为其他模块删除已设置的监听器，故目前只能重载当前模块，常用调用方法：``reload(__name__)``
在重载前必须使用``removeListener``删除所有已设置的监听器，并且尽可能停止或堵塞启动的子线程/子进程，取消设置的计划任务等，必须处理一切可能在重载后继续运行的代码，否则可能引发服务器崩溃或其他问题！

### setCommandDescription(cmd:str, description:str, callback:function) -> None

设置指令说明，参数三是可选参数，
用于触发命令回调，回调函数原型：callback(player:mc.Entity) -> None

### getPlayerByXuid(xuid:str) -> mc.Entity

根据Xuid获取玩家

### getPlayerList() -> list

获取在线玩家列表

### setDamage(dmg:int) -> None

设置生物受伤的伤害值
注:此函数仅在``onMobHurt``事件下调用才能生效

### setServerMotd(motd:str)

设置服务器外显名字

### getBlock(x:int, y:int, z:int, did:int) -> dict

获取指定位置方块信息

### setBlock(name:str, x:int, y:int, z:int, did:int) -> none

设置指定位置的方块，name必须使用驼峰式，如RedStoneOre

### getStructure(x1:int, y1:int, z1:int, x2:int, y2:int, z2:int, did:int) -> str

获取两个坐标之间的结构nbt数据

### setStructure(data:str, x:int, y:int, z:int, did:int) -> None

在(x,y,z)处设放置一个结构，data为结构JSON字符串

### getStructureRaw(x1:int, y1:int, z1:int, x2:int, y2:int, z2:int, did:int) -> str

从指定地点获取二进制NBT结构数据

### setStructureRaw(data:str, x:int, y:int, z:int, did:int) -> None

从二进制NBT结构数据导出结构到指定地点

### explode(x:float, y:float, z:float, did:int, power:float, destroy:bool, range:float, fire:bool) -> None

产生爆炸

### spawnItem(data:str, x:int, y:int, z:int, did:int) -> None

生成一个掉落物，data为物品JSON字符串

### isSlimeChunk(x:int, y:int) -> Boolean

检查是否为史莱姆区块

### setSignBlockMessage(msg:str, x:int, y:int, z:int, did:int) -> None

设置牌子文字

## class Entity

介绍：实体类，包括玩家、生物、实体。

### Entity的属性

1. name:str - 实体名字（可修改）
2. uuid:str - 玩家UUID
3. xuid:str - 玩家XUID
4. pos:list - 实体坐标
5. did:int - 实体维度ID
6. is_standing:bool - 实体是否站立在方块上
7. is_sneaking:bool - 实体是否潜行
8. health:int - 实体当前生命
9. maxhealth:int - 实体最大生命
10. perm:int - 玩家权限值（可修改，有0,1,2,3,4）
11. platform_online_id:str - 玩家设备ID
12. platform:int - 玩家设备操作系统（1代表Android，7代表Win10）
13. IP:str - 玩家IP

### getAllItem() -> str

获取玩家所有物品，返回值为JSON字符串，共有五种容器:``Hand``,``OffHand``,``Inventory``,``Armor``,``EndChest``

### setAllItem(data:str) -> None

设置玩家所有物品，data为JSON字符串，共有四种容器:``OffHand``,``Inventory``,``Armor``,``EndChest``

### setHand(data:str) -> None

设置玩家手中物品，data为JSON字符串

### addItem(data:str) -> None

为玩家新添物品，data为JSON字符串

### removeItem(slot:int, count:int) -> None

移除玩家背包slot格子的count个物品

### openInventoryGUI() -> None

打开玩家的背包GUI

### teleport(x:float, y:float, z:float, did:int) -> None

传送玩家到指定坐标和维度

### sendCommandPacket(cmd:str) -> None

模拟玩家发送命令包，也就是替玩家执行命令

### sendTextPacket(msg:str, type:int = 0) -> None

模拟玩家发送文本包，type = 0为原始文本，相当于指令tellraw，type = 1为聊天文本，相当于玩家说话

### sendPlaySoundPacket(sound_name:str, x:float, y:float, z:float, volume:float = 1.0, pitch:float = 1.0)

向玩家发送声音包以播放声音，参数与``/playsound``命令相近。[命令用法](https://minecraft.fandom.com/zh/wiki/%E5%91%BD%E4%BB%A4/playsound)
示例：

```python
pos = player.pos
player.sendPlaySoundPacket("ambient.weather.thunder", pos[0], pos[1], pos[2])
```

这将会使玩家听到一阵雷声

### resendAllChunks() -> None

重新发送玩家客户端的地图区块，可能造成亮度渲染问题

### disconnect(msg:str = '')

断开玩家连接，msg将显示在玩家断开连接后的屏幕上

### transferServer(ip:str, port:int) -> None

传送玩家到指定服务器

### getScore(scoreboard:str) -> int

获取玩家在名为scoreboard的计分板的分数

### modifyScore(scoreboard:str, count:int, mode:int) -> None

修在玩家在名为``scoreboard``的计分板的分数
``arg: mode``:
``0``: 设置
``1``: 增加
``2``: 减少

### addLevel(level:int) -> None

增加玩家经验等级

### setBossBar(msg:str, percent:float) -> None

设置玩家BOSS栏，percent是血条百分比(min:0, max:1)

### removeBossBar() -> None

移除玩家BOSS栏

### addTag(name:str) -> None

增加标签

### removeTag(name:str) -> None

移除标签

### getTags() -> list

获取标签

### setSidebar(title:str, content:str) -> None

设置玩家计分板侧边栏
例:`player.setSidebar('自定义侧边栏', '{"第一行":0, "第二行":2, "我在哪行?":3}')`

### removeSidebar() -> None

移除玩家计分板侧边栏

### sendCustomForm(data:str, callback:function) -> None

向指定的玩家发送一个自定义表单，回调函数原型为``callback(Entity:player, selected_data:str) -> None``
例:

```python
player.sendCustomForm('{"content":[{"type":"label","text":"这是一个文本标签"},{"placeholder":"水印文本","default":"","type":"input","text":""},{"default":true,"type":"toggle","text":"开关~或许是吧"},{"min":0.0,"max":10.0,"step":2.0,"default":3.0,"type":"slider","text":"游标滑块！？"},{"default":1,"steps":["Step1","Step2","Step 3"],"type":"step_slider","text":"矩阵滑块？!"},{"default":1,"options":["Option 1","Option2","Option3"],"type":"dropdown","text":"如你所见 下拉框"}], "type":"custom_form","title":"这是一个自定义窗体"}'，cb)
```

### sendSimpleForm(title:str, content:str, buttons:list, images:list, callback:function) -> None

向指定的玩家发送一个简单表单，回调函数原型为``callback(Entity:player, selected_item:int) -> None``
例:

```python
player.sendSimpleForm('标题', '内容', ["生存","死亡","求助"], ['','',''], cb)
```

### sendModalForm(title:str, content:str, button1:str, button2:str, callback:function) -> None

向指定的玩家发送一个模式对话框，回调函数原型为``callback(Entity:player, selected_item:str) -> None``
例:

```python
player.sendModalForm('标题', '内容', '按钮1', '按钮2', cb)
```

返回的``selected_item``:
``按钮1``: "true"
``按钮2``: "false"
