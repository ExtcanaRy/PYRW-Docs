# mc.py

# Introduction

This file module is located in `plugins/py/mc.py` and provides various functions, including listener name compatibility, API modification, log output functions, configuration file manipulation functions, etc.

# Contents

##### 1. Listener Name Compatibility

We can achieve compatibility between old and new listener names by modifying the listener names passed in by `mc.setListener` and `mc.removeListener`, for example

```python
def setListener(event: str, function: Callable[[object], Optional[bool]]) -> None:
    notContainer = True
    if event == "onJoin": # Listener used inside py plugin
        event = "onPlayerJoin" # Listener provided by BDSpyrunnerW
    if event == "onOpenContainer": # Parse open container as multiple listeners at once to simplify code
        notContainer = False
        mco.setListener("onOpenChest", function) # Open the chest
        mco.setListener("onOpenBarrel", function) # Open the barrel
    if notContainer:
        return mco.setListener(event, function)
```

##### 2. API modification

We modify the values we want to pass in and provide a clearer function prototype by wrapping the `API` provided by `BDSpyrunnerW`, for example

```python
def setCommandDescription(cmd:str, description:str, function: Callable[[object], Optional[bool]] = None) -> None:
    If function:
        return mco.setCommandDescription(cmd, description, function)
    else:
        return mco.setCommandDescription(cmd, description)
```

##### 3. Log output functions

The module provides a unified log output interface to help developers standardize the console output of the plugin. You first need to fill in the following code in your plugin, then the plugin does not need to fill in the `name` parameter when outputting the log, the plugin name is the file name by default

```python
def logout(*content, name: str = __name__, level: str = "INFO", info: str = ""):
    mc.log(content, name=name, level=level, info=info)
```

To generate the first output, we write the following code

```python
def testonServerStarted(e):
	logout("Listener onServerStarted")
mc.setListener("onServerStarted", testonServerStarted)
```

It will output the following when the server finishes starting

```plaintext
14:23:07 INFO [myplugin] Listener onServerStarted
```

To make the output more diverse, we modified the code as follows

```python
def testonServerStarted(e):
	logout("Listener onServerStarted", name="MY_FIRST_PLUGIN", level="WARN", info="LOG")
mc.setListener("onServerStarted", testonServerStarted)
```

This will produce the following output

```plaintext
14:37:05 WARN [MY_FIRST_PLUGIN][LOG] Listener onServerStarted
```

##### 4. Configuration file manipulation

Function prototype

```python
# read
read_conf(folder:str, filename:str, encoding="utf-8")

# Save
save_conf(folder:str, filename:str, config={}, encoding="utf-8")

# Create
make_conf(folder:str, filename:str, config={}, encoding="utf-8")
```

Parameters

```
folder: folder where the configuration file is stored, located in the plugins/py/ directory
```

```
filename: the name of the file, located in the plugins/py/<folder>/ directory
```

```
encoding: encoding of the file, default is utf-8
```

Here is the sample code. Suppose your plugin file name is `myplugin.py`

```python
# Define the default configuration file
def_conf = {}
def_conf['obj_1'] = 3
def_conf['obj_2'] = True
def_conf['i_am_3'] = "I am 3"
def_conf['the_4_obj'] = [{'name': 'this is 1'}, {'name': 'another_obj', 'type': 'str'}]
def_conf['i_am_none'] = None

# Create a configuration file, but do nothing if it already exists
mc.make_conf(__name__, f"{__name__}.json", def_conf)

# Read the configuration file
config = mc.read_conf("myplugin", "myplugin.json")

# Output configuration content
logout(config['i_am_3'])
logout(config['the_4_obj'][1]['name'])
```

This will generate the following in `plugins/py/myplugin/myplugin.json`

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

and output the following on the console

```plaintext
14:58:38 INFO [myplugin] I am 3
14:58:38 INFO [myplugin] another_obj
```

By changing the contents of the configuration file, the output on the console will change accordingly
