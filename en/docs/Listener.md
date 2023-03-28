# Listener

Event description format:

```format
Listener keyword
Introduction
Can intercept
return data
```

## Event listener

* Use ``setListener`` to set the listener
* Use ``removeListener`` to remove the listener
* The callback function has one and only one argument, is of type dictionary, and needs to access data using subscripts, e.g. ``onPlayerAttack``:

```python
def onPlayerAttack(event):
    actor = event['actor']
    player = event['player']
    damage_ptr = event['damage']
    print(player.name, " == ", event['player'].name)
```

* When there is only one data return, you can use parameters directly as data without subscript access, e.g. ``onConsoleInput``:

```python
def onConsoleInput(event):
    print("Input: ", event)
```

## onConsoleInput

* Console input listener
* Can intercept: Yes
* Return data:


* ``cmd`` - command data

## onConsoleOutput

* Console output listener
* Can intercept: Yes
* Return data:


* ``output`` - output information

## onPlayerJoin

* Player join server listener
* Can intercept: No
* Return data:


* ``player`` - player

## onPlayerLeft

* Player leaving the server listener
* Can intercept: No
* Return data:


* ``player`` - player

## onPlayerAttack

* Player attack listener
* Can intercept: Yes
* Return data:


* ``actor: object`` - the attacked entity
* ``player: object`` - the player
* ``damage: pointer.c_float`` - the damage

## onSelectForm

* Player selection GUI form listener
* Can intercept: Yes
* Return data:


* ``formid`` - Form ID
* ``selected`` - the information about the selected item returned by the form
* ``player`` - the player

## onUseItem

* Use item listener
* Note: Win10 client use item event will trigger multiple times within a single click
* Can intercept: Yes
* Return data:


* ``player`` - player
* ``itemid`` - item ID
* ``itemaux`` - item aux value
* ``itemcount`` - number of items
* ``itemname`` - the name of the item
* ``blockname`` - the name of the block being manipulated
* ``blockid`` - ID of the block being manipulated
* ``position`` - the coordinates of the block being manipulated

## onUseItemEx

* Using item listener (optimized version)
* Can intercept: Yes
* Return data:


* ``player`` - the player
* ``itemid`` - item ID
* ``itemaux`` - item special value
* ``itemcount`` - number of items
* ``itemname`` - the name of the item

## onPlaceBlock

* Place Block listener
* Can intercept: Yes
* Return data:


* ``position`` - the location of the action block
* ``blockid`` - block ID
* ``blockname`` - the name of the block
* ``player`` - player

## onPlacedBlock

* Placed Block listener
* Can intercept: No
* Return data:


* ``position`` - the location of the action block
* ``blockid`` - block ID
* ``blockname`` - the name of the block
* ``player`` - player

## onDestroyBlock

* Destroy block listener
* Can intercept: Yes
* Return data:


* ``position`` - the location of the manipulated block
* ``blockid`` - block ID
* ``blockname`` - the name of the block
* ``player`` - player

## onDestroyedBlock

* Destroyed block listener
* Can intercept: No
* Return data:


* ``position`` - the location of the manipulated block
* ``blockid`` - block ID
* ``blockname`` - the name of the block
* ``player`` - player

## onOpenChest

* OpenChest listener
* Can intercept: Yes
* Return data:


* ``position`` - the location of the operation cube
* ``player`` - the player

## onCloseChest

* Close chest listener
* Can intercept: No
* Return data:


* ``position`` - the location of the action box
* ``player`` - the player

## onOpenBarrel

* Open barrel listener
* Can intercept: No
* Return data:


* ``position`` - the location of the action square
* ``player`` - the player

## onCloseBarrel

* Close barrel listener
* Can intercept: No
* Return data:


* ``position`` - the location of the action barrel
* ``player`` - the player

## onContainerChange

* Put in and take out item listener
* Can intercept: No
* Return data:


* ``itemid`` - item ID
* ``itemcount`` - the number of items
* ``itemname`` - the name of the item
* ``itemaux`` - the item's special value
* ``position`` - the location of the operation block
* ``blockid`` - block ID
* ``blockname`` - the name of the block
* ``slot`` - the position of the action grid
* ``player`` - player

## onPlayerInventoryChange

* Player inventory content change listener
* Can intercept: No
* Return data:


* ``itemid`` - item ID
* ``itemcount`` - the number of items
* ``itemname`` - the name of the item
* ``itemaux`` - the item's special value
* ``slot`` - the position of the action grid
* ``player`` - player

## onChangeDimension

* Switching dimension listener
* Can intercept: Yes
* Return data:


* ``player`` - player

## onMobDie

* Creature death listener
* Can intercept: No
* Return data:


* ``dmcase`` - Damage specific cause ID
* ``actor1`` - death entity
* ``actor2`` - the source entity of the damage

## onMobHurt

* The mob hurt listener
* Can use setDamage to set the damage value under this listener
* Can intercept: Yes
* Return data:


* ``dmcase`` - Damage specific cause ID
* ``actor1`` - the entity that died
* ``actor2`` - Damage source entity
* ``damage`` - theoretical damage value

## onRespawn

* Player respawn listener
* Can intercept: No
* Return data:


* ``player`` - player

## onChat

* Chat listener
* Can intercept: No
* Return data:


