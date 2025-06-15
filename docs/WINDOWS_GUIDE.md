# Windows Installation and Usage Guide

This guide provides detailed instructions for Windows users to install and run the AutoGen Multi-Agent Voice Assistant.

## 📋 Prerequisites

### System Requirements
- Windows 10 or Windows 11
- Python 3.8 or higher
- Internet connection
- At least 4GB RAM (8GB recommended)

## 🛠️ Installation

### Step 1: Install Python

1. **Download Python**
   - Visit [python.org](https://www.python.org/downloads/windows/)
   - Download Python 3.8+ (latest stable version recommended)

2. **Install Python**
   - Run the installer
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH"
   - Choose "Install Now"

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Download the Project

**Option A: Using Git**
```cmd
git clone https://github.com/RRiiiccckkk/X-program-autogen_voice_agent.git
cd autogen_voice_agent
```

**Option B: Download ZIP**
1. Go to the [GitHub repository](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent)
2. Click "Code" → "Download ZIP"
3. Extract to your desired location
4. Open Command Prompt in the extracted folder

### Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
```

If you encounter permission issues, try:
```cmd
pip install --user -r requirements.txt
```

### Step 4: Configure API

1. **Copy the configuration template**
   ```cmd
   copy OAI_CONFIG_LIST OAI_CONFIG_LIST.backup
   ```

2. **Edit OAI_CONFIG_LIST** (use Notepad or any text editor)
   ```json
   [
       {
           "model": "gpt-4o-2024-11-20",
           "api_key": "YOUR_API_KEY_HERE",
           "base_url": "https://api.openai.com/v1",
           "api_type": "openai"
       },
       {
           "model": "o3-2025-04-16",
           "api_key": "YOUR_API_KEY_HERE",
           "base_url": "https://api.openai.com/v1",
           "api_type": "openai"
       },
       {
           "model": "o4-mini",
           "api_key": "YOUR_API_KEY_HERE",
           "base_url": "https://api.openai.com/v1",
           "api_type": "openai"
       }
   ]
   ```

## 🚀 Running the Application

### Method 1: Double-Click Launch (Easiest)
1. Double-click `start.bat` in the project folder
2. The system will automatically check dependencies and start

### Method 2: Command Prompt
```cmd
# Navigate to project directory
cd path\to\autogen_voice_agent

# Run with full checks
python start.py

# Run directly
python app.py

# Run tests only
python start.py --test
```

### Method 3: PowerShell
```powershell
# Navigate to project directory
Set-Location "path\to\autogen_voice_agent"

# Run the application
python start.py
```

## 🧪 Testing

### Run All Tests
```cmd
python start.py --test
```

### Individual Tests
```cmd
python test_model_config.py
python unit_test.py
python test_web_search.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solutions**:
- Reinstall Python and check "Add Python to PATH"
- Use `py` instead of `python`:
  ```cmd
  py start.py
  ```
- Manually add Python to PATH:
  1. Search "Environment Variables" in Start Menu
  2. Click "Environment Variables"
  3. Add Python installation path to PATH

#### 2. Permission Denied
**Error**: `Permission denied` or `Access is denied`

**Solutions**:
- Run Command Prompt as Administrator
- Use `--user` flag:
  ```cmd
  pip install --user -r requirements.txt
  ```

#### 3. SSL Certificate Error
**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions**:
- Update certificates:
  ```cmd
  pip install --upgrade certifi
  ```
- Use trusted hosts:
  ```cmd
  pip install --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
  ```

#### 4. Module Not Found
**Error**: `ModuleNotFoundError: No module named 'autogen'`

**Solutions**:
- Ensure you're in the correct directory
- Reinstall dependencies:
  ```cmd
  pip uninstall pyautogen
  pip install pyautogen
  ```

#### 5. API Connection Issues
**Error**: API connection failed

**Solutions**:
- Check internet connection
- Verify API keys in `OAI_CONFIG_LIST`
- Test with a simple API call
- Check firewall/antivirus settings

### Windows-Specific Tips

1. **Use Windows Terminal** (recommended over Command Prompt)
   - Install from Microsoft Store
   - Better Unicode support
   - Improved copy/paste

2. **Antivirus Software**
   - Some antivirus may block Python scripts
   - Add project folder to exclusions if needed

3. **Windows Defender**
   - May flag Python executables
   - Allow through Windows Defender if prompted

## 📁 File Associations

To make `.py` files executable by double-click:

1. Right-click any `.py` file
2. Choose "Open with" → "Choose another app"
3. Select Python
4. Check "Always use this app"

## 🔄 Updates

To update the project:

```cmd
git pull origin main
pip install -r requirements.txt --upgrade
```

## 💡 Performance Tips

1. **Use SSD storage** for better performance
2. **Close unnecessary applications** to free up RAM
3. **Use Windows Terminal** for better experience
4. **Enable Windows Subsystem for Linux (WSL)** for advanced users

## 🆘 Getting Help

If you encounter issues:

1. Check this guide first
2. Run diagnostics:
   ```cmd
   python start.py --test
   ```
3. Check [GitHub Issues](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/issues)
4. Create a new issue with:
   - Windows version
   - Python version
   - Error messages
   - Steps to reproduce

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/issues)
- **Discussions**: [Ask questions](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/discussions)

---

Happy coding! 🎉
