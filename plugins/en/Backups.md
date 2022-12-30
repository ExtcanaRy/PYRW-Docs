# Backups

# Introduction

This plugin is used to automate hot backups, supports scheduled tasks and specified directories, and can copy maps to specified directories at specified times

# Dependency modules

`apscheduler`: built-in task manager dependency, optional. Not used: configure `use_internel_task_manager` item to `false` in the configuration file

# configuration file

The configuration file is generated when the plugin is loaded for the first time and is located in `plugins/py/Backups/Backups.json`

`max_backups`: the maximum number of backups, if the number of backups exceeds this value, the old backups will be deleted automatically, allowed values: natural numbers

`use_internel_task_manager`: use the built-in task manager, allowed values: `true`(yes)/`false`(no)

`backup_folder`: path where backup files are stored, relative or absolute paths are allowed, e.g. `E:/my_bds_server/backups` or `plugins/backups`

`scheduled_jobs`: scheduled backup task, multiple tasks can be defined here, be sure to follow the json syntax when writing!

`name`: the name of the scheduled task, can be arbitrary

`type`: task type, default is `cron`.

The following timer parameters, you can specify the execution of the task at a certain time, if not used, fill in `null`, you can also fill in the configuration file in the shape of the following. For example, `backup_task` means the task will be executed at 12:0 on the 1st, 3rd and 5th of each month. And `another_task` means that the task will be executed at the 30th minute of each hour from 0800 to 2000 every day, that is, the task will be executed 13 times a day.

`month`: month

`day`: day

`hour`: hour

`minute`: seconds

```json
{
	"max_backups": 3,
	"use_internel_task_manager": true,
	"backup_folder": "bak",
	"scheduled_jobs": [
		{
			"name": "backup_task",
			"type": "cron",
			"month": null,
			"day": "1, 3, 5",
			"hour": 12,
			"minute": 0
		},
		{
			"name": "another_task",
			"type": "cron",
			"month": null,
			"day": null,
			"hour": "8-20",
			"minute": 30
		}
	]
}
```
