#!/bin/sh
#导入所有的provision文件以及p12证书，如果有provsion或者证书有更新，请先执行这个脚本

print_success(){
  printf "%s: \x1B[0;32m%s\n\x1B[0m" "$1" "$2"
}

print_faile(){
  printf "%s: \x1B[0;31m%s\n\x1B[0m" "$1" "$2"
}

check_return() {
  value=$?
	if [ $value -ne 0 ]
	then
		print_faile "$1" Failure
		exit 1
	else
		print_success "$1" Success
	fi
}

CURRENT_PATH=$(cd "$(dirname "$0")" && pwd)

import_provisions(){
  find "$CURRENT_PATH" -name '*.mobileprovision' -print0 | xargs open
  check_return "Import all provisions"
}
import_provisions

install_p12(){
  #安装p12
  PASSWORDS=(123456 \"\")
  ALL_P12=$(find "$CURRENT_PATH" -name '*.p12')
  USERLOGIN_KEYCHIN="$HOME/Library/Keychains/login.keychain"

  for p12 in $ALL_P12; do
    SUCCESS=1
      for passwd in "${PASSWORDS[@]}"; do
          CMD="security import \"$p12\" -k $USERLOGIN_KEYCHIN  -P $passwd -T /usr/bin/codesign 2> /dev/null"
          #echo "Excute: [ $CMD ]"
          bash -c "$CMD"
          value=$?
          if ! [ $value -ne 0 ]; then
            SUCCESS=0
            break
          fi
      done

      if [ $SUCCESS -ne 0 ]; then
        #导入失败
        print_faile "Import p12 $p12" Failure
      else
        #导入成功
        print_success "Import p12 $p12" Success
      fi
  done
}

install_p12
