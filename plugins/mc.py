import mco

import os
import time
import json
import ctypes
import hashlib
import inspect
import threading
from typing import Optional, Callable
from datetime import datetime

# Listener
def setListener(event: str, function: Callable[[object], Optional[bool]]) -> None:
    notContainer = True
    if event == "onConsoleCmd":
        event = "onConsoleInput"
    if event == "onJoin": #listener name (from py plugin)
        event = "onPlayerJoin" #pyr provided listener name
    if event == "onLeft":
        event = "onPlayerLeft"
    if event == "onFormSelected":
        event = "onSelectForm"
    if event == "onOpenContainer":
        notContainer = False
        mco.setListener("onOpenChest", function)
        mco.setListener("onOpenBarrel", function)
    if event == "onCloseContainer":
        notContainer = False
        mco.setListener("onCloseChest", function)
        mco.setListener("onCloseBarrel", function)
    if event == "onChangeDim":
        event = "onChangeDimension"
    if event == "onPlayerCmd":
        event = "onInputCommand"
    if event == "onCmdBlockExecute":
        event = "onCommandBlockPerform"
    if event == "onFarmLandDecay":
        event = "onFallBlockTransform"
    if event == "onUseRespawnAnchor":
        event = "onUseRespawnAnchorBlock"
    if notContainer:
        return mco.setListener(event, function)


def removeListener(event: str, function: Callable[[object], Optional[bool]]) -> None:
    notContainer = True
    if event == "onConsoleCmd":
        event = "onConsoleInput"
    if event == "onJoin": #listener name (from py plugin)
        event = "onPlayerJoin" #pyr provided listener name
    if event == "onLeft":
        event = "onPlayerLeft"
    if event == "onFormSelected":
        event = "onSelectForm"
    if event == "onOpenContainer":
        notContainer = False
        mco.removeListener("onOpenChest", function)
        mco.removeListener("onOpenBarrel", function)
    if event == "onCloseContainer":
        notContainer = False
        mco.removeListener("onCloseChest", function)
        mco.removeListener("onCloseBarrel", function)
    if event == "onChangeDim":
        event = "onChangeDimension"
    if event == "onPlayerCmd":
        event = "onInputCommand"
    if event == "onCmdBlockExecute":
        event = "onCommandBlockPerform"
    if event == "onFarmLandDecay":
        event = "onFallBlockTransform"
    if event == "onUseRespawnAnchor":
        event = "onUseRespawnAnchorBlock"
    if notContainer:
        return mco.removeListener(event, function)


# API
def minVersionRequire(major: int, minor: int, micro: int) -> None:
    return mco.minVersionRequire(major, minor, micro)

def getBDSVersion() -> str:
    return mco.getBDSVersion()

def getServerProtocolVersion() -> int:
    return mco.getServerProtocolVersion()

def logout(message: str) -> None:
    return mco.logout(message)

def runcmd(command: str) -> None:
    return mco.runcmd(command)

def setCommandDescription(cmd:str, description:str, function: Callable[[object], Optional[bool]] = None) -> None:
    if function:
        return mco.setCommandDescription(cmd, description, function)
    else:
        return mco.setCommandDescription(cmd, description)

def getPlayerByXuid(xuid: str) -> mco.Entity:
    return mco.getPlayerByXuid(xuid)

def getPlayerList() -> list:
    return mco.getPlayerList()

def setDamage(dmg:int) -> None:
    return mco.setDamage(dmg)

def setServerMotd(motd:str):
    return mco.setServerMotd(motd)

def getBlock(x:int, y:int, z:int, dim:int) -> dict:
    return mco.getBlock(x, y, z, dim)

def setBlock(name:str, x:int, y:int, z:int, dim:int) -> None:
    return mco.setBlock(name, x, y, z, dim)

def getStructure(x1:int, y1:int, z1:int, x2:int, y2:int, z2:int, dim:int) -> str:
    return mco.getStructure(x1, y1, z1, x2, y2, z2, dim)

def setStructure(data:str, x:int, y:int, z:int, dim:int) -> None:
    return mco.setStructure(data, x, y, z, dim)

def explode(x:float, y:float, z:float, dim:int, power:float, destroy:bool, range:float, fire:bool) -> None:
    return explode(x, y, z, dim, power, destroy, range, fire)

