import os
import shutil
import time
import hashlib
from datetime import datetime

# 自定义需要备份的文件和文件夹列表
backup_items = [
    '/home/bulescy/.bashrc',
    '/home/bulescy/.tmux.conf',
    '/home/bulescy/.config/clash/update.sh',
]

# 日志文件名
log_file = 'backup_log.txt'

def backup_items_to_current_dir(items):
    for item in items:
        if os.path.exists(item):
            item_name = os.path.basename(item.rstrip('/\\'))
            if os.path.isdir(item):
                # 处理文件夹
                dest_folder = os.path.join(os.getcwd(), f"{item_name}_backup")

                shutil.copytree(item, dest_folder)
                with open(log_file, 'a') as log:
                    log.write(f"{datetime.now()}: {item} backed up to {dest_folder}\n")

            elif os.path.isfile(item):
                # 处理文件
                dest_file = os.path.join(os.getcwd(), f"{item_name}_backup")

                shutil.copy2(item, dest_file)
                with open(log_file, 'a') as log:
                    log.write(f"{datetime.now()}: {item} backed up to {dest_file}\n")
        else:
            print(f"{item} does not exist. Skipping backup.")
            with open(log_file, 'a') as log:
                log.write(f"{datetime.now()}: {item} does not exist. Skipping backup.\n")

if __name__ == "__main__":
    with open(log_file, 'a') as log:
        log.write(f"================={datetime.now()}=================\n")
    backup_items_to_current_dir(backup_items)
    with open(log_file, 'a') as log:
        log.write(f"================={datetime.now()}=================\n")
        log.write(f"\n")

