# API
# Function description format.

```
Function Prototypes
Introduction
```

# mc

Introduction: `mc` is a built-in module of BDSpyrunner

## getBDSVersion() -> str

Get the version number of BDS

## logout(msg:str) -> None

Standard output stream sends output messages to the console (interceptable)

## runcmd(cmd:str) -> None

Execute a console command

## setListener(key:str,callback:function) -> None

Bind the callback to the key event, and the callback will be called when the event is triggered.
The available keys can be found in the Listener interface

## removeListener(key:str,callback:function) -> None

Remove the set listener, the corresponding callback will no longer be called when the event occurs after the removal.

## setCommandDescription(cmd:str,callback:function，description:str) -> None

Set the command description, parameter three is an optional parameter that
Used to trigger the command callback, callback function prototype: callback(player:mc.Entity) -> None

## getPlayerByXuid(xuid:str) -> mc.Entity

Get player based on Xuid

## getPlayerList() -> list

Get a list of online players

## setDamage(dmg:int) -> None

Set the damage value of the creature wounded
Note: This function can only be called with the `onMobHurt` event.

## setServerMotd(motd:str)

Set the server motd name

## getBlock(x:int,y:int,z:int,did:int) -> dict

Get the information of the specified location block

## setBlock(name:str,x:int,y:int,z:int,did:int) -> none

Set the block at the specified position, name must be in camel case, e.g. RedStoneOre

## getStructure(x1:int,y1:int,z1:int,x2:int,y2:int,z2:int,did:int) -> str

Get the structure nbt data between two coordinates

## setStructure(data:str,x:int,y:int,z:int,did:int) -> None

Set a structure at (x,y,z), data is the structure JSON string

## getStructureRaw(x1:int,y1:int,z1:int,x2:int,y2:int,z2:int,did:int) -> str

Get the binary NBT structure data from the specified location

## setStructureRaw(data:str,x:int,y:int,z:int,did:int) -> None

Export structure from binary NBT structure data to the specified location

## explode(x:float,y:float,z:float,did:int,power:float,destroy:bool,range:float,fire:bool) -> None

Generate an explosion

## spawnItem(data:str,x:int,y:int,z:int,did:int) -> None

Generate a dropped item, with data as the item JSON string

## isSlimeChunk(x:int,y:int) -> Boolean

Check if it is a slime block

## setSignBlockMessage(msg:str,x:int,y:int,z:int,did:int) -> None

Set the token text

## class Entity

Introduction: Entity class, including players, creatures, and entities.

# Entity's properties

1. name:str - Entity name (modifiable)
2. uuid:str - Player UUID
3. xuid:str - Player XUID
4. pos:list - Entity coordinates
5. did:int - Entity dimension ID
6. is_standing:bool - Whether the entity is standing on the block
7. is_sneaking:bool - Whether the entity is sneaked
8. health:int - Entity current health
9. maxhealth:int - Entity max health
10. perm:int - Player permission value (modifiable, with 0,1,2,3,4)
11. platform_online_id:str - Player device ID
12. platform:int - Player device OS (1 for Android, 7 for Win10)
13. IP:str - Player P

### getAllItem() -> str

Get all the player's items, the return value is a JSON string, there are five containers: Hand,OffHand,Inventory,Armor,EndChest

### setAllItem(data:str) -> None

Set the player all items, data is JSON string, there are four kinds of containers: OffHand,Inventory,Armor,EndChest

### setHand(data:str) -> None

Set the item in the player's hand, data as JSON string

### addItem(data:str) -> None

Add a new item for the player, data is a JSON string

### removeItem(slot:int,count:int) -> None

Remove count items from the player's backpack slot.

### openInventoryGUI() -> None

Open the player's Inventory GUI

### teleport(x:float,y:float,z:float,did:int) -> None

Teleport the player to the specified coordinates and dimensions

### sendCommandPacket(cmd:str) -> None

Simulates the player sending command packets, i.e. executing commands for the player

### sendTextPacket(msg:str,type:int = 0) -> None

Simulates the player sending a text packet, type = 0 is the original text, equivalent to the command tellraw, type = 1 is the chat text, equivalent to the player speaking

### resendAllChunks() -> None

Resending the player client's map blocks may cause brightness rendering problems

### disconnect(msg:str = '')

Disconnect the player, msg will be displayed on the screen after the player is disconnected

### transferServer(ip:str,port:int) -> None

Transferring players to the designated server

### getScore(scoreboard:str) -> int

Get the player's score on the scoreboard called scoreboard

### setScore(scoreboard:str,count:int) -> None

Set the player's score on the scoreboard called scoreboard

### addScore(scoreboard:str,count:int) -> None

Increase the player's score on the scoreboard called scoreboard

### reduceScore(scoreboard:str,count:int) -> None

Reduce the player's score on the scoreboard called scoreboard

### addLevel(level:int) -> None

Increase player experience level

### setBossBar(msg:str,percent:float) -> None

Set the player BOSS bar, percent is the blood bar percentage (min:0,max:1)

### removeBossBar() -> None

Remove player boss bar

### addTag(name:str) -> None

Add Tag

### removeTag(name:str) -> None

Remove Tag

### getTags() -> list

Get Tags

### setSidebar(title:str,content:str) -> None

Set player scoreboard sidebar
Example:`player.setSidebar('Custom Sidebar', '{"first row":0, "second row":2, "Which row am I on?" :3}')`

### removeSidebar() -> None

Remove player scoreboard sidebar

### sendCustomForm(data:str,callback:function) -> None

Send a custom form to the specified player, the callback function prototype is callback(Entity:player,selected_data:str) -> None
Example:player.sendCustomForm('{"content":[{"type": "label", "text": "This is a text label"},{"placeholder": "Watermark text", "default":"", "type": "input", "text":" "},{"default":true, "type": "toggle", "text": "switch~ maybe"},{"min":0.0, "max":10.0, "step":2.0, "default":3.0, "type": "slider", "text": "Cursor slider! "} ,{"default":1, "steps":["Step1", "Step2", "Step 3"], "type": "step_slider", "text": "Matrix slider?!"} ,{"default":1, "options":["Option 1", "Option2", "Option3"], "type": "dropdown", "text": "As you can see Dropdown box"}], "type": "custom_form", "title": "This is a custom form"}', cb)

### sendSimpleForm(title:str,content:str,buttons:list,images:list,callback:function) -> None

Send a simple form to the specified player, callback function prototype is callback(Entity:player,selected_item:int) -> None
Example:player.sendSimpleForm('title', 'content', ["survive", "die", "help"], ['', '', ''], cb)

### sendModalForm(title:str,content:str,button1:str,button2:str,callback:function) -> None

Send a modal dialog to the specified player, the callback function prototype is callback(Entity:player,selected_item:bool) -> None
Example:player.sendModalForm('title', 'content', 'button1', 'button2', cb)
