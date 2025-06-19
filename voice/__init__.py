"""
语音模块
包含语音转文本(STT)、文本转语音(TTS)和音频处理功能
"""

from .stt import WhisperSTT, MockSTT, get_stt_engine
from .tts import get_tts_engine
from .audio_io import get_audio_recorder, get_audio_player

__all__ = [
    'WhisperSTT',
    'MockSTT',
    'get_stt_engine',
    'get_tts_engine',
    'get_audio_recorder',
    'get_audio_player'
]
