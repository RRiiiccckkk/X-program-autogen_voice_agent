# AutoGen Multi-Agent Voice Assistant

[中文文档](docs/README_CN.md) | [日本語](docs/README_JP.md)

A powerful multi-agent collaborative system built with Microsoft AutoGen framework, featuring advanced language models (o3-2025-04-16, o4-mini) and integrated web search capabilities.

## ✨ Key Features

### 🎙️ Voice Interaction (NEW!)
- **Speech Recognition**: Powered by OpenAI Whisper (runs locally)
- **Text-to-Speech**: System TTS support (macOS/Linux)
- **Dual Mode**: Switch between voice and text interaction
- **Real-time Processing**: Instant voice-to-text conversion
- **Multi-language**: Primary support for Chinese, also handles English

### 🤖 Five-Agent Collaborative Architecture
- **Planner Agent** (o3-2025-04-16): Deep problem understanding and strategic planning
- **Executor Agent** (o3-2025-04-16): Code execution and web search capabilities
- **Summarizer Agent** (o4-mini): Content reorganization and formatting
- **Reviewer Agent** (gpt-4o-2024-11-20): Quality assurance and feedback
- **User Proxy**: Interaction management and flow control

### 🌐 Integrated Web Search
- DuckDuckGo search (no API key required)
- Wikipedia knowledge base
- Real-time news search
- Web content extraction
- Currency exchange rates
- Weather information
- Automatic source selection

### 🚀 Cross-Platform Support
- **Windows**: Native batch scripts and PowerShell support
- **macOS**: One-click `.command` launcher
- **Linux**: Shell script compatibility

## 📋 Requirements

- Python 3.8 or higher
- pip package manager
- Internet connection (for web search features)

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/RRiiiccckkk/X-program-autogen_voice_agent.git
cd autogen_voice_agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API

Create or edit `OAI_CONFIG_LIST` file:

```json
[
    {
        "model": "gpt-4o-2024-11-20",
        "api_key": "YOUR_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "api_type": "openai"
    },
    {
        "model": "o3-2025-04-16",
        "api_key": "YOUR_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "api_type": "openai"
    },
    {
        "model": "o4-mini",
        "api_key": "YOUR_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "api_type": "openai"
    }
]
```

### 🔑 API Flexibility

This system supports **any OpenAI-compatible API service**. While we recommend using the OpenAI format for best compatibility, you can use:

- **OpenAI** (official)
- **Azure OpenAI**
- **LiaoBots** 
- **Local deployments** (LM Studio, Ollama, etc.)
- **Any OpenAI-compatible service**

Simply adjust the `base_url` and `api_key` in your configuration.

## 🚀 Quick Start

### 🎯 GUI Launcher (v3.0) - RECOMMENDED
The easiest way to start the system with a graphical interface:

#### macOS
Double-click `launch_mac.command`

#### Windows  
Double-click `launch_win.bat`

#### Linux
```bash
chmod +x launch_linux.sh  # First time only
./launch_linux.sh
```

The GUI launcher provides three modes:
- **🎯 Demo Mode** - View system demonstrations
- **⌨️ Text Mode** - Keyboard-based interaction
- **🎙️ Voice Mode** - Speech-based interaction

### Command Line Options
```bash
# Start with voice/text mode selection
python3 start_voice.py

# Direct voice mode
python3 start_voice.py --mode voice

# Direct text mode
python3 start_voice.py --mode text

# Specify Whisper model size
python3 start_voice.py --model tiny   # Fast but less accurate
python3 start_voice.py --model base   # Balanced
python3 start_voice.py --model small  # More accurate
```

### Traditional Launch
```bash
# Run with full checks
python3 start.py

# Run directly
python3 app.py

# Run tests only
python3 start.py --test
```

## 💡 Usage Examples

### Basic Questions
- "What is machine learning?"
- "Search for the latest AI trends"
- "What's the weather like today?"

### Web Search
- "Search for Python best practices"
- "Find news about OpenAI"
- "What's the USD to CNY exchange rate?"

### Complex Tasks
- "Search for machine learning algorithms and write a simple implementation"
- "Find information about quantum computing and create a presentation outline"
- "Research current AI trends and summarize the key findings"

## 🏗️ System Architecture

```
User Input → Planner → Executor → Summarizer → Reviewer → User Output
                ↓          ↓          ↓            ↓
            Planning   Execution  Formatting  Quality Check
```

## 📁 Project Structure

```
autogen_voice_agent/
├── app.py                 # Main application
├── config.py              # Configuration management
├── tools.py               # Web search tools
├── start.py               # Smart launcher
├── start_voice.py         # Voice-enabled launcher
├── start_mac.command      # macOS launcher
├── start.bat              # Windows launcher
├── run.sh                 # Linux/Unix launcher
├── test_*.py              # Test suites
├── voice/                 # Voice modules
│   ├── __init__.py
│   ├── stt.py            # Speech-to-text (Whisper)
│   ├── tts.py            # Text-to-speech
│   ├── audio_io.py       # Audio recording/playback
│   └── voice_session.py  # Voice interaction manager
├── docs/                  # Documentation
│   ├── WINDOWS_GUIDE.md
│   ├── LINUX_GUIDE.md
│   ├── MACOS_GUIDE.md
│   └── VOICE_GUIDE.md    # Voice feature guide
└── examples/              # Usage examples
```

## 🧪 Testing

Run all tests:
```bash
python3 test_model_config.py
python3 unit_test.py
python3 test_web_search.py
python3 test_whisper_integration.py  # Voice feature test
```

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Check your internet connection
   - Verify API keys and endpoints
   - Ensure the API service is compatible with OpenAI format

2. **Model Not Found**
   - Verify model names in OAI_CONFIG_LIST
   - Check if your API provider supports the requested models

3. **Web Search Failed**
   - Check internet connectivity
   - Some searches may be rate-limited

For detailed platform-specific guides, see:
- [Windows Guide](docs/WINDOWS_GUIDE.md)
- [Linux Guide](docs/LINUX_GUIDE.md)
- [macOS Guide](docs/MACOS_GUIDE.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft AutoGen team for the excellent framework
- OpenAI for the powerful language models
- Community contributors

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/discussions)

---

Made with ❤️ by Rick | [GitHub](https://github.com/RRiiiccckkk)
