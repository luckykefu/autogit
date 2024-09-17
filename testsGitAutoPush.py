# 000\Test000.py
# --coding:utf-8--
# Time:2024-09-17 22:56:54
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import os

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 更改当前工作目录
os.chdir(script_dir)

#####################################################
# TODO: GitAutoPush
from src.git_auto_push import git_auto_push

if __name__ == '__main__':
    git_repo_paths=r'D:\Github\0MyApp main'

    git_auto_push(git_repo_paths)

#####################################################
