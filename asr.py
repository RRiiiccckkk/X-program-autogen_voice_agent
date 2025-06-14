import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import os
import librosa

class ASR:
    def __init__(self, model_name="openai/whisper-base"): # 移除 model_path 参数
        self.device = self._get_device()
        self.model_name = model_name # 保存模型名称
        # 直接使用 model_name 来调用 from_pretrained
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(self.model_name).to(self.device)
        self.sample_rate = 16000

    def _get_device(self):
        if torch.cuda.is_available():
            return "cuda:0"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    # _get_default_model_path 方法不再需要

    def record_audio(self, duration=5, filename="output.wav"):
        print(f"正在录音 {duration} 秒...")
        audio = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float32')
        sd.wait()
        wavfile.write(filename, self.sample_rate, audio)
        print(f"录音完成，保存到 {filename}")
        return filename

    def transcribe_audio(self, audio_path):
        print(f"正在转录 {audio_path}...")
        audio_input, sr = librosa.load(audio_path, sr=self.sample_rate)
        if audio_input.dtype != np.float32:
            audio_input = audio_input.astype(np.float32)

        inputs = self.processor(audio_input, sampling_rate=self.sample_rate, return_tensors="pt").to(self.device)
        with torch.no_grad():
            generated_ids = self.model.generate(inputs.input_features)
        transcription = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(f"转录结果: {transcription}")
        return transcription

    def get_speech_input(self, duration=5):
        audio_filename = self.record_audio(duration)
        transcribed_text = self.transcribe_audio(audio_filename)
        # os.remove(audio_filename) # 可以选择删除临时音频文件
        return transcribed_text

if __name__ == "__main__":
    # 直接使用模型名称
    asr_processor = ASR(model_name="openai/whisper-base")
    text = asr_processor.get_speech_input(duration=5)
    print(f"最终获取的文本: {text}")
