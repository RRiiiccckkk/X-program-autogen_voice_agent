"""
语音会话管理器
管理语音交互的完整流程
"""

import time
from typing import Optional, Callable, Any
from .stt import STTBase
from .tts import TTSBase
from .audio_io import AudioRecorder, AudioPlayer


class VoiceSession:
    """语音会话管理器"""
    
    def __init__(
        self,
        stt: STTBase,
        tts: TTSBase,
        recorder: AudioRecorder,
        player: AudioPlayer,
        process_message: Callable[[str], str]
    ):
        """
        初始化语音会话
        
        Args:
            stt: 语音转文本引擎
            tts: 文本转语音引擎
            recorder: 录音器
            player: 播放器
            process_message: 处理消息的回调函数
        """
        self.stt = stt
        self.tts = tts
        self.recorder = recorder
        self.player = player
        self.process_message = process_message
        self.running = False
    
    def start_conversation(self) -> None:
        """开始对话循环"""
        print("\n" + "="*50)
        print("🎙️  语音对话模式已启动")
        print("="*50)
        print("提示: 按 Ctrl+C 退出对话\n")
        
        self.running = True
        
        # 欢迎语
        welcome_text = "你好！我是你的智能助手，有什么可以帮助你的吗？"
        self.tts.speak(welcome_text)
        
        try:
            while self.running:
                # 录音
                input("按 Enter 开始说话...")
                audio_bytes = self.recorder.record(duration=5.0)
                
                # 转文字
                user_text = self.stt.transcribe_bytes(audio_bytes)
                
                if not user_text or user_text.strip() == "":
                    print("❓ 没有检测到语音，请重试")
                    continue
                
                print(f"\n👤 你说: {user_text}")
                
                # 检查退出命令
                if any(word in user_text for word in ["退出", "再见", "拜拜"]):
                    farewell = "好的，再见！"
                    print(f"🤖 助手: {farewell}")
                    self.tts.speak(farewell)
                    break
                
                # 处理消息
                print("🤔 思考中...")
                response = self.process_message(user_text)
                
                print(f"🤖 助手: {response}")
                
                # 语音回复
                self.tts.speak(response)
                
        except KeyboardInterrupt:
            print("\n\n👋 对话已结束")
        finally:
            self.running = False
    
    def single_interaction(self, duration: float = 5.0) -> tuple[str, str]:
        """
        单次交互
        
        Args:
            duration: 录音时长
            
        Returns:
            (用户输入, 系统回复) 元组
        """
        # 录音
        audio_bytes = self.recorder.record(duration=duration)
        
        # 转文字
        user_text = self.stt.transcribe_bytes(audio_bytes)
        
        if not user_text or user_text.strip() == "":
            return "", "抱歉，我没有听清楚"
        
        # 处理消息
        response = self.process_message(user_text)
        
        # 语音回复
        self.tts.speak(response)
        
        return user_text, response


class TextSession:
    """文本会话管理器（对比用）"""
    
    def __init__(self, process_message: Callable[[str], str]):
        """
        初始化文本会话
        
        Args:
            process_message: 处理消息的回调函数
        """
        self.process_message = process_message
        self.running = False
    
    def start_conversation(self) -> None:
        """开始对话循环"""
        print("\n" + "="*50)
        print("💬 文本对话模式已启动")
        print("="*50)
        print("提示: 输入 '退出' 结束对话\n")
        
        self.running = True
        
        try:
            while self.running:
                # 获取用户输入
                user_text = input("\n👤 你: ").strip()
                
                if not user_text:
                    continue
                
                # 检查退出命令
                if user_text.lower() in ["退出", "exit", "quit"]:
                    print("👋 再见！")
                    break
                
                # 处理消息
                print("🤔 思考中...")
                response = self.process_message(user_text)
                
                print(f"🤖 助手: {response}")
                
        except KeyboardInterrupt:
            print("\n\n👋 对话已结束")
        finally:
            self.running = False


def create_voice_session(
    stt_engine: str = "whisper",
    tts_engine: str = "system",
    process_message: Optional[Callable] = None,
    **kwargs
) -> VoiceSession:
    """
    创建语音会话的快捷函数
    
    Args:
        stt_engine: STT 引擎类型
        tts_engine: TTS 引擎类型
        process_message: 消息处理函数
        **kwargs: 其他配置参数
        
    Returns:
        配置好的语音会话实例
    """
    from . import get_stt_engine, get_tts_engine, get_audio_recorder, get_audio_player
    
    # 创建组件
    stt = get_stt_engine(stt_engine, **kwargs.get('stt_config', {}))
    tts = get_tts_engine(tts_engine, **kwargs.get('tts_config', {}))
    recorder = get_audio_recorder()
    player = get_audio_player()
    
    # 默认消息处理函数
    if process_message is None:
        def process_message(text: str) -> str:
            return f"你说了: {text}"
    
    return VoiceSession(stt, tts, recorder, player, process_message)
