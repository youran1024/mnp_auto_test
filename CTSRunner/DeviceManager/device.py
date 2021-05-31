#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@File   : device.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-11-4
@Desc   : 设备信息
"""


class Device(object):

    def __init__(self,
                 udid='',
                 name='',
                 version='',
                 device_type='',
                 info=None
                 ):
        """
        设备信息初始化
        :param udid:
        :param name:
        :param version:
        :param device_type:
        :param info:
            {
                "DeviceName": "",
                "UniqueDeviceID": "",
                "ProductVersion": "",
                "ProductType": ""
            }
        """
        super(Device, self).__init__()
        if info:
            self._name = info['DeviceName']
            self._udid = info['UniqueDeviceID']
            self._version = info['ProductVersion']
            self._device_type = info['ProductType']
            self._plate_form: str = info['PlateForm']
            # device name
        else:
            # 设备号
            self._udid = udid
            # 设备名称
            self._name = name
            # 系统版本
            self._version = version
            # 设备类型
            self._device_type = device_type
            # 设备类型
            self._plate_form: str = 'iOS'

    @property
    def is_ios(self):
        """
        是否是iOS
        :return:
        """
        return self._plate_form.lower() == 'ios'

    @property
    def plate_form(self):
        """
        平台 iOS 、Android
        :return:
        """
        return self._plate_form

    @property
    def udid(self):
        """
        设备UDID
        :return:
        """
        return self._udid

    @property
    def name(self):
        """
        设备名称 例如iPhone 8
        :return:
        """
        return self._name

    @property
    def version(self):
        """
        设备版本号
        :return:
        """
        return self._version

    @property
    def type(self):
        """
        设备类型
        :return:
        """
        return self._device_type

    def to_dic(self):
        """
        对象转换成字典
        :return:
        """
        device = dict()
        for name, value1 in vars(self).items():
            device[name] = value1
        # device.pop('client')
        return device

    def parse_dic(self, device: dict):
        """
        用字典初始化
        :param device:
        :return:
        """
        for name, value1 in device.items():
            setattr(self, name, value1)
