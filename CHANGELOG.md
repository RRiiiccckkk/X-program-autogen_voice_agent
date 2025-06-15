# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-06-15

### 🎉 Major Release - Multi-Agent Architecture with Web Search

### Added
- **Five-Agent Collaborative System**
  - Planner Agent (o3-2025-04-16): Advanced problem understanding and strategic planning
  - Executor Agent (o3-2025-04-16): Code execution with integrated web search capabilities
  - Summarizer Agent (o4-mini): Efficient content reorganization and formatting
  - Reviewer Agent (gpt-4o-2024-11-20): Quality assurance and feedback
  - User Proxy: Intelligent interaction management

- **Integrated Web Search Capabilities**
  - DuckDuckGo search (no API key required)
  - Wikipedia knowledge base access
  - Real-time news search via Google News RSS
  - Web content extraction from any URL
  - Currency exchange rate queries
  - Automatic search source selection

- **Cross-Platform Launch Scripts**
  - `start_mac.command` - One-click macOS launcher
  - `start.bat` - Windows batch script
  - `start.py` - Smart Python launcher with environment checks
  - `run.sh` - Linux/Unix shell script

- **Comprehensive Testing Suite**
  - `test_model_config.py` - Model configuration validation
  - `unit_test.py` - Complete unit testing framework
  - `test_web_search.py` - Web search functionality testing

- **Enhanced Configuration Management**
  - Multi-model configuration support
  - Flexible API provider compatibility
  - Automatic model routing for different agents

- **Documentation and Examples**
  - Complete README rewrite with international support
  - Usage examples and best practices
  - Cross-platform installation guides
  - API flexibility documentation

### Changed
- **Model Architecture Upgrade**
  - Upgraded from single-agent to five-agent collaborative system
  - Implemented o3-2025-04-16 for planner and executor agents
  - Added o4-mini for efficient summarization tasks
  - Enhanced system prompts for better reasoning

- **Improved User Experience**
  - Automatic environment checking and validation
  - Intelligent error handling and recovery
  - Better formatted output and responses
  - Cross-platform compatibility

### Technical Improvements
- **Code Organization**
  - Modular tool system in `tools.py`
  - Separated configuration management
  - Clean project structure
  - Comprehensive error handling

- **Performance Optimizations**
  - Efficient model routing
  - Optimized search algorithms
  - Better memory management
  - Reduced API calls through intelligent caching

### Dependencies
- Added `requests>=2.31.0` for web functionality
- Added `beautifulsoup4>=4.12.0` for HTML parsing
- Added `lxml>=4.9.0` for XML processing
- Updated `pyautogen>=0.2.0` for latest features

## [1.0.0] - Previous Version

### Features
- Basic AutoGen voice assistant
- Single-agent conversation system
- Local voice recognition support
- Basic LLM integration

---

## Migration Guide from v1.x to v2.0

### Configuration Changes
1. Update your `OAI_CONFIG_LIST` to include multiple models
2. Add new model configurations for o3-2025-04-16 and o4-mini
3. Ensure API compatibility with OpenAI format

### New Dependencies
```bash
pip install -r requirements.txt
```

### Usage Changes
- The system now uses a five-agent workflow
- Web search capabilities are automatically available
- Use platform-specific launchers for easier startup

For detailed migration instructions, see the [README.md](README.md).
