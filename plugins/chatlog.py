import mc
import time
import os


def logout(*content, name: str = "Plugin", level: str = "INFO", info: str = ""):
    mc.log(content, name = __name__, level = level, info = info)

def onPlayerCmd(e):
    player = e['player']
    cmd = e["cmd"]
    data = f"{str(int(player.pos[0]))} {str(int(player.pos[1]) - 1)} {str(int(player.pos[2]))}, {cmd}"
    logout(f"<{player}>-><CMD> {data}")

def logChat(e):
    sender = e['sender']
    target = e['target']
    msg = e['msg']
    if target == "":
        pass
    else:
        logout(f"<{sender}>-><{target}> {msg}")

def onInputText(e):
    sender = e['player']
    msg = e['msg']
    logout(f"<{sender}> {msg}")
        
mc.setListener("onPlayerCmd", onPlayerCmd)
mc.setListener('onChat', logChat)
mc.setListener('onInputText', onInputText)
