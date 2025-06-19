"""
文本转语音模块
支持多种 TTS 引擎
"""

import os
import tempfile
from abc import ABC, abstractmethod
from typing import Optional

# pyttsx3 是可选依赖
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class TTSBase(ABC):
    """文本转语音基类"""
    
    @abstractmethod
    def speak(self, text: str) -> None:
        """直接播放语音"""
        pass
    
    @abstractmethod
    def save_to_file(self, text: str, filename: str) -> None:
        """保存语音到文件"""
        pass
    
    @abstractmethod
    def text_to_wav(self, text: str) -> bytes:
        """将文本转换为 WAV 字节流"""
        pass


class Pyttsx3TTS(TTSBase):
    """使用 pyttsx3 进行本地 TTS"""
    
    def __init__(self, rate: int = 150, volume: float = 0.9, voice_id: Optional[str] = None):
        """
        初始化 TTS
        
        Args:
            rate: 语速
            volume: 音量 (0.0-1.0)
            voice_id: 语音 ID（可选）
        """
        if not PYTTSX3_AVAILABLE:
            raise ImportError(
                "TTS 功能需要 pyttsx3。\n"
                "请运行: pip install pyttsx3"
            )
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # 设置语音
        if voice_id:
            self.engine.setProperty('voice', voice_id)
        else:
            # 尝试选择中文语音
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
    
    def speak(self, text: str) -> None:
        """直接播放语音"""
        print(f"🔊 播放: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def save_to_file(self, text: str, filename: str) -> None:
        """保存语音到文件"""
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
    
    def text_to_wav(self, text: str) -> bytes:
        """将文本转换为 WAV 字节流"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        self.save_to_file(text, tmp_path)
        
        with open(tmp_path, 'rb') as f:
            wav_bytes = f.read()
        
        os.unlink(tmp_path)
        return wav_bytes


class MockTTS(TTSBase):
    """模拟 TTS，用于测试"""
    
    def speak(self, text: str) -> None:
        """模拟播放"""
        print(f"[模拟 TTS] 播放: {text}")
    
    def save_to_file(self, text: str, filename: str) -> None:
        """模拟保存"""
        print(f"[模拟 TTS] 保存到文件: {filename}")
        # 创建一个空的 WAV 文件
        with open(filename, 'wb') as f:
            f.write(b'RIFF' + b'\x00' * 40)
    
    def text_to_wav(self, text: str) -> bytes:
        """模拟转换"""
        print(f"[模拟 TTS] 转换文本: {text}")
        return b'RIFF' + b'\x00' * 40


class SystemTTS(TTSBase):
    """使用系统命令进行 TTS（macOS/Linux）"""
    
    def __init__(self):
        """初始化系统 TTS"""
        import platform
        self.system = platform.system()
        
        if self.system == "Darwin":  # macOS
            self.command = "say"
        elif self.system == "Linux":
            # 检查可用的 TTS 命令
            if os.system("which espeak > /dev/null 2>&1") == 0:
                self.command = "espeak"
            elif os.system("which festival > /dev/null 2>&1") == 0:
                self.command = "festival --tts"
            else:
                raise RuntimeError("Linux 系统需要安装 espeak 或 festival")
        else:
            raise RuntimeError(f"不支持的系统: {self.system}")
    
    def speak(self, text: str) -> None:
        """使用系统命令播放语音"""
        print(f"🔊 播放: {text}")
        
        # 转义特殊字符
        text = text.replace("'", "\\'").replace('"', '\\"')
        
        if self.system == "Darwin":
            os.system(f'{self.command} "{text}"')
        else:
            os.system(f'echo "{text}" | {self.command}')
    
    def save_to_file(self, text: str, filename: str) -> None:
        """保存语音到文件"""
        text = text.replace("'", "\\'").replace('"', '\\"')
        
        if self.system == "Darwin":
            os.system(f'{self.command} -o "{filename}" "{text}"')
        else:
            # espeak 示例
            if "espeak" in self.command:
                os.system(f'{self.command} -w "{filename}" "{text}"')
            else:
                # festival 不直接支持保存到文件，使用 arecord
                raise NotImplementedError("Festival 不支持直接保存到文件")
    
    def text_to_wav(self, text: str) -> bytes:
        """将文本转换为 WAV 字节流"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        self.save_to_file(text, tmp_path)
        
        with open(tmp_path, 'rb') as f:
            wav_bytes = f.read()
        
        os.unlink(tmp_path)
        return wav_bytes


def get_tts_engine(engine: str = "auto", **kwargs) -> TTSBase:
    """
    获取 TTS 引擎实例
    
    Args:
        engine: 引擎类型 (auto, pyttsx3, system, mock)
        **kwargs: 引擎配置参数
        
    Returns:
        TTS 引擎实例
    """
    if engine == "auto":
        # 自动选择可用的引擎
        if PYTTSX3_AVAILABLE:
            return Pyttsx3TTS(**kwargs)
        else:
            try:
                return SystemTTS()
            except:
                return MockTTS()
    elif engine == "pyttsx3":
        return Pyttsx3TTS(**kwargs)
    elif engine == "system":
        return SystemTTS()
    elif engine == "mock":
        return MockTTS()
    else:
        raise ValueError(f"不支持的 TTS 引擎: {engine}")
