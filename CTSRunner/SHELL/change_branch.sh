#!/usr/bin/env bash
: '
@File   : git_pull.sh
@Author : YouRan
@Contact: YouRan@baidou.com
@Date   : 2019-12-05
@Desc   : 更新CTS代码，并执行测试
'
BRANCH=$2
ROOT_PATH=$1
file_path="$ROOT_PATH"/cts

function change_branch() {
    CURRENT_BRANCH="$(git branch | grep '\*')"
    printf "当前分支: \x1B[0;32m%s\n\x1B[0m" "$CURRENT_BRANCH"
    if [ -n "$BRANCH" ]; then
        if ! [ "* $BRANCH" == "$CURRENT_BRANCH" ]; then
             printf "切换分支: \x1B[0;32m%s\n\x1B[0m" "$BRANCH"
            git stash
            # 不允许分支有变动(可能是本地开发分支，不再使用）
            # git checkout -- .
            # 检查本地是否有对应的分支
            check_branch=$(git branch | grep "$BRANCH")
            if [ -n "$check_branch" ]; then
                git checkout "$BRANCH"
                value=$?
                if [ $value -ne 0 ]; then
                    printf "\x1B[0;31m切换分支失败，程序结束。\n\x1B[0m"
                    exit 1
                fi
            else
                check_branch=$(git branch -a | grep "$BRANCH")
                if [ -n "$check_branch" ]; then
                    git checkout -b "$BRANCH" origin/"$BRANCH"
                    value=$?
                    if [ $value -ne 0 ]; then
                        printf "\x1B[0;31m切换分支失败，程序结束。\n\x1B[0m"
                        exit 1
                    fi
                else
                    printf "\x1B[0;31m切换分支失败，请检查分支是否存在，程序结束。\n\x1B[0m"
                    exit 1
                fi
            fi
        fi
    else
        printf "\x1B[0;31m缺少分支参数 \n\x1B[0m"
        exit 1
    fi
}

if [ -d "$file_path" ]; then
  cd "${file_path}" || exit
  echo "-------------- 切换分支 --------------"
  # echo "仓库路径：$ROOT_PATH"
  change_branch

  printf "切换后分支: \x1B[0;32m%s\n\x1B[0m" "$(git branch | grep '\*')"
  echo "--------------- Done ----------------"
  else
    echo "$file_path不存在"
fi
