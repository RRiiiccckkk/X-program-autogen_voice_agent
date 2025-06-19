"""
语音转文本模块
支持多种 STT 引擎，包括 Whisper 本地模型
"""

import os
import tempfile
import time
from typing import Optional
from abc import ABC, abstractmethod


class STTBase(ABC):
    """语音转文本基类"""
    
    @abstractmethod
    def transcribe_file(self, audio_path: str) -> str:
        """转录音频文件"""
        pass
    
    @abstractmethod
    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        """转录音频字节流"""
        pass


class WhisperSTT(STTBase):
    """使用 OpenAI Whisper 进行本地语音识别"""
    
    def __init__(self, model_name: str = "tiny", device: str = "cpu", language: str = "zh"):
        """
        初始化 Whisper STT
        
        Args:
            model_name: 模型名称 (tiny, base, small, medium, large)
            device: 运行设备 (cpu, cuda, mps)
            language: 默认语言代码
        """
        try:
            import whisper
            self.whisper = whisper
        except ImportError:
            raise ImportError(
                "Whisper 未安装。请运行: pip install openai-whisper"
            )
        
        print(f"正在加载 Whisper {model_name} 模型...")
        start_time = time.time()
        self.model = self.whisper.load_model(model_name, device=device)
        self.language = language
        print(f"Whisper 模型加载完成，耗时: {time.time() - start_time:.2f}秒")
    
    def transcribe_file(self, audio_path: str) -> str:
        """
        转录音频文件
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            识别的文本
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        result = self.model.transcribe(audio_path, language=self.language)
        return result["text"].strip()
    
    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        """
        转录音频字节流
        
        Args:
            audio_bytes: WAV 格式的音频字节流
            
        Returns:
            识别的文本
        """
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            # 转录
            text = self.transcribe_file(tmp_path)
            return text
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def transcribe_with_timestamps(self, audio_path: str) -> dict:
        """
        转录音频并返回带时间戳的结果
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            包含文本和时间戳的完整结果
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        result = self.model.transcribe(audio_path, language=self.language)
        return result


class MockSTT(STTBase):
    """模拟 STT，用于测试"""
    
    def transcribe_file(self, audio_path: str) -> str:
        """模拟转录"""
        return "这是模拟的语音识别结果"
    
    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        """模拟转录"""
        return "这是模拟的语音识别结果"


def get_stt_engine(engine: str = "whisper", **kwargs) -> STTBase:
    """
    获取 STT 引擎实例
    
    Args:
        engine: 引擎类型 (whisper, mock)
        **kwargs: 引擎配置参数
        
    Returns:
        STT 引擎实例
    """
    if engine == "whisper":
        return WhisperSTT(**kwargs)
    elif engine == "mock":
        return MockSTT()
    else:
        raise ValueError(f"不支持的 STT 引擎: {engine}")
