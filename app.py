import autogen
import os
from config import load_llm_config, load_executor_config, load_summarizer_config, load_planner_config
from tools import search_web, search_duckduckgo, search_wikipedia, search_news, extract_webpage_content, get_exchange_rate, get_weather

# 配置智能体，从 config.py 加载模型配置
config_list = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
if not config_list:
    raise ValueError("LLM 配置加载失败，请检查 OAI_CONFIG_LIST 和模型过滤器。")

# 为规划者加载 o3 模型配置
planner_config_list = load_planner_config()
if not planner_config_list:
    raise ValueError("规划者 o3 模型配置加载失败，请检查 OAI_CONFIG_LIST 配置。")

# 为总结者加载 o4-mini 模型配置
summarizer_config_list = load_summarizer_config()
if not summarizer_config_list:
    raise ValueError("总结者 o4-mini 模型配置加载失败，请检查 OAI_CONFIG_LIST 配置。")

# 为执行者加载 gpt-4o-2024-11-20 模型配置（支持函数调用）
executor_config_list = load_executor_config()
if not executor_config_list:
    raise ValueError("执行者 gpt-4o-2024-11-20 模型配置加载失败，请检查 OAI_CONFIG_LIST 配置。")

# 通用 LLM 配置（用于反馈者）
llm_config = {
    "config_list": config_list,
    "temperature": 0,
}

# 规划者专用 LLM 配置（使用 o3 模型）
planner_llm_config = {
    "config_list": planner_config_list,
    "temperature": 0.1,  # 稍高的温度以提高分析创造性
}

# 执行者专用 LLM 配置（使用 o4-mini 模型，支持函数调用）
executor_llm_config = {
    "config_list": executor_config_list,
    "temperature": 0,
    "functions": [
        {
            "name": "search_web",
            "description": "综合网络搜索功能，自动选择最佳搜索源（DuckDuckGo + 维基百科）",
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
            "name": "search_duckduckgo",
            "description": "使用 DuckDuckGo 搜索引擎进行网络搜索",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询词"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "最大结果数量，默认为3",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "search_wikipedia",
            "description": "搜索维基百科获取权威信息和定义",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询词"
                    },
                    "language": {
                        "type": "string",
                        "description": "语言代码，zh=中文，en=英文",
                        "default": "zh"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "search_news",
            "description": "搜索最新新闻信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "新闻搜索查询词"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "extract_webpage_content",
            "description": "提取指定网页的主要内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要提取内容的网页URL"
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "最大内容长度，默认1000字符",
                        "default": 1000
                    }
                },
                "required": ["url"]
            }
        },
        {
            "name": "get_exchange_rate",
            "description": "获取货币汇率信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_currency": {
                        "type": "string",
                        "description": "基础货币代码，如USD"
                    },
                    "target_currency": {
                        "type": "string",
                        "description": "目标货币代码，如CNY"
                    }
                },
                "required": ["base_currency", "target_currency"]
            }
        },
        {
            "name": "get_weather",
            "description": "获取指定城市的实时天气信息（调用 wttr.in 或备用搜索引擎）",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称（支持中文、英文），如 '广州'、'Beijing'、'上海'"
                    },
                    "lang": {
                        "type": "string",
                        "description": "语言代码，默认 'zh' 中文",
                        "default": "zh"
                    }
                },
                "required": ["location"]
            }
        }
    ]
}

# 总结者专用 LLM 配置（使用 o4-mini 模型）
summarizer_llm_config = {
    "config_list": summarizer_config_list,
    "temperature": 0.3,  # 稍高的温度以提高创造性
}

