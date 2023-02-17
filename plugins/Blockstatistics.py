#-*- coding: utf-8 -*-
import mc

logger = mc.Logger(__name__)
conf_mgr = mc.ConfigManager(__name__)

data = {}
can_save = 0
def init():
	global data
	conf_mgr.make(data)
	data = conf_mgr.read()
	

def save():
	conf_mgr.save(data)


def onDestroyBlock(e):
	global can_save
	global data
	player = e['player']
	name = player.name
	
	if name in data:
		data[name] += 1
	else:
		data[name] = 1
	if can_save == 50:
		save()
		can_save = 0
	else:
		can_save += 1
	return True

# 通过字典的 值 返回 键
def get_keys(dict, value):
    return [key for key,v in dict.items() if v == value]

def onCmd(e):
	if e['cmd'] == "/stat" or e['cmd'] == "/statt":
		playerNameList = getPlayerNameList()
		playerList = "\""
		sortedData = sorted(data.values(), reverse=True)
		for count in sortedData:
			savedName = get_keys(data, count)[0]
			if e['cmd'] == "/statt":
				# 高亮（黄色）执行命令的玩家的名字
				if e['player'].name == savedName:
					playerList += f"§e{savedName} : §a{str(count)}\n"
					continue
				playerList += f"§b{savedName} : §a{str(count)}\n"
			if e['cmd'] == "/stat":
				# 高亮（黄色）执行命令的玩家的名字
				if e['player'].name == savedName:
					playerList += f"§e{savedName} : §a{str(count)}\n"
					continue
				for name in playerNameList:
					# 将非在线玩家剔除
					if savedName != name:
						continue
					playerList += f"§b{savedName} : §a{str(count)}\n"
		playerList += "\""
		e['player'].sendCustomForm('{"content":[{"type":"label","text":' + playerList + '}], "type":"custom_form","title":"挖掘榜"}')
		return False

#获取玩家列表
def getPlayerNameList():
	playerNameList = []
	playerList = mc.getPlayerList()
	for player in playerList:
		playerNameList.append(player.name)
	return playerNameList

init()
def join(player):
	save()
def exit(player):
	save()
mc.setListener('onJoin', join)
mc.setListener('onLeft', exit)
mc.setListener('onPlayerCmd',onCmd)
mc.setListener('onDestroyBlock', onDestroyBlock)
mc.setCommandDescription('stat','在线挖掘榜')
mc.setCommandDescription('statt','总挖掘榜')
logger.info("Loaded!")
