import unittest
import os
import time
from asr import ASR

class TestASR(unittest.TestCase):
    def setUp(self):
        # ASR 类现在会自动处理模型下载，无需手动指定路径
        self.asr_processor = ASR()
        self.audio_filename = "test_output.wav"

    def tearDown(self):
        if os.path.exists(self.audio_filename):
            os.remove(self.audio_filename)

    def test_record_audio(self):
        # 录制 1 秒钟的音频
        recorded_file = self.asr_processor.record_audio(duration=1, filename=self.audio_filename)
        self.assertTrue(os.path.exists(recorded_file))
        self.assertTrue(os.path.getsize(recorded_file) > 0)

    def test_transcribe_audio_on_dummy_file(self):
        # 创建一个假的音频文件用于测试转录功能
        # 注意: 这个测试不会调用真实的 Whisper 模型进行转录
        # 因为没有实际的语音数据，模型会输出空字符串或类似结果
        # 但它会验证 transcribe_audio 方法的调用流程
        dummy_audio_path = "dummy_audio.wav"
        # 创建一个简单的空白 WAV 文件
        from scipy.io.wavfile import write
        samplerate = 16000
        duration = 1  # seconds
        frequency = 440  # Hz (A4 note)
        t = np.linspace(0., duration, int(samplerate * duration), endpoint=False)
        amplitude = 0.5
        data = amplitude * np.sin(2. * np.pi * frequency * t)
        write(dummy_audio_path, samplerate, data.astype(np.float32))

        transcribed_text = self.asr_processor.transcribe_audio(dummy_audio_path)
        self.assertIsInstance(transcribed_text, str)
        # 这里不判断转录结果的长度，因为对于空白音频，可能会转录为空
        os.remove(dummy_audio_path)


if __name__ == "__main__":
    unittest.main()
