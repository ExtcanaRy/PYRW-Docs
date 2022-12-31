# mc.py

# 简介

该文件模块位于 `plugins/py/mc.py`，提供多种功能，包括监听器名字兼容，API修改，日志输出函数，配置文件操作函数等功能

# 内容

##### 1.监听器名字兼容

我们通过修改 `mc.setListener`和 `mc.removeListener`传入的监听器名字来实现兼容新旧监听器名字，例如

```python
def setListener(event: str, function: Callable[[object], Optional[bool]]) -> None:
    notContainer = True
    if event == "onJoin": # py插件内使用的监听器
        event = "onPlayerJoin" # BDSpyrunnerW 提供的监听器
    if event == "onOpenContainer": # 将打开容器解析为同时设置多个监听器以简化代码
        notContainer = False
        mco.setListener("onOpenChest", function) # 打开箱子
        mco.setListener("onOpenBarrel", function) # 打开木桶
    if notContainer:
        return mco.setListener(event, function)
```

##### 2.API修改

我们通过包装 `BDSpyrunnerW`提供的 `API`来修改想要传入的值并提供更为清晰的函数原型，例如

```python
def setCommandDescription(cmd:str, description:str, function: Callable[[object], Optional[bool]] = None) -> None:
    if function:
        return mco.setCommandDescription(cmd, description, function)
    else:
        return mco.setCommandDescription(cmd, description)
```

##### 3.日志输出函数

模块内提供了统一的日志输出接口来帮助开发者规范插件的控制台输出，您首先需要在您的插件中填写以下代码，此后插件在输出日志时便不必填写 `name`参数，插件名默认为文件名

```python
def logout(*content, name: str = __name__, level: str = "INFO", info: str = ""):
    mc.log(content, name=name, level=level, info=info)
```

要产生第一条输出，我们编写了如下代码

```python
def testonServerStarted(e):
	logout("Listener onServerStarted")
mc.setListener("onServerStarted", testonServerStarted)
```

它将会在服务器完成启动时输出以下内容

```plaintext
14:23:07 INFO [myplugin] Listener onServerStarted
```

为了使输出更加多样化，我们修改了代码，如下

```python
def testonServerStarted(e):
	logout("Listener onServerStarted", name="MY_FIRST_PLUGIN", level="WARN", info="LOG")
mc.setListener("onServerStarted", testonServerStarted)
```

这将会产生如下输出

```plaintext
14:37:05 WARN [MY_FIRST_PLUGIN][LOG] Listener onServerStarted
```

##### 4.配置文件操作

函数原型

```python
# 读取
read_conf(folder:str, filename:str, encoding="utf-8")

# 保存
save_conf(folder:str, filename:str, config={}, encoding="utf-8")

# 创建
make_conf(folder:str, filename:str, config={}, encoding="utf-8")
```

参数

```
folder: 保存配置文件的文件夹，位于 plugins/py/ 目录下
```

```
filename: 文件名，位于 plugins/py/<folder>/ 目录下
```

```
encoding: 文件编码，默认为utf-8
```

以下是示例代码，假设您的插件文件名为 `myplugin.py`

```python
# 定义默认配置文件
def_conf = {}
def_conf['obj_1'] = 3
def_conf['obj_2'] = True
def_conf['i_am_3'] = "I am 3"
def_conf['the_4_obj'] = [{'name': 'this is 1'}, {'name': 'another_obj', 'type': 'str'}]
def_conf['i_am_none'] = None

# 创建配置文件，已有则不做任何操作
mc.make_conf(__name__, f"{__name__}.json", def_conf)

# 读取配置文件
config = mc.read_conf("myplugin", "myplugin.json")

# 输出配置内容
logout(config['i_am_3'])
logout(config['the_4_obj'][1]['name'])
```

这将会在 `plugins/py/myplugin/myplugin.json`中产生如下内容

```json
{
	"obj_1": 3,
	"obj_2": true,
	"i_am_3": "I am 3",
	"the_4_obj": [
		{
			"name": "this is 1"
		},
		{
			"name": "another_obj",
			"type": "str"
		}
	],
	"i_am_none": null
}
```

并且在控制台输出以下内容

```plaintext
14:58:38 INFO [myplugin] I am 3
14:58:38 INFO [myplugin] another_obj
```

修改配置文件中的内容，在控制台上的输出也会相应的发生改变
