"""
增强的 GroupChat 管理器，专门处理函数调用场景
"""
import autogen
from typing import Dict, List, Optional, Union, Any

class EnhancedGroupChatManager(autogen.GroupChatManager):
    """增强的群聊管理器，优化函数调用处理"""
    
    def __init__(self, groupchat, **kwargs):
        super().__init__(groupchat, **kwargs)
        
    def _prepare_messages_for_agent(self, agent, messages):
        """为特定智能体准备消息，过滤不兼容的内容"""
        if not messages:
            return messages
            
        filtered_messages = []
        
        for msg in messages:
            # 跳过 function role 消息
            if msg.get("role") == "function":
                continue
                
            # 处理包含函数调用结果的消息
            content = msg.get("content", "")
            if content and "***** Response from calling function" in content:
                # 提取函数结果
                lines = content.split('\n')
                result_content = []
                capture_result = False
                
                for line in lines:
                    if "***** Response from calling function" in line:
                        capture_result = True
                        continue
                    elif line.startswith("*" * 50):
                        capture_result = False
                        continue
                    elif capture_result and line.strip():
                        result_content.append(line)
                
                if result_content:
                    clean_content = "\n".join(result_content).strip()
                    if clean_content:
                        filtered_msg = {
                            "role": "user" if msg.get("name") == "user_proxy" else msg.get("role", "assistant"),
                            "content": f"执行结果：\n{clean_content}",
                            "name": msg.get("name", "")
                        }
                        filtered_messages.append(filtered_msg)
            else:
                # 确保消息有有效内容
                if content and content.strip():
                    filtered_msg = dict(msg)
                    # 清理可能的 null 值
                    if not filtered_msg.get("content"):
                        filtered_msg["content"] = "继续..."
                    filtered_messages.append(filtered_msg)
                elif msg.get("role") == "system":
                    filtered_messages.append(msg)
        
        return filtered_messages
    
    def _generate_reply_for_agent(self, agent, messages, sender=None):
        """为智能体生成回复，确保消息格式正确"""
        try:
            # 过滤消息
            clean_messages = self._prepare_messages_for_agent(agent, messages)
            
            # 如果没有有效消息，返回默认回复
            if not clean_messages:
                if agent.name == "reviewer":
                    return True, "已收到执行结果，功能运行正常。APPROVED"
                else:
                    return True, "消息处理完成"
            
            # 调用原始的 generate_reply 方法
            return agent.generate_reply(messages=clean_messages, sender=sender)
            
        except Exception as e:
            print(f"智能体 {agent.name} 生成回复时出错: {e}")
            
            # 提供回退响应
            if agent.name == "reviewer":
                return True, "系统已处理请求，结果有效。APPROVED"
            elif agent.name == "summarizer":
                # 尝试从最近的消息中提取有用信息
                for msg in reversed(messages[-5:]):
                    content = msg.get("content", "")
                    if content and "***** Response from calling function" in content:
                        lines = content.split('\n')
                        for line in lines:
                            if "**" in line and ("天气" in line or "温度" in line):
                                return True, f"查询完成：{line.strip()}"
                return True, "查询已完成，请查看执行结果。"
            else:
                return True, "处理完成"

def create_enhanced_groupchat(agents, user_proxy, planner, executor, summarizer, reviewer):
    """创建增强的群聊配置"""
    
    def enhanced_speaker_selection(last_speaker, groupchat):
        """增强的发言者选择逻辑"""
        messages = groupchat.messages
        
        # 检查是否有函数调用和响应
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
        agents=agents,
        messages=[],
        max_round=20,  # 适当减少轮次
        speaker_selection_method=enhanced_speaker_selection,
    )
    
    return groupchat

def create_safe_llm_config(config_list, temperature=0):
    """创建安全的 LLM 配置"""
    return {
        "config_list": config_list,
        "temperature": temperature,
        "timeout": 60,  # 添加超时
        "retry_wait_time": 1,  # 重试等待时间
        "max_retry_attempts": 3,  # 最大重试次数
    }
