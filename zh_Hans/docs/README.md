# BDSpyrunnerW 文档

欢迎来到``BDSpyrunnerW 文档``！

此文档将帮助你开发适用于BDSpyrunnerW的插件。

## 要求

1. 阅读了README并且成功安装了pyrw。
2. 掌握Python3的相关知识，可前往[菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html)学习。
3. 有一颗善于钻研的心。

## 开始

如果你已经了满足上面的要求就可以开始写插件了

### 1. 创建新文件

注意：你所创建的任何``Python``文件都要使用``UTF-8``编码，否则在加载时可能会出现错误，其他文件如``json``，我们也推荐使用``UTF-8``编码

在``plugins/py``目录下创建``myplugin.py``，键入以下内容:

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

将文件保存为``UTF-8``格式以支持多语言
启动BDS，进入游戏使用物品，你将在控制台看到输出
实际上``player``是Entity类的一个对象，``name``和``pos``则是它的属性
``sendTextPacket``是它的成员函数。

### 4. 控制台调试

在服务器后台输入``pydebug``即可进入控制台调试模式，在这个模式下，你可以键入``Python``语句进行执行，再次键入``pydebug``以返回服务器控制台

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

### 5. 热重载插件

* 阅读本节前您可能需要首先阅读其他文档来了解相应API

热重载对于开发人员是非常有意义的功能，可以节省大量时间。我们不仅可以在控制台使用命令``pyreload``重载所有插件，也可以为自己的插件单独设置一个重载命令。以下是热重载的用法。

我们创建一个名为``reloader.py``的文件，并在其中编写如下代码：

```python
import mc

logger = mc.Logger(__name__)

def onConsoleInput(cmd: str):
    logger.debug(cmd, info="Input")
    cmd = cmd.split()
    if len(cmd) > 0 and cmd[0] == "reloader":
        if len(cmd) > 1 and cmd[1] == "reload":
            mc.removeListener("onConsoleInput", onConsoleInput)
            mc.removeListener("onConsoleOutput", onConsoleOutput)
            mc.reload(__name__)
            return False

def onConsoleOutput(output: str):
    logger.debug(output, info="Output")

mc.setListener("onConsoleInput", onConsoleInput)
mc.setListener("onConsoleOutput", onConsoleOutput)
```

然后在服务器控制台键入命令``list``，你将看到形如以下内容：

```plaintext
list
[2023-02-17 04:11:49:266 DEBUG][reloader][Input] list
[2023-02-17 04:11:49:872 DEBUG][reloader][Output] There are 0/10 players online:


There are 0/10 players online:
```

这时我们去插件中修改代码。

* 注释``mc.setListener("onConsoleOutput", onConsoleOutput)``
* 注释``mc.removeListener("onConsoleOutput", onConsoleOutput)``
* 将``logger.debug``改为``logger.error``

以下是修改完毕后的代码：

```python
import mc

logger = mc.Logger(__name__)

def onConsoleInput(cmd: str):
    logger.error(cmd, info="Input") # 已修改
    cmd = cmd.split()
    if len(cmd) > 0 and cmd[0] == "reloader":
        if len(cmd) > 1 and cmd[1] == "reload":
            mc.removeListener("onConsoleInput", onConsoleInput)
            # mc.removeListener("onConsoleOutput", onConsoleOutput)
            mc.reload(__name__)
            return False

def onConsoleOutput(output: str):
    logger.debug(output, info="Output")

mc.setListener("onConsoleInput", onConsoleInput)
# mc.setListener("onConsoleOutput", onConsoleOutput)
```

在保存文件后，在控制台键入``reloader reload``，你将看到形如以下内容：

```plaintext
reloader reload
[2023-02-17 04:21:18:194 DEBUG][reloader][Input] reloader reload
[2023-02-17 04:21:18:194 INFO][BDSpyrunnerW] Reloading reloader
```

再次输入``list``，你将看到形如以下内容：

```plaintext
list
[2023-02-17 04:21:22:193 ERROR][reloader][Input] list
There are 0/10 players online:
```

你可以注意到``Output``的输出消失了，且``reloader``的日志输出等级从``DEBUG``变为了``ERROR``，这说明插件热重载成功了。

你也可以使用``mc.py``文件模块中提供的``FileMonitor``类，在文件内容发生变化时进行热重载，以下是一个示例

```python
import mc

logger = mc.Logger(__name__)

# 不传入任何参数时，默认自动重载所有模块
file_monitor = mc.FileMonitor("plugins/py/reloader.py", callback=mc.reload, args=(__name__,), interval=1)

file_monitor.start()

# 反复注释本行并保存文件，可观察到自动热重载
logger.debug("Reload")

def onConsoleInput(cmd: str):
    logger.debug(cmd, info="Input")
    cmd = cmd.split()
    if len(cmd) > 0 and cmd[0] == "reloader":
        if len(cmd) > 1 and cmd[1] == "reload":
            mc.removeListener("onConsoleInput", onConsoleInput)
            mc.removeListener("onConsoleOutput", onConsoleOutput)
            mc.reload(__name__)
            return False

def onConsoleOutput(output: str):
    logger.debug(output, info="Output")

mc.setListener("onConsoleInput", onConsoleInput)
mc.setListener("onConsoleOutput", onConsoleOutput)
```

## 扩展

除了上面的例子外，我们还提供了丰富的其他接口：

* [mc.py](mc.py.md "文件模块")
* [API](API.md "接口")
* [Listener](Listener.md "监听器")

## 结束

好了现在你已经完全掌握了插件开发的基础内容
去尽情发挥创造力吧！
