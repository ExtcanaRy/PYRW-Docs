# teleport

# Introduction

This plugin is a teleport family bucket, providing home, tpa, tpah, warp and other functions

# Download

[here](https://extcanary.github.io/PYRW-Docs/plugins/teleport.py "click me to download")

# configuration file

| configuration file path | plugins/py/teleport/teleport.json                                                                                                                                                                           |
| ----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| configure projects      | explain                                                                                                                                                                                                     |
| wait_time               | The tpa timeout period in seconds                                                                                                                                                                           |
| max_home                | The maximum number of people per player                                                                                                                                                                     |
| lockTime                | The cooldown time after a player completes a random teleport, in seconds                                                                                                                                    |
| tpRange                 | The range of the random teleport.                                                                                                                                                                           |
| processTime             | The waiting time after the first teleportation to a high altitude, adjustable for servers with low configuration, but not too high, so that the player will fall to his death before tp reaches the ground. |
| tpHeight                | The height of the first time the player is sent to altitude.                                                                                                                                                |

## Default configuration/data file. Only the contents of `config` can be changed.

```json
{
	"config": {
		"maxHome": 10,
		"waitTime": 30,
		"lockTime": 300,
		"tpRange": 100000,
		"processTime": 5,
		"tpHeight": 500,
		"stepLenth": 10
	},
	"home": {},
	"warp": {}
}

```

# Available commands

| command | explanation                                                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /tpa    | tpa interface, request others to teleport to others                                                                                                                 |
| /tpah   | The tpahere interface, requesting others to teleport to you                                                                                                         |
| /tpac   | Accept teleport request                                                                                                                                             |
| /tpad   | Reject transfer request                                                                                                                                             |
| /home   | hone interface                                                                                                                                                      |
| /warp   | warp interface, teleportation point                                                                                                                                 |
| /tpr    | Random teleportation -- This feature is currently unstable and may fail or crash, please practice landing water before using it! Failure consequences are your own! |
