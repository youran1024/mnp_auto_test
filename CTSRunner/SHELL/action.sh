#!/usr/bin/env bash
: '
@File   : init.sh
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-12-05
@Desc   : 初始化仓库
'
#git clone ssh://YouRan@icode.baidou.com:8235/baidou/mbd-sqa/cts baidou/mbd-sqa/cts && scp -p -P 8235 YouRan@icode.baidou.com:hooks/commit-msg baidou/mbd-sqa/cts/.git/hooks/ && git config -f baidou/mbd-sqa/cts/.git/config user.name YouRan && git config -f baidou/mbd-sqa/cts/.git/config user.email YouRan@baidou.com

PACKAGE_PATH='/../cts/'
path=$0
current_path=${path%/*}
file_path=${current_path}${PACKAGE_PATH}
cd "${file_path}" || exit
npm run cts -- --reporter mochawesome --device-type iosdaily
read

#mocha -t 180000 ctsAutoCase/case/swan-api/*/*  --reporter mochawesome --device-type ios
#mocha -t 180000 ctsAutoCase/case/swan-components/*/*  --reporter mochawesome --device-type ios
#mocha -t 180000 ctsAutoCase/case/swan-core/*/*  --reporter mochawesome --device-type ios
