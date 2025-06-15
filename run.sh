#!/bin/bash

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 打印启动横幅
echo "============================================================"
echo "🤖 多智能体语音助手系统"
echo "============================================================"
echo "📊 规划者: o3-2025-04-16 (问题理解 + 战略规划)"
echo "🚀 执行者: o3-2025-04-16 (代码执行 + 技术实现)"
echo "📝 总结者: o4-mini (内容重组 + 格式优化)"
echo "🔍 反馈者: gpt-4o-2024-11-20 (质量评估)"
echo "👤 用户代理: 交互管理"
echo "============================================================"
echo ""
echo "🚀 启动多智能体系统..."
echo "💡 提示: 输入您的问题，系统将通过五智能体协作为您解答"
echo "📌 工作流程: 用户代理 → 规划者 → 执行者 → 总结者 → 反馈者"
echo "------------------------------------------------------------"

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到 Python，请确保已安装 Python 3.8+"
    exit 1
fi

# 优先使用 python3，如果不存在则使用 python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# 使用智能启动脚本
if [ -f "start.py" ]; then
    $PYTHON_CMD start.py --no-test
else
    # 如果启动脚本不存在，直接运行主程序
    $PYTHON_CMD app.py
fi
