#!/usr/bin/env python3
"""
测试 Whisper 集成
"""

import os
import sys
from pathlib import Path

def test_whisper_import():
    """测试 Whisper 是否可以导入"""
    print("测试 1: 导入 Whisper")
    try:
        import whisper
        print("✅ Whisper 导入成功")
        print(f"   版本: {whisper.__version__ if hasattr(whisper, '__version__') else '未知'}")
        return True
    except ImportError as e:
        print(f"❌ Whisper 导入失败: {e}")
        print("   请运行: pip install openai-whisper")
        return False

def test_voice_module():
    """测试语音模块"""
    print("\n测试 2: 导入语音模块")
    try:
        from voice.stt import WhisperSTT, get_stt_engine
        from voice.tts import get_tts_engine
        from voice.audio_io import get_audio_recorder, get_audio_player
        print("✅ 语音模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 语音模块导入失败: {e}")
        return False

def test_whisper_stt():
    """测试 Whisper STT 实例化"""
    print("\n测试 3: 创建 Whisper STT 实例")
    try:
        from voice.stt import WhisperSTT
        
        # 使用 tiny 模型进行测试（最小的模型）
        print("   正在加载 Whisper tiny 模型...")
        stt = WhisperSTT(model_name="tiny", language="zh")
        print("✅ Whisper STT 创建成功")
        return True
    except Exception as e:
        print(f"❌ Whisper STT 创建失败: {e}")
        return False

def test_mock_stt():
    """测试 Mock STT（备用方案）"""
    print("\n测试 4: 创建 Mock STT 实例")
    try:
        from voice.stt import MockSTT
        
        mock_stt = MockSTT()
        result = mock_stt.transcribe_bytes(b"fake audio data")
        print(f"✅ Mock STT 工作正常: {result}")
        return True
    except Exception as e:
        print(f"❌ Mock STT 创建失败: {e}")
        return False

def test_tts_engine():
    """测试 TTS 引擎"""
    print("\n测试 5: 创建 TTS 引擎")
    try:
        from voice.tts import get_tts_engine
        
        # 使用系统 TTS（macOS 的 say 命令）
        tts = get_tts_engine("system")
        print("✅ System TTS 创建成功")
        
        # 测试 Mock TTS
        mock_tts = get_tts_engine("mock")
        print("✅ Mock TTS 创建成功")
        return True
    except Exception as e:
        print(f"❌ TTS 引擎创建失败: {e}")
        return False

def test_audio_io():
    """测试音频输入输出"""
    print("\n测试 6: 音频输入输出模块")
    try:
        from voice.audio_io import get_audio_recorder, get_audio_player
        
        # 获取录音器（如果 pyaudio 不可用，会返回 mock）
        recorder = get_audio_recorder()
        print(f"✅ 录音器创建成功: {type(recorder).__name__}")
        
        # 获取播放器
        player = get_audio_player()
        print(f"✅ 播放器创建成功: {type(player).__name__}")
        return True
    except Exception as e:
        print(f"❌ 音频 I/O 模块失败: {e}")
        return False

def test_voice_session():
    """测试语音会话"""
    print("\n测试 7: 语音会话管理器")
    try:
        from voice.voice_session import VoiceSession, TextSession, create_voice_session
        
        # 测试文本会话
        def dummy_processor(text):
            return f"处理了: {text}"
        
        text_session = TextSession(dummy_processor)
        print("✅ 文本会话创建成功")
        
        # 测试语音会话创建函数（使用 mock）
        voice_session = create_voice_session(
            stt_engine="mock",
            tts_engine="mock",
            process_message=dummy_processor
        )
        print("✅ 语音会话创建成功")
        return True
    except Exception as e:
        print(f"❌ 会话管理器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🔍 Whisper 集成测试")
    print("=" * 60)
    
    # 切换到项目目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 运行所有测试
    tests = [
        test_whisper_import,
        test_voice_module,
        test_whisper_stt,
        test_mock_stt,
        test_tts_engine,
        test_audio_io,
        test_voice_session
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"测试异常: {e}")
            results.append(False)
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n✅ 所有测试通过！Whisper 集成成功")
        print("\n下一步:")
        print("1. 运行 python start_voice.py 启动语音助手")
        print("2. 选择语音模式进行测试")
    else:
        print("\n⚠️  部分测试失败")
        print("\n建议:")
        print("1. 安装 Whisper: pip install openai-whisper")
        print("2. (可选) 安装 PyAudio: ")
        print("   - macOS: brew install portaudio && pip install pyaudio")
        print("   - Linux: sudo apt-get install portaudio19-dev && pip install pyaudio")
        print("3. 即使没有安装所有依赖，系统仍可使用文本模式或 Mock 模式")

if __name__ == "__main__":
    main()
