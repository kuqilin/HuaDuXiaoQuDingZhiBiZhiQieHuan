# 花都校区定制壁纸切换

给广东广雅中学（花都校区）写的开机壁纸自动切换程序：每次登录 Windows 时，从指定文件夹里随机挑一张图片设为桌面壁纸。

## 功能

- 登录时自动随机切换桌面壁纸
- 自带图形设置界面，可自由指定壁纸文件夹
- 用「启动文件夹 + 快捷方式」实现自启，不写注册表 Run 项，不需要管理员权限
- 一条命令卸载，且不会删除你的图片

## 三个程序

| 程序 | 作用 |
| --- | --- |
| `auto_install.exe` | 安装 / 卸载，创建快捷方式 |
| `change_wallpaper.exe` | 随机换壁纸，由「启动」里的快捷方式在登录时调用 |
| `settings.exe` | 图形界面，修改壁纸文件夹路径 |

## 环境要求

- Windows 10 / 11
- Python >= 3.12（只有从源码运行时才需要）
- PyQt5 >= 5.15.11
- pywin32 >= 306

## 安装

把 Release 里的 exe 解压到**同一个文件夹**，双击 `auto_install.exe`。安装器会：

1. 把 `change_wallpaper.exe`、`settings.exe` 和 `config.json` 复制到 `%LOCALAPPDATA%\HuaDuWallpaper`
2. 在「启动」文件夹里创建快捷方式 `花都校区定制壁纸切换.lnk`
3. 在开始菜单创建 `花都校区定制壁纸切换 → 设置`
4. 创建壁纸文件夹 `D:\花都校区定制壁纸`（已存在则跳过）

安装目录结构：

```
%LOCALAPPDATA%\HuaDuWallpaper\
    change_wallpaper.exe
    settings.exe
    config.json
```

> 快捷方式的「起始位置」被设为安装目录，所以无论从「启动」还是从资源管理器双击，
> 程序读写的都是同一份 `config.json`，改设置才会真正生效。

## 卸载

```bat
auto_install.exe --uninstall
```

会删除两个快捷方式和 `%LOCALAPPDATA%\HuaDuWallpaper` 整个目录。
**不会**删除壁纸图片文件夹，图片需要你自己清理。

> 卸载时请保留 `auto_install.exe`，删掉它就只能手动清理了。

## 配置

配置文件：`%LOCALAPPDATA%\HuaDuWallpaper\config.json`

```json
{
    "folder_path": "D:\\花都校区定制壁纸"
}
```

支持的图片格式：`.jpg` `.jpeg` `.png` `.bmp` `.gif`
（gif 只会用到第一帧，Windows 桌面壁纸不支持动图。）

## 从源码运行

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python settings.py           # 打开设置界面
python change_wallpaper.py   # 立即换一张壁纸（需 Windows + pywin32）
python auto_install.py       # 安装
python auto_install.py --uninstall   # 卸载
```

## 打包 exe

主程序：
```bat
pyinstaller -F -w -i .\GY_1080x1080.ico --version-file .\change_wallpaper_version_info.txt .\change_wallpaper.py --clean
```

设置：
```bat
pyinstaller -F -w -i .\GY_1080x1080.ico --version-file .\settings_version_info.txt .\settings.py --clean
```

自动安装：
```bat
pyinstaller -F -w -i .\GY_1080x1080.ico --version-file .\auto_install_version_info.txt --hidden-import win32com.client .\auto_install.py --clean
```

`auto_install` 通过 `win32com.client` 调用 `WScript.Shell` 创建快捷方式，
打包时必须加 `--hidden-import win32com.client`，否则运行时会报找不到模块。

## 常见问题

**开机后壁纸没变？**
按 `Win+R` 输入 `shell:startup`，确认里面有「花都校区定制壁纸切换」快捷方式；
再确认 `config.json` 里的 `folder_path` 存在且文件夹里有图片。

**设置保存了，但壁纸没跟着变？**
重启一次即可（登录时才触发）。也可以直接运行安装目录下的 `change_wallpaper.exe` 验证。

**偶尔两次开机是同一张图？**
随机选择可能重复，属于正常现象。

**界面字体和设计稿不一样？**
界面用的是「霞鹜文楷 GB 屏幕阅读版」，系统没装会回退到默认字体。

**想让这台电脑的所有用户都生效？**
把快捷方式放到 `%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\StartUp`，
并把安装目录改成 `%PROGRAMDATA%` 下的路径（需要管理员权限）。

## 许可

[MIT License](LICENSE)
