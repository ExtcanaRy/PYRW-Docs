import mc
import threading
import time
import shutil
import os
import warnings

warnings.simplefilter('ignore')

start_flag = False
query_flag = False
copy_lock = False
config = {}

logger = mc.Logger(__name__)
conf_mgr = mc.ConfigManager(__name__)

def init():
    global config
    config = {}
    config['max_backups'] = 3
    config['use_internel_task_manager'] = True
    config['backup_folder'] = "bak"
    config['scheduled_jobs'] = [{'name': 'backup_task', 'type': 'cron', 'month': None, 'day': "1,3,5", 'hour': 0, 'minute': 0},
                                {'name': 'another_task', 'type': 'cron', 'month': None, 'day': "3-10", 'hour': 12, 'minute': 12}]
    conf_mgr.make(config)
    config = conf_mgr.read()
    logger.info("Loaded!")


init()
backup_folder = config['backup_folder']


def auto_del():
    while True:
        if not os.path.exists(backup_folder):
            continue
        max_num = config['max_backups']
        folders = [folder for folder in os.listdir(
            backup_folder) if os.path.isdir(os.path.join(backup_folder, folder))]
        if len(folders) > max_num:
            folders.sort()
            for folder in folders[:len(folders) - max_num]:
                shutil.rmtree(os.path.join(backup_folder, folder))
        time.sleep(1)


def start_bak():
    global start_flag, query_flag, copy_lock
    logger.info("Started.")
    mc.runcmd("save hold")
    start_flag = True
    query_flag = True
    query_loop()


if config["use_internel_task_manager"]:
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduled_jobs = config['scheduled_jobs']
    scheduler = BackgroundScheduler()
    for scheduled_job in scheduled_jobs:
        job_func = scheduled_job['name']
        scheduler.add_job(
            start_bak, scheduled_job['type'], month=scheduled_job['month'], day=scheduled_job['day'], hour=scheduled_job['hour'], minute=scheduled_job['minute'])
    scheduler.start()


def query_loop():
    while query_flag:
        mc.runcmd("save query")
        time.sleep(1)


def finish_bak():
    global start_flag, copy_lock
    start_flag = False
    copy_lock = False
    mc.runcmd("save resume")
    logger.info("Finished.")


def copy_files(file_path):
    global copy_lock, query_flag
    if copy_lock:
        return False
    query_flag = False
    copy_lock = True
    folder_name = time.strftime(f"{backup_folder}/%Y.%m.%d-%H.%M")
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    logger.info("Copying files...")
    shutil.copytree("worlds/" + file_path, folder_name)
    finish_bak()


def onConsoleInput(e: str):
    if e == "bak" and not start_flag:
        threading.Thread(target=start_bak, daemon=True).start()
        return False
    elif e == "bak" and start_flag:
        logger.warn("Backing up now!")
        return False


def onConsoleOutput(e):
    if "Data saved. Files are now ready to be copied." in e:
        file_list = e.split("\n")[1]
        world_path = file_list.split(", ")[0].split(":")[0].split("/")[0]
        threading.Thread(target=copy_files, daemon=True,
                         args=(world_path,)).start()
        return False
    if "Saving..." in e or "A previous save has not been completed." in e or "Changes to the world are resumed." in e:
        return False


def onPlayerCmd(e):
    player = e['player']
    if e['cmd'] == "/bak":
        if player.perm < 2:
            player.sendTextPacket("You are not an admin!")
            return False
        if not start_flag:
            threading.Thread(target=start_bak, daemon=True).start()
            player.sendTextPacket("Backing up task started!")
            return False
        else:
            player.sendTextPacket("Backing up now!")
            return False


mc.setListener("onConsoleInput", onConsoleInput)
mc.setListener("onConsoleOutput", onConsoleOutput)
mc.setListener("onPlayerCmd", onPlayerCmd)
threading.Thread(target=auto_del, daemon=True).start()
