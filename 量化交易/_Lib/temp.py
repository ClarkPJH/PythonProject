import win32con
import win32gui
from time import *
from pywinauto import mouse
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import os

exe_path = 'D:/Softwares/东方财富/mainfree.exe'
win_name = '东方财富终端'


app = Application().connect(path=exe_path, timeout=3)

# win_id = str(app.window(found_index=2).win_identifiers()).split(', ')[1]
# hwnd = win32gui.FindWindow(win_id, win_name)
# print(hwnd)


def get_hwnd(app):
    """
    --获取窗口hwnd--

    需要在 pywinauto.application 中第597行插入以下方法
    def win_identifiers(self):
        return self.__resolve_control(self.criteria)[-1]
    """

    for i in range(0, 9):
        # 获取窗口id
        win_id = str(app.window(found_index=i).win_identifiers()).split(', ')[1]
        # 获取窗口hwnd
        hwnd = win32gui.FindWindow(win_id, win_name)
        if hwnd > 0:
            break
    return i, hwnd


def reopen_app(app):
    for i in range(0, 5):
        app.kill()
        sleep(5)
        app = Application().start(exe_path, timeout=10)
        sleep(10)
        if get_hwnd(app)[0] == 0:
            print('客户端重启成功')
            break
        # else:
        #     print(f'客户端第{i + 1}次重启失败')
        #     sleep(10)
        #     if i == 4:
        #         print(f'客户端第{i + 1}次重启失败')


# hwnd = get_hwnd[1]
# win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
# win32gui.SetForegroundWindow(hwnd)
# sleep(3)
# win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

# if get_hwnd(app)[0] == 1:
#     print('交易完成!')
#     win32gui.ShowWindow(get_hwnd(app)[1], win32con.SW_MINIMIZE)
# else:
#     reopen_app(app)

print(get_hwnd(app)[0])
