import mc
import time
import os

logger = mc.Logger(__name__)

def onPlayerCmd(e):
    player = e['player']
    cmd = e["cmd"]
    data = f"{str(int(player.pos[0]))} {str(int(player.pos[1]) - 1)} {str(int(player.pos[2]))}, {cmd}"
    logger.info(f"<{player}>-><CMD> {data}")

def logChat(e):
    sender = e['sender']
    target = e['target']
    msg = e['msg']
    if target == "":
        pass
    else:
        logger.info(f"<{sender}>-><{target}> {msg}")

def onInputText(e):
    sender = e['player']
    msg = e['msg']
    logger.info(f"<{sender}> {msg}")
        
mc.setListener("onPlayerCmd", onPlayerCmd)
mc.setListener('onChat', logChat)
mc.setListener('onInputText', onInputText)
