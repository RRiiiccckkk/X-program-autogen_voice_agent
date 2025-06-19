#!/bin/bash
# AutoGen Voice Agent Launcher for Linux

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到项目目录
cd "$DIR"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    echo "请安装 Python 3 后再试"
    read -p "按 Enter 键退出..."
    exit 1
fi

# 启动图形界面
python3 launcher.py
