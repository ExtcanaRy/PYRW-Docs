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

注意：你所创建的任何 `Python`文件都要使用 `UTF-8`编码，否则在加载时可能会出现错误，其他文件如`json`，我们也推荐使用`UTF-8`编码

在`plugins/py`目录下创建`myplugin.py`，键入以下内容:

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
mc.setListener('onUseItem', onUseItem)
```

保存并启动BDS，进入服务器。
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
实际上 `player`是Entity类的一个对象，`name`和 `pos`则是它的属性
`sendTextPacket`是它的成员函数。

### 4. 控制台调试

在服务器后台输入`pydebug`即可进入控制台调试模式，在这个模式下，你可以键入`Python`语句进行执行，再次键入`pydebug`以返回服务器控制台

以下是一段示例

```python
pydebug
>>> import mc
>>> mc.log("Here is pydebug!", name="PYDEBUG") 
17:05:56 INFO [PYDEBUG] Here is pydebug!
>>> mc.log(mc.getBDSVerion(), name="PYDEBUG")  
17:07:05 INFO [PYDEBUG] 1.19.51.01
>>> pydebug

```

## 扩展

除了上面的例子外，我们还提供了丰富的其他接口：

* [mc.py](mc.py.md "文件模块")
* [API](API.md "接口")
* [Listener](Listener.md "监听器")

## 结束

好了现在你已经完全掌握了插件开发的基础内容
去尽情发挥创造力吧！