* ``sender`` - sender's name
* ``target`` - the name of the receiver
* ``msg`` - the received message
* ``style`` - the type of chat

## onInputText

* Player input text listener
* Can intercept: yes
* Return data:


* ``msg`` - the input text
* ``player`` - the player

## onCommandBlockUpdate

* Player update command block listener
* Can intercept: Yes
* Return data:


* ``player`` - player
* ``cmd`` - the new command that will be updated
* ``mode`` - command cube mode
* ``condition`` - if there is a condition
* ``redstone`` - whether to redstone or not
* ``output`` - last output
* ``rawname`` - the name of the command cube
* ``delay`` - delay
* ``position`` - the location of the command block

## onInputCommand

* Player input command listener
* Can intercept: Yes
* Return data:


* ``cmd`` - the command entered by the player
* ``player`` - the player

## onCommandBlockPerform

* Command Block Perform Listens for commands
* Can intercept: Yes
* Return data:


* ``cmd`` - the command that will be executed
* ``rawname`` - the name of the command block
* ``position`` - the location of the executor
* ``mode`` - the mode of the command block
* ``condition`` - whether there is a condition

## onLevelExplode

* Explosion Listening
* Can intercept: yes
* Return data:


* ``actor`` - the exploder entity (this is invalid when the bed explodes)
* ``position`` - the location of the explosion point
* ``dimensionid`` - the dimension ID of the exploder
* ``power`` - the strength of the explosion

## onSetArmor

* Player wear listener
* Can intercept: no
* Return data:


* ``player`` - player
* ``itemid`` - item ID
* ``itemcount`` - number of items
* ``itemname`` - item name
* ``itemaux`` - item's special value
* ``slot`` - the position of the action grid

## onFallBlockTransform

* Plot destruction listener
* Can intercept: Yes
* Return data:


* ``player`` - player
* ``position`` - the location of the block
* ``dimensionid`` - the ID of the dimension it is in

## onUseRespawnAnchorBlock

* Use the respawn anchor listener
* Can intercept: yes
* Return data:


* ``player`` - player
* ``position`` - the location of the block
* ``dimensionid`` - the ID of the dimension it is in

## onScoreChanged

* Scoreboard change listener
* Can intercept: No
* Return data:


* ``scoreboardid`` - scoreboard ID
* ``playersnum`` - the player score
* ``objectivename`` - the actual name of the object
* ``objectivedisname`` - the object's display name

## onMove

* Player Move Listening
* Can intercept: No
* Return data:


* ``player`` - player

## onPistonPush

* Piston push listener
* Can intercept: No
* Return data:


* ``blockname`` - the name of the block
* ``blockid`` - block ID
* ``blockpos`` - block coordinates
* ``pistonpos`` - piston coordinates
* ``dimensionid`` - dimension ID

## onEndermanRandomTeleport

* Enderman Random Teleport Listening
* Can intercept: Yes
* Return data:


* ``actor`` - entity

## onServerStarted

* Server start completion listener
* Can intercept: No
* Return data:


* ``none`` - none

## onDropItem

* Player drop item listener
* Can intercept: Yes
* Return data:


* ``player`` - player
* ``itemid`` - item ID
* ``itemcount`` - number of items
* ``itemname`` - item name
* ``itemaux`` - item special value

## onTakeIte

* Player picking up items listens
* Can intercept: Yes
* Return data:


* ``player`` - the player
* ``actor`` - the picked up item

## onRide

* Creature Ride Listening
* Can intercept: Yes
* Return data:


* ``actor1`` - rider
* ``actor2`` - the rider

## onUseFrameBlock

* Operation display frame listener
* Can intercept: Yes
* Return data:


* ``player`` - player
* ``blockpos`` - block coordinates
* ``dimensionid`` - the dimension of the block

## onJump

* Player jump listener
* Can intercept: No
* Return data:


* ``player`` - player

## onSneak

* Player sneak listener
* Can intercept: No
* Return data:


* ``player`` - player

## onBlockInteracted

* The block accepts player interaction listeners
* Can intercept: Yes
* Return data:


* ``player`` - player
* ``blockpos`` - block coordinates
* ``blockname`` - block name
* ``blockid`` - block ID
* ``dimensionid`` - block dimension

## onBlockExploded

* Block exploded listens
* Can intercept: No
* Return data:


* ``actor`` - the entity that exploded
* ``blockpos`` - block coordinates
* ``blockname`` - block name
* ``blockid`` - block ID
* ``dimensionid`` - the dimension of the block

## onUseSignBlock

* Signboard use listener
* Can intercept: Yes
* Return data:


* ``player`` - player
* ``text`` - text content
* ``position`` - coordinates

## onLiquidSpread

* Liquid flow listener
* Can intercept: Yes
* Return data:


* ``src_name`` - name of the source block
* ``src_pos`` - coordinate of the source block
* ``dst_name`` - name of the block to be flowed to
* ``src_pos`` - coordinate of the block to be flowed to

## onChatPkt

* Send chat packet listener
* Can intercept: No
* Return data:


* ``player`` - player
* ``name_ptr: pointer.c_char_p`` - player name, set to empty string to show no player name
* ``msg_ptr: pointer.c_char_p`` - message
* ``xuid`` - player xuid

## onTick

* The time moment trigger listener, under normal circumstances, will trigger 20 times per second
* Can intercept: No
* Return data:


* ``null`` - empty string
