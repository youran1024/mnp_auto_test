#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@File   : device_manager.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-10-13
@Desc   : 模拟器管理
"""

from . import HTSingleton
from .device import Device
from .ios_device import IOSDevice
from .android_device import AndroidDevice


class DeviceManager(HTSingleton):

    def __init__(self):
        super(DeviceManager, self).__init__()
        if self._first_init:
            self._devices = None
            self._first_init = False
            self.ios_devices = IOSDevice().devices
            self.android_devices = AndroidDevice().devices

    @property
    def devices(self) -> [Device]:
        """
        获取所有的设备信息（iOS、Android）
        :return:
        """
        if not self._devices:
            self._devices = self.ios_devices + self.android_devices

        return self._devices

    @devices.setter
    def devices(self, devices_tmp):
        """
        设置devices
        :param devices_tmp:
        :return:
        """
        if len(devices_tmp):
            self._devices = devices_tmp

    def get_device(self, udid=None) -> Device or None:
        """
        获取设备信息
        :param udid:
        :return:
        """
        # 如果不传，则默认取第一台设备
        if not udid or len(udid) == 0:
            if self.devices and len(self.devices):
                return self.devices[0]
            return None

        for device in self.devices:
            if device.udid == udid:
                return device
        return None

