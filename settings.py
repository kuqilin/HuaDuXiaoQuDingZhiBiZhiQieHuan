# -*- coding: utf-8 -*-
#
# File: settings.py
# Author: Chen Qizhou <kuqilin@88.com>
# Date: 2025Year 12Month 16Day
# Version: 2.0 Alpha
# license: MIT License
# GitHub: https://github.com/kuqilin/HuaDuXiaoQuDingZhiBiZhiQieHuan.git
#
# Description: The settings GUI for changing the wallpaper folder path.
#
# Requirements:
#    - Python >= 3.12
#    - PyQt5
#
# Install Requirements:
#    pip install qt5-applications
#
# Usage:
#    pyinstaller -F -w -i .\GY_1080x1080.ico --version-file .\settings_version_info.txt .\settings.py --clean
#
# Notes:
#    - This script is packed with PyInstaller.
#    - It is located in the folder "D:\花都校区定制壁纸切换" to be part of the application.



import sys, webbrowser, json, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize
from settings_ui import Ui_MainWindow  # 导入转换的UI类
from change_wallpaper import reset_folder

about_content = "<font size=\"5\">花都校区定制壁纸切换器 v2.0</font><br /><font size=\"3\">因为想要让学校电脑每次开机自动切换壁纸，所以花了一点小时间写了这个程序。希望大家能够喜欢。</font><br />本程序还有很多缺陷和不足，欢迎大家在 GitHub 上提交 issue 和代码。<br />作者：陈麒州（2027届）<br />联系我：<a href=\"mailto:kuqilin@88.com\">kuqilin@88.com</a><br />维护程序：<a href=\"https://github.com/kuqilin/HuaDuXiaoQuDingZhiBiZhiQieHuan.git\">GitHub</a>"



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        font = QFont()
        font.setFamily("霞鹜文楷 GB 屏幕阅读版")
        font.setPointSize(12)
        self.statusBar().setFont(font)

        # 连接按钮点击信号到槽函数
        self.statusBar().showMessage("就绪")
        self.btn_browse.clicked.connect(self.browse_file)
        self.btn_save.clicked.connect(self.save_settings)
        self.action_about.triggered.connect(self.show_about)
        self.action_website.triggered.connect(self.open_website)
        self.action_exit_2.triggered.connect(self.exit_app)
        self.action_reset_folder.triggered.connect(self.reset_folder)
        self.btn_exit.clicked.connect(self.exit_app)
        
    def browse_file(self):
        """打开文件对话框选择路径"""
        # 打开文件选择对话框
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",  # 对话框标题
            "D:\\花都校区定制壁纸"  # 初始目录
        )

        # 如果选择了文件夹，更新文本框
        if folder_path:
            self.lineEdit_path.setText(folder_path)

    def show_about(self):
        """显示关于对话框"""
        # msg = QMessageBox.about(self, "关于", "这是一个示例应用程序，用于更改壁纸路径。")
        msg = QMessageBox()
        msg.setFixedSize(QSize(400, 300))
        # msg.setStyleSheet("QMessageBox{min-width: 600px;min-height: 300px;}")
        msg.setFont(QFont("霞鹜文楷 GB 屏幕阅读版", 12))
        msg.setWindowTitle("关于")
        msg.setTextFormat(1)  # 设置为富文本格式
        msg.setText(about_content)
        msg.exec_()

    def open_website(self):
        webbrowser.open("https://github.com/kuqilin/HuaDuXiaoQuDingZhiBiZhiQieHuan.git")

    def exit_app(self):
        QApplication.quit()
    
    def reset_folder(self):
        reset_folder()
        QMessageBox.information(self, "重置文件夹路径", "文件夹路径已重置为默认值。")

    def save_settings(self):
        folder_path = self.lineEdit_path.text()
        config_file = "config.json"

        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config_data["folder_path"] = folder_path

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
        self.statusBar().showMessage("保存成功", 5000)  # 显示5秒

if __name__ == '__main__':
    if not os.path.exists('config.json'):
        reset_folder()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())