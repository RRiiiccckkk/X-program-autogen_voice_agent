#!/usr/bin/env python3
"""
支持语音/文本模式的多智能体助手启动脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🤖 多智能体语音助手系统")
    print("=" * 60)
    print("🎙️  语音识别: OpenAI Whisper (本地运行)")
    print("🔊 语音合成: 系统 TTS (macOS say 命令)")
    print("💬 交互模式: 语音/文本可选")
    print("")
    print("🤖 智能体配置:")
    print("   • 规划者: 问题理解 + 战略规划")
    print("   • 执行者: 代码执行 + 函数调用")
    print("   • 总结者: 内容重组 + 格式优化")
    print("   • 反馈者: 质量评估")
    print("   • 用户代理: 交互管理")
    print("=" * 60)

def check_voice_dependencies():
    """检查语音依赖"""
    print("\n🔍 检查语音依赖...")
    
    # 检查 Whisper
    try:
        import whisper
        print("✅ OpenAI Whisper 已安装")
        return True
    except ImportError:
        print("❌ OpenAI Whisper 未安装")
        print("   请运行: pip install openai-whisper")
        return False

def choose_interaction_mode():
    """选择交互模式"""
    print("\n🎯 选择交互模式:")
    print("1. 文本模式 (默认)")
    print("2. 语音模式 (需要麦克风)")
    
    choice = input("\n请选择 [1/2] (默认1): ").strip() or "1"
    
    if choice == "2":
        # 检查语音依赖
        if not check_voice_dependencies():
            print("\n⚠️  语音依赖未满足，自动切换到文本模式")
            return "text"
        
        # 检查 pyaudio（可选）
        try:
            import pyaudio
            print("✅ PyAudio 已安装 (支持实时录音)")
        except ImportError:
            print("⚠️  PyAudio 未安装 (录音功能受限)")
            print("   macOS 用户安装方法:")
            print("   brew install portaudio")
            print("   pip install pyaudio")
            choice = input("\n是否继续使用语音模式？[y/N]: ").lower()
            if choice != 'y':
                return "text"
        
        return "voice"
    
    return "text"

def start_voice_mode():
    """启动语音模式"""
    print("\n🎙️  启动语音模式...")
    
    # 导入必要的模块
    import autogen
    from config import load_llm_config, load_executor_config, load_summarizer_config, load_planner_config
    from tools import search_web, search_duckduckgo, search_wikipedia, search_news, extract_webpage_content, get_exchange_rate, get_weather
    from voice.voice_session import VoiceSession
    from voice import get_stt_engine, get_tts_engine, get_audio_recorder, get_audio_player
    
    try:
        # 加载配置
        print("正在加载智能体配置...")
        config_list = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
        planner_config_list = load_planner_config()
        summarizer_config_list = load_summarizer_config()
        executor_config_list = load_executor_config()
        
        if not all([config_list, planner_config_list, summarizer_config_list, executor_config_list]):
            raise ValueError("智能体配置加载失败")
        
        # 创建智能体配置
        llm_config = {"config_list": config_list, "temperature": 0}
        planner_llm_config = {"config_list": planner_config_list, "temperature": 0.1}
        summarizer_llm_config = {"config_list": summarizer_config_list, "temperature": 0.3}
        
        executor_llm_config = {
            "config_list": executor_config_list,
            "temperature": 0,
            "functions": [
                {
                    "name": "search_web",
                    "description": "综合网络搜索功能",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "搜索查询词"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_weather",
                    "description": "获取天气信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "城市名称"},
                            "lang": {"type": "string", "description": "语言代码", "default": "zh"}
                        },
                        "required": ["location"]
                    }
                }
            ]
        }
        
        # 创建智能体
        print("正在初始化智能体...")
        
        planner = autogen.AssistantAgent(
            name="planner",
            system_message="你是规划者，负责理解用户问题并制定执行计划。",
            llm_config=planner_llm_config,
        )
        
        executor = autogen.AssistantAgent(
            name="executor",
            system_message="你是执行者，负责执行代码和搜索网络信息。",
            llm_config=executor_llm_config,
        )
        
        summarizer = autogen.AssistantAgent(
            name="summarizer",
            system_message="你是总结者，负责整理和格式化最终答案。",
            llm_config=summarizer_llm_config,
        )
        
        reviewer = autogen.AssistantAgent(
            name="reviewer",
            system_message="你是评审者，负责检查答案质量并决定是否需要修改。",
            llm_config=llm_config,
        )
        
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            is_termination_msg=lambda x: x.get("content", "") and "APPROVED" in x.get("content", ""),
            code_execution_config={"work_dir": "coding", "use_docker": False},
            function_map={
                "search_web": search_web,
                "get_weather": get_weather,
            }
        )
        
        # 创建群聊
        groupchat = autogen.GroupChat(
            agents=[user_proxy, planner, executor, summarizer, reviewer],
            messages=[],
            max_round=20,
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=llm_config,
        )
        
        # 创建语音组件
        print("正在加载语音组件...")
        stt = get_stt_engine("whisper", model_name="tiny", language="zh")
        tts = get_tts_engine("system")  # macOS 使用系统 TTS
        recorder = get_audio_recorder()
        player = get_audio_player()
        
        # 定义消息处理函数
        def process_message(user_input: str) -> str:
            """处理用户输入并返回响应"""
            try:
                # 清空之前的消息
                groupchat.messages = []
                
                # 初始化对话
                user_proxy.initiate_chat(
                    manager,
                    message=user_input,
                    clear_history=True
                )
                
                # 获取最后的响应
                if groupchat.messages:
                    # 从最后几条消息中找到最终答案
                    for msg in reversed(groupchat.messages[-5:]):
                        if msg.get("name") in ["reviewer", "summarizer"] and "APPROVED" in msg.get("content", ""):
                            # 找到前一条消息作为答案
                            for prev_msg in reversed(groupchat.messages):
                                if prev_msg != msg and prev_msg.get("name") == "summarizer":
                                    return prev_msg.get("content", "处理完成")
                        elif msg.get("name") == "summarizer" and "SUMMARY_COMPLETE" in msg.get("content", ""):
                            return msg.get("content", "").replace("SUMMARY_COMPLETE", "").strip()
                
                return "处理完成，但未找到具体答案。"
                
            except Exception as e:
                return f"处理过程中出现错误: {str(e)}"
        
        # 创建语音会话
        session = VoiceSession(stt, tts, recorder, player, process_message)
        
        # 开始对话
        session.start_conversation()
        
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用语音助手！")
    except Exception as e:
        print(f"\n❌ 语音模式启动失败: {e}")
        print("建议使用文本模式")

def start_text_mode():
    """启动文本模式"""
    print("\n💬 启动文本模式...")
    
    # 导入必要的模块
    import autogen
    from config import load_llm_config, load_executor_config, load_summarizer_config, load_planner_config
    from tools import search_web, search_duckduckgo, search_wikipedia, search_news, extract_webpage_content, get_exchange_rate, get_weather
    from voice.voice_session import TextSession
    
    try:
        # 加载配置（与语音模式相同）
        print("正在加载智能体配置...")
        config_list = load_llm_config(model_filter=["gpt-4o-2024-11-20"])
        planner_config_list = load_planner_config()
        summarizer_config_list = load_summarizer_config()
        executor_config_list = load_executor_config()
        
        if not all([config_list, planner_config_list, summarizer_config_list, executor_config_list]):
            raise ValueError("智能体配置加载失败")
        
        # 创建智能体配置
        llm_config = {"config_list": config_list, "temperature": 0}
        planner_llm_config = {"config_list": planner_config_list, "temperature": 0.1}
        summarizer_llm_config = {"config_list": summarizer_config_list, "temperature": 0.3}
        
        executor_llm_config = {
            "config_list": executor_config_list,
            "temperature": 0,
            "functions": [
                {
                    "name": "search_web",
                    "description": "综合网络搜索功能",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "搜索查询词"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_weather",
                    "description": "获取天气信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "城市名称"},
                            "lang": {"type": "string", "description": "语言代码", "default": "zh"}
                        },
                        "required": ["location"]
                    }
                }
            ]
        }
        
        # 创建智能体
        print("正在初始化智能体...")
        
        planner = autogen.AssistantAgent(
            name="planner",
            system_message="你是规划者，负责理解用户问题并制定执行计划。",
            llm_config=planner_llm_config,
        )
        
        executor = autogen.AssistantAgent(
            name="executor",
            system_message="你是执行者，负责执行代码和搜索网络信息。",
            llm_config=executor_llm_config,
        )
        
        summarizer = autogen.AssistantAgent(
            name="summarizer",
            system_message="你是总结者，负责整理和格式化最终答案。",
            llm_config=summarizer_llm_config,
        )
        
        reviewer = autogen.AssistantAgent(
            name="reviewer",
            system_message="你是评审者，负责检查答案质量并决定是否需要修改。",
            llm_config=llm_config,
        )
        
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            is_termination_msg=lambda x: x.get("content", "") and "APPROVED" in x.get("content", ""),
            code_execution_config={"work_dir": "coding", "use_docker": False},
            function_map={
                "search_web": search_web,
                "get_weather": get_weather,
            }
        )
        
        # 创建群聊
        groupchat = autogen.GroupChat(
            agents=[user_proxy, planner, executor, summarizer, reviewer],
            messages=[],
            max_round=20,
        )
        
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=llm_config,
        )
        
        # 定义消息处理函数
        def process_message(user_input: str) -> str:
            """处理用户输入并返回响应"""
            try:
                # 清空之前的消息
                groupchat.messages = []
                
                # 初始化对话
                user_proxy.initiate_chat(
                    manager,
                    message=user_input,
                    clear_history=True
                )
                
                # 获取最后的响应
                if groupchat.messages:
                    # 从最后几条消息中找到最终答案
                    for msg in reversed(groupchat.messages[-5:]):
                        if msg.get("name") in ["reviewer", "summarizer"] and "APPROVED" in msg.get("content", ""):
                            # 找到前一条消息作为答案
                            for prev_msg in reversed(groupchat.messages):
                                if prev_msg != msg and prev_msg.get("name") == "summarizer":
                                    return prev_msg.get("content", "处理完成")
                        elif msg.get("name") == "summarizer" and "SUMMARY_COMPLETE" in msg.get("content", ""):
                            return msg.get("content", "").replace("SUMMARY_COMPLETE", "").strip()
                
                return "处理完成，但未找到具体答案。"
                
            except Exception as e:
                return f"处理过程中出现错误: {str(e)}"
        
        # 创建文本会话
        session = TextSession(process_message)
        
        # 开始对话
        session.start_conversation()
        
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用多智能体助手！")
    except Exception as e:
        print(f"\n❌ 文本模式启动失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="支持语音的多智能体助手")
    parser.add_argument("--mode", choices=["text", "voice"], help="指定交互模式")
    parser.add_argument("--model", default="tiny", help="Whisper 模型 (tiny/base/small)")
    
    args = parser.parse_args()
    
    # 切换到脚本目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 打印横幅
    print_banner()
    
    # 选择模式
    if args.mode:
        mode = args.mode
        print(f"\n已指定模式: {mode}")
    else:
        mode = choose_interaction_mode()
    
    # 启动相应模式
    if mode == "voice":
        # 设置 Whisper 模型
        os.environ["WHISPER_MODEL"] = args.model
        start_voice_mode()
    else:
        start_text_mode()

if __name__ == "__main__":
    main()
