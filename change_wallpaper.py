# -*- coding: utf-8 -*-
#
# File: change_wallpaper.py
# Author: Chen Qizhou <kuqilin@88.com>
# Date: 2025Year 12Month 16Day
# Version: 2.0 Alpha
# license: MIT License
# GitHub: https://github.com/kuqilin/HuaDuXiaoQuDingZhiBiZhiQieHuan.git
#
# Description: Randomly select a picture from a special folder which is set by settings.py and set it as the desktop wallpaper.
#
# Requirements:
#    - Python >= 3.12
#    - pywin32 >= 305
#
# Install Requirements:
#    pip install "pywin32>=305"
#
# Usage:
#    pyinstaller -F -w -i .\GY_1080x1080.ico --version-file .\change_wallpaper_version_info.txt .\change_wallpaper.py --clean
#
# Notes:
#    - This script is packed with PyInstaller.
#    - It is located in the folder "~\Microsoft\Windows\Start Menu\Programs\Startup" to be a startup program.


import os
import json
import random
from win32gui import SystemParametersInfo
from win32con import SPI_SETDESKWALLPAPER, SPIF_UPDATEINIFILE, SPIF_SENDCHANGE

original_folder_path = {"folder_path" : "D:\\花都校区定制壁纸"}

def reset_folder():
    config_file = "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(original_folder_path, f, ensure_ascii=False, indent=4)
#         f.write("""{
#     \"folder_path\": \"D:\\花都校区定制壁纸\"
# }""")

def set_wallpaper(image_path):
    """
    调用 Windows API 设置壁纸
    """
    try:
        # SPI_SETDESKWALLPAPER: 设置桌面壁纸
        # SPIF_UPDATEINIFILE: 写入注册表
        # SPIF_SENDCHANGE: 通知所有窗口壁纸已更改
        SystemParametersInfo(SPI_SETDESKWALLPAPER, image_path, WinIni=SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        print(f"壁纸已成功设置为: {image_path}")
    except Exception as e:
        print(f"设置壁纸时出错: {e}")

def main():

    if not os.path.exists('config.json'):
        reset_folder()

    with open('config.json', 'r', encoding='utf-8') as f:
        folder_path = json.load(f)["folder_path"]

    # folder_path = config["folder_path"]

    # 1. 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹 {folder_path} 不存在.")
        reset_folder()
        return

    # 2. 获取文件夹内所有图片文件
    # 这里定义支持的图片后缀
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    images = [f for f in os.listdir(folder_path) 
              if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(folder_path, f))]
    
    if not images:
        print(f"错误: 文件夹 {folder_path} 中没有找到图片文件.")
        reset_folder()
        return

    # 3. 随机选择一张
    selected_image = random.choice(images)
    full_path = os.path.join(folder_path, selected_image)

    # 4. 设置壁纸
    set_wallpaper(full_path)

if __name__ == '__main__':
    main()
    # 程序执行完毕后自动退出，不保留任何窗口