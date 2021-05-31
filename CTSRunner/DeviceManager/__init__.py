#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@File   : __init__.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2020-04-14
@Desc   :
"""

import os


def execute_cmd(command):
    """
    执行命令行获取执行结果, 并对结果去重
    :param command:
    :return:
    """
    result_list = []
    with os.popen(command) as f:
        result = f.readlines()
    for i in result:
        if i == '\n':
            continue
        result_list.append(i.strip('\n'))
    result_list = list(set(result_list))
    return result_list


class HTSingleton(object):
    """
    单例模式基类
    """
    _instance = None
    _first_init = True

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args)
            cls._instance.init()
        return cls._instance

    def __init__(self):
        pass

    def init(self):
        """初始化"""
        pass
