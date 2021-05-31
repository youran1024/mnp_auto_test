#!/usr/bin/env python3
# coding=utf-8

"""
@File   : ht_service_log_center.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2020/2/18 4:26 下午
@Desc   : 
"""

import os
import logging
import datetime
from os import pardir
from .singleton_base import HTSingleton

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), pardir)
Info = None
Debug = None
Error = None
log_path_global = None


class HTServiceLogCenter(HTSingleton):
    """
    日志调试模块
    """
    def __init__(self, log_path=None, log_name=None):
        super(HTServiceLogCenter, self).__init__()
        if self._first_init:
            self._first_init = False
            global Info
            global Debug
            global Error
            global log_path_global
            Info = self._instance.info
            Debug = self._instance.debug
            Error = self._instance.error

            self.logger = logging.getLogger()
            # 创建一个文件对象  创建一个文件对象,以UTF-8 的形式写入 标配版.log 文件中
            if not log_path or len(log_path) == 0:
                log_path = self._get_log_name()

            if not os.path.exists(log_path):
                os.makedirs(log_path)
            if not log_name or len(log_name) == 0:
                log_name = self._get_log_name()

            log_path_global = log_path
            log_path = os.path.join(log_path, log_name + '.log')
            # 配置显示格式  可以设置两个配置格式  分别绑定到文件和屏幕上
            formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

            fh = logging.FileHandler(log_path, encoding='utf-8')
            fh.setFormatter(formatter)  # 将格式绑定到两个对象上
            fh.setLevel(10)  # 写入文件的从10开始
            self.logger.addHandler(fh)  # 将两个句柄绑定到logger

            # 创建一个屏幕对象
            # sh = logging.StreamHandler()
            # sh.setFormatter(formatter)
            # sh.setLevel(20)  # 在屏幕显示的从30开始
            # self.logger.addHandler(sh)

            self.logger.setLevel(10)  # 总开关

    @staticmethod
    def _get_log_path():
        return os.path.join(LOG_PATH, 'Logs')

    @staticmethod
    def _get_log_name():
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M")
        return now

    def debug(self, msg):
        """
        调试模式
        :param msg:
        :return:
        """
        self.logger.debug(msg)

    def waring(self, msg):
        """
        警告模式
        :param msg:
        :return:
        """
        self.logger.warning(msg)

    def info(self, *args, **kwargs):
        """
        msg info
        :param args:
        :param kwargs:
        :return:
        """
        info = ''
        for value in args:
            info += str(value)
        self.logger.info(info)

    def error(self, msg):
        """
        错误模式
        :param msg:
        :return:
        """
        self.logger.error(msg)

