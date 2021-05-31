#!/usr/bin/env python3
# coding=utf-8

"""
@File   : ht_log_center.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2020/2/18 3:02 下午
@Desc   : 
"""

import os
import logging
import datetime
from .singleton_base import HTSingleton

DEBUG = True


class HTLogCenter(HTSingleton):
    """
    服务检测日志模块
    """

    def __init__(self):
        super(HTLogCenter, self).__init__()
        self.logger = logging.getLogger()

    def init_env(self, path='', debug_info=''):
        """
        初始化环境
        :param path:
        :param path:
        :param debug_info:
        :return:
        """
        if self._first_init:
            self._first_init = False

            if DEBUG:
                level = logging.DEBUG
            else:
                level = logging.INFO

            self.logger.setLevel(level)

            if not debug_info or len(debug_info) == 0:
                debug_info = 'cts-runner'

            if not os.path.exists(path):
                os.makedirs(path)
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            debug_info += date
            file_name = os.path.join(path, debug_info + '.log')
            fh = logging.FileHandler(file_name, encoding='utf-8')
            # 配置显示格式  可以设置两个配置格式  分别绑定到文件和屏幕上
            formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            fh.setLevel(logging.INFO)

            # if DEBUG:
            #     # 创建一个屏幕对象
            #     sh = logging.StreamHandler()
            #     sh.setFormatter(formatter)
            #     self.logger.addHandler(sh)
            #     sh.setLevel(logging.DEBUG)
        return self

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

    def info(self, *args):
        """
        信息模式
        :param args:
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


HTLogInfo = HTLogCenter().info
HTLogDebug = HTLogCenter().debug
HTLogError = HTLogCenter().error


