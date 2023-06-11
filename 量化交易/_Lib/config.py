# coding: utf-8
from .setLog import *
exe_path = 'D:/Softwares/东方财富/mainfree.exe'
win_name = '东方财富终端'

# 东方财富客户端快速交易窗口坐标
buy_cds = (580, 320)
sell_cds = (580, 350)
code_cds = (830, 360)
count_cds = (830, 500)
exit_cds = (980, 270)

# 日志生成
create_date = time.strftime("%Y%m%d", time.localtime(time.time()))
log_path = 'TransLogs/%s.log' % create_date
L = Logging(log_path)
