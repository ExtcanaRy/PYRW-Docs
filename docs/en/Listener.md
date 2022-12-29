---
sort: 2
---
# Listener
Event description format.

```
Listener keyword
Introduction
Can intercept
return data
```

# Listener

Event Listener

* Use setListener to set the listener
* The callback function has one and only one parameter and is of type dictionary

The following are all events.

# onConsoleInput

Can the console input listener intercept: is the return data: ## onConsoleInput

* cmd - command data

## onConsoleOutput

Can the console output listener intercept: Yes or No.

* output - output information

## onPlayerJoin

PlayerJoin ServerListeningInterceptedCan: NoData returned: * player - PlayerJoin

* player - player

## onPlayerLeft

Can the player leaving the server listen to the interception: No.

* player - Player

## onPlayerAttack

Can the player attack listener intercept: Yes Return data: * player - player ## onPlayerAttack

* actor - attacked entity
* player - player

## onSelectForm

Can the player select GUI form listener intercept: Yes or No. Return data: * actor - the attacked entity

* formid - Form ID
* selected - information about the selected item returned by the form
* player - player

## onUseItem

Use item listener `Note: Win10 client use item event will be triggered multiple times within a single click ` Interception allowed: Yes return data: * position - the location of the operation cube

* position - the location of the operation cube
* itemid - item ID
* itemaux - item special value
* itemname - the name of the item
* player - player

## onPlaceBlock

Can the onPlaceBlock listener intercept: is the return data: ## onPlaceBlock

* position - the location of the action block
* blockid - block ID
* blockname - the name of the block
* player - player

## onDestroyBlock

Can the destroy block listener intercept: is returning data: * position - the location of the block

* position - the location of the operation block
* blockid - block ID
* blockname - the name of the block
* player - player

## onOpenChest

Can the openChest listener intercept: is the return data: ## onChest

* position - the location of the operating block
* player - player

## onCloseChest

Can the CloseChest listener intercept: No. Return data: * position - the location of the action cube

* position - the location of the operation cube
* player - the player

## onOpenBarrel

Can the open barrel listener intercept: No Data returned: * position - the location of the action square

* position - the location of the action box
* player - the player

## onCloseBarrel

CloseBarrelListeningInterceptedCan: NoData returned: * position - the location of the action square

* position - the location of the action barrel
* player - the player

## onContainerChange

Putting in and taking out items listens to intercept whether or not: No. Return data: * itemid - item ID

* itemid - item ID
* itemcount - the number of items
* itemname - item name
* itemaux - the item's special value
* position - the location of the operation block
* blockid - block ID
* blockname - the name of the block
* slot - the position of the action grid
* player - player

## onChangeDimension

Can the onChangeDimension listener intercept: is the return data.

* player - player

## onMobDie

Creature Death Listening Interception Can: No Return data: * player - player ## onMobDie

* dmcase - damage specific cause ID
* actor1 - the entity that died
* actor2 - damage source entity

## onMobHurt

The creature injury listener can use setDamage to set the damage value under this listener Interceptable: yes Return data: * dmcase - the damage specific cause ID * actor1 - the death entity

* dmcase - Damage specific cause ID
* actor1 - the entity that died
* actor2 - damage source entity
* damage - theoretical damage value

## onRespawn

Player respawn listener can intercept: no Return data.

* player - player

## onChat

Can the chat listener intercept: No. Return data: ## onChat

* sender - sender's name
* target - the name of the receiver
* msg - the received message
* style - the type of chat

## onInputText

Can the player input text listener intercept: is the return data.

* msg - the input text
* player - the player

## onCommandBlockUpdate

Can the player update the command block listener intercept: Yes or No.

* player - the player
* cmd - the new command that will be updated
* mode - command block mode
* condition - if there is a condition
* redstone - whether to redstone or not
* output - last output
* rawname - the name of the command cube
* delay - delay
* position - the location of the command block

## onInputCommand

Can the player input command listener intercept: is the return data.

* cmd - the command entered by the player
* player - the player

## onCommandBlockPerform

CommandBlockPerform CommandBlockPerform CommandBlockListeningInterceptable: Yes or No

* cmd - the command that will be executed
* rawname - the name of the command block
* position - the location of the executor
* mode - the mode of the command block
* condition - whether there is a condition

## onLevelExplode

Can the explosion listener intercept: yes return data: ## onLevelExplode

* actor - the exploder entity (this is invalid for bed explosion)
* position - the location of the explosion point
* dimensionid - the dimension ID of the exploder
* power - the strength of the explosion

## onSetArmor

Can the player wear a listener intercept: No Return data: ## onSetArmor

* player - player
* itemid - item ID
* itemcount - number of items
* itemname - item name
* itemaux - item special value
* slot - the position of the action grid

## onFallBlockTransform

Can the farming damage listener intercept: is returning data: ## onFallBlockTransform

* player - player
* position - the location of the square
* dimensionid - the dimension ID of the dimension in which it is located

## onUseRespawnAnchorBlock

Can the onUseRespawnAnchorBlock listener intercept: yes return data: * player - player

* player - player
* position - the location of the block
* dimensionid - the dimension ID of the block

## onScoreChanged

Can the scoreboard change listener intercept: No Data returned: * player - the player's position * position - the location of the square * dimensionid - the dimension ID of the player

* scoreboardid - scoreboard ID
* playersnum - player score
* objectivename - the actual name of the object
* objectivedisname - the object's display name

## onMove

Player Move Listening Intercepted Can: No Return data: ## player - player

* player - player

## onPistonPush

Can the piston push listener intercept: No. Return data: ## onPistonPush

* blockname - block name
* blockid - block ID
* blockpos - block coordinates
* pistonpos - piston coordinates
* dimensionid - dimension ID

## onEndermanRandomTeleport

Can the onEndermanRandomTeleport listener intercept: is the return data.

* actor - entity

## onServerStarted

ServerStarted finish listening to intercept Can: No Return data: * actor - entity

* none - none

## onDropItem

Can the player drop item listener intercept: Yes Data returned: * player - player

* player - player
* itemid - item ID
* itemcount - number of items
* itemname - item name
* itemaux - item's special value

## onTakeIte

Can the player pick up the item listener intercept: is the return data: ## onTakeIte

* player - player
* actor - the item being picked up

## onRide

Can the creature ride listener intercept: yes return data: * actor1 - rider

* actor1 - rider
* actor2 - ridden

## onUseFrameBlock

Can the onUseFrameBlock listener intercept: Yes or No.

* player - player
* blockpos - block coordinates
* dimensionid - the dimension of the block

## onJump

Can the player jump listener intercept: No Data returned: * player - player

* player - player

## onSneak

Player Sneak Listening
Can intercept: No
Return data.
*player - player

## onBlockInteracted

Block Accepted Player Interaction Listening Interceptable: Yes Return Data:

* player - player
* blockpos - block coordinates
* blockname - block name
* blockid - block ID
* dimensionid - block dimension

## onBlockExploded

Block is exploded listen to intercept whether: no return data.

* actor - exploded entity
* blockpos - block coordinates
* blockname - block name
* blockid - block ID
* dimensionid - the dimension of the block

## onUseSignBlock

Can the signboard use a listener to intercept: is the return data.

* player - player
* text - text content
* position - coordinates
