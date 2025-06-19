"""
直接测试天气功能集成
"""
from tools import get_weather
import autogen
from config import load_llm_config, load_executor_config

# 1. 首先测试函数本身
print("1. 测试 get_weather 函数:")
print("-" * 60)
result = get_weather("广州")
print(result)
print("-" * 60)

# 2. 测试函数在 autogen 中的注册
print("\n2. 测试函数注册:")
print("-" * 60)

# 创建一个简单的测试配置
executor_config = load_executor_config()
if not executor_config:
    print("无法加载执行者配置")
else:
    # 创建执行者
    executor = autogen.AssistantAgent(
        name="test_executor",
        system_message="You are a test executor. When asked about weather, use get_weather function.",
        llm_config={
            "config_list": executor_config,
            "temperature": 0,
            "functions": [
                {
                    "name": "get_weather",
                    "description": "Get real-time weather for a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name"
                            }
                        },
                        "required": ["location"]
                    }
                }
            ]
        }
    )
    
    # 创建用户代理
    user_proxy = autogen.UserProxyAgent(
        name="test_user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
        function_map={
            "get_weather": get_weather
        }
    )
    
    print("执行者配置:", executor.llm_config.get("functions"))
    print("用户代理函数映射:", list(user_proxy.function_map.keys()))
    
    # 测试对话
    print("\n3. 测试对话:")
    print("-" * 60)
    try:
        user_proxy.initiate_chat(
            executor,
            message="What's the weather in Beijing?"
        )
    except Exception as e:
        print(f"对话出错: {e}")
