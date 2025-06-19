#!/usr/bin/env python3
"""
语音功能演示脚本
展示 Whisper 语音识别的基本功能
"""

import os
import sys
from pathlib import Path

def demo_whisper():
    """演示 Whisper 语音识别"""
    print("=" * 60)
    print("🎙️  Whisper 语音识别演示")
    print("=" * 60)
    
    try:
        from voice.stt import WhisperSTT
        from voice.tts import get_tts_engine
        from voice.audio_io import get_audio_recorder
        
        # 初始化组件
        print("\n1. 初始化语音组件...")
        print("   加载 Whisper tiny 模型...")
        stt = WhisperSTT(model_name="tiny", language="zh")
        tts = get_tts_engine("system")  # macOS 系统 TTS
        recorder = get_audio_recorder()  # 会自动使用 Mock 如果没有 pyaudio
        
        print("✅ 语音组件初始化成功")
        
        # 演示语音识别
        print("\n2. 演示语音识别流程:")
        
        # 如果是 Mock 录音器，创建一个测试音频文件
        if type(recorder).__name__ == "MockAudioRecorder":
            print("\n⚠️  使用模拟录音器（未安装 pyaudio）")
            print("   实际使用时需要安装 pyaudio 以支持真实录音")
            
            # 创建一个测试音频文件
            import tempfile
            test_text = "你好，我是智能助手"
            
            print(f"\n模拟语音输入: '{test_text}'")
            print("模拟语音识别结果: '这是模拟的语音识别结果'")
            
            # 使用 TTS 播放
            print("\n3. 演示语音合成:")
            tts.speak("这是模拟的语音识别结果")
            
        else:
            print("\n准备录音...")
            print("按 Enter 开始录音（5秒）:")
            input()
            
            # 录音
            audio_bytes = recorder.record(duration=5.0)
            
            # 识别
            print("正在识别...")
            text = stt.transcribe_bytes(audio_bytes)
            print(f"\n识别结果: {text}")
            
            # 语音回复
            response = f"你说的是：{text}"
            print(f"语音回复: {response}")
            tts.speak(response)
        
        print("\n✅ 演示完成！")
        
    except ImportError as e:
        print(f"\n❌ 缺少依赖: {e}")
        print("\n请安装必要的依赖:")
        print("pip install openai-whisper")
        print("pip install pyaudio  # 可选，用于真实录音")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")

def demo_multi_agent():
    """演示多智能体系统"""
    print("\n" + "=" * 60)
    print("🤖 多智能体系统演示")
    print("=" * 60)
    
    print("\n多智能体架构:")
    print("1. 规划者 (Planner) - 理解问题，制定计划")
    print("2. 执行者 (Executor) - 执行代码，搜索信息")
    print("3. 总结者 (Summarizer) - 整理格式化答案")
    print("4. 评审者 (Reviewer) - 质量控制")
    print("5. 用户代理 (User Proxy) - 交互管理")
    
    print("\n工作流程:")
    print("用户输入 → 规划 → 执行 → 总结 → 评审 → 输出")
    
    print("\n支持的功能:")
    print("• 网络搜索")
    print("• 天气查询")
    print("• 代码执行")
    print("• 信息分析")
    print("• 任务处理")

def main():
    """主函数"""
    # 切换到项目目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🎯 AutoGen 语音多智能体助手演示\n")
    
    # 演示 Whisper
    demo_whisper()
    
    # 演示多智能体
    demo_multi_agent()
    
    print("\n" + "=" * 60)
    print("💡 下一步:")
    print("1. 运行 python start_voice.py 启动完整系统")
    print("2. 选择语音或文本模式")
    print("3. 开始与智能助手对话")
    print("=" * 60)

if __name__ == "__main__":
    main()
