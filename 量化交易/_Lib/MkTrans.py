# coding: utf-8
import win32con
import win32gui
from time import *
from pywinauto import mouse
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from .config import *


class Treader:
    def __init__(self):
        try:
            self.app = Application().connect(path=exe_path, timeout=30)
            sleep(1)
        except Exception as e:
            print(e)
            self.app = Application().start(exe_path, timeout=30)
            sleep(10)

    def get_hwnd(self):
        """
        --获取窗口hwnd--

        需要在 pywinauto.application 中第597行插入以下方法
        def win_identifiers(self):
            return self.__resolve_control(self.criteria)[-1]
        """

        for i in range(0, 9):
            # 获取窗口id
            win_id = str(self.app.window(found_index=i).win_identifiers()).split(', ')[1]
            # 获取窗口hwnd
            hwnd = win32gui.FindWindow(win_id, win_name)
            if hwnd > 0:
                break
        return i, hwnd

    def show_window(self):
        """--窗口置顶并最大化--"""
        hwnd = self.get_hwnd()[1]
        # 窗口置顶
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(hwnd)

    def login_trans_acct(self):
        """--登录快速交易窗口--"""
        self.show_window()
        sleep(0.5)

        send_keys('{ENTER}')
        # F12 打开快速交易窗口登录界面
        send_keys('{F12}')
        # 输入交易密码
        send_keys('960724')
        # 回车进入快速交易窗口
        send_keys('{ENTER}')
        sleep(2)
        # 此时回车关闭意外的弹窗
        send_keys('{ENTER}')

    def reopen_app(self):
        L.log('WARN', '为保证后续交易正常，将重启客户端')
        for i in range(0, 5):
            self.app.kill()
            sleep(5)
            self.app = Application().start(exe_path, timeout=10)
            sleep(10)
            if self.get_hwnd()[0] == 0:
                L.log('TIPS', '客户端重启成功')
                break
            else:
                L.log('WARN', f'客户端第{i + 1}次重启失败')
                sleep(10)
                if i == 4:
                    L.log('ERROR', f'客户端第{i + 1}次重启失败')

    def mk_trans(self, action, code, count):
        """--进行交易操作--"""
        # print("\n{0}:\n{1} {2}s".format(code, action, count))
        self.login_trans_acct()

        # 点击进入买/卖界面
        if action == 'B':
            mouse.click(button='left', coords=buy_cds)
        if action == 'S':
            mouse.click(button='left', coords=sell_cds)
        # 点击股票代码输入框
        mouse.click(button='left', coords=code_cds)
        # 输入交易的股票代码
        send_keys(str(code))
        # 点击买入数量输入框
        mouse.click(button='left', coords=count_cds)
        # 输入买入的数量
        send_keys(str(count))
        # 回车确认
        send_keys('{ENTER}')
        sleep(1)
        # 回车关闭确认弹窗
        send_keys('{ENTER}')
        sleep(1)
        # 回车关闭提示弹窗
        send_keys('{ENTER}')
        # 点击退出按钮
        mouse.click(button='left', coords=exit_cds)
        sleep(0.5)
        # 回车关闭确认弹窗, 退出交易界面
        send_keys('{ENTER}')

        if self.get_hwnd()[0] == 1:
            L.log('TIPS', '交易完成!')
            win32gui.ShowWindow(self.get_hwnd()[1], win32con.SW_MINIMIZE)
        else:
            L.log('WARN', '交易流程未正常结束')
            self.reopen_app()


# TD = Treader()
# TD.mk_trans('B', 600115, 100)
# sleep(2)
# TD.mk_trans('S', 600115, 100)

