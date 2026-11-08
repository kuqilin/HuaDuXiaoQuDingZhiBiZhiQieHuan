# 花都校区定制壁纸切换

给广东广雅中学（花都校区）写的开机壁纸自动切换程序：每次登录 Windows 时，从指定文件夹里随机挑一张图片设为桌面壁纸。

## 1 功能

- 登录时自动随机切换桌面壁纸
- 自带图形设置界面，可自由指定壁纸文件夹
- 用「启动文件夹 + 快捷方式」实现自启，不写注册表 Run 项，不需要管理员权限
- 一条命令卸载，且不会删除你的图片

## 2 三个程序

| 程序 | 作用 |
| --- | --- |
| `auto_install.exe` | 安装 / 卸载，创建快捷方式 |
| `change_wallpaper.exe` | 随机换壁纸，由「启动」里的快捷方式在登录时调用 |
| `settings.exe` | 图形界面，修改壁纸文件夹路径 |

## 3 环境要求

- Windows 10 / 11
- Python >= 3.12（只有从源码运行时才需要）
- PyQt5 >= 5.15.11
- pywin32 >= 306

## 4 安装

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

## 5 卸载

```bat
auto_install.exe --uninstall
```

会删除两个快捷方式和 `%LOCALAPPDATA%\HuaDuWallpaper` 整个目录。
**不会**删除壁纸图片文件夹，图片需要你自己清理。

> 卸载时请保留 `auto_install.exe`，删掉它就只能手动清理了。

## 6 配置

配置文件：`%LOCALAPPDATA%\HuaDuWallpaper\config.json`

```json
{
    "folder_path": "D:\\花都校区定制壁纸"
}
```

支持的图片格式：`.jpg` `.jpeg` `.png` `.bmp` `.gif`
（gif 只会用到第一帧，Windows 桌面壁纸不支持动图。）

## 7 从源码运行

### 7.1 创建虚拟环境

在项目根目录执行：

```powershell
python -m venv venv
```

`venv\` 已经写进 `.gitignore`，不会被提交到仓库。

### 7.2 激活虚拟环境

直接执行 `.\venv\Scripts\activate` 会失败：

```
无法加载文件 ...\venv\Scripts\Activate.ps1。证书已被颁发者直接吊销。
```

这是 Python 安装包自带的签名证书过期导致的（3.12 / 3.13 的部分版本用微软的短期签名证书，
有效期只有几天，签发后不久就会被吊销），和本项目无关。PowerShell 默认的 `RemoteSigned`
策略遇到「有签名但验签失败」的脚本会直接拒绝执行。

先对**当前窗口**放开执行策略，再激活：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
```

`-Scope Process` 只对这一个窗口生效，关掉窗口即恢复，不会改动系统设置。
注意**每次新开窗口都要先执行一次**这条命令。

### 7.3 安装依赖

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

直连 PyPI 在国内经常很慢——`PyQt5-Qt5` 单个 wheel 约 60 MB，整套接近 70 MB，
很容易卡在 `Collecting PyQt5` 十分钟不动，所以建议加国内镜像。

想让以后都默认走镜像（写入 `%APPDATA%\pip\pip.ini`，对本机所有项目生效）：

```powershell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

可用的镜像：

```
清华   https://pypi.tuna.tsinghua.edu.cn/simple
阿里   https://mirrors.aliyun.com/pypi/simple/
中科大 https://mirrors.ustc.edu.cn/pypi/simple/
腾讯   https://mirrors.cloud.tencent.com/pypi/simple/
```

> 中断安装不会留下坏状态，pip 的安装是原子的，直接重跑即可，不用删 venv 重建。

### 7.4 运行

```powershell
python settings.py                  # 打开设置界面
python change_wallpaper.py          # 立即换一张壁纸
python auto_install.py              # 安装
python auto_install.py --uninstall  # 卸载
```

## 8 打包 exe

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

## 9 常见问题

**开机后壁纸没变？**
按 `Win+R` 输入 `shell:startup`，确认里面有「花都校区定制壁纸切换」快捷方式；
再确认 `config.json` 里的 `folder_path` 存在且文件夹里有图片。

**设置保存了，但壁纸没跟着变？**
重启一次即可（登录时才触发）。也可以直接运行安装目录下的 `change_wallpaper.exe` 验证。

**偶尔两次开机是同一张图？**
随机选择可能重复，属于正常现象。

**`pip install` 卡在 `Collecting PyQt5` 好久不动？**
见上面「从源码运行 → 2. 安装依赖」。这是 PyQt5 体积大 + 直连 PyPI 慢导致的，
换成国内镜像即可。

**`.\venv\Scripts\activate` 报「证书已被颁发者直接吊销」？**
见上面「从源码运行 → 2. 激活虚拟环境」。这是 Python 安装包自带的签名证书过期，
和本项目无关，先执行 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` 再激活即可。

**想让这台电脑的所有用户都生效？**
把快捷方式放到 `%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\StartUp`，
并把安装目录改成 `%PROGRAMDATA%` 下的路径（需要管理员权限）。

## 10 许可

[MIT License](LICENSE)
