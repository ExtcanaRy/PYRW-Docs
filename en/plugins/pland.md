# pland

# pland

1. Compatible with old territorial data
2. Support all dimensions
3. Compatible with 2D territories and 3D territories
4. use scoreboard economy
5. add set territory default permission, prevent territory farming destruction, territory explosion, etc.
6. rich expansion interface

# Download

[main](https://pyr.jfishing.love/plugins/pland.py "click me to download")

[submodule](https://pyr.jfishing.love/plugins/landAPI.pyc "click me to download")

# Configuration file

##### 1. Folder

`pyplugins\land`

##### 2.config.json

| Project              | Explanation                                                                                                      | Allowed value types     |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------- |
| accuracy             | Accuracy. Recommended 10-500, the smaller the value the larger the memory footprint, but the faster the judgment | int                     |
| around_place         | Whether to allow preventing squares around the territory                                                         | bool                    |
| land_2D_buy_money    | 2D territory buy price                                                                                           | int                     |
| land_2D_maxsize      | The maximum size of a 2D territory                                                                               | int                     |
| land_2D_open         | 2D territory switch                                                                                              | bool                    |
| land_2D_sell_money   | 2D territory sell price                                                                                          | int                     |
| land_3D_buy_money    | 3D territory buy price                                                                                           | int                     |
| land_3D_maxsize      | 3D territory max size                                                                                            | int                     |
| land_3D_open         | Land_3D_open                                                                                                     | Land_3D_sell_money      |
| land_3D_sell_money   | land_3D_sell_money                                                                                               | 3D territory sell price |
| land_ender_open      | Mordecai Territory Switch                                                                                        | bool                    |
| land_maxnum          | Maximum number of territories a player can own                                                                   | int                     |
| land_nether_open     | hell_territory_switch                                                                                            | bool                    |
| land_teleport        | Whether players can teleport to territories                                                                      | bool                    |
| land_world_open      | main_world_territory_switch                                                                                      | bool                    |
| landop_xuid          | The xuid of the territory administrator, fill in the format ["xuid1", "xuid2"]                                   | list                    |
| menu_itemname        | The name of the item that opens the menu, such as compass for compass                                            | string                  |
| mobile_listener      | Whether or not to enable player movement listener, used for territory information display                        | bool                    |
| pistonBlock_listener | Whether or not to enable piston push/pull listener                                                               | bool                    |
| scoreboard           | The name of the scoreboard used by the economy                                                                   | string                  |
| playerbuyland        | Sets whether players can buy territories                                                                         | bool                    |
| version              | version                                                                                                          | string                  |

##### 3.config.json sample

```
{
    "accuracy": 10,
    "round_place": false,
    "land_2D_buy_money": 0,
    "land_2D_maxsize": 10000,
    "land_2D_open": true,
    "land_2D_sell_money": 0,
    "land_3D_buy_money": 1,
    "land_3D_maxsize": 100000,
    "land_3D_open": true,
    "land_3D_sell_money": 1,
    "land_ender_open": true,
    "land_maxnum": 10,
    "land_nether_open": true,
    "land_teleport": true,
    "land_world_open": true,
    "landop_xuid": [
        "2535424098181234",
        "2535416022290000",
        "2535445654591145"
    ],
    "menu_itemname": "compass",
    "mobile_listener": true,
    "pistonBlock_listener": true,
    "playerbuyland": true,
    "scoreboard": "money",
    "version": "1.2.0"
}
```

##### 4.land.json

Record data, do not modify it!

# Available commands

##### 1. In-game

| Commands | Explanation |
| ------------ | ---------------------- |
| /pland | Open menu |
| /plandremove | Force territory removal by territory administrator |

##### 2. Server Console

| Command | Explanation
| ------------- | ---------------------------------------------------------------------------- |
| plandreload | Reload the configuration file |
| oldlandreload | Convert the old territory data to the new version, the old territory is: land-g7.dll, do not delete the land folder when converting. | oldlandreload

# Call the interface

##### 1. Call the territory menu

```python
impot mc
landhelp=mc.getShareData('landhelp')
landhelp(player)
# Parameters: player pointer
```

##### 2. Core function interface

```python
lapi=mc.getShareData('landAPI')
# Please don't use the impot method

lapi.island(x,y,z,worldid)
# Check if it is a territory, parameters: (int)coordinates - (int)worldid, return value: (string)territory name, not present return "noland"

lapi.islandplayer(playerxuid,x,y,z,worldid,powername)
# Check if the player has a certain permission in the territory, parameters: (string)playerxuid - (int)coordinates - (int)worldid - (string)permission name, return value: bool
# powername values: "useitem"|"putblock"|"destroyblock"|"openchest"|"attack"

lapi.getlandinfo(landname)
# Get land information, parameter: (string) landname, return value: (dict) dictionary

lapi.getplayerland(playerxuid)
# Get the player owned territory, parameter: (string)playerxuid
# Return value: (dict) dictionary, "world" - main world territory, "nether" - hell territory, "ender" - mordor territory

lapi.getland_area(x1,y1,z1,x2,y2,z2,worldid,Dim)
# Get all the territories in a region
# Dim values: "2D"|"3D"

lapi.getland_point(x,y,z,worldid,Dim)
# Get the territory around a point
# Dim values: "2D"|"3D"

lapi.createlanddata(playerxuid,x1,y1,z1,x2,y2,z2,worldid,Dim)
# Create a territory, parameters: (string)playerxuid-(int)coordinate1-(int)coordinate2-(int)worldid-(string)territory mode
# Return value: (dict)dictionary, create success return -{"2D":[], "3D":[]}, create failure return the name of the overlapping territory
# Dim values: "2D"|"3D"

lapi.removeanddata(landname):
# Remove a territory, parameter: (string)landname, return: bool

lapi.setlandop(playerxuid,mode)
# Set the territory administrator, parameter: playerxuid-mode, return value: bool
# mode value: "add"|"del"
```

##### 3. Extension function interface

```python
lapi.addlandsign(landname,signname,data)
# Add a sign for the territory, arguments: (string)territoryname - (string)signname - (dict)dictionary, return value: bool

lapi.removelandsign(landname,signname)
# remove landsign, arguments: (string)landsname - (string)signname, return value: bool

lapi.getlandsign(landname,signname)
# Get landsign, arguments: (string)landsname - (string)signname, return value (dict)dictionary, does not exist return -{}
```
