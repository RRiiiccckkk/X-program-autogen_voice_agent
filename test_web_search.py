#!/usr/bin/env python3
"""
网络搜索功能测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from tools import search_web, search_duckduckgo, search_wikipedia, search_news, extract_webpage_content, get_exchange_rate

def test_search_functions():
    """测试所有搜索功能"""
    print("🔍 开始测试网络搜索功能...")
    print("=" * 60)
    
    # 测试 1: DuckDuckGo 搜索
    print("\n1. 测试 DuckDuckGo 搜索:")
    try:
        result = search_duckduckgo("Python 编程语言", max_results=2)
        print("✅ DuckDuckGo 搜索成功")
        print(f"结果预览: {result[:200]}...")
    except Exception as e:
        print(f"❌ DuckDuckGo 搜索失败: {e}")
    
    # 测试 2: 维基百科搜索
    print("\n2. 测试维基百科搜索:")
    try:
        result = search_wikipedia("人工智能")
        print("✅ 维基百科搜索成功")
        print(f"结果预览: {result[:200]}...")
    except Exception as e:
        print(f"❌ 维基百科搜索失败: {e}")
    
    # 测试 3: 综合搜索
    print("\n3. 测试综合搜索:")
    try:
        result = search_web("机器学习是什么")
        print("✅ 综合搜索成功")
        print(f"结果预览: {result[:200]}...")
    except Exception as e:
        print(f"❌ 综合搜索失败: {e}")
    
    # 测试 4: 新闻搜索
    print("\n4. 测试新闻搜索:")
    try:
        result = search_news("人工智能")
        print("✅ 新闻搜索成功")
        print(f"结果预览: {result[:200]}...")
    except Exception as e:
        print(f"❌ 新闻搜索失败: {e}")
    
    # 测试 5: 汇率查询
    print("\n5. 测试汇率查询:")
    try:
        result = get_exchange_rate("USD", "CNY")
        print("✅ 汇率查询成功")
        print(f"结果: {result}")
    except Exception as e:
        print(f"❌ 汇率查询失败: {e}")
    
    # 测试 6: 网页内容提取
    print("\n6. 测试网页内容提取:")
    try:
        result = extract_webpage_content("https://www.python.org", max_length=300)
        print("✅ 网页内容提取成功")
        print(f"结果预览: {result[:200]}...")
    except Exception as e:
        print(f"❌ 网页内容提取失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 网络搜索功能测试完成！")

def test_dependencies():
    """测试依赖包"""
    print("📦 检查依赖包...")
    
    try:
        import requests
        print("✅ requests 包已安装")
    except ImportError:
        print("❌ 缺少 requests 包，请运行: pip install requests")
        return False
    
    try:
        import bs4
        print("✅ beautifulsoup4 包已安装")
    except ImportError:
        print("❌ 缺少 beautifulsoup4 包，请运行: pip install beautifulsoup4")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 网络搜索功能测试")
    print("=" * 60)
    
    # 检查依赖
    if not test_dependencies():
        print("\n❌ 依赖包检查失败，请安装缺少的包后重试")
        sys.exit(1)
    
    # 运行搜索测试
    test_search_functions()
    
    print("\n💡 提示:")
    print("   - 如果某些搜索失败，可能是网络连接问题")
    print("   - 搜索功能已集成到执行者智能体中")
    print("   - 现在可以运行 'python app.py' 测试完整系统")
