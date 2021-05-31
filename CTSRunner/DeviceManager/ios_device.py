#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@File   : ios_device.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-11-4
@Desc   : iOS设备管理
"""

from . import execute_cmd
from .device import Device
from .ios_device_table import DEVICE_TYPE_TABLE

# 获取设备列表
UDID_LIST_SHELL = 'idevice_id -l'
# 获取设备信息
# DEVICE_INFO = 'ideviceinfo'
DEVICE_INFO = 'ideviceinfo --simple'


class IOSDevice(object):

    @property
    def devices(self) -> [Device]:
        udids = execute_cmd(UDID_LIST_SHELL)
        if len(udids) == 0:
            return []

        device_info = self._get_device_info(udids)
        if len(device_info) == 0:
            return []

        devices = []
        for info in device_info:
            device = Device(info=info)
            devices.append(device)
        return devices

    def _get_device_info(self, udids: [str]) -> [dict]:
        devices_info = []
        if udids and len(udids):
            for udid in udids:
                # info = execute_cmd(DEVICE_INFO + ' -u ' + udid)
                # 只支持单台设备
                info = execute_cmd(DEVICE_INFO)
                if not isinstance(info, list) or len(info) == 1:
                    # 如果没有获取到信息，则跳过
                    # 只有一条信息的时候是错误
                    continue
                if len(info):
                    info_dic = self._string_to_dic(info)
                    if info_dic and isinstance(info_dic, dict):
                        devices_info.append(info_dic)
        return devices_info

    def _string_to_dic(self, info_string):
        """
        将获取设备信息的字符串转换成字典
        :param info_string:
        :return: 设备字典
             {
                "DeviceName": "",
                "UniqueDeviceID": "",
                "ProductVersion": "",
                "ProductType": ""
                "PlateForm": "iOS"
             }
        """
        info_dic = {}
        for info in info_string:
            split_array = info.split(':')
            key1 = split_array[0].strip()
            value1 = split_array[1].strip()
            if key1 == 'ProductType':
                value1 = self._parse_device_type(value1)
            info_dic[key1] = value1

        info_dic["PlateForm"] = "iOS"

        return info_dic

    @staticmethod
    def _parse_device_type(product_type):
        product_type = product_type.strip()
        device_type = DEVICE_TYPE_TABLE.get(product_type, None)
        if device_type:
            return device_type
        else:
            return 'Other'

