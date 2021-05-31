#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@File   : android_device.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-11-4
@Desc   : Android设别管理
"""

from . import execute_cmd
from .device import Device


DEVICES_LIST_SHELL = 'adb devices'
# 设备类型
DEVICE_TYPE = 'ro.product.manufacturer'
# 系统版本
DEVICE_VERSION = 'ro.build.version.release'
# 设备型号
DEVICE_MODEL = 'ro.product.codename'
DEVICE_MODEL_HW = 'ro.product.model'
# 设备名称
DEVICE_NAME = 'net.devicename'
DEVICE_NAME_HW = 'net.hostname'


class AndroidDevice(object):

    @property
    def devices(self) -> [Device]:
        device_udids = execute_cmd(DEVICES_LIST_SHELL)
        _device_udids = []
        for udid in device_udids:
            if "List of devices" in udid:
                continue
            device = udid.split('\t')[0]
            _device_udids.append(device)

        devices = []
        for udid in _device_udids:
            device_info = self._fetch_device_info(udid)
            device = Device(info=device_info)
            devices.append(device)
        return devices

    def _fetch_device_info(self, udid):
        """
        设备信息
        :param udid:
        :return:
             {
                "DeviceName": "",
                "UniqueDeviceID": "",
                "ProductVersion": "",
                "ProductType": ""
                "PlateForm": "Android"
             }
        """
        device_info = dict()
        device_info['PlateForm'] = 'Android'
        device_info['UniqueDeviceID'] = udid
        name = self._get_info(udid, DEVICE_NAME, DEVICE_NAME_HW)
        if isinstance(name, list) and len(name):
            name = name[0].strip()
        if not name or len(name) == 0:
            name = 'no name'
        device_info['DeviceName'] = name
        version = self._get_info(udid, DEVICE_VERSION)
        if version and isinstance(version, list) and len(version):
            version = version[0]
        device_info['ProductVersion'] = version
        device_type = self._get_info(udid, DEVICE_MODEL, DEVICE_MODEL_HW)
        if isinstance(device_type, list) and len(device_type):
            device_type = device_type[0]
        device_info['ProductType'] = device_type

        return device_info

    def _get_info(self, udid, *cmd_list):
        _info = None
        for cmd in cmd_list:
            _cmd = self._generate_cmd(udid, cmd)
            _info = execute_cmd(_cmd)
            if _info and len(_info):
                break
        return _info

    @staticmethod
    def _generate_cmd(udid, cmd):
        _cmd = list()
        _cmd.append('adb -s')
        _cmd.append(udid)
        _cmd.append('shell getprop')
        _cmd.append(cmd)
        _cmd = ' '.join(_cmd)
        return _cmd
