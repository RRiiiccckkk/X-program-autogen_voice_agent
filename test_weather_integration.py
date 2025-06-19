"""
集成测试：测试多智能体系统的天气查询功能
"""
import subprocess
import sys
import time

def test_weather_query():
    """测试天气查询功能"""
    print("开始测试多智能体系统天气查询功能...")
    
    # 创建测试输入
    test_input = "今日广州天气\n"
    
    # 启动系统并发送输入
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # 发送输入
    stdout, stderr = process.communicate(input=test_input, timeout=120)
    
    # 打印输出
    print("系统输出:")
    print(stdout)
    
    if stderr:
        print("错误输出:")
        print(stderr)
    
    # 检查是否包含关键信息
    if "广州实时天气" in stdout and "温度" in stdout and "wttr.in" in stdout:
        print("\n✅ 测试成功！系统正确调用了 get_weather 函数并返回了实时天气数据。")
        return True
    else:
        print("\n❌ 测试失败！系统未能正确返回天气数据。")
        return False

if __name__ == "__main__":
    try:
        success = test_weather_query()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"测试出错: {e}")
        sys.exit(1)
