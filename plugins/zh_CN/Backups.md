---
sort: 2
---
# Backups
# 简介

本插件用于自动化热备份，支持计划任务和指定目录，可以在指定时间复制地图到指定目录

# 依赖模块

`apscheduler`：内置任务管理器依赖，可选。不使用的方法：在配置文件中配置 `use_internel_task_manager`项目为 `false`

# 配置文件

配置文件会在第一次加载插件时生成，位于`plugins/py/Backups/Backups.json`

`max_backups`: 最大备份数量，备份数量超过此值时会自动删除旧的备份，允许的值：自然数

`use_internel_task_manager`：使用内置的任务管理器，允许的值：`true`(是)/`false`(否)

`backup_folder`：备份文件存储的路径，允许使用相对路径或绝对路径，如`E:/my_bds_server/backups`或`plugins/backups`

`scheduled_jobs`：定时备份任务，可以在此定义多个任务，编写时务必遵守json语法！

    `name`：计划任务的名字，可随意

    `type`：任务类型，默认为 `cron`

以下为定时器参数，可指定在某时间执行任务，若不使用则填写 `null`，也可填写形如以下配置文件的配置。如 `backup_task`表示每月的1，3，5日的12时0分执行任务。而 `another_task`则表示每天的8时至20时的每个小时中的第30分时执行任务，也就是任务会在每天执行13次

    `month`：月

    `day`：日

    `hour`：时

    `minute`：秒

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
