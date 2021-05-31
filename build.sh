#!/usr/bin/env bash
: '
@File   : build.sh
@Author : YouRan
@Date   : 2020-04-07
@Desc   : 打包脚本
'

CURRENT_PATH=$(cd "$(dirname "$0")" && pwd)
RESOURCE="$CURRENT_PATH"/Resource/

cp ./README.md ./../../docsify/sat/
pyinstaller --clean  test.spec --onefile
cp ./dist/test ./Resource/cts
tar -zcvf ./Versions/cts-runner.tar.gz ./Resource ./Script ./README.md
tar -zcvf ./Versions/cts-runner-lite.tar.gz ./Resource/Certificates ./Resource/cts ./Script/init_lite.sh ./README.md

cd "/usr/local/bin" || exit
rm -rf cts
# ln -s "$RESOURCE"/cts cts
cp "$RESOURCE"/cts cts
