# 更新日志

## [2025.06.19 - v3.0] - 语音交互与图形界面

### 🎯 重大更新
- **语音交互支持**
  - 集成 OpenAI Whisper 进行本地语音识别
  - 支持系统 TTS（文本转语音）macOS/Linux
  - 语音和文本双模式交互
  - 实时语音转文字处理
  - 多语言支持（中文/英文）

- **图形界面启动器**
  - 跨平台 GUI 应用（基于 tkinter）
  - 三种模式选择：演示模式、文字模式、语音模式
  - 一键启动脚本（macOS/Windows/Linux）
  - 可视化模式选择界面

- **新增模块**
  - `voice/` - 完整的语音处理模块
  - `launcher.py` - GUI 启动器应用
  - `start_voice.py` - 支持语音的启动脚本
  - `demo_voice.py` - 功能演示脚本

### 📁 新增文件
- 语音模块：
  - `voice/stt.py` - 语音转文字（Whisper）
  - `voice/tts.py` - 文字转语音
  - `voice/audio_io.py` - 音频录制和播放
  - `voice/voice_session.py` - 会话管理
- 启动器：
  - `launcher.py` - 图形界面
  - `launch_mac.command` - macOS 快捷启动
  - `launch_win.bat` - Windows 快捷启动
  - `launch_linux.sh` - Linux 快捷启动
- 文档：
  - `VOICE_GUIDE.md` - 语音功能使用指南
  - `WHISPER_INTEGRATION_SUMMARY.md` - 集成技术细节

### 🔧 技术特性
- Whisper 模型支持：tiny, base, small（可配置）
- 自动降级：缺少依赖时自动使用 Mock 组件
- 线程安全的语音会话管理
- 完整的错误处理和用户提示

### 📈 改进
- 增强的系统架构，支持语音输入输出
- 改进的错误处理和优雅降级
- 更新的依赖项（包含 Whisper）
- 更友好的用户界面和交互体验

## [2025.06.16 - v2.0] - 系统架构大幅简化

### 重大更新
- 🎯 **统一模型配置**：所有智能体现在使用同一个模型 gpt-4o-2024-11-20
  - 删除了复杂的多模型配置（o3、o4-mini等）
  - 简化了 config.py，只保留 `load_default_config()`
  - 减少了配置复杂度和潜在的兼容性问题

- 🛠️ **简化函数调用**：精简到3个核心功能
  - `search_web(query)` - 综合网络搜索（DuckDuckGo + 维基百科）
  - `get_weather(location)` - 实时天气查询
  - `open_web_page(url, action)` - 网页浏览器功能（截图/内容提取）

- 🌐 **新增浏览器功能**
  - 集成了网页访问能力
  - 支持截图、内容提取、日志获取
  - 提供了 MCP browser-tools 集成和备用方案

- 📝 **优化的 GroupChat 处理**
  - 改进了函数调用时的消息处理逻辑
  - 解决了 null content 错误
  - 优化了发言者选择机制

### 新增文件
- `app_simplified.py` - 简化版的多智能体应用
- `test_simplified_system.py` - 简化系统的测试脚本
- `enhanced_groupchat.py` - 增强的群聊管理器

### 改进
- 统一的错误处理和回退机制
- 更清晰的代码结构
- 减少了系统复杂度
- 提高了可维护性


## [2025.06.16] - 添加实时天气查询功能

### 新增功能
- ✨ 添加了 `get_weather()` 函数，支持查询任意城市的实时天气信息
  - 主要使用 wttr.in API（无需密钥）
  - 支持中英文城市名称
  - 返回详细天气信息：温度、体感温度、天气状况、风向风力、湿度、降水概率、气压、能见度等
  - 包含备用方案：当 wttr.in 无法访问时，自动切换到 DuckDuckGo 搜索引擎查询
- ✨ 天气功能已集成到多智能体系统中，执行者可以自动调用获取实时数据

### 改进
- 🔧 修复了模型兼容性问题
  - 将执行者从 o3-2025-04-16 改为 gpt-4o-2024-11-20 模型
  - 确保函数调用功能正常工作
  - 解决了 o3 和 o4-mini 模型不支持 function role 消息的问题
- 📝 更新了系统架构说明，明确各智能体使用的模型
- 🛠️ 添加了自定义发言者选择函数，优化了包含函数调用时的工作流程

### 技术细节
- 天气数据来源：wttr.in（主要）、DuckDuckGo（备用）
- 支持的功能：
  - 实时天气查询
  - 今日天气预报（最高/最低温度）
  - 天气描述自动翻译（英文转中文）
  - 风向自动翻译（16方位）
- 模型配置：
  - 规划者: o3-2025-04-16 (问题理解 + 战略规划)
  - 执行者: gpt-4o-2024-11-20 (代码执行 + 技术实现 + 函数调用)
  - 总结者: o4-mini (内容重组 + 格式优化)
  - 反馈者: gpt-4o-2024-11-20 (质量评估)

### 测试
- ✅ 单元测试：`test_get_weather.py` - 测试天气函数的各种场景
- ✅ 函数测试：`test_weather_direct.py` - 测试函数在 autogen 中的直接调用
- ✅ 注册测试：`test_function_registration.py` - 测试函数在 GroupChat 中的注册和调用
- ✅ 实际测试：成功获取了广州、北京等城市的实时天气数据

### 已知问题
- ⚠️ GroupChat 在处理某些函数响应时可能出现 null content 错误
- 📌 建议：可能需要进一步优化 GroupChat 的消息处理逻辑

### 新增文件
- `test_get_weather.py` - 天气函数单元测试
- `test_weather_direct.py` - 直接函数调用测试
- `test_function_registration.py` - GroupChat 函数注册测试
- `test_weather_integration.py` - 多智能体系统集成测试

## [之前的版本]
- 语音对话功能
- 多智能体协作系统
- 网络搜索功能
- 货币汇率查询
