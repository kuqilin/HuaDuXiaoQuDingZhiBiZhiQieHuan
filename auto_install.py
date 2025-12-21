# -*- coding: utf-8 -*-
#
# File: auto_install.py
# Author: Chen Qizhou <kuqilin@88.com>
# Date: 2025Year 12Month 16Day
# Version: 2.0 Alpha
# license: MIT License
# GitHub: https://github.com/kuqilin/HuaDuXiaoQuDingZhiBiZhiQieHuan.git
#
# Description: Auto copy the change_wallpaper.py file to the startup folder.
#
# Requirements:
#    - Python >= 3.12
#
# Usage:
#    pyinstaller -F -w -i .\GY_1080x1080.ico --version-file .\auto_install_version_info.txt .\auto_install.py --clean
#
# Notes:
#    - This script is packed with PyInstaller.


import os, shutil, sys
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QFont

path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
shutil.copy("./change_wallpaper.exe", path)

app = QApplication([])
msg = QMessageBox.about(None, "自动安装", "自动安装成功！")

app.exec_()

sys.sleep(5)
sys.exit(0)