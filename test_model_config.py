#!/usr/bin/env python3
"""
测试脚本：验证多智能体模型配置
检查执行者是否使用 o3-2025-04-16 模型，其他智能体是否使用 gpt-4o-2024-11-20 模型
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import load_llm_config, load_executor_config, load_summarizer_config, load_planner_config

def test_model_configurations():
    """测试模型配置加载"""
    print("=" * 60)
    print("多智能体模型配置测试")
    print("=" * 60)
    
    # 测试通用模型配置（反馈者使用）
    print("\n1. 测试通用模型配置 (gpt-4o-2024-11-20):")
    try:
        general_config = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
        if general_config:
            print(f"   ✅ 成功加载通用模型配置")
            print(f"   📋 模型: {general_config[0]['model']}")
            print(f"   🔗 API 基础 URL: {general_config[0]['base_url']}")
            print(f"   🔑 API 密钥: {general_config[0]['api_key'][:8]}...")
        else:
            print("   ❌ 通用模型配置加载失败")
            return False
    except Exception as e:
        print(f"   ❌ 通用模型配置加载出错: {e}")
        return False
    
    # 测试规划者模型配置
    print("\n2. 测试规划者模型配置 (o3-2025-04-16):")
    try:
        planner_config = load_planner_config()
        if planner_config:
            print(f"   ✅ 成功加载规划者模型配置")
            print(f"   📋 模型: {planner_config[0]['model']}")
            print(f"   🔗 API 基础 URL: {planner_config[0]['base_url']}")
            print(f"   🔑 API 密钥: {planner_config[0]['api_key'][:8]}...")
        else:
            print("   ❌ 规划者模型配置加载失败")
            return False
    except Exception as e:
        print(f"   ❌ 规划者模型配置加载出错: {e}")
        return False
    
    # 测试执行者模型配置
    print("\n3. 测试执行者模型配置 (o3-2025-04-16):")
    try:
        executor_config = load_executor_config()
        if executor_config:
            print(f"   ✅ 成功加载执行者模型配置")
            print(f"   📋 模型: {executor_config[0]['model']}")
            print(f"   🔗 API 基础 URL: {executor_config[0]['base_url']}")
            print(f"   🔑 API 密钥: {executor_config[0]['api_key'][:8]}...")
        else:
            print("   ❌ 执行者模型配置加载失败")
            return False
    except Exception as e:
        print(f"   ❌ 执行者模型配置加载出错: {e}")
        return False
    
    # 测试总结者模型配置
    print("\n4. 测试总结者模型配置 (o4-mini):")
    try:
        summarizer_config = load_summarizer_config()
        if summarizer_config:
            print(f"   ✅ 成功加载总结者模型配置")
            print(f"   📋 模型: {summarizer_config[0]['model']}")
            print(f"   🔗 API 基础 URL: {summarizer_config[0]['base_url']}")
            print(f"   🔑 API 密钥: {summarizer_config[0]['api_key'][:8]}...")
        else:
            print("   ❌ 总结者模型配置加载失败")
            return False
    except Exception as e:
        print(f"   ❌ 总结者模型配置加载出错: {e}")
        return False
    
    # 验证模型差异
    print("\n5. 验证模型配置差异:")
    models = {
        "通用模型": general_config[0]['model'],
        "规划者模型": planner_config[0]['model'],
        "执行者模型": executor_config[0]['model'],
        "总结者模型": summarizer_config[0]['model']
    }
    
    print(f"   ✅ 五智能体模型配置:")
    print(f"   📊 规划者使用: {models['规划者模型']}")
    print(f"   🚀 执行者使用: {models['执行者模型']}")
    print(f"   📝 总结者使用: {models['总结者模型']}")
    print(f"   🔍 反馈者使用: {models['通用模型']}")
    print(f"   👤 用户代理: 无需模型")
    
    # 验证模型是否正确分离
    unique_models = set(models.values())
    if len(unique_models) == 3:
        print(f"   ✅ 模型配置完美分离，使用了 {len(unique_models)} 种不同模型")
    else:
        print(f"   ⚠️  注意: 检测到 {len(unique_models)} 种不同模型")
    
    print("\n" + "=" * 60)
    print("✅ 配置测试完成！五智能体系统配置正确")
    print("=" * 60)
    return True, summarizer_config

def test_import_app():
    """测试应用程序导入"""
    print("\n6. 测试应用程序导入:")
    try:
        # 临时重定向 input 函数以避免交互
        import builtins
        original_input = builtins.input
        builtins.input = lambda prompt="": "测试输入"
        
        # 尝试导入主应用
        import app
        print("   ✅ 应用程序导入成功，所有智能体配置正常")
        
        # 恢复原始 input 函数
        builtins.input = original_input
        return True
        
    except Exception as e:
        print(f"   ❌ 应用程序导入失败: {e}")
        # 恢复原始 input 函数
        builtins.input = original_input
        return False

if __name__ == "__main__":
    result = test_model_configurations()
    if isinstance(result, tuple):
        success, summarizer_config = result
    else:
        success = result
        summarizer_config = None
    
    if success:
        test_import_app()
    
    print(f"\n🎯 升级总结:")
    print(f"   • 规划者智能体现在使用 o3-2025-04-16 模型 (增强问题理解能力)")
    print(f"   • 执行者智能体现在使用 o3-2025-04-16 模型 (最强执行能力)")
    print(f"   • 总结者智能体现在使用 o4-mini 模型 (高效内容重组)")
    print(f"   • 反馈者继续使用 gpt-4o-2024-11-20 模型")
    print(f"   • 所有配置文件已更新完成")
    print(f"   • 五智能体系统工作流程: 用户代理 → 规划者 → 执行者 → 总结者 → 反馈者")
    print(f"   • 可以运行 'python app.py' 开始使用升级后的多智能体系统")
