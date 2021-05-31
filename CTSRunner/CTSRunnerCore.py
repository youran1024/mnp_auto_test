# !/usr/bin/env python3
# coding=utf-8

"""
@File   : CTSRunner.py
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-12-05
@Desc   : CTS 包管理工具
"""
import os
import sys
import multiprocessing as mp
from enum import Enum, unique
from CTSRunner.DeviceManager import execute_cmd
from CTSRunner.SatUtil import ht_service_log_center as logger
from CTSRunner.DeviceManager.device_manager import DeviceManager
from CTSRunner.SatUtil.pipelineGetMochaFail import handle_report
from CTSRunner.SatUtil.ht_service_log_center import HTServiceLogCenter
from CTSRunner.SatUtil.ht_monitor_log_center import HTMonitorLogCenter


SERVICE_MONITOR_SHELL = 'ps -A | grep -v grep | grep xcodebuild | grep id=%s'

CTS = 'cts'
INIT_PATH = 'init.sh'
ACTION_PATH = 'action.sh'
SERVICE_PATH = 'start.sh'
BRANCH = 'change_branch.sh'
BAT_SERVICE_PATH = 'start_bat.sh'
REPO_HANDLE_PATH = 'git_handle.sh'

PS_SHELL = "ps -ef | grep '%s' | grep -v grep"
RESULT_PORT = 'cts/mochawesome-report/mochawesome.html'

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
WORK_PATH = os.path.join(os.path.expanduser('~'), 'cts-runner')
CASE_PATH = os.path.join(WORK_PATH, 'cts', 'ctsAutoCase', 'case')

ALL_CASE = 'ctsAutoCase/case/*/*'
CTS_COMPONENTS = ['api', 'core', 'components', 'plugin']

is_test_finish = False


@unique
class DeviceType(Enum):
    """
    运行设备类型
    """
    iOS = "iosdaily"
    iOSRelease = "iosnew"
    Android = "android"
    Web = "web"

    @staticmethod
    def get_device_type(key):
        """
        获取运行设备类型
        :param key:
        :return:
        """
        if key and len(key):
            key = key.lower()
            key = key.replace("-", "")
            device_table = {name.lower(): member for name, member in DeviceType.__members__.items()}
            if key in device_table:
                return device_table[key]
        return DeviceType.Android


@unique
class TestType(Enum):
    """
    测试类型
    """
    All = 'all'
    Api = 'api'
    Core = 'core'
    Components = 'components'

    @staticmethod
    def get_test_type(key):
        """
        获取测试类型
        :param key:
        :return:
        """
        if key and len(key):
            test_table = {name.lower(): member for name, member in TestType.__members__.items()}
            if key in test_table:
                return test_table[key]
        return TestType.All


def start_service_process(path):
    """
    启动相关服务
    :path:
    :return:
    """
    import sys
    import time
    import subprocess
    if path:
        cmd = 'sh ' + path + ' ' + WORK_PATH
        task = subprocess.Popen(cmd,
                                shell=True,
                                stdin=sys.stdin,
                                stderr=sys.stderr,
                                bufsize=-1)
        while task.poll() is None:
            time.sleep(2)
        return task.returncode == 0
    return True


def start_service(path):
    """
    启动相关服务
    :path:
    :return:
    """
    import sys
    import subprocess
    if path:
        cmd = 'sh ' + path + ' ' + WORK_PATH
        # task = subprocess.Popen(cmd,
        #                         shell=True,
        #                         stdin=sys.stdin,
        #                         stderr=sys.stderr,
        #                         bufsize=-1)
        return os.system(cmd) == 0
    return True


def start_service_monitor(device, log_path, shell_path):
    """
    监控wda服务
    :device: 要启动的设备
    :log_path: 日志存放路径
    :shell_path: wda服务启动脚本路径
    :return:
    """
    import time
    check_duration = 2
    if not device.is_ios:
        return
    monitor = HTMonitorLogCenter(log_path=log_path, log_name='monitor')
    monitor.info('开启监控')
    try:
        while not is_test_finish:
            result = os.popen(SERVICE_MONITOR_SHELL % device.udid).readline().strip()
            if result and len(result):
                time.sleep(check_duration)
            else:
                monitor.info('监控到程序崩溃')
                monitor.info(result)
                monitor.info(f'重启服务:')
                start_service_process(shell_path)
    except Exception as e:
        print(e)
        monitor.error(str(e))


