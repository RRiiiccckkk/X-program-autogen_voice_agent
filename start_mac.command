#!/bin/bash

# macOS 专用启动脚本
# 双击即可运行

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 打印启动横幅
echo "============================================================"
echo "🤖 多智能体语音助手系统 (macOS)"
echo "============================================================"
echo "📊 规划者: o3-2025-04-16 (问题理解 + 战略规划)"
echo "🚀 执行者: o3-2025-04-16 (代码执行 + 技术实现)"
echo "📝 总结者: o4-mini (内容重组 + 格式优化)"
echo "🔍 反馈者: gpt-4o-2024-11-20 (质量评估)"
echo "👤 用户代理: 交互管理"
echo "============================================================"
echo ""
echo "🔍 检查运行环境..."

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "💡 请安装 Python 3.8+ 或使用 Homebrew: brew install python"
    echo "按任意键退出..."
    read -n 1
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查必要文件
required_files=("config.py" "app.py" "OAI_CONFIG_LIST")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件: $file"
        echo "按任意键退出..."
        read -n 1
        exit 1
    fi
    echo "✅ 找到文件: $file"
done

# 检查 AutoGen 包
if ! python3 -c "import autogen" 2>/dev/null; then
    echo "❌ 缺少 AutoGen 包"
    echo "💡 请运行: pip3 install pyautogen"
    echo "按任意键退出..."
    read -n 1
    exit 1
fi

echo "✅ AutoGen 包已安装"
echo ""
echo "🚀 启动多智能体系统..."
echo "💡 提示: 输入您的问题，系统将通过五智能体协作为您解答"
echo "📌 工作流程: 用户代理 → 规划者 → 执行者 → 总结者 → 反馈者"
echo "------------------------------------------------------------"
echo ""

# 启动应用
python3 app.py

echo ""
echo "👋 感谢使用多智能体语音助手系统！"
echo "按任意键关闭窗口..."
read -n 1
