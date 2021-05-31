# !/usr/bin/env python
# -*-encoding: utf-8 -*-
"""
解析mochawesome.json，重试cts
copy from cts
"""

import json
import os
import sys
import re

CTS_PATH = os.path.join(os.path.expanduser('~'), 'cts-runner', 'cts')


def replace(path):
    """
    替换失败Case路径
    :param path: 执行失败的用例路径
    :return: retry路径
    """
    path1 = re.sub(r'/swan-api/', '/swan-retry-api/', path)
    if path1 == path:
        path1 = re.sub(r'/swan-retry-api/.*?/', '/swan-retry-api/retry/', path)
    path2 = re.sub(r'/swan-components/', '/swan-retry-components/', path1)
    if path2 == path1:
        path2 = re.sub(r'/swan-retry-components/.*?/', '/swan-retry-components/retry/', path1)
    path3 = re.sub(r'/swan-core/', '/swan-retry-core/', path2)
    if path3 == path2:
        path3 = re.sub(r'/swan-retry-core/.*?/', '/swan-retry-core/retry/', path2)
    return path3


def handle_report():
    """
    处理测试结果
    :return:
    """
    # 读取mocha awesome-report文件夹下的json文件
    # report_path = sys.argv[1] + '/mochawesome-report/mochawesome.json'
    report_path = os.path.join(CTS_PATH, 'mochawesome-report/mochawesome.json')
    with open(report_path, 'rb') as fs:
        report_json = json.load(fs)

    # 判断mochaReport中，['suites']['suites']字段数组下，skipped、failures字段数组不为空的object对应的file字段
    if "results" in report_json:
        suites = report_json["results"][0]
    elif "suites" in report_json:
        suites = report_json["suites"]
    else:
        raise Exception('parse mochawesome.json fail')
    if isinstance(suites["suites"], list):
        for suite in suites["suites"]:
            if suite['failures']:
                file_path = suite['fullFile']
                # 将失败文件目录复制到ctsAutoCase/case/retry目录下
                retry_path = replace(file_path)
                retry_path = os.path.dirname(retry_path)
                if not os.path.exists(retry_path):
                    os.mkdir(retry_path)
                command = 'cp -r ' + file_path + ' ' + retry_path
                os.system(command)
