#!/usr/bin/env bash
: '
@File   : init.sh
@Author : YouRan
@Date   : 2020-03-31
@Desc   : 只跑Android的话，只需运行这个文件即可
'

ROOT_PATH=~/cts-runner
CURRENT_PATH=$(cd "$(dirname "$0")" && pwd)
RESOURCE="$CURRENT_PATH"/../Resource/
LIB_LOCATION="/usr/local/lib/node_modules/"

print_success(){
  printf "\x1B[0;32m%s\n\x1B[0m" "$1"
}

print_faile(){
  printf "\x1B[0;31m%s\n\x1B[0m" "$1"
}

check_return() {
  value=$?
	if [ $value -ne 0 ]
	then
		print_faile "$1失败"
		exit 1
	else
		print_success "$1成功"
	fi
}

is_install(){
  if [ -x "$(command -v "$1")" ]; then
    return 0
  fi
  return 1
}

f_install(){
  echo "👨‍💻 正在检查 ==> $1"
  if ! is_install "$1"; then
  	echo "😝 正在安装 ==> $1"
  	if [ "$3" == 1 ]; then
  	  pip3 install "$2"
  	elif [ "$3" == 2 ]; then
  	  brew install "$2"
  	elif [ "$3" == 3 ]; then
      npm --registry http://registry.npm.baidou-int.com install -g "$2"
  	else
  	  echo "$2"
  	  ($2)
  	fi

    if is_install "$1"; then
      print_success "😃 安装成功 ==> $1"
    else
      print_faile "😂 安装失败 ==> $1"
    fi
  else
    print_success "😃 已经安装 ==> $1"
  fi
}

pip_install(){
  f_install "$1" "$2" 1
}

_install_npm_package(){
  if [ ! -e "$LIB_LOCATION$1" ]; then
    echo "安装：$1"
    npm --registry http://registry.npm.baidou-int.com install -g "$1" > /dev/null
    check_return "安装：$1"
  fi
}

_install_npm_package_tb(){
  # https://developer.aliyun.com/mirror/NPM
  # https://npm.taobao.org/mirrors/npm/
  if [ ! -e "$LIB_LOCATION$1" ]; then
    echo "安装：$1"
    npm --registry http://npm.taobao.org/mirrors/chromedriver install -g "$1" > /dev/null
    check_return "安装：$1"
  fi
}

_install_npm_chromedriver(){
  if [ ! -e "$LIB_LOCATION$1" ]; then
    echo "安装：$1"
    npm --chromedriver_cdnurl=http://cdn.npm.taobao.org/dist/chromedriver install -g chromedriver > /dev/null
    check_return "安装：$1"
  fi
}

install_npm_package(){
  _install_npm_package 'bat-agent'
  _install_npm_package 'mocha'
  _install_npm_package 'mochawesome'
  # _install_npm_package_tb 'chromedriver'
  _install_npm_chromedriver 'chromedriver'
}

_pip_install(){
  echo "安装 $1"
  cmd="python3 -m pip install $1 -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com"
  bash -c "$cmd" > /dev/null
  check_return "安装 $1"
}

pip_install_all(){
  value=$(ls /Applications/*iTerm*)
  if [ "$value" = "Contents" ]; then
    _pip_install imgcat
  fi
}

check_git_repo(){
  file_path=$ROOT_PATH/cts
  echo "$file_path"
  if [ ! -d "$file_path" ]; then
    echo "仓库不存在：$file_path"
    echo "需要初始化仓库"
    echo "请输入本地仓库路径, 没有则直接回车"
    read -r LOCAL_PATH
    if [ -n "$LOCAL_PATH" ]; then
        cd "$ROOT_PATH" || exit
        ln -s "$LOCAL_PATH" cts
        cd - || exit
    else
      echo "请输入iCode用户名"
      echo "举例: ssh://YouRan@icode.baidou.com:8235/baidou/mbd-sqa/cts 则输入YouRan"
      read -r NAME
    fi
  fi
}

install_package(){
  pip_install_all
  install_npm_package
}

start(){
  # git pull > /dev/null 2>&1
  if [ ! -d "$ROOT_PATH" ]; then
    mkdir "$ROOT_PATH"
  fi
  check_git_repo
  install_package

  echo "安装命令行"
  cd "/usr/local/bin" || exit
  rm -rf cts
  # ln -s "$RESOURCE"/cts cts
  cp "$RESOURCE"/cts cts
  check_return "命令行安装"

  if [ -n "$NAME" ]; then
    echo "克隆仓库"
    sh "$CURRENT_PATH"/repo_init.sh "$NAME" "$ROOT_PATH"
    check_return "克隆仓库"
  fi
}

start
print_success "初始化完成"
