import autogen
import os

def load_llm_config(config_file="OAI_CONFIG_LIST", model_filter=None):
    """
    从指定的配置文件加载 LLM 配置。
    Args:
        config_file (str): 包含 LLM 配置的 JSON 文件路径。
        model_filter (list): 用于筛选模型的列表，例如 ["gemini-2.5-flash-preview-05-20"]。
    Returns:
        list: 过滤后的 LLM 配置列表。
    """
    # 获取当前文件 (config.py) 的目录
    current_dir = os.path.dirname(__file__)
    # 构建 OAI_CONFIG_LIST 的完整路径
    full_config_path = os.path.join(current_dir, config_file)

    try:
        config_list = autogen.config_list_from_json(
            full_config_path, # 使用完整路径
            filter_dict={"model": model_filter} if model_filter else None,
        )
        if not config_list:
            raise ValueError(f"在 {full_config_path} 中未找到与过滤器 {model_filter} 匹配的模型配置。")
        return config_list
    except Exception as e:
        print(f"加载 LLM 配置时发生错误: {e}")
        return []

def load_executor_config(config_file="OAI_CONFIG_LIST"):
    """
    专门为执行者智能体加载 o3-2025-04-16 模型配置。
    Args:
        config_file (str): 包含 LLM 配置的 JSON 文件路径。
    Returns:
        list: o3 模型的配置列表。
    """
    return load_llm_config(config_file, model_filter=["o3-2025-04-16"])

def load_summarizer_config(config_file="OAI_CONFIG_LIST"):
    """
    专门为总结者智能体加载 o4-mini 模型配置。
    Args:
        config_file (str): 包含 LLM 配置的 JSON 文件路径。
    Returns:
        list: o4-mini 模型的配置列表。
    """
    return load_llm_config(config_file, model_filter=["o4-mini"])

def load_planner_config(config_file="OAI_CONFIG_LIST"):
    """
    专门为规划者智能体加载 o3-2025-04-16 模型配置。
    Args:
        config_file (str): 包含 LLM 配置的 JSON 文件路径。
    Returns:
        list: o3 模型的配置列表。
    """
    return load_llm_config(config_file, model_filter=["o3-2025-04-16"])
