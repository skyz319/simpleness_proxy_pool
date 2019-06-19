#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   LogHandler.py
@Time    :   2019/06/18 15:04:47
@Author  :   Sky.z
@Version :   1.0
@Contact :   skyz319@gmail.com
@License :   (C)Copyright 2017-2018, Sky.z
@Desc    :   日志工具
"""
import os
import logging

from logging.handlers import TimedRotatingFileHandler

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')


class LogHandler(logging.Logger):
    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()
    
    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))

        # 设置日志回滚，保存在log目录，一天一个文件，保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D',
                                                interval=1, backupCount=15, encoding='utf-8')
        file_handler.suffix = '%Y%m%d.log'

        # 设置日志级别
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)

        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)

        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        # 设置日志级别
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)

        self.addHandler(stream_handler)


if __name__ == '__main__':
    log = LogHandler('test')
    print('this is a test msg')
