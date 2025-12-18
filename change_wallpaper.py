import os
import random
import sys
from win32gui import SystemParametersInfo
from win32con import SPI_SETDESKWALLPAPER, SPIF_UPDATEINIFILE, SPIF_SENDCHANGE

def set_wallpaper(image_path):
    """
    调用 Windows API 设置壁纸
    """
    try:
        # SPI_SETDESKWALLPAPER: 设置桌面壁纸
        # SPIF_UPDATEINIFILE: 写入注册表
        # SPIF_SENDCHANGE: 通知所有窗口壁纸已更改
        abs_path = os.path.abspath(image_path)
        SystemParametersInfo(SPI_SETDESKWALLPAPER, abs_path, 0)
        print(f"壁纸已成功设置为: {image_path}")
    except Exception as e:
        print(f"设置壁纸时出错: {e}")

def main():
    folder_path = r"D:\花都校区定制壁纸"
    
    # 1. 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹 {folder_path} 不存在.")
        return

    # 2. 获取文件夹内所有图片文件
    # 这里定义支持的图片后缀
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    images = [f for f in os.listdir(folder_path) 
              if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(folder_path, f))]
    
    if not images:
        print(f"错误: 文件夹 {folder_path} 中没有找到图片文件.")
        return

    # 3. 随机选择一张
    selected_image = random.choice(images)
    full_path = os.path.join(folder_path, selected_image)

    # 4. 设置壁纸
    set_wallpaper(full_path)

if __name__ == '__main__':
    main()
    # 程序执行完毕后自动退出，不保留任何窗口