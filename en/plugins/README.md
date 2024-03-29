# List of Plugins

Plugins that have been adapted for `BDSpyrunnerW` are included here, All plugins should be put into the ``plugins/py/`` folder for loading

# Install plugin dependencies

For the dependencies mentioned in the plugin introduction page, please follow these steps to install them.

Note: If you install the Python runtime environment using method one mentioned in the tutorial, you should open the terminal in the ``plugins/py/env/`` folder in the server directory, or make sure the working directory is located there.

1. Open your favorite terminal, such as cmd or Powershell
2. [optional/one-time] Using the official pip source in China is very slow, here we recommend using the Tsinghua source to improve the download speed, type

```powershell
python.exe -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

3.[optional/one-time] To upgrade your pip, type

```powershell
python.exe -m pip install --upgrade pip
```

4. To install dependency modules, type `python.exe -m pip install <dependency>`, e.g. if I want to install `numpy ` and `chardet` dependencies, then use the command `python.exe -m pip install numpy chardet`

# Download Plugins

If after clicking on the download link your browser opens the file directly instead of downloading it. You can `right-click` on the page where you opened the file and click `Save As` to save the file

# Plugin List

| Name            | Description                                                                     | Original Author | Author | Details                             |
| --------------- | ------------------------------------------------------------------------------- | --------------- | ------ | ----------------------------------- |
| teleport        | teleport plugin                                                                 | twoone3         | wsr    | [View Details](teleport.md "here")        |
| Backups         | Map Backups plugin                                                              | /               | wsr    | [View Details](Backups.md "here")         |
| Blockstatistics | Mining Statistics Plugin                                                        | twoone3         | wsr    | [View Details](Blockstatistics.md "here") |
| ban             | Blacklist Plugin                                                                | /               | wsr    | [View Details](ban.md "here")             |
| BehaviorLog     | BehaviorLog plugin                                                              | /               | wsr    | [View Details](BehaviorLog.md "here")     |
| pland           | Territory plugin                                                                | /               | 05007  | [View Details](pland.md "here")           |
| votekick        | Votekick plugin                                                                 | /               | wsr    | [View Details](votekick.md "here")        |
| chatlog         | Behavior log simplified version, only console output player chat, commands, etc | /               | wsr    | [View Details](chatlog.md "here")         |
| BestScoreBoard     | hides offline players' scoreboard | /       | Moxiner   | [View Details](BestScoreboard.md "here")     |
