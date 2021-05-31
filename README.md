
# CTS 自动测试命令行工具（iOS && Android）
> 关于小程序的命令行工具， 仅供参考学习
1. 提供命令行打包脚本
2. 提供命令行调用
3. 提供iOS调起


### 主要功能
1. 支持任意位置调起`cts`、`cts --help`获取所有能力
1. 支持iOS && Android
1. 支持显示宿主二维码
2. 支持分支切换
3. 支持命令行任意位置启动
4. 支持引用本地仓库
5. 支持单Case调试
6. 支持指定Case模糊 `cts -c 'brig*.js'`
7. 支持Case分组测试 api/components/core
6. 支持Mocha所有的参数
8. 支持wda服务重启
9. 支持case重试


### 步骤
* [下载最新版工具包, 增量更新只需下载lite版本](http://172.20.115.56:3001/)
* 增量更新下载lite版本，执行`init_lite`则只更新`cts`工具

1. 执行`./Script/init.sh`(初始化使用，只需首次调用)

    1.1. 脚本要求输入本地cts仓库地址，如果没有直接回车 举例：`/Users/YouRan/Developer/CTS/baidou/mbd-sqa/cts/`
    
    1.2. 如果没有本地仓库，则会要求输入iCode用户名 `ssh://YouRan@icode...` 则输入YouRan
    
    1.3. 如果都没有输入则不拉取仓库，可以在后续步骤中重新拉取仓库

2. 打开宿主调试工具二维码`cts -q`， 手百扫码打开调试工具

    2.1 打开`请求不校验https`
    
    2.2 打开`加载cts性能测试`
    
    2.3 打开`域名校验豁免`
    
3. shell任意目录下调用`cts`， 系统自动打开服务，并执行测试

```sh
@参数说明:（以下皆为可选参数）
    仓库操作
    --branch -b 分支名
    --noUpdate -n 不需要更新仓库
    
    设备类型
    --ios (iOS手百Daily包，可以缺省，缺省则自动获取插入的设备，多台设备优先启动Android)
    --ios-release  测试手百release包
    --android （可以缺省，同上）
    --web (可以缺省，没有设备则执行web化相关测试)

    cts操作 缺省则是全部Case
    --api api测试
    --components  组件测试
    --core core测试
    --case -c 指定case路径
    
    mocha相关操作
    --mock, is mock
    --cov, collect coverage
    --host <value>, suzhu scheme
    --swan-api <value>, specify appkey of swan-api
    --swan-components <value>, specify appkey of swan-components
    --swan-core <value>, specify appkey of swan-core
    --swan-plugin <value>, specify appkey of swan-plugin
    --swan-life <value>, specify appkey of swan-life
    --local <value>, use local smartapp, a:api, c:components, o:core, p:plugin, localBuild
    --agile-pipeline-build-id <value>, AGILE_PIPELINE_BUILD_ID
    --jsnative <value>, specify AB_test
    --v8jsc <value>, specify AB_test
    
    初始化操作
    --user -u iCode用户名
        仓库不存在时，用来拉取cts仓库存储路径:`~/cts-runner`
        传入说明ssh://YouRan@icode...则传入：YouRan
    --path -p 用户本地仓库路径

    测试工具 
    --qrcode -q 显示宿主调试工具二维码
    --help -h 帮助文档    
    
@举个栗子:
    测试 daily包 本地对应分支 所有case
    cts
    
    测试 release包 branch分支 case brightness.js
    注意：切分支时会将本地修改 git stash
    cts -r -b test -c ctsAutoCase/case/swan-api/device/brightness.js
    
```


### 注意事项
* 无证书的话可以使用个人证书`修改位置 ~/cts-runner/webdriveragent/`
* [个人证书修改参考](https://testerhome.com/topics/7220)
* 切换分支的话，需要注意把本地修改保存后切换
* 如果搜索框无法输入，请检查键盘是否为系统键盘， 不支持三方键盘
* 如果无响应，请检查开源工具设置是否正确， `cts -q`打开开源工具二维码，使用手百扫码
* 如果无响应请重试`cts`命令
* mocha 参数未经测试，遇到问题还需要大家反馈一下


### 意见&Bug反馈 ^_^
如有意见欢迎反馈给`YouRan@baidou.com`


