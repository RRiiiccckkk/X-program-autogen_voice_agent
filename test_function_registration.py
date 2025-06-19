"""
测试函数注册问题
"""
import autogen
from config import load_executor_config
from tools import get_weather

print("1. 测试直接函数调用:")
print(get_weather("广州"))
print("-" * 60)

print("\n2. 测试 GroupChat 中的函数注册:")
# 加载配置
executor_config = load_executor_config()

# 创建执行者
executor = autogen.AssistantAgent(
    name="executor",
    system_message="You are a helpful assistant. Use get_weather function when asked about weather.",
    llm_config={
        "config_list": executor_config,
        "temperature": 0,
        "functions": [
            {
                "name": "get_weather",
                "description": "Get weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"}
                    },
                    "required": ["location"]
                }
            }
        ]
    }
)

# 创建用户代理
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config=False,
    function_map={"get_weather": get_weather}
)

# 创建群聊
groupchat = autogen.GroupChat(
    agents=[user_proxy, executor],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin"
)

# 创建管理器
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": executor_config}
)

print("用户代理函数映射:", list(user_proxy.function_map.keys()))
print("执行者函数配置:", executor.llm_config.get("functions", []))

# 测试对话
print("\n3. 启动 GroupChat 对话:")
print("-" * 60)
try:
    user_proxy.initiate_chat(
        manager,
        message="What's the weather in Guangzhou?"
    )
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
