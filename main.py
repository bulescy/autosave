import os
import shutil
import time
import hashlib
from datetime import datetime

# 自定义需要备份的文件和文件夹列表
backup_items = [
    '/home/bulescy/.bashrc',
    '/home/bulescy/.tmux.conf',
    '/home/bulescy/testcpy',
]

# 日志文件名
log_file = 'backup_log.txt'

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
#    print(hash_md5.hexdigest())
    return hash_md5.hexdigest()

def folder_md5(folder_path):
    md5_dict = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            md5_dict[file_path.replace(folder_path, '')] = calculate_md5(file_path)
    return md5_dict

def file_needs_backup(file_path, dest_file_path):
    if not os.path.exists(dest_file_path):
        return True
    return calculate_md5(file_path) != calculate_md5(dest_file_path)

def backup_items_to_current_dir(items):
    for item in items:
        if os.path.exists(item):
            item_name = os.path.basename(item.rstrip('/\\'))
            if os.path.isdir(item):
                # 处理文件夹
                dest_folder = os.path.join(os.getcwd(), f"{item_name}_backup")

                source_md5 = folder_md5(item)
                existing_backups = [d for d in os.listdir(os.getcwd()) if d.startswith(item_name + "_backup")]
                if existing_backups:
                    latest_backup = max(existing_backups, key=os.path.getmtime)
                    latest_backup_folder = os.path.join(os.getcwd(), latest_backup)
                    backup_md5 = folder_md5(latest_backup_folder)

                    if source_md5 == backup_md5:
                        print(f"No changes detected in {item}. Skipping backup.")
                        with open(log_file, 'a') as log:
                            log.write(f"{datetime.now()}: No changes detected in {item}. Skipping backup.\n")
                        continue

                shutil.copytree(item, dest_folder)
                with open(log_file, 'a') as log:
                    log.write(f"{datetime.now()}: {item} backed up to {dest_folder}\n")

            elif os.path.isfile(item):
                # 处理文件
                dest_file = os.path.join(os.getcwd(), f"{item_name}_backup")

                if not file_needs_backup(item, dest_file):
                    print(f"No changes detected in {item}. Skipping backup.")
                    with open(log_file, 'a') as log:
                        log.write(f"{datetime.now()}: No changes detected in {item}. Skipping backup.\n")
                    continue

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

