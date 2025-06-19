import autogen
import os

def load_default_config(config_file="OAI_CONFIG_LIST"):
    """
    加载默认的 LLM 配置，统一使用 gpt-4o-2024-11-20 模型。
    Args:
        config_file (str): 包含 LLM 配置的 JSON 文件路径。
    Returns:
        list: gpt-4o-2024-11-20 模型的配置列表。
    """
    # 获取当前文件 (config.py) 的目录
    current_dir = os.path.dirname(__file__)
    # 构建 OAI_CONFIG_LIST 的完整路径
    full_config_path = os.path.join(current_dir, config_file)

    try:
        config_list = autogen.config_list_from_json(
            full_config_path,
            filter_dict={"model": ["gpt-4o-2024-11-20"]},
        )
        if not config_list:
            raise ValueError(f"在 {full_config_path} 中未找到 gpt-4o-2024-11-20 模型配置。")
        return config_list
    except Exception as e:
        print(f"加载 LLM 配置时发生错误: {e}")
        return []

# 保持向后兼容性的别名
def load_llm_config(config_file="OAI_CONFIG_LIST", model_filter=None):
    """向后兼容性函数"""
    return load_default_config(config_file)

def load_executor_config(config_file="OAI_CONFIG_LIST"):
    """向后兼容性函数"""
    return load_default_config(config_file)

def load_summarizer_config(config_file="OAI_CONFIG_LIST"):
    """向后兼容性函数"""
    return load_default_config(config_file)

def load_planner_config(config_file="OAI_CONFIG_LIST"):
    """向后兼容性函数"""
    return load_default_config(config_file)
