import autogen
import os
from config import load_default_config
from tools import search_web, get_weather, open_web_page

# 统一加载配置
config_list = load_default_config()
if not config_list:
    raise ValueError("LLM 配置加载失败，请检查 OAI_CONFIG_LIST 文件。")

# 统一的 LLM 配置
default_llm_config = {
    "config_list": config_list,
    "temperature": 0,
    "timeout": 60,
}

# 执行者专用配置（包含函数调用）
executor_llm_config = {
    "config_list": config_list,
    "temperature": 0,
    "timeout": 60,
    "functions": [
        {
            "name": "search_web",
            "description": "综合网络搜索功能（DuckDuckGo + 维基百科）",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询词"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_weather",
            "description": "获取指定城市的实时天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称（支持中文、英文），如 '广州'、'Beijing'"
                    }
                },
                "required": ["location"]
            }
        },
        {
            "name": "open_web_page",
            "description": "打开网页并执行操作（截图、获取内容等）",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要打开的网页URL"
                    },
                    "action": {
                        "type": "string",
                        "description": "操作类型：screenshot（截图）、content（获取内容）、logs（获取日志）",
                        "enum": ["screenshot", "content", "logs"],
                        "default": "screenshot"
                    }
                },
                "required": ["url"]
            }
        }
    ]
}

# 定义智能体
planner = autogen.AssistantAgent(
    name="planner",
    system_message="""You are a Strategic Planner. 用中文回答。

职责：
1. 深入理解用户的问题和需求
2. 制定详细的执行计划
3. 为执行者提供明确的指导

当规划完成时，说"PLAN_COMPLETE"。""",
    llm_config=default_llm_config,
)

executor = autogen.AssistantAgent(
    name="executor",
    system_message="""You are a Code Execution Expert with web capabilities. 用中文回答。

职责：
1. 根据规划者的计划执行任务
2. 使用提供的工具获取实时信息
3. 提供详细的执行结果

可用工具：
- search_web(query): 网络搜索
- get_weather(location): 获取天气信息
- open_web_page(url, action): 打开网页并截图/获取内容

重要：当用户询问天气时，必须使用 get_weather() 函数获取实时数据。
当用户要求访问网页时，使用 open_web_page() 函数。

执行完成时，说"EXECUTION_COMPLETE"。""",
    llm_config=executor_llm_config,
)

summarizer = autogen.AssistantAgent(
    name="summarizer",
    system_message="""You are an Answer Summarizer. 用中文回答。

职责：
1. 整理执行者的输出结果
2. 格式化答案以便用户理解
3. 确保信息完整和易读

总结完成时，说"SUMMARY_COMPLETE"。""",
    llm_config=default_llm_config,
)

reviewer = autogen.AssistantAgent(
    name="reviewer",
    system_message="""You are a Quality Reviewer. 用中文回答。

职责：
1. 评估答案质量
2. 检查是否满足用户需求
3. 确定是否需要改进

如果满意，说"APPROVED"。
如果需要改进，说"NEEDS_REVISION"并说明原因。""",
    llm_config=default_llm_config,
)

# 用户代理
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "") and "APPROVED" in x.get("content", ""),
    code_execution_config={"work_dir": "coding", "use_docker": False},
    function_map={
        "search_web": search_web,
        "get_weather": get_weather,
        "open_web_page": open_web_page,
    }
)

def enhanced_speaker_selection(last_speaker, groupchat):
    """增强的发言者选择逻辑"""
    messages = groupchat.messages
    
    # 检查是否有函数调用响应
    has_function_response = False
    for msg in messages[-2:]:
        if msg.get("content", "").find("***** Response from calling function") != -1:
            has_function_response = True
            break
    
    # 发言顺序
    if last_speaker is user_proxy:
        return planner
    elif last_speaker is planner:
        return executor
    elif last_speaker is executor:
        # 如果有函数响应，直接跳到审查者
        if has_function_response:
            return reviewer
        else:
            return summarizer
    elif last_speaker is summarizer:
        return reviewer
    elif last_speaker is reviewer:
        return None  # 结束对话
    else:
        return planner

# 创建群聊
groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, executor, summarizer, reviewer],
    messages=[],
    max_round=15,
    speaker_selection_method=enhanced_speaker_selection,
)

# 创建群聊管理器
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=default_llm_config,
)

# 获取用户输入并启动
if __name__ == "__main__":
    user_input = input("请输入您的问题或任务: ")
    user_proxy.initiate_chat(manager, message=user_input)
