import mc
import time
import os


logger = mc.Logger(__name__)


def writeLog(mode, player, data):
    day = time.strftime("%Y-%m-%d")
    if not os.path.exists(f"logs/{day}"):
        os.makedirs(f"logs/{day}")
    fileName = f"logs/{day}/{mode}.log"
    with open(fileName, 'a') as fileObject:
        fileObject.write(f"{getTime()}, {player.name}, {data}\n")
        fileObject.close()


def getTime():
    return time.strftime("%H:%M:%S")


def onUseItem(e):
    player = e['player']
    blockPos = e['position']
    data = f"{str(int(player.pos[0]))} {str(int(player.pos[1]) - 1)} {str(int(player.pos[2]))}, {str(blockPos[0])} {str(blockPos[1])} {str(blockPos[2])}, {e['itemname']}"
    writeLog("useItem", e['player'], data)


def onPlaceBlock(e):
    blockPos = e['position']
    #blockName = e['blockname'][10:]
    blockName = e['blockid']
    data = f"{str(blockPos[0])} {str(blockPos[1])} {str(blockPos[2])}, Place, {blockName}"
    writeLog("Block", e['player'], data)


def onDestroyBlock(e):
    blockPos = e['position']
    #blockName = e['blockname'][10:]
    blockName = e['blockid']
    data = f"{str(blockPos[0])} {str(blockPos[1])} {str(blockPos[2])}, Destory, {blockName}"
    writeLog("Block", e['player'], data)


def onOpenContainer(e):
    blockPos = e['position']
    data = f"{str(blockPos[0])} {str(blockPos[1])} {str(blockPos[2])}"
    writeLog("Container", e['player'], data)


def onPlayerCmd(e):
    player = e['player']
    cmd = e["cmd"]
    data = f"{str(int(player.pos[0]))} {str(int(player.pos[1]) - 1)} {str(int(player.pos[2]))}, {cmd}"
    writeLog("CMD", e['player'], data)


def logChat(e):
    sender = e['sender']
    target = e['target']
    msg = e['msg']
    if target == "":
        pass
        #logger.info(f"<{sender}> {msg}")
    else:
        logger.info(f"<{sender}>-><{target}> {msg}")

    day = time.strftime("%Y-%m-%d")
    if not os.path.exists(f"logs/{day}"):
        os.mkdir(f"logs/{day}")
    fileName = f"logs/{time.strftime('%Y-%m-%d')}/Chat.log"
    with open(fileName, 'a') as fileObject:
        fileObject.write(f"{getTime()}, {sender}, {target}, {msg}")
        fileObject.close()


def onInputText(e):
    sender = e['player']
    msg = e['msg']
    logger.info(f"<{sender}> {msg}")
    day = time.strftime("%Y-%m-%d")
    if not os.path.exists(f"logs/{day}"):
        os.mkdir(f"logs/{day}")
    fileName = f"logs/{time.strftime('%Y-%m-%d')}/ChatONLY.log"
    with open(fileName, 'a') as fileObject:
        fileObject.write(f"{getTime()}, {sender}, {msg}")
        fileObject.close()


mc.setListener("onUseItem", onUseItem)
mc.setListener("onPlaceBlock", onPlaceBlock)
mc.setListener("onDestroyBlock", onDestroyBlock)
mc.setListener("onOpenContainer", onOpenContainer)
mc.setListener("onOpenContainer", onOpenContainer)
mc.setListener("onPlayerCmd", onPlayerCmd)
mc.setListener('onChat', logChat)
mc.setListener('onInputText', onInputText)
logger.info(f"Loaded!")