def spawnItem(data:str, x:int, y:int, z:int, dim:int) -> None:
    return spawnItem(data, x, y, z, dim)

def isSlimeChunk(x:int, y:int) -> bool:
    return isSlimeChunk(x, y)

def setSignBlockMessage(msg:str, x:int, y:int, z:int, dim:int) -> None:
    return setSignBlockMessage(msg, x, y, z, dim)

def reload(name: str):
    return mco.reload(name)


######### TOOL API ########## 

class Logger:
    def __init__(self, name):
        self.name = name
    
    def log(self, *content, info: str = ""):
        level = inspect.currentframe().f_back.f_code.co_name.upper()
        if not os.path.exists("bedrock_server_mod.exe"):
            date = datetime.now().strftime("[%Y-%m-%d %H:%M:%S:%f")[:-3]
            level += "]"
        else:
            date = datetime.now().strftime("%H:%M:%S")
            level += " "
        if __name__ != '__main__':
            if info != "":
                print(f"{date} {level}[{self.name}][{info}] ", *content, sep="")
            else:
                print(f"{date} {level}[{self.name}] ", *content, sep="")
    
    def info(self, *content, info=""):
        self.log(*content, info=info)
    
    def warn(self, *content, info=""):
        self.log(*content, info=info)
    
    def error(self, *content, info=""):
        self.log(*content, info=info)
    
    def fatal(self, *content, info=""):
        self.log(*content, info=info)

    def debug(self, *content, info=""):
        self.log(*content, info=info)


class ConfigManager:
    def __init__(self, filename:str, folder:str = "", encoding="utf-8"):
        self.filename = filename
        self.encoding = encoding
        if folder:
            self.folder = folder
        else:
            self.folder = filename
        
    def read(self):
        if os.path.exists(f"plugins/py/{self.folder}/{self.filename}.json"):
            try:
                with open(f"plugins/py/{self.folder}/{self.filename}.json", "r", encoding=self.encoding) as file:
                    config = json.load(file)
            except:
                with open(f"plugins/py/{self.folder}/{self.filename}.json", "r", encoding="gbk") as file:
                    config = json.load(file)
            return config
        else:
            return {}
    
    def save(self, config={}):
        with open(f"plugins/py/{self.folder}/{self.filename}.json", 'w+', encoding=self.encoding) as file:
            json.dump(config, file, indent='\t', ensure_ascii=False)
    
    def make(self, config={}):
        if not os.path.exists(f"plugins/py/{self.folder}/{self.filename}.json"):
            os.makedirs(f"plugins/py/{self.folder}", exist_ok=True)
            self.save(config)
            return True
        else:
            return False


class Pointer:
    def __init__(self, pointer: int, data_type: type):
        self.pointer = ctypes.cast(pointer, ctypes.POINTER(data_type))

    def get(self):
        return self.pointer.contents.value

    def set(self, value: any):
        self.pointer.contents.value = value


class FileMonitor:
    def __init__(self, path="plugins/py/", callback=reload, args=("",), interval=1):
        """
        :param path: file or folder path
        :param callback: callback function
        :param args: callback function arguments
        :param interval: monitoring interval, in seconds
        """
        self.path = path
        self.callback = callback
        self.args = args
        self.interval = interval
        self.hash = self.get_hash()
        self.loop = True
        self.thread = threading.Thread(target=self.monitor, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.loop = False

    def get_hash(self):
        # Get file or folder hash
        if os.path.isdir(self.path):
            md5 = hashlib.md5()
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    with open(os.path.join(root, file), 'rb') as f:
                        while True:
                            data = f.read(8192)
                            if not data:
                                break
                            md5.update(data)
            return md5.hexdigest()
        else:
            md5 = hashlib.md5()
            with open(self.path, 'rb') as f:
                while True:
                    data = f.read(8192)
                    if not data:
                        break
                    md5.update(data)
            return md5.hexdigest()

    def monitor(self):
        while self.loop:
            time.sleep(self.interval)
            new_hash = self.get_hash()
            if new_hash != self.hash:
                if self.callback.__name__ == "reload":
                    self.loop = False
                self.hash = new_hash
                self.callback(*self.args)
