# mc.py

## Introduction

This file module is located in ``plugins/py/mc.py`` and provides various functions, including listener name compatibility, API modification, log output functions, configuration file manipulation functions, etc.

### Contents

#### 1. Listener Name Compatibility

We can achieve compatibility between old and new listener names by modifying the listener names passed in by ``mc.setListener`` and ``mc.removeListener``, for example

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

#### 2. API modification

We modify the values we want to pass in and provide a clearer function prototype by wrapping the ``API`` provided by ``BDSpyrunnerW``, for example

```python
def setCommandDescription(cmd:str, description:str, function: Callable[[object], Optional[bool]] = None) -> None:
    If function:
        return mco.setCommandDescription(cmd, description, function)
    else:
        return mco.setCommandDescription(cmd, description)
```

#### 3. Log output functions

The module provides a uniform log output interface to help developers standardize the console output of the plugin.

Initialize the class, here ``__name__`` is used to use the plugin's filename as the output log name. Suppose we currently write a plugin named ``myplugin.py``.

```python
logger = mc.Logger(__name__)
```

To generate the first output, we write the following code

```python
def testonServerStarted(e):
    logger.info("Listener onServerStarted")
mc.setListener("onServerStarted", testonServerStarted)
```

It will output the following when the server finishes starting

```plaintext
14:23:07 INFO [myplugin] Listener onServerStarted
```

To make the output more diverse, we modified the code as follows

```python
def testonServerStarted(e):
    logger.warn("Listener onServerStarted", info="LOG")
mc.setListener("onServerStarted", testonServerStarted)
```

This will produce the following output

```plaintext
14:37:05 WARN [myplugin][LOG] Listener onServerStarted
```

#### 4. Configuration file manipulation

We use the ``ConfigManager`` class to simplify the management of ``json`` configuration files

Available member functions:

```python
def __init__(self, filename:str, folder:str = "", encoding="utf-8")
def read(self)
def save(self, config={})
def make(self, config={})
```

Init Parameters

```plaintext
filename: filename, located in plugins/py/<folder>/ directory, no need to add the file suffix ".json"
```

```plaintext
folder: folder where the configuration file is stored, located in the plugins/py/ directory, default is filename
```

```plaintext
encoding: file encoding, default is utf-8
```

Here is the sample code, assuming your plugin file name is ``myplugin.py``

```python
import mc
conf_mgr = mc.ConfigManager(__name__)
# Define the default configuration file
def_conf = {}
def_conf['obj_1'] = 3
def_conf['obj_2'] = True
def_conf['i_am_3'] = "I am 3"
def_conf['the_4_obj'] = [{'name': 'this is 1'}, {'name': 'another_obj', 'type': 'str'}]
def_conf['i_am_none'] = None

# Create a configuration file, but do nothing if it already exists
conf_mgr.make(def_conf)

# Read the configuration file
config = conf_mgr.read()

# Output configuration content
logout(config['i_am_3'])
logout(config['the_4_obj'][1]['name'])
```

This will generate the following in ``plugins/py/myplugin/myplugin.json``

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

#### 5. Pointer operations

To simplify the operation of modifying values using the function interface, we have chosen to use pointers as a bridge for data exchange between ``C++`` and ``Python``.
The pointer provided by ``BDSpyrunnerW`` in ``Python`` is usually of type ``int`` represented by a string of numbers, which we call type ``pointer`` in the documentation, and requires the use of the ``ctypes`` library to take and modify its value.
When you need to modify the value pointed by the pointer, you can use the ``Pointer`` class provided in the ``mc`` documentation module, which provides an easy way to access the memory data pointed by the pointer and modify it.

The following is an example of modifying the damage generated during a player attack.

```python
import mc
import ctypes

logger = mc.logger("ATK")

def onPlayerAttack(event):
    pointer = mc.Pointer(event['damage'], ctypes.c_float)
    damage = pointer.get()
    pointer.set(100)
    logger.info(
        f"{event['player'].name}: ",
        f"{damage} -> {pointer.get()} ({event['damage']})",
        info="onPlayerAttack"
    )

mc.setListener("onPlayerAttack", onPlayerAttack)
```

When initializing ``mc.Pointer``, you need to pass in a pointer and a pointer type. The damage value in ``BDS`` is of type ``float``, so pass in ``ctypes.c_float``. The memory modification takes effect immediately, so the value obtained after calling the ``set`` member function is the modified one, whether the memory is accessed in ``C++`` or ``Python``. This is the basic principle of the method.

When using an empty-handed attack on a creature within the server, the creature will normally be killed outright and the console will print something like this

```plaintext
11:45:14 INFO [ATK][onPlayerAttack] SenpaiHomo: 1.0 -> 100.0 (114514001919810)
```

When the pointer type is ``c_char_p``, the data is obtained and processed in a slightly different way, using the ``get`` method to obtain data of type ``bytes``, and the ``set`` method to set the value also requires passing in data of type ``bytes``, consider using ``.encode()`` and ``.decode ()`` to complete the conversion between ``str`` and ``bytes``, e.g. the following code modifies a chat message:

```python
import mc
import ctypes

def on_player_chat(event):
    player = event['player']
    name_ptr = mc.Pointer(event['name_ptr'], ctypes.c_char_p)
    msg_ptr = mc.Pointer(event['msg_ptr'], ctypes.c_char_p)

    player_dimension = player.did
    player_pos = ",".join([f"{int(num)}" for num in player.pos])

    msg = msg_ptr.get().decode()
    name_mod = ""
    msg_mod = f"[{player_dimension}][{player_pos}] <{player.name}> {msg}"

    name_ptr.set(name_mod.encode())
    msg_ptr.set(msg_mod.encode())

mc.setListener('onChatPkt', on_player_chat)
```

When the player sends a ``test`` message, then the chat box will display something similar to the following:
```plaintext
[0][11, 45, 14] <SenpaiHomo> test
```

#### 6. File monitoring

Sometimes we need to monitor the file content changes and perform the appropriate actions after that, the ``FileMonitor`` class provides this function and can be used for hot reloading of plugins or configuration files and so on.

Available member functions.

```python
# Initialize, pass no arguments to automatically hot-reload all plugins
def __init__(self, path="plugins/py/", callback=reload, args=("",), interval=1)
# Start monitoring
def start(self)
# Stop monitoring
def stop(self)
```
