"""
测试 get_weather 函数
"""
from tools import get_weather

def test_get_weather():
    print("测试 get_weather 函数...")
    print("=" * 60)
    
    # 测试1: 获取广州天气
    print("\n1. 测试获取广州天气:")
    result = get_weather("广州")
    print(result)
    
    # 测试2: 获取北京天气
    print("\n" + "=" * 60)
    print("\n2. 测试获取北京天气:")
    result = get_weather("北京") 
    print(result)
    
    # 测试3: 获取上海天气（英文）
    print("\n" + "=" * 60)
    print("\n3. 测试获取上海天气（英文模式）:")
    result = get_weather("Shanghai", lang="en")
    print(result)
    
    # 测试4: 测试无效城市
    print("\n" + "=" * 60)
    print("\n4. 测试无效城市:")
    result = get_weather("不存在的城市名称")
    print(result)
    
    print("\n" + "=" * 60)
    print("测试完成！")

if __name__ == "__main__":
    test_get_weather()
