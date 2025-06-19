@echo off
:: AutoGen Voice Agent Launcher for Windows

:: 设置编码为UTF-8
chcp 65001 > nul

:: 获取脚本所在目录
set DIR=%~dp0

:: 切换到项目目录
cd /d "%DIR%"

:: 启动图形界面
python launcher.py

:: 如果出错则暂停
if errorlevel 1 pause
