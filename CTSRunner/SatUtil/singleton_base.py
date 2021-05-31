#!/usr/bin/env python3
# coding=utf-8

"""
@File   : singleton_base.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019/12/10 3:28 下午
@Desc   : 单例模板基类
"""


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

    def init(self, *args):
        """初始化"""
        pass

