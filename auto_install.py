# -*- coding: utf-8 -*-
#
# File: auto_install.py
# Author: Chen Qizhou <kuqilin@88.com>
# Date: 2025Year 12Month 16Day
# Version: 2.0 Alpha
# license: MIT License
# GitHub: https://github.com/kuqilin/HuaDuXiaoQuDingZhiBiZhiQieHuan.git
#
# Description: Install / uninstall the wallpaper switcher.
#              Copies the executables to %LOCALAPPDATA%\HuaDuWallpaper and creates
#              a shortcut in the Startup folder (instead of copying the exe there),
#              so the working directory, the config file and uninstall all stay
#              under control.
#
# Requirements:
#    - Python >= 3.12
#    - PyQt5
#    - pywin32 >= 306
#
# Install Requirements:
#    pip install -r requirements.txt
#
# Usage:
#    pyinstaller -F -w -i .\GY_1080x1080.ico --version-file .\auto_install_version_info.txt --hidden-import win32com.client .\auto_install.py --clean
#
#    auto_install.exe                 # 安装（创建快捷方式）
#    auto_install.exe --uninstall     # 卸载
#
# Notes:
#    - This script is packed with PyInstaller.
#    - 快捷方式的「起始位置」（working directory）被设置为安装目录，
#      这样 change_wallpaper.exe / settings.exe 在不同入口启动时，
#      读写的都是同一份 config.json。


import json
import os
import shutil
import sys
import traceback

import win32com.client
from PyQt5.QtWidgets import QApplication, QMessageBox

APP_NAME = "花都校区定制壁纸切换"
INSTALL_DIR_NAME = "HuaDuWallpaper"
DEFAULT_WALLPAPER_DIR = r"D:\花都校区定制壁纸"

APPDATA = os.environ.get("APPDATA") or os.path.expanduser("~")
LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")

