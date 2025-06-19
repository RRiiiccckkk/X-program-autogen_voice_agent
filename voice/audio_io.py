"""
音频输入输出模块
处理录音和播放功能
"""

import wave
import struct
import tempfile
import os
from typing import Optional, Tuple

# pyaudio 是可选依赖
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False


class AudioRecorder:
    """音频录制器"""
    
    def __init__(self, rate: int = 16000, channels: int = 1, chunk: int = 1024):
        """
        初始化录音器
        
        Args:
            rate: 采样率
            channels: 声道数
            chunk: 缓冲区大小
        """
        if not PYAUDIO_AVAILABLE:
            raise ImportError(
                "录音功能需要 pyaudio。\n"
                "请运行: pip install pyaudio\n"
                "macOS 用户可能需要先运行: brew install portaudio"
            )
        
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.format = pyaudio.paInt16
        self.p = pyaudio.PyAudio()
    
    def record(self, duration: float = 3.0) -> bytes:
        """
        录制音频
        
        Args:
            duration: 录音时长（秒）
            
        Returns:
            WAV 格式的音频字节流
        """
        print(f"🎤 录音中... ({duration}秒)")
        
        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        frames = []
        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        print("✅ 录音完成")
        
        # 转换为 WAV 格式
        return self._frames_to_wav(frames)
    
    def record_until_silence(self, timeout: float = 10.0, silence_threshold: int = 500) -> bytes:
        """
        录音直到检测到静音
        
        Args:
            timeout: 最大录音时长
            silence_threshold: 静音阈值
            
        Returns:
            WAV 格式的音频字节流
        """
        print("🎤 录音中... (检测静音自动停止)")
        
        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        frames = []
        silent_chunks = 0
        max_chunks = int(self.rate / self.chunk * timeout)
        
        for _ in range(max_chunks):
            data = stream.read(self.chunk)
            frames.append(data)
            
            # 计算音量
            volume = self._calculate_volume(data)
            if volume < silence_threshold:
                silent_chunks += 1
                if silent_chunks > 20:  # 约 0.5 秒静音
                    break
            else:
                silent_chunks = 0
        
        stream.stop_stream()
        stream.close()
        
        print("✅ 录音完成")
        return self._frames_to_wav(frames)
    
    def _frames_to_wav(self, frames: list) -> bytes:
        """将音频帧转换为 WAV 格式字节流"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        wf = wave.open(tmp_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        with open(tmp_path, 'rb') as f:
            wav_bytes = f.read()
        
        os.unlink(tmp_path)
        return wav_bytes
    
    def _calculate_volume(self, data: bytes) -> int:
        """计算音频数据的音量"""
        count = len(data) // 2
        format = "%dh" % count
        shorts = struct.unpack(format, data)
        return sum(abs(short) for short in shorts) // count
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'p'):
            self.p.terminate()


class AudioPlayer:
    """音频播放器"""
    
    def __init__(self):
        """初始化播放器"""
        if not PYAUDIO_AVAILABLE:
            raise ImportError(
                "播放功能需要 pyaudio。\n"
                "请运行: pip install pyaudio\n"
                "macOS 用户可能需要先运行: brew install portaudio"
            )
        
        self.p = pyaudio.PyAudio()
    
    def play_wav(self, wav_path: str) -> None:
        """
        播放 WAV 文件
        
        Args:
            wav_path: WAV 文件路径
        """
        wf = wave.open(wav_path, 'rb')
        
        stream = self.p.open(
            format=self.p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        
        stream.stop_stream()
        stream.close()
        wf.close()
    
    def play_bytes(self, wav_bytes: bytes) -> None:
        """
        播放 WAV 字节流
        
        Args:
            wav_bytes: WAV 格式的音频字节流
        """
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(wav_bytes)
            tmp_path = tmp_file.name
        
        self.play_wav(tmp_path)
        os.unlink(tmp_path)
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'p'):
            self.p.terminate()


class MockAudioRecorder:
    """模拟录音器，用于测试"""
    
    def record(self, duration: float = 3.0) -> bytes:
        """模拟录音"""
        print(f"[模拟] 录音 {duration} 秒")
        # 返回一个简单的 WAV 头部
        return b'RIFF' + b'\x00' * 40
    
    def record_until_silence(self, timeout: float = 10.0, silence_threshold: int = 500) -> bytes:
        """模拟录音"""
        print(f"[模拟] 录音直到静音")
        return b'RIFF' + b'\x00' * 40


class MockAudioPlayer:
    """模拟播放器，用于测试"""
    
    def play_wav(self, wav_path: str) -> None:
        """模拟播放"""
        print(f"[模拟] 播放音频文件: {wav_path}")
    
    def play_bytes(self, wav_bytes: bytes) -> None:
        """模拟播放"""
        print(f"[模拟] 播放音频字节流 ({len(wav_bytes)} bytes)")


def get_audio_recorder(mock: bool = False) -> AudioRecorder:
    """获取录音器实例"""
    if mock or not PYAUDIO_AVAILABLE:
        return MockAudioRecorder()
    return AudioRecorder()


def get_audio_player(mock: bool = False) -> AudioPlayer:
    """获取播放器实例"""
    if mock or not PYAUDIO_AVAILABLE:
        return MockAudioPlayer()
    return AudioPlayer()
