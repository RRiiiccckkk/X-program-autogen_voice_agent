# Autogen 语音对话代理

本项目旨在实现一个基于 Autogen 框架的实时语音对话系统，集成了语音识别 (ASR) 和语音合成 (TTS) 功能。

## 功能特性

*   **语音识别 (ASR)**: 利用本地的 `models--ope...-whisper-base` 模型将语音输入转换为文本。
*   **大语言模型 (LLM) 交互**: 通过 `Autogen` 框架与 `liaobots.work` 提供的 `OpenAI compatible API` 进行交互，实现智能对话。
*   **语音合成 (TTS)**: (待集成) 使用 `edge-tts` 库将文本回复转换为语音输出。

## 环境准备

### 1. Python 环境

确保您的系统已安装 Python 3.9 或更高版本。建议使用 `conda` 或 `venv` 创建虚拟环境。

```bash
conda create -n autogen_voice python=3.11
conda activate autogen_voice
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
pip install openai autogen pyautogen transformers torchaudio whisper-openai # whisper-openai 是为了兼容老的 `openai-whisper` 包
pip install google-genai vertexai
```

### 3. 配置 LLM API

编辑 `autogen_voice_agent/OAI_CONFIG_LIST` 文件，配置您的 API 密钥和模型信息。

```json
[
    {
        "model": "gpt-3.5-turbo",
        "api_key": "YOUR_LIAOBOTS_API_KEY", 
        "base_url": "https://ai.liaobots.work/v1",
        "api_type": "openai"
    }
]
```
请将 `YOUR_LIAOBOTS_API_KEY` 替换为您在 `liaobots.work` 获取的 API 密钥。

## 运行项目

1.  **启动 `app.py`**:
    ```bash
    python autogen_voice_agent/app.py
    ```

2.  **进行语音输入**:
    程序将自动录制 5 秒的音频。请对着麦克风说话。

3.  **查看对话**:
    程序会将您的语音转录为文本，并发送给大语言模型获取回复。回复将显示在终端中。

## 故障排除

*   **`ImportError: Please install google-genai and 'vertexai' to use Google's API.`**:
    这是因为您的 `OAI_CONFIG_LIST` 配置中 `api_type` 设置为 `google`，但缺少 `google-genai` 和 `vertexai` 库。
    解决方案：执行 `pip install google-genai vertexai`，或者将 `api_type` 设置为 `openai`。

*   **`openai.BadRequestError: Error code: 400 - {'error': {'message': 'Unable to submit request because it must include at least one parts field...`**:
    这通常发生在您使用 `gemini` 系列模型，但 `autogen` 在发送请求时缺少必要的 `parts` 字段。
    解决方案：
    1.  确认 `OAI_CONFIG_LIST` 中的 `api_type` 已设置为 `openai`。
    2.  如果问题依然存在，可以尝试将模型暂时切换为 `gpt-3.5-turbo`。这可能表示 `liaobots.work` 对 `gemini` 模型的兼容性可能存在细微差异。

## 贡献

欢迎通过提交 Pull Request 来贡献代码或报告问题。

## 许可证

本项目采用 MIT 许可证。