class CTSRunner(object):
    """CTS 测试执行"""
    def __init__(
            self,
            user=None,
            branch=None,
            need_update=True,
            device_type=None,
            test_type='all',
            case_path=None,
            mocha_array=None,
            mocha_dic=None
    ):
        self.user = user
        self.branch = branch
        self.need_update = need_update

        self.device_type = DeviceType.get_device_type(device_type)
        self.case_path = case_path

        self.mocha_array = mocha_array
        self.mocha_dic = mocha_dic
        self._log_path = self.get_log_path()

        HTServiceLogCenter(log_path=self._log_path, log_name='service')

        if not case_path:
            self.test_type = TestType.get_test_type(test_type)
            if self.test_type != TestType.All:
                self.case_path = 'ctsAutoCase/case/swan-%s/*' % self.test_type.value
            else:
                self.case_path = ALL_CASE
        else:
            paths = self.case_path.split('/')
            if paths and len(paths) == 1:
                path = os.path.join(WORK_PATH, 'cts', 'ctsAutoCase', '*')
                cmd_line = 'find %s -name %s' % (path, self.case_path)
                files = execute_cmd(cmd_line)

                if files and len(files):
                    if len(files) == 1:
                        self.case_path = files[0]
                    else:
                        for index, file in enumerate(files):
                            print("%s index:\033[1;34m [%d]\033[0m" % (file, index))
                        case_index = int(input("请输入Case的index:[eg 1, 2, 3 ...]\n"))
                        if case_index < len(files):
                            self.case_path = files[case_index]
                        else:
                            raise Exception('你输入的index超出界限')
                else:
                    print('没有找到相关Case文件:', path)
                    raise Exception('没有找到相关的文件:' + path)
        logger.Info('casePath:' + self.case_path)
        self.device_manager = DeviceManager()
        mg = self.device_manager
        logger.Info('设备信息：')
        logger.Info(self.device_manager.devices)
        if not len(mg.devices):
            self.device_type = DeviceType.Web
        if self.device_type in (DeviceType.iOS, DeviceType.iOSRelease):
            if not len(mg.ios_devices):
                self.device_type = DeviceType.Android
        if self.device_type == DeviceType.Android:
            if not len(mg.android_devices):
                if len(mg.ios_devices):
                    self.device_type = DeviceType.iOS

        if not self.mocha_dic:
            self.mocha_dic = {}
        self.mocha_dic["device-type"] = self.device_type.value
        self.mocha_dic["reporter"] = "mochawesome"
        if self.device_type in (DeviceType.iOS, DeviceType.iOSRelease):
            self.mocha_dic["sat-dev"] = mg.ios_devices[0].udid
            self.mocha_dic["wda-port"] = "8100"

        if not os.path.exists(WORK_PATH):
            os.makedirs(WORK_PATH)
            self.repo_handle()
        else:
            if self.change_branch():
                if not self.repo_handle():
                    raise Exception('仓库不存在，请提供iCode用户名， 或者本地仓库地址')

    @staticmethod
    def get_log_path():
        """
        获取日志目录地址
        :return:
        """
        import datetime
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:00")
        return os.path.join(WORK_PATH, 'cmd-log', now)

    def get_mocha_param(self):
        """
        获取mocha的参数
        :return:
        """
        def _param(x):
            return '--' + str(x)
        param = ''
        if self.mocha_array and len(self.mocha_array):
            params = list(map(_param, self.mocha_array))
            param = ' '.join(params)
        params = []
        if self.mocha_dic and len(self.mocha_dic):
            for key, value in self.mocha_dic.items():
                param1 = _param(key) + ' ' + str(value)
                params.append(param1)
        if len(param) or len(params):
            param += ' ' + ' '.join(params)
        return param

    def repo_handle(self):
        """
        更新CTS 仓库代码， 更新npm 依赖
        :return:
        """
        file_path = self._get_shell_path(REPO_HANDLE_PATH)
        cmd = 'sh ' + file_path + ' ' + WORK_PATH
        if self.need_update or self.user:
            sign = 0 if self.need_update else 1
            if self.need_update:
                logger.Info('更新仓库')
            cmd += ' ' + str(sign)

            if self.user:
                cmd += ' ' + self.user

            result = os.system(cmd)
            logger.Info('仓库操作完成')
            # self._waite_to_finish('npm')
            return result == 0
        return True

    def change_branch(self):
        """
        切换分支, 不需要切换这直接返回True
        :return:
        """
        if self.branch and len(self.branch):
            file_path = self._get_shell_path(BRANCH)
            cmd = 'sh ' + file_path + ' ' + WORK_PATH
            cmd += ' ' + self.branch
            return os.system(cmd) == 0
        return True

    @staticmethod
    def _get_shell_path(file):
        """
        获取执行文件路径
        :param file:
        :return:
        """
        return os.path.join(CURRENT_PATH, 'SHELL', file)

    def get_service_shell_path(self):
        """
        获取wda服务启动shell的path
        :return:
        """
        path = None
        if self.device_type in (DeviceType.iOS, DeviceType.iOSRelease):
            path = self._get_shell_path(SERVICE_PATH)
        elif self.device_type == DeviceType.Android:
            path = self._get_shell_path(BAT_SERVICE_PATH)
        return path

    @staticmethod
    def clear_test_env():
        """
        清理运行环境
        :return:
        """
        retry_path = os.path.join(CASE_PATH, 'swan-retry-*')
        cmd = 'rm -rf ' + retry_path
        if os.system(cmd) != 0:
            raise Exception('清理Case运行环境失败')

    def init_test_env(self):
        """
        清理运行环境
        :return:
        """
        logger.Info('初始化CTS运行环境')
        self.clear_test_env()
        path = os.path.join(CASE_PATH, 'swan-retry-')
        for name in CTS_COMPONENTS:
            os.makedirs(path + name)
        logger.Info('初始化CTS运行环境完成')

    def _waite_to_finish(self, cmd):
        import time
        time.sleep(3)
        while self._is_finish(cmd):
            time.sleep(1)

    @staticmethod
    def _is_finish(cmd):
        shell = PS_SHELL % cmd
        with os.popen(shell) as f:
            result = f.readlines()
            logger.Info(result)
        return len(result)

    @staticmethod
    def _do_action(path):
        file_path = os.path.join(CURRENT_PATH, path)
        os.system('open -a Terminal.app ' + file_path)

    def _generate_shell(self):
        import stat
        shell = r'''#!/usr/bin/env bash
        
        WORK_PATH=~/cts-runner
        file_path=${WORK_PATH}/cts
        cd "${file_path}" || exit
        '''
        shell = shell.replace("\t", "").replace("        ", '')
        shell1 = '\nmocha -t 240000 %s %s' % (self.case_path, self.get_mocha_param())
        print(shell1)
        logger.Info(shell1)
        shell = shell + shell1
        report = os.path.join(WORK_PATH, RESULT_PORT)
        shell = shell + '\nopen ' + report
        if not os.path.exists(WORK_PATH):
            os.makedirs(WORK_PATH)
        file_path = os.path.join(WORK_PATH, 'tmp')
        with open(file_path, 'w') as f:
            f.write(shell)
        # 执行该文件需要加权限
        os.chmod(file_path, stat.S_IRWXU)
        return file_path

    def run(self):
        """
        启动服务，并开始测试
        :return:
        """
        self.init_test_env()
        shell_path = self.get_service_shell_path()
        if start_service(shell_path):
            # 启动服务监控
            if self.device_type in (DeviceType.iOS, DeviceType.iOSRelease):
                # mp.set_start_method('forkserver')
                # p = mp.Pool(2)
                _device = self.device_manager.devices[0]
                import threading
                thread = threading.Thread(
                    target=start_service_monitor,
                    args=(_device, self._log_path, shell_path),
                    daemon=True
                )
                thread.start()

            cmd = 'sh ' + self._generate_shell() + ' ' + WORK_PATH
            if os.system(cmd) == 0:
                handle_report()
                cmd = 'cd ' + CASE_PATH + " && ls -lR swan-retry-* | grep '^-'"
                lines = execute_cmd(cmd)
                if len(lines):
                    print(lines)
                    logger.Info(str(lines))
                    print('存在失败的Case，需要重试')
                    self.case_path = 'ctsAutoCase/case/swan-retry-*/*/*'
                    print('重试地址:', self.case_path)
                    cmd = 'sh ' + self._generate_shell() + ' ' + WORK_PATH
                    os.system(cmd)
        global is_test_finish
        is_test_finish = True
        self.clear_test_env()


if __name__ == '__main__':
    device_tmp = DeviceType.iOS
    table = DeviceType.get_device_type('ios')

    parameter = {
        # "user": 'YouRan',
        # "is_daily": True,
        # "branch": 'master',
        # 'test_type': 'api',
        "case_path": '"generalIdentify*"',
        # "need_update": True
    }
    runner = CTSRunner(**parameter)
    runner.run()
