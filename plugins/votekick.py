import json
import threading

import mc

logger = mc.Logger(__name__)
conf_mgr = mc.ConfigManager(__name__)

config = {}
config['tax'] = 1 / 3
config['reset_time'] = 300
config['ban_time'] = 600

conf_mgr.make(config)
config = conf_mgr.read()

tax = config['tax']
reset_time = config['reset_time']
ban_time = config['ban_time']

formid = 0
reported_name_list = []
reporter_name_list = []
ban_name_list = []
label = False

def get_player_name_list():
    global totalPlayer, player_name_list
    player_name_list = []
    for pl in mc.getPlayerList():
        player_name_list.append(pl.name)
    totalPlayer = len(player_name_list)

def onPlayerCmd(e):
    if e['cmd'] == "/vklist":
        e['player'].sendTextPacket("The players who have been voted:" + json.dumps(reported_name_list))
        return False
    if e['cmd'] == "/vk":
        get_player_name_list()
        reporter = e['player']
        for i in reporter_name_list:
            if i == reporter.name:
                reporter.sendTextPacket("You have voted, please wait for the next round of voting!")
                return False
        reporter.sendCustomForm('{"content":[{"default":0,"options":'+json.dumps(player_name_list)+',"type":"dropdown","text":"Please select the player you want to vote for"}],"type":"custom_form","title":"VOTEKICK"}', onSelectForm)
        return False

def onSelectForm(player, selected):
    global label
    global reset_time
    if selected == "null":
        return False
    selected = json.loads(selected)[0]
    player.sendTextPacket("Voting success!")
    reporter_name_list.append(player.name)
    player.sendTextPacket("Players who have voted: " + json.dumps(reporter_name_list))
    if label:
        return False
    player.sendTextPacket(f"You have created a vote to kick out, valid for {reset_time / 60} minutes")
    label = True
    t = threading.Timer(reset_time, vote_finished)
    t.setDaemon(True)
    t.start()

    reported_name_list.append(player_name_list[selected])
    most_appear_player_name = max(set(reported_name_list), key=reported_name_list.count)
    most_appear_player_count = reported_name_list.count(most_appear_player_name)
    if most_appear_player_count >= totalPlayer * tax and most_appear_player_count >= 3:
        for pl in mc.getPlayerList():
            if pl.name == most_appear_player_name:
                pl.disconnect(f"You have been voted to kick out, please wait for {ban_time / 60} minutes!")
        for pl in mc.getPlayerList():
            pl.sendTextPacket(f"[VOTEKICK] {most_appear_player_name} has been kick by report, the number of {most_appear_player_count}")
        logger.info(f"{most_appear_player_name} has been kicked out of the vote, the number of votes: {most_appear_player_count}")
        ban_name_list.append(most_appear_player_name)
        t = threading.Timer(ban_time, cancle_ban)
        t.setDaemon(True)
        t.start()
        vote_finished()

def ban(player):
    for player_name in ban_name_list:
        if player.name == player_name:
            player.disconnect(f"You have been voted to kick out, please wait for {ban_time / 60} minutes!")

def cancle_ban():
    ban_name_list.remove(ban_name_list[0])

def vote_finished():
    global label,reporter_name_list,reported_name_list
    label = False
    reporter_name_list = []
    reported_name_list = []
    for pl in mc.getPlayerList():
        pl.sendTextPacket(f"[VOTEKICK] The last round of voting has ended!")

mc.setListener('onJoin', ban)
mc.setListener('onPlayerCmd', onPlayerCmd)
mc.setCommandDescription('vk', f'Vote kickout, votes will be kicked out when the number of votes reaches {str(tax * 100)[0:3]}%% of the number of people online')
mc.setCommandDescription('vklist','View the players who have been voted')

logger.info("Loaded! Author: ExtcanaRy")
