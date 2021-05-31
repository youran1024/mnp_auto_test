# !/usr/bin/env python3
# coding=utf-8

"""
@File   : test_cts.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-08-10
@Desc   : 打开CTS 小程序并进行测试
"""

import os
import sys
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CTS_RUNNER = os.path.join(CURRENT_PATH, 'CTSRunner')
sys.path.append(CTS_RUNNER)
from CTSRunner import CTSRunnerCore
from CTSRunner.SatUtil.ht_log_center import HTLogCenter, HTLogInfo

WORK_PATH = os.path.join(os.path.expanduser('~'), 'cts-runner')

DEVICE_TYPE_KEY = ['ios-release', 'ios', 'android', 'web']
TEST_TYPE_KEY = ['all', 'api', 'components', 'core']
MOCHA_SINGLE_KEY = ['mock', 'cov']
MOCHA_VALUE_KEY = [
    'host', 'swan-api', 'swan-components',
    'swan-core', 'swan-plugin', 'swan-life', 'local',
    'agile-pipeline-build-id', 'jsnative', 'v8jsc'
]

RUNNER_VERSION = "2.1.7"
VERSION_DETAIL = "http://wiki.baidou.com/pages/viewpage.action?pageId=1092795201"

# iOS如何进行CTS自动化测试
# http://wiki.baidou.com/pages/viewpage.action?pageId=976243971


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_var_name(var):
    return dict(var=var).keys()[0]


def get_param(_params):
    def __param(x):
        return str(x) + '='
    return list(map(__param, _params))


def array_to_dic(array):
    dic = {}
    for obj in array:
        dic[obj] = obj


def print_help():
    """
    打印帮助信息
    """
    print("版本信息： " + VERSION_DETAIL)
    print('''
@参数说明:（以下皆为可选参数）
    \033[4;37m仓库操作\033[0m
    \033[1;34m--branch -b\033[0m 分支名
    \033[1;34m--noUpdate -n\033[0m 不需要更新仓库
    
    \033[4;37m设备类型-可以缺省\033[0m
    \033[1;34m--ios\033[0m (iOS手百Daily包，可以缺省，缺省则自动获取插入的设备，多台设备优先启动Android)
    \033[1;34m--ios-release\033[0m 测试手百release包
    \033[1;34m--android \033[0m（可以缺省，同上）
    \033[1;34m--web \033[0m(web化相关测试，可以缺省，没有任何设备则指定为web测试)
    
    \033[4;37mcts操作，缺省测试全部\033[0m
    \033[1;34m--api\033[0m api测试
    \033[1;34m--components\033[0m 组件测试
    \033[1;34m--core\033[0m core测试
    \033[1;34m--case\033[0m -c 指定case路径
    
    \033[4;37mmocha相关操作\033[0m
    \033[1;34m--mock\033[0m, is mock
    \033[1;34m--cov\033[0m, collect coverage
    \033[1;34m--host <value>\033[0m, suzhu scheme
    \033[1;34m--swan-api <value>\033[0m, specify appkey of swan-api
    \033[1;34m--swan-components <value>\033[0m, specify appkey of swan-components
    \033[1;34m--swan-core <value>\033[0m, specify appkey of swan-core
    \033[1;34m--swan-plugin <value>\033[0m, specify appkey of swan-plugin
    \033[1;34m--swan-life <value>\033[0m, specify appkey of swan-life
    \033[1;34m--local <value>\033[0m, use local smartapp, a:api, c:components, o:core, p:plugin, localBuild
    \033[1;34m--agile-pipeline-build-id <value>\033[0m, AGILE_PIPELINE_BUILD_ID
    \033[1;34m--jsnative <value>\033[0m, specify AB_test
    \033[1;34m--v8jsc <value>\033[0m, specify AB_test;
    
@举个栗子:
    测试 daily包 本地对应分支 所有case
    \033[1;34m cts \033[0m
    
    测试 release包 branch分支 case brightness.js
    注意：切分支时会将本地修改 git stash
    \033[1;34m cts -r -b test -c \'bright*.js\'\033[0m
    ''')


if __name__ == "__main__":
    # 获取传入的参数
    import getopt
    from sys import exit

    params = sys.argv[1:]
    log_path = os.path.join(WORK_PATH, "log")
    HTLogCenter().init_env(log_path)
    HTLogInfo(params)
    opts = dict()
    try:
        g_param = ["case=", "branch=", "user=", "mocha=", "path=", "help", "release", "noupdate", "qrcode", "version"]
        g_param += MOCHA_SINGLE_KEY
        g_param += DEVICE_TYPE_KEY
        g_param += TEST_TYPE_KEY
        g_param += get_param(MOCHA_VALUE_KEY)

        opts, argv = getopt.getopt(
            params, "qrnhvc:b:u:m:p:",
            g_param
        )
    except getopt.GetoptError as e:
        HTLogInfo('解析参数出错' + str(e))
        print(" \033[1;31m%s \033[0m" % e)
        print(" cts -h to get help")
        exit()

    user = None
    path = None

    branch = None
    need_update = True

    device_type = 'android'
    test_type = 'all'
    case_path = None

    mocha_array = []
    mocha_dic = {}

    show_qr_code = False

    HTLogInfo(opts)
    for key, value in opts:
        key = key.replace('--', '')
        if key in ('-b', "branch"):
            branch = value
        elif key in ('-n', "noupdate"):
            need_update = False

        elif key in DEVICE_TYPE_KEY:
            device_type = key

        elif key in TEST_TYPE_KEY:
            test_type = key
        elif key in ('-c', "case"):
            case_path = value

        elif key in ('-u', "user"):
            user = value
        elif key in ('-p', "path"):
            path = value

        elif key in ('-q', 'qrcode'):
            show_qr_code = True
        elif key in ('-v', 'version'):
            print(RUNNER_VERSION)
            exit()
        elif key in ('-h', "help"):
            print_help()
            exit()
        else:
            if key in MOCHA_VALUE_KEY:
                if value:
                    mocha_dic[key] = value
            elif key in MOCHA_SINGLE_KEY:
                mocha_array.append(key)

    if path and len(path):
        user = None
        cmd_line = 'cd %s && rm -rf cts && ln -s %s cts' % (WORK_PATH, path)
        os.system(cmd_line)

    if show_qr_code:
        import os
        HTLogInfo('展示宿主工具二维码')
        image_path = resource_path('CTSRunner/SHELL/qrcode.jpg')
        is_ok = os.system('command -v imgcat && imgcat ' + image_path) == 0
        if not is_ok:
            file_path = '~/cts-runner/'
            os.system('cp ' + image_path + ' ' + file_path)
            os.system('open ' + file_path + 'qrcode.jpg')
    else:
        parameter = dict(
            user=user,
            branch=branch,
            need_update=need_update,
            device_type=device_type,
            test_type=test_type,
            case_path=case_path,
            mocha_array=mocha_array,
            mocha_dic=mocha_dic
        )

        HTLogInfo(parameter)
        try:
            CTSRunnerCore.CTSRunner(**parameter).run()
        except Exception as error:
            HTLogInfo('运行错误' + str(error))
