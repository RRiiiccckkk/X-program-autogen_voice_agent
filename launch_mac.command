#!/bin/bash
# AutoGen Voice Agent Launcher for macOS

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到项目目录
cd "$DIR"

# 启动图形界面
python3 launcher.py
