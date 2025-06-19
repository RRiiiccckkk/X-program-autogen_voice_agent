# 语音多智能体助手使用指南

## 📖 概述

本系统已成功集成 OpenAI Whisper 语音识别技术，支持语音和文本两种交互模式。系统基于多智能体架构，提供智能的问题解答和任务执行能力。

## 🎯 功能特点

### 语音功能
- **语音识别**: 使用 OpenAI Whisper 进行本地语音转文字
- **语音合成**: 支持 macOS 系统 TTS (say 命令)
- **实时交互**: 支持语音对话模式
- **多语言支持**: 主要支持中文，也可处理英文

### 智能体架构
- **规划者**: 理解问题并制定执行计划
- **执行者**: 执行代码和调用工具函数
- **总结者**: 整理和格式化答案
- **评审者**: 质量控制和最终审核
- **用户代理**: 管理交互流程

## 🚀 快速开始

### 1. 环境检查
运行集成测试确认所有组件正常：
```bash
python test_whisper_integration.py
```

### 2. 启动系统
```bash
python start_voice.py
```

### 3. 选择交互模式
系统启动后会提示选择：
- **1. 文本模式** (默认) - 键盘输入
- **2. 语音模式** - 语音输入

## 📋 依赖要求

### 必需依赖
```bash
pip install openai-whisper==20231117
pip install pyautogen>=0.2.0
pip install openai>=1.0.0
pip install requests>=2.31.0
pip install beautifulsoup4>=4.12.0
```

### 可选依赖
```bash
# 实时录音功能 (推荐)
brew install portaudio  # macOS
pip install pyaudio

# 增强 TTS 功能
pip install pyttsx3
```

## 🎮 使用方法

### 语音模式操作
1. 选择语音模式 (选项 2)
2. 按 Enter 键开始说话
3. 说话 5 秒后自动停止录音
4. 系统会语音播放回答
5. 重复步骤 2-4 继续对话
6. 说 "退出"、"再见" 或按 Ctrl+C 结束

### 文本模式操作
1. 选择文本模式 (选项 1，默认)
2. 输入问题或任务
3. 查看文字回答
4. 输入 "退出" 或按 Ctrl+C 结束

### 支持的功能
- **网络搜索**: "搜索最新的人工智能新闻"
- **天气查询**: "北京今天天气怎么样"
- **代码执行**: "用Python计算斐波那契数列"
- **信息查询**: "解释什么是机器学习"
- **任务处理**: 各种复杂的分析和处理任务

## ⚙️ 配置选项

### Whisper 模型大小
启动时可指定模型：
```bash
python start_voice.py --model tiny    # 最快，准确度较低
python start_voice.py --model base    # 平衡
python start_voice.py --model small   # 较慢，准确度较高
```

### 直接指定模式
```bash
python start_voice.py --mode text     # 直接启动文本模式
python start_voice.py --mode voice    # 直接启动语音模式
```

## 🔧 故障排除

### 常见问题

#### 1. Whisper 导入失败
```bash
# 解决方案
pip install openai-whisper
```

#### 2. 录音功能不可用
系统会自动使用 Mock 录音器，您仍可以手动测试：
```bash
# macOS 安装 PyAudio
brew install portaudio
pip install pyaudio
```

#### 3. TTS 语音播放失败
- macOS: 确保系统 TTS 功能正常
- 其他系统: 系统会使用文字输出

#### 4. 模型加载时间长
- 首次使用需要下载模型文件
- 建议使用 `tiny` 模型进行快速测试
- 后续启动会更快

### 系统兼容性
- **推荐**: macOS (完整功能支持)
- **支持**: Linux (部分功能)
- **有限支持**: Windows (文本模式)

## 🎵 音频设置建议

### 录音质量优化
- 使用质量良好的麦克风
- 在安静环境中录音
- 清晰发音，语速适中
- 避免背景噪音

### 语音识别提示
- 中文识别准确度较高
- 支持普通话和部分方言
- 专业术语可能需要重复
- 可以混用中英文

## 🔄 更新和维护

### 定期更新
```bash
pip install --upgrade openai-whisper
pip install --upgrade pyautogen
```

### 日志查看
系统运行日志保存在 `coding/` 目录中，可用于问题诊断。

## 📞 技术支持

如遇到问题：
1. 首先运行 `python test_whisper_integration.py` 检查系统状态
2. 查看错误信息和建议解决方案
3. 尝试使用文本模式作为备用方案
4. 检查依赖包是否正确安装

## 🎯 最佳实践

### 语音交互
- 问题要清晰具体
- 一次说一个问题
- 等待系统完全回答后再继续
- 复杂任务可以分步骤提问

### 文本交互
- 详细描述需求
- 提供必要的上下文
- 可以要求不同格式的输出
- 支持多轮对话

---

🎉 **享受与智能助手的语音交互体验！**
