#!/usr/bin/env bash
: '
@File   : git_pull.sh
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-12-05
@Desc   : 初始化仓库和更新仓库
'

ROOT_PATH=$1
UPDATE_SIGN=$2
ICODE_NAME=$3
CTS_PACKAGE="package.json"
SMART_PACKAGE="smartium$CTS_PACKAGE"
REPO_PATH="$ROOT_PATH/cts"
SMART_PATH="$REPO_PATH/smartium"
GIT_BRANCH_UPSTREAM='--set-upstream-to'

function npm_install() {
  echo "更新npm仓库，如果长时间等待，请重新执行"
  # npm i --chromedriver_cdnurl=http://cdn.npm.taobao.org/dist/chromedriver
  npm i --registry=https://npm.taobao.org/mirrors/npm/
  npm i --registry=http://registry.npm.baidou-int.com
  echo "--------------- Done ----------------"
}

function clone() {
  if [ -z "$ICODE_NAME" ]; then
    echo "缺少用户名，请传入iCode用户名"
    echo "举例: ssh://YouRan@icode.baidou.com:8235/baidou/mbd-sqa/cts 则传入 -u YouRan"
    read -p '请输入iCode用户名' -r ICODE_NAME
  fi

  echo "-------------- 克隆仓库 --------------"
  echo "仓库存储路径：$ROOT_PATH"
  GIT_CLONE="ssh://$ICODE_NAME@icode.baidou.com:8235/baidou/mbd-sqa/cts"
  cd "$WORK_PATH" || exit 1
  git clone "$GIT_CLONE"
  cd "$REPO_PATH" || exit 1
  npm_install
  cd "$SMART_PATH" || exit 1
  npm_install
}

function pull() {
  response=$(git pull 2>&1)
  result=$(echo "$response" | grep "$CTS_PACKAGE" | head -1)
  result=$(echo "$result" | grep "^$CTS_PACKAGE")
  if [ -n "$result" ]; then
    echo "更新package.json"
    cd "$CTS_PATH" || exit
    npm_install
  fi

  if [[ $response =~ $SMART_PACKAGE ]]; then
    echo "更新smartium/package.json"
    cd "$SMART_PATH" || exit
    npm_install
  fi
  CURRENT_BRANCH=$(git branch | grep '\*' | sed "s/* //g")
  if [[ $response =~ $GIT_BRANCH_UPSTREAM ]]; then
    echo "关联远程分支origin/$CURRENT_BRANCH $CURRENT_BRANCH"
    git branch --set-upstream-to=origin/"$CURRENT_BRANCH" "$CURRENT_BRANCH"
  fi
}

if  [ ! -d "$REPO_PATH" ]; then
  clone
else
  if [ "$UPDATE_SIGN" == "0" ]; then
    echo "-------------- 更新仓库 --------------"
    cd "$REPO_PATH" || exit
    CURRENT_BRANCH=$(git branch | grep '\*' | sed "s/* //g")
    printf "更新分支: \x1B[0;32m%s\n\x1B[0m" "* $CURRENT_BRANCH"
    pull
    echo "更新完成"
#    result=$(git checkout "$CURRENT_BRANCH" 2>&1 | grep 'git pull')
#    if [ -n "$result" ]; then
#      pull
#    else
#      echo "已经是最新了"
#    fi
  fi
fi

