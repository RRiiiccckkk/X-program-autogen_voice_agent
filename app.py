import autogen
import os
from config import load_llm_config
from asr import ASR # 导入 ASR 模块

# 配置智能体，从 config.py 加载模型配置
# 确保 OAI_CONFIG_LIST 文件在当前目录，并且 YOUR_OPENAI_API_KEY 已被替换
config_list = load_llm_config(model_filter=["gpt-3.5-turbo"])
if not config_list:
    raise ValueError("LLM 配置加载失败，请检查 OAI_CONFIG_LIST 和模型过滤器。")

# 定义 assistant_agent
# 这是一个 AI 助手，它会根据用户的问题提供答案或执行任务
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "seed": 42,  # 随机种子，用于复现性
        "config_list": config_list,
        "temperature": 0,  # 温度参数，控制模型的创造性，0表示更确定性
    },
)

# 定义 user_proxy_agent
# 这是一个代理人，可以代表用户与 assistant_agent 交流，
# 并且能够执行代码（如果 assistant_agent 建议执行代码的话）
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # "NEVER" 表示不向用户请求输入，自动回复
    max_consecutive_auto_reply=10,  # 最多连续自动回复的次数
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),  # 定义对话终止的条件
    code_execution_config={"work_dir": "coding", "use_docker": False},  # 如果智能体建议执行代码，代码将在 'coding' 目录下执行
)

# 初始化 ASR 处理器
asr_processor = ASR() # 移除 model_path 参数

# 获取语音输入并转录
user_speech_input = asr_processor.get_speech_input(duration=5)

# 启动智能体之间的对话
# user_proxy 向 assistant 提出一个问题
user_proxy.initiate_chat(
    assistant,
    message=user_speech_input # 使用转录的文本作为消息
)
