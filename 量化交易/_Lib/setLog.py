# coding: utf-8

import time
import os


class Logging:
    def __init__(self, log_path):
        self.log_path = log_path

    def mik_log(self):
        file_object = open(self.log_path, 'w', encoding='utf-8')
        file_object.write('======================= 初始化日志文件 ======================= \n\n')
        file_object.close()

    def log(self, Type, desc):
        t = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        if os.path.exists(self.log_path) is True:
            file_object = open(self.log_path, 'a+', encoding='utf-8')
            file_object.write(str(t) + ' [ %s ]  ' % Type + str(desc) + '\n')