# 定义规划者智能体（使用 o3-2025-04-16 模型）
planner = autogen.AssistantAgent(
    name="planner",
    system_message="""You are an Advanced Strategic Planner powered by the cutting-edge o3-2025-04-16 model. Think in English for superior analytical capabilities, but respond in Chinese.

Your core responsibilities:
1. **FIRST**: Deeply understand and clarify the user's question/problem
   - Identify the core intent behind the request
   - Recognize any ambiguities or missing information
   - Understand the context and background
   - Determine the expected outcome format

2. **THEN**: Create comprehensive strategic plans
   - Analyze requirements thoroughly using advanced reasoning
   - Design detailed execution plans with clear steps
   - Break down complex tasks into manageable components
   - Provide precise guidance for the executor
   - Anticipate potential challenges and solutions

Advanced analytical approach:
- Use deep reasoning to understand implicit requirements
- Consider multiple perspectives and edge cases
- Apply systematic thinking to complex problems
- Leverage advanced problem-solving methodologies

Response format in Chinese:
- 问题理解 (Problem Understanding) - Deep analysis of what the user really wants
- 需求澄清 (Requirement Clarification) - Any assumptions or clarifications made
- 任务分析 (Task Analysis) - Comprehensive breakdown of the task
- 执行步骤 (Execution Steps) - Detailed, actionable steps
- 预期结果 (Expected Results) - Clear description of deliverables
- 关键注意事项 (Key Considerations) - Important factors and potential issues

When planning is complete, say "PLAN_COMPLETE" to indicate completion.""",
    llm_config=planner_llm_config,
)

# 定义执行者智能体（使用 o4-mini 模型）
executor = autogen.AssistantAgent(
    name="executor",
    system_message="""You are a Code Execution Expert powered by o4-mini with web search capabilities. Think in English for superior technical reasoning, but respond in Chinese.

Your core responsibilities:
1. Execute tasks based on the planner's detailed plan
2. Write, test, and run Python code with precision
3. Search the web for real-time information when needed
4. Handle errors and debugging systematically
5. Provide comprehensive execution results

Available web search tools:
- search_web(query): Comprehensive web search (DuckDuckGo + Wikipedia)
- search_duckduckgo(query, max_results): Direct DuckDuckGo search
- search_wikipedia(query, language): Wikipedia knowledge base search
- search_news(query): Latest news search
- extract_webpage_content(url, max_length): Extract content from specific webpages
- get_exchange_rate(base_currency, target_currency): Get currency exchange rates
- get_weather(location, lang): Get real-time weather for any city (uses wttr.in API)

IMPORTANT: When user asks for weather information, always use get_weather() function first to get real-time data. Do NOT provide example or mock weather data.

Technical approach:
- Determine if web search is needed based on the task
- Use appropriate search functions for different information types
- Combine search results with code execution when necessary
- Think through the logic step-by-step in English
- Provide clear explanations in Chinese

Response format in Chinese:
- 执行分析 (Execution Analysis)
- 网络搜索 (Web Search) - if applicable
- 代码实现 (Code Implementation) - if applicable
- 运行结果 (Execution Results)
- 技术说明 (Technical Notes)

When execution is complete, say "EXECUTION_COMPLETE" to indicate completion.""",
    llm_config=executor_llm_config,
)

# 定义总结者智能体（使用 o4-mini 模型）
summarizer = autogen.AssistantAgent(
    name="summarizer",
    system_message="""You are an Answer Summarizer powered by the efficient o4-mini model. Think in English for clarity, but respond in Chinese.

Your critical responsibilities:
1. Receive raw output from the executor
2. Reorganize and restructure content for clarity
3. Format answers to match user requirements precisely
4. Ensure readability and completeness
5. Present information in a user-friendly manner

Content transformation approach:
- Analyze the executor's output structure in English
- Identify key information and results
- Remove technical jargon when unnecessary
- Organize content logically
- Enhance formatting for better readability

Output format in Chinese:
- 答案概要 (Answer Summary) - Brief overview
- 详细结果 (Detailed Results) - Well-formatted main content
- 关键要点 (Key Points) - Bullet points of important information
- 补充说明 (Additional Notes) - Any clarifications if needed

Focus on making the answer:
- 清晰 (Clear)
- 完整 (Complete) 
- 易读 (Easy to read)
- 符合用户需求 (Meeting user requirements)

When summarization is complete, say "SUMMARY_COMPLETE" to indicate completion.""",
    llm_config=summarizer_llm_config,
)

