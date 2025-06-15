#!/usr/bin/env python3
"""
多智能体语音助手启动脚本
提供多种运行模式和环境检查
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🤖 多智能体语音助手系统")
    print("=" * 60)
    print("📊 规划者: o3-2025-04-16 (问题理解 + 战略规划)")
    print("🚀 执行者: o3-2025-04-16 (代码执行 + 技术实现)")
    print("📝 总结者: o4-mini (内容重组 + 格式优化)")
    print("🔍 反馈者: gpt-4o-2024-11-20 (质量评估)")
    print("👤 用户代理: 交互管理")
    print("=" * 60)

def check_environment():
    """检查运行环境"""
    print("\n🔍 检查运行环境...")
    
    # 检查 Python 版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 版本过低，需要 Python 3.8+")
        return False
    print(f"✅ Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要文件
    required_files = [
        "config.py",
        "app.py", 
        "OAI_CONFIG_LIST"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return False
        print(f"✅ 找到文件: {file}")
    
    # 检查依赖包
    try:
        import autogen
        print(f"✅ AutoGen 版本: {autogen.__version__}")
    except ImportError:
        print("❌ 缺少 AutoGen 包，请运行: pip install pyautogen")
        return False
    
    return True

def run_tests():
    """运行测试"""
    print("\n🧪 运行系统测试...")
    
    # 运行配置测试
    print("\n1. 运行配置测试:")
    try:
        result = subprocess.run([sys.executable, "test_model_config.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ 配置测试通过")
        else:
            print("❌ 配置测试失败")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 配置测试出错: {e}")
        return False
    
    # 运行单元测试
    print("\n2. 运行单元测试:")
    try:
        result = subprocess.run([sys.executable, "unit_test.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ 单元测试通过")
        else:
            print("❌ 单元测试失败")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 单元测试出错: {e}")
        return False
    
    # 运行网络搜索测试
    print("\n3. 运行网络搜索测试:")
    try:
        result = subprocess.run([sys.executable, "test_web_search.py"], 
                              capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ 网络搜索功能测试通过")
        else:
            print("❌ 网络搜索功能测试失败")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 网络搜索测试出错: {e}")
        return False
    
    return True

def start_app():
    """启动主应用"""
    print("\n🚀 启动多智能体系统...")
    print("💡 提示: 输入您的问题，系统将通过五智能体协作为您解答")
    print("📌 工作流程: 用户代理 → 规划者 → 执行者 → 总结者 → 反馈者")
    print("-" * 60)
    
    try:
        # 直接运行 app.py
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用多智能体语音助手系统！")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="多智能体语音助手启动脚本")
    parser.add_argument("--test", action="store_true", help="只运行测试，不启动应用")
    parser.add_argument("--no-check", action="store_true", help="跳过环境检查")
    parser.add_argument("--no-test", action="store_true", help="跳过测试直接启动")
    
    args = parser.parse_args()
    
    # 切换到脚本目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 打印横幅
    print_banner()
    
    # 环境检查
    if not args.no_check:
        if not check_environment():
            print("\n❌ 环境检查失败，请修复后重试")
            sys.exit(1)
    
    # 运行测试
    if args.test:
        if run_tests():
            print("\n✅ 所有测试通过！系统配置正确")
        else:
            print("\n❌ 测试失败，请检查配置")
            sys.exit(1)
        return
    
    if not args.no_test:
        if not run_tests():
            print("\n⚠️  测试失败，但您可以选择继续启动")
            choice = input("是否继续启动？(y/N): ").lower()
            if choice != 'y':
                sys.exit(1)
    
    # 启动应用
    start_app()

if __name__ == "__main__":
    main()
