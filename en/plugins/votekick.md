# votekick

# Introduction

Let players vote to kick out players when the administrator is not online

# Download

[here](https://pyr.jfishing.love/plugins/votekick.py "click me to download")

# Configuration file

The configuration file is located in `plugins/py/votekick/votekick.json`

| Configuration Items | Explanation                                                                                                                                                                                                                                                            |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tax                 | The ratio of votes to the total number of players online, 0.333 means one-third, which means a player will be kicked out when the number of votes cast reaches one-third of the total number of players currently online. Reference: 0.666 (two-thirds) 0.5 (one-half) |
| resetTime           | The duration of each vote, after which time the player is not kicked out, the voting data is reset, in seconds.                                                                                                                                                        |
| banTime             | The time when the kicked player is forbidden to enter the server again, equivalent to ban for a period of time, unit:sec                                                                                                                                               |

# Default configuration file

```json
{
	"tax": 0.333333333333333333,
	"reset_time": 300,
	"ban_time": 600
}
```

# Available commands

| command | explanation                                                                               |
| ------- | ----------------------------------------------------------------------------------------- |
| /vk     | Vote kickout, votes will be kicked out when it reaches xx% of the number of people online |
| /vklist | View the players who have voted                                                           |
