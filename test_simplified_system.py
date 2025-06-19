"""
测试简化的多智能体系统
"""
import subprocess
import sys
import time

def test_simplified_weather():
    """测试简化系统的天气查询功能"""
    print("测试简化系统 - 天气查询...")
    
    # 创建测试输入
    test_input = "今日北京天气\n"
    
    # 启动系统并发送输入
    process = subprocess.Popen(
        [sys.executable, "app_simplified.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # 发送输入
        stdout, stderr = process.communicate(input=test_input, timeout=120)
        
        # 打印输出
        print("系统输出:")
        print(stdout)
        
        if stderr:
            print("错误输出:")
            print(stderr)
        
        # 检查是否包含关键信息
        if "北京实时天气" in stdout and "温度" in stdout:
            print("\n✅ 天气查询测试成功！")
            return True
        else:
            print("\n❌ 天气查询测试失败！")
            return False
            
    except subprocess.TimeoutExpired:
        process.kill()
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def test_browser_functionality():
    """测试浏览器功能"""
    print("\n测试浏览器功能...")
    
    # 直接测试 open_web_page 函数
    try:
        from tools import open_web_page
        
        # 测试访问示例网站
        result = open_web_page("https://example.com", "content")
        print("浏览器功能测试结果:")
        print(result)
        
        if "网页内容获取" in result or "网页访问成功" in result:
            print("\n✅ 浏览器功能测试成功！")
            return True
        else:
            print("\n❌ 浏览器功能测试失败！")
            return False
            
    except Exception as e:
        print(f"❌ 浏览器功能测试出错: {e}")
        return False

def test_web_search():
    """测试网络搜索功能"""
    print("\n测试网络搜索功能...")
    
    try:
        from tools import search_web
        
        # 测试搜索
        result = search_web("Python编程")
        print("搜索功能测试结果:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        if "搜索结果" in result or "维基百科" in result:
            print("\n✅ 网络搜索测试成功！")
            return True
        else:
            print("\n❌ 网络搜索测试失败！")
            return False
            
    except Exception as e:
        print(f"❌ 网络搜索测试出错: {e}")
        return False

def main():
    """运行所有测试"""
    print("开始测试简化的多智能体系统...")
    print("=" * 60)
    
    results = []
    
    # 测试天气查询
    results.append(test_simplified_weather())
    
    # 测试浏览器功能
    results.append(test_browser_functionality())
    
    # 测试网络搜索
    results.append(test_web_search())
    
    # 总结结果
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print(f"✅ 成功: {sum(results)} 项")
    print(f"❌ 失败: {len(results) - sum(results)} 项")
    
    if all(results):
        print("\n🎉 所有测试通过！简化系统配置成功。")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查配置。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
