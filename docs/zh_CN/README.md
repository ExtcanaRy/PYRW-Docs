# BDSpyrunnerW 文档

欢迎来到 `BDSpyrunnerW Docs`！
此文档将帮助你开发适用于BDSpyrunnerW的插件。

## 要求

1. 阅读了README并且成功安装了pyr。
2. 掌握Python3的相关知识，可前往[菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html)学习。
3. 有一颗善于钻研的心。

## 开始

如果你已经了满足上面的要求就可以开始写插件了

### 1. 创建新文件

在plugins/py目录下创建myplugin.py，键入以下内容:

```py
import mc

help(mc)
```

保存之后启动BDS，你将看到mc模块的详细信息

### 2. 监听游戏内事件

BDSpyrunner使用Detours勾住BDS的函数点来实现事件的拦截与监听，
我们可以使用setListener函数来将一个函数与某个事件绑定起来，如下：

```py
import mc

def onUseItem(e):
	print(e)
mc.setListener('onUseItem',onUseItem)
```

保存并启动BDS，进入服务器，
当你使用物品时，一些相关的数据就会打印的控制台上。

### 3. 获取实体数据

有了监听器回传的这些数据，我们该怎么处理呢？
来看下面这个例子

```py
import mc

def onUseItem(e):
	player = e['player']
	pos = player.pos
	msg = f"{p.name}在{pos}使用了物品"
	print(msg)
	player.sendTextPacket(msg)
mc.setListener('onUseItem', onUseItem)
```

将文件保存为 `UTF-8`格式以支持中文
启动BDS，进入游戏使用物品，你将在控制台看到输出
实际上 `player`是Entity类的一个对象，`name`和 `pos`则是它的属性，
`sendTextPacket`是它的成员函数。

## 扩展

除了上面的例子外，我们还提供了丰富的其他接口：

* [API](https://github.com/twoone-3/BDSpyrunner/wiki/API)
* [Listener](https://github.com/twoone-3/BDSpyrunner/wiki/Listener)

## 结束

好了现在你已经完全掌握了插件开发的基础内容
去尽情发挥创造力吧！