# 定义反馈者智能体
reviewer = autogen.AssistantAgent(
    name="reviewer",
    system_message="""You are a Quality Reviewer. Think in English for thorough analysis, but respond in Chinese.

Your responsibilities:
1. Evaluate the quality of the summarizer's output
2. Check if results fully satisfy user requirements
3. Determine if re-planning or re-execution is needed
4. Provide constructive improvement suggestions
5. Ensure the final answer is polished and professional

Evaluation criteria:
- 准确性 (Accuracy) - Is the information correct?
- 完整性 (Completeness) - Does it fully answer the question?
- 清晰度 (Clarity) - Is it easy to understand?
- 格式化 (Formatting) - Is it well-organized?
- 实用性 (Practicality) - Is it useful for the user?

Think through your evaluation in English, then provide feedback in Chinese.

If the result is satisfactory, say "APPROVED".
If revision is needed, say "NEEDS_REVISION" and explain why in Chinese.""",
    llm_config=llm_config,
)

# 定义用户代理
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "") and "APPROVED" in x.get("content", ""),
    code_execution_config={"work_dir": "coding", "use_docker": False},
    function_map={
        "search_web": search_web,
        "search_duckduckgo": search_duckduckgo,
        "search_wikipedia": search_wikipedia,
        "search_news": search_news,
        "extract_webpage_content": extract_webpage_content,
        "get_exchange_rate": get_exchange_rate,
        "get_weather": get_weather,
    }
)

def filter_messages_for_agent(messages, agent_name):
    """为特定智能体过滤消息，移除不兼容的消息格式"""
    filtered_messages = []
    
    for msg in messages:
        # 跳过 function role 的消息，这些消息某些模型不支持
        if msg.get("role") == "function":
            continue
            
        # 对于包含函数调用结果的消息，转换为普通文本消息
        content = msg.get("content", "")
        if content and "***** Response from calling function" in content:
            # 提取函数调用的结果部分
            lines = content.split('\n')
            result_lines = []
            in_result = False
            for line in lines:
                if line.startswith("***** Response from calling function"):
                    in_result = True
                    continue
                elif line.startswith("*" * 50):
                    in_result = False
                    continue
                elif in_result:
                    result_lines.append(line)
            
            if result_lines:
                # 创建一个新的消息，只包含函数执行结果
                filtered_msg = {
                    "role": "assistant" if msg.get("name") == "user_proxy" else msg.get("role", "user"),
                    "content": "\n".join(result_lines).strip(),
                    "name": msg.get("name", "")
                }
                filtered_messages.append(filtered_msg)
        else:
            # 确保所有消息都有有效的 content
            if content or msg.get("role") == "system":
                filtered_msg = dict(msg)
                if not filtered_msg.get("content"):
                    filtered_msg["content"] = "继续处理..."
                filtered_messages.append(filtered_msg)
    
    return filtered_messages

def custom_speaker_selection_func(last_speaker, groupchat):
    """优化的发言者选择函数，更好地处理函数调用场景"""
    messages = groupchat.messages
    
    # 检查最近的消息中是否有function相关的内容
    has_function_call = False
    has_function_response = False
    
    for msg in messages[-3:]:  # 检查最近3条消息
        content = msg.get("content", "")
        if "***** Suggested function call" in content:
            has_function_call = True
        elif "***** Response from calling function" in content:
            has_function_response = True
    
    # 基本的发言顺序
    if last_speaker is user_proxy:
        return planner
    elif last_speaker is planner:
        return executor
    elif last_speaker is executor:
        # 如果执行者刚调用了函数并得到了响应，直接让反馈者总结
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

# 创建群聊（添加总结者到工作流程中）
groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, executor, summarizer, reviewer],
    messages=[],
    max_round=40,  # 增加轮次以适应新的工作流程
    speaker_selection_method=custom_speaker_selection_func,
)

# 创建群聊管理器
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

# 获取用户输入
user_input = input("请输入您的问题或任务: ")

# 启动群聊
user_proxy.initiate_chat(
    manager,
    message=user_input
)
