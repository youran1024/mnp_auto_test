#!/usr/bin/env bash
: '
@File   : init.sh
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-12-05
@Desc   : 初始化仓库
'
#git clone ssh://YouRan@icode.baidou.com:8235/baidou/mbd-sqa/cts baidou/mbd-sqa/cts && scp -p -P 8235 YouRan@icode.baidou.com:hooks/commit-msg baidou/mbd-sqa/cts/.git/hooks/ && git config -f baidou/mbd-sqa/cts/.git/config user.name YouRan && git config -f baidou/mbd-sqa/cts/.git/config user.email YouRan@baidou.com

NAME=$1
ROOT_PATH=~/cts-runnter
GIT_CLONE="ssh://$NAME@icode.baidou.com:8235/baidou/mbd-sqa/cts"

cd "$ROOT_PATH" || exit
git clone "$GIT_CLONE"
echo "$CLONE_CMD"
cd 'cts' || exit
echo "更新npm仓库，初始化等待时间可能较长，如果时间过长，请重新执行"
npm i --chromedriver_cdnurl=http://cdn.npm.taobao.org/dist/chromedriver
npm i --registry https://npm.taobao.org/mirrors/npm/
npm i --registry http://registry.npm.baidou-int.com &
sleep 15
