# BDSpyrunnerW Docs

Welcome to the `BDSpyrunnerW Docs`!

This document will help you develop plugins for BDSpyrunnerW.

## Requirements

1. have read the README and have successfully installed pyr.
2. Knowledge of Python3, go to [Official Website](https://www.python.org/about/gettingstarted/) to learn it.
3. have a good heart for research.

## Start

If you have met the above requirements, you can start writing the plugin

### 1. Create a new file

Note: Any `Python` files you create should be in `UTF-8` encoding, otherwise you may get errors when loading them, other files such as `json`, we also recommend using `UTF-8` encoding

Create `myplugin.py` in the `plugins/py` directory and type the following:

```py
import mc

help(mc)
```

After saving, start BDS and you will see the details of the mc module

### 2. Listening to in-game events

BDSpyrunner uses Detours to hook the BDS function points to intercept and listen for events.
We can use the setListener function to bind a function to an event, as follows.

```py
import mc

def onUseItem(e):
	print(e)
mc.setListener('onUseItem',onUseItem)
```

Save and start BDS, go to the server and
When you use the item, some relevant data will be printed on the console.

### 3. Get entity data

With all this data coming back from the listener, what do we do with it?
Take a look at the following example

```py
import mc

def onUseItem(e):
	player = e['player']
	pos = player.pos
	msg = f"{p.name} used item at {pos}"
	print(msg)
	player.sendTextPacket(msg)
mc.setListener('onUseItem', onUseItem)
```

Save the file in ``UTF-8`` format to support Chinese
Start BDS, enter the game and use the item, you will see the output in the console
Actually `player` is an object of Entity class, `name` and `pos` are its properties.
`sendTextPacket` is its member function.

### 4. Console debugging

Type `pydebug` in the server backend to enter console debugging mode, where you can type `Python` statements for execution and type `pydebug` again to return to the server console

Here is an example

```python
pydebug
>>> import mc
>>> mc.log("Here is pydebug!", name="PYDEBUG") 
17:05:56 INFO [PYDEBUG] Here is pydebug!
>>> mc.log(mc.getBDSVerion(), name="PYDEBUG")  
17:07:05 INFO [PYDEBUG] 1.19.51.01
>>> pydebug

```

### 5. Hot Reload Plugin

Hot reloading is a very meaningful feature for developers and can save a lot of time. Not only can we reload all plugins with the command ``pyreload`` from the console, but we can also set up a separate reload command for our own plugins. Here's how hot reloads are used.

We create a file called ``reloader.py`` and write the following code in it.

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

Then type the command ``list`` in the server console and you will see something like this.

```plaintext
list
[2023-02-17 04:11:49:266 DEBUG][reloader][Input] list
[2023-02-17 04:11:49:872 DEBUG][reloader][Output] There are 0/10 players online:


There are 0/10 players online:
```

At this point we go to the plugin and change the code.

* Comment ``mc.setListener("onConsoleOutput", onConsoleOutput)``
* Comment ``mc.removeListener("onConsoleOutput", onConsoleOutput)``
* Replace ``logger.debug`` with ``logger.error``

Here is the code after the change.

```python
import mc

logger = mc.Logger(__name__)

def onConsoleInput(cmd: str):
    logger.error(cmd, info="Input") # Modified
    cmd = cmd.split()
    if len(cmd) > 0 and cmd[0] == "reloader":
        if len(cmd) > 1 and cmd[1] == "reload":
            mc.removeListener("onConsoleInput", onConsoleInput)
            # mc.removeListener("onConsoleOutput", onConsoleOutput)
            mc.reload(__name__)
            return False

def onConsoleOutput(output: str):
    logger.error(output, info="Output")

mc.setListener("onConsoleInput", onConsoleInput)
# mc.setListener("onConsoleOutput", onConsoleOutput)
```

After saving the file, type ``reloader reload`` in the console and you will see something that looks like this

```plaintext
reloader reload
[2023-02-17 04:21:18:194 DEBUG][reloader][Input] reloader reload
[2023-02-17 04:21:18:194 INFO][BDSpyrunnerW] Reloading reloader
```

Type ``list`` again and you will see something that looks like the following.

```plaintext
list
[2023-02-17 04:21:22:193 ERROR][reloader][Input] list
There are 0/10 players online:
```

You can notice that the output of ``Output`` disappears and the log output level of ``reloader`` changes from ``DEBUG`` to ``ERROR``, which means the plugin hot reload was successful.

You can also use the ``FileMonitor`` class provided in the ``mc.py`` file module to perform hot reloading when the contents of a file change, as shown in the following example

```python
import mc

logger = mc.Logger(__name__)

# Automatically reload all modules by default when no arguments are passed in
file_monitor = mc.FileMonitor("plugins/py/reloader.py", callback=mc.reload, args=(__name__,), interval=1)

file_monitor.start()

# Comment this line and save the file repeatedly, automatic hot reloading can be observed
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

## Extensions

In addition to the above example, we provide a rich set of other interfaces.

* [mc.py](mc.py.md "file module")
* [API](API.md)
* [Listener](Listener.md)

## End

Well now that you have fully mastered the basics of plugin development
Go ahead and get creative!