STARTUP_DIR = os.path.join(
    APPDATA, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
START_MENU_DIR = os.path.join(
    APPDATA, "Microsoft", "Windows", "Start Menu", "Programs", APP_NAME)
INSTALL_DIR = os.path.join(LOCALAPPDATA, INSTALL_DIR_NAME)

CONFIG_FILE = os.path.join(INSTALL_DIR, "config.json")
WALLPAPER_EXE = os.path.join(INSTALL_DIR, "change_wallpaper.exe")
SETTINGS_EXE = os.path.join(INSTALL_DIR, "settings.exe")

STARTUP_LNK = os.path.join(STARTUP_DIR, APP_NAME + ".lnk")
SETTINGS_LNK = os.path.join(START_MENU_DIR, "设置.lnk")


def source_dir():
    """返回 auto_install.exe 所在目录。

    PyInstaller onefile 模式下 __file__ 指向临时解包目录，不能用，必须用
    sys.executable；从源码运行时才回退到 __file__。
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def create_shortcut(lnk_path, target, working_dir, description, icon=None):
    """用 WScript.Shell 创建 .lnk 快捷方式，同名文件会被覆盖。"""
    parent = os.path.dirname(lnk_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    shell = win32com.client.Dispatch("WScript.Shell")
    link = shell.CreateShortCut(lnk_path)
    link.TargetPath = target
    link.WorkingDirectory = working_dir
    link.IconLocation = "{},0".format(icon or target)
    link.Description = description
    link.save()


def write_default_config():
    os.makedirs(INSTALL_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"folder_path": DEFAULT_WALLPAPER_DIR}, f,
                  ensure_ascii=False, indent=4)


def wallpaper_folder():
    """读取安装目录下的 config.json，返回壁纸文件夹路径；配置损坏时重建。"""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            folder = json.load(f)["folder_path"]
        if not isinstance(folder, str) or not folder.strip():
            raise ValueError("folder_path 为空")
        return folder
    except (OSError, ValueError, KeyError, TypeError):
        write_default_config()
        return DEFAULT_WALLPAPER_DIR


def install():
    """安装：复制程序到安装目录并创建快捷方式。返回 (是否成功, 提示文本)。"""
    src = source_dir()
    if not os.path.isfile(os.path.join(src, "change_wallpaper.exe")):
        return False, (
            "找不到 change_wallpaper.exe。\n\n"
            "请确认安装包已经完整解压，并且 auto_install.exe 与 "
            "change_wallpaper.exe、settings.exe 放在同一个文件夹里。"
        )

    notes = []
    os.makedirs(INSTALL_DIR, exist_ok=True)

    # 1. 复制程序文件（安装目录与源目录相同时跳过，避免 SameFileError）
    for name in ("change_wallpaper.exe", "settings.exe"):
        s = os.path.join(src, name)
        d = os.path.join(INSTALL_DIR, name)
        if os.path.isfile(s) and os.path.abspath(s) != os.path.abspath(d):
            shutil.copy2(s, d)

    if not os.path.isfile(SETTINGS_EXE):
        notes.append("没有找到 settings.exe，设置程序未安装；"
                     "需要修改路径时可以直接编辑 config.json。")

    # 2. 配置文件
    if not os.path.isfile(CONFIG_FILE):
        cfg_src = os.path.join(src, "config.json")
        if os.path.isfile(cfg_src):
            shutil.copy2(cfg_src, CONFIG_FILE)
        else:
            write_default_config()
    folder = wallpaper_folder()

    # 3. 壁纸文件夹
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as exc:
        notes.append("无法创建壁纸文件夹 {}，请手动创建后再放入图片。（{}）"
                     .format(folder, exc))

    # 4. 快捷方式：启动文件夹里放 .lnk，不再拷贝 exe
    create_shortcut(
        STARTUP_LNK, WALLPAPER_EXE, INSTALL_DIR,
        "登录时从指定文件夹随机挑选一张图片作为桌面壁纸")
    if os.path.isfile(SETTINGS_EXE):
        create_shortcut(
            SETTINGS_LNK, SETTINGS_EXE, INSTALL_DIR,
            "花都校区定制壁纸切换 - 设置")

    lines = [
        "安装完成！",
        "",
        "程序目录",
        "    " + INSTALL_DIR,
        "开机自启",
        "    「启动」文件夹 → " + os.path.basename(STARTUP_LNK),
        "修改设置",
    ]
    if os.path.isfile(SETTINGS_EXE):
        lines.append("    开始菜单 → {} → 设置".format(APP_NAME))
    else:
        lines.append("    编辑 " + CONFIG_FILE)
    lines += [
        "壁纸文件夹",
        "    " + folder,
    ]
    if notes:
        lines += ["", "注意"] + ["    " + n for n in notes]
    return True, "\n".join(lines)


def uninstall():
    """卸载：删除快捷方式和安装目录，不动用户的壁纸图片。返回 (是否成功, 提示文本)。"""
    notes = []

    for lnk in (STARTUP_LNK, SETTINGS_LNK):
        if os.path.isfile(lnk):
            try:
                os.remove(lnk)
            except OSError as exc:
                notes.append("无法删除快捷方式 {}（{}）".format(lnk, exc))

    try:
        if os.path.isdir(START_MENU_DIR) and not os.listdir(START_MENU_DIR):
            os.rmdir(START_MENU_DIR)
    except OSError:
        pass

    if os.path.isdir(INSTALL_DIR):
        shutil.rmtree(INSTALL_DIR, ignore_errors=True)
    if os.path.isdir(INSTALL_DIR):
        notes.append("安装目录未能完全删除（可能有程序正在运行），请手动删除："
                     + INSTALL_DIR)

    lines = [
        "卸载完成。",
        "",
        "已删除开机自启快捷方式和程序文件。",
        "壁纸图片文件夹及其中的图片没有被删除。",
    ]
    if notes:
        lines += ["", "注意"] + ["    " + n for n in notes]
    return True, "\n".join(lines)


def main():
    app = QApplication([sys.argv[0]])  # noqa: F841  (需保持引用，否则对象会被回收)
    try:
        if "--uninstall" in sys.argv[1:]:
            ok, text = uninstall()
        else:
            ok, text = install()
    except Exception:
        QMessageBox.critical(
            None, APP_NAME + " - 出错",
            "操作过程中出现异常：\n\n" + traceback.format_exc(limit=4))
        return 1

    if ok:
        QMessageBox.information(None, APP_NAME, text)
    else:
        QMessageBox.critical(None, APP_NAME + " - 安装失败", text)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
