#!/bin/bash

# 进入项目目录
cd "$(dirname "$0")"

# 激活虚拟环境
source .venv/bin/activate

# 运行 Python 脚本
.venv/bin/python app.py
