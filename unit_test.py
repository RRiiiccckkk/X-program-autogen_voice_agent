#!/usr/bin/env python3
"""
单元测试：验证多智能体模型升级
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import load_llm_config, load_executor_config, load_summarizer_config, load_planner_config

class TestModelUpgrade(unittest.TestCase):
    """测试模型升级的单元测试类"""
    
    def test_general_model_config(self):
        """测试通用模型配置加载"""
        config = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
        
        # 验证配置不为空
        self.assertIsNotNone(config, "通用模型配置不应为空")
        self.assertTrue(len(config) > 0, "通用模型配置列表不应为空")
        
        # 验证模型名称
        self.assertEqual(config[0]['model'], "gpt-4o-2024-11-20", 
                        "通用模型应为 gpt-4o-2024-11-20")
        
        # 验证必要字段存在
        self.assertIn('api_key', config[0], "配置应包含 api_key")
        self.assertIn('base_url', config[0], "配置应包含 base_url")
        self.assertIn('api_type', config[0], "配置应包含 api_type")
    
    def test_executor_model_config(self):
        """测试执行者模型配置加载"""
        config = load_executor_config()
        
        # 验证配置不为空
        self.assertIsNotNone(config, "执行者模型配置不应为空")
        self.assertTrue(len(config) > 0, "执行者模型配置列表不应为空")
        
        # 验证模型名称
        self.assertEqual(config[0]['model'], "o3-2025-04-16", 
                        "执行者模型应为 o3-2025-04-16")
        
        # 验证必要字段存在
        self.assertIn('api_key', config[0], "配置应包含 api_key")
        self.assertIn('base_url', config[0], "配置应包含 base_url")
        self.assertIn('api_type', config[0], "配置应包含 api_type")
    
    def test_model_separation(self):
        """测试模型配置分离"""
        general_config = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
        executor_config = load_executor_config()
        
        # 验证两个配置都加载成功
        self.assertIsNotNone(general_config, "通用配置加载失败")
        self.assertIsNotNone(executor_config, "执行者配置加载失败")
        
        # 验证模型不同
        self.assertNotEqual(general_config[0]['model'], executor_config[0]['model'],
                           "执行者和其他智能体应使用不同的模型")
        
        # 验证具体模型名称
        self.assertEqual(general_config[0]['model'], "gpt-4o-2024-11-20")
        self.assertEqual(executor_config[0]['model'], "o3-2025-04-16")
    
    def test_planner_model_config(self):
        """测试规划者模型配置加载"""
        config = load_planner_config()
        
        # 验证配置不为空
        self.assertIsNotNone(config, "规划者模型配置不应为空")
        self.assertTrue(len(config) > 0, "规划者模型配置列表不应为空")
        
        # 验证模型名称
        self.assertEqual(config[0]['model'], "o3-2025-04-16", 
                        "规划者模型应为 o3-2025-04-16")
        
        # 验证必要字段存在
        self.assertIn('api_key', config[0], "配置应包含 api_key")
        self.assertIn('base_url', config[0], "配置应包含 base_url")
        self.assertIn('api_type', config[0], "配置应包含 api_type")
    
    def test_summarizer_model_config(self):
        """测试总结者模型配置加载"""
        config = load_summarizer_config()
        
        # 验证配置不为空
        self.assertIsNotNone(config, "总结者模型配置不应为空")
        self.assertTrue(len(config) > 0, "总结者模型配置列表不应为空")
        
        # 验证模型名称
        self.assertEqual(config[0]['model'], "o4-mini", 
                        "总结者模型应为 o4-mini")
        
        # 验证必要字段存在
        self.assertIn('api_key', config[0], "配置应包含 api_key")
        self.assertIn('base_url', config[0], "配置应包含 base_url")
        self.assertIn('api_type', config[0], "配置应包含 api_type")
    
    def test_five_agent_model_separation(self):
        """测试五智能体模型配置分离"""
        general_config = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
        planner_config = load_planner_config()
        executor_config = load_executor_config()
        summarizer_config = load_summarizer_config()
        
        # 验证所有配置都加载成功
        self.assertIsNotNone(general_config, "通用配置加载失败")
        self.assertIsNotNone(planner_config, "规划者配置加载失败")
        self.assertIsNotNone(executor_config, "执行者配置加载失败")
        self.assertIsNotNone(summarizer_config, "总结者配置加载失败")
        
        # 验证模型名称正确
        self.assertEqual(general_config[0]['model'], "gpt-4o-2024-11-20")
        self.assertEqual(planner_config[0]['model'], "o3-2025-04-16")
        self.assertEqual(executor_config[0]['model'], "o3-2025-04-16")
        self.assertEqual(summarizer_config[0]['model'], "o4-mini")
        
        # 验证模型都不相同（除了规划者和执行者都使用o3）
        models = [general_config[0]['model'], planner_config[0]['model'], executor_config[0]['model'], summarizer_config[0]['model']]
        unique_models = set(models)
        self.assertEqual(len(unique_models), 3, "应该有3种不同的模型")
    
    def test_api_consistency(self):
        """测试 API 配置一致性"""
        general_config = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
        executor_config = load_executor_config()
        summarizer_config = load_summarizer_config()
        
        # 验证使用相同的 API 密钥和基础 URL
        self.assertEqual(general_config[0]['api_key'], executor_config[0]['api_key'],
                        "应使用相同的 API 密钥")
        self.assertEqual(general_config[0]['base_url'], executor_config[0]['base_url'],
                        "应使用相同的基础 URL")
        self.assertEqual(general_config[0]['api_type'], executor_config[0]['api_type'],
                        "应使用相同的 API 类型")
        
        # 验证总结者也使用相同的 API 配置
        self.assertEqual(general_config[0]['api_key'], summarizer_config[0]['api_key'],
                        "总结者应使用相同的 API 密钥")
        self.assertEqual(general_config[0]['base_url'], summarizer_config[0]['base_url'],
                        "总结者应使用相同的基础 URL")
        self.assertEqual(general_config[0]['api_type'], summarizer_config[0]['api_type'],
                        "总结者应使用相同的 API 类型")

def run_unit_tests():
    """运行单元测试"""
    print("🧪 开始运行单元测试...")
    print("=" * 50)
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModelUpgrade)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 50)
    if result.wasSuccessful():
        print("✅ 所有单元测试通过！模型升级配置正确。")
        return True
    else:
        print("❌ 部分单元测试失败，请检查配置。")
        return False

if __name__ == "__main__":
    success = run_unit_tests()
    
    if success:
        print("\n🎉 升级验证完成！")
        print("📋 升级摘要:")
        print("   ✓ 规划者智能体已升级为 o3-2025-04-16 模型 (增强问题理解能力)")
        print("   ✓ 执行者智能体已升级为 o3-2025-04-16 模型 (最强执行能力)")
        print("   ✓ 总结者智能体使用 o4-mini 模型 (高效内容重组)")
        print("   ✓ 反馈者保持使用 gpt-4o-2024-11-20 模型")
        print("   ✓ 所有配置文件已正确更新")
        print("   ✓ 单元测试全部通过")
        print("\n📌 五智能体系统工作流程:")
        print("   用户代理 → 规划者 → 执行者 → 总结者 → 反馈者")
        print("\n🚀 现在可以运行 'python app.py' 使用升级后的多智能体系统！")
