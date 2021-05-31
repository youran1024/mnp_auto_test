#!/usr/bin/env bash
: '
@File   : start.sh
@Author : YouRan
@Date   : 2020-03-31
@Desc   : 初始化工程
'

#UDID=$1
#PORT=$2
#WDA_PATH=$3
BAT_PORT=8090
ROOT_PATH=$1


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

clear_process_sys(){
  # 清理系统级进程
  CMD_LINE="ps -A | grep -v grep | grep $1 | grep $2 | awk '{print \$1}' | xargs kill -9"
  bash -c "$CMD_LINE"
  check_return "关闭$1:$2服务"
}

clear_port_service(){
  CMD_LINE="lsof -i:$1 | awk 'NR>1{print \$2}' | xargs kill -9"
  bash -c "$CMD_LINE"
  check_return "关闭$1端口服务"
}

start_bat(){
  bat_log="$1"/bat-"$2".log
  clear_process_sys bat $BAT_PORT
  clear_port_service $BAT_PORT
  # clear_port_service $BAT_PORT
  # nohup bat $BAT_PORT > /dev/null 2>&1 &
  bat $BAT_PORT > "$bat_log" 2>&1 &
#  nohup bat $BAT_PORT &
  check_return "打开Bat:$BAT_PORT"
}

echo "-------------- 启动服务 --------------"
start(){
  time=$(date '+%Y-%m-%d %H:%M')
  log_dir="$ROOT_PATH"/log/
  mkdir -p "$log_dir"

  start_bat "$log_dir" "$time"
}

start