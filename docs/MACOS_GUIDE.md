# macOS Installation and Usage Guide

This guide provides detailed instructions for macOS users to install and run the AutoGen Multi-Agent Voice Assistant.

## 📋 Prerequisites

### System Requirements
- macOS 10.15 (Catalina) or later
- Python 3.8 or higher
- Internet connection
- At least 4GB RAM (8GB recommended)

## 🛠️ Installation

### Step 1: Install Python

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

**Option B: Official Python Installer**
1. Visit [python.org](https://www.python.org/downloads/macos/)
2. Download Python 3.8+ for macOS
3. Run the installer package

**Verify Installation**
```bash
python3 --version
pip3 --version
```

### Step 2: Download the Project

**Option A: Using Git**
```bash
git clone https://github.com/RRiiiccckkk/X-program-autogen_voice_agent.git
cd autogen_voice_agent
```

**Option B: Download ZIP**
1. Go to the [GitHub repository](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent)
2. Click "Code" → "Download ZIP"
3. Extract to your desired location
4. Open Terminal in the extracted folder

### Step 3: Install Dependencies

```bash
pip3 install -r requirements.txt
```

If you encounter permission issues:
```bash
pip3 install --user -r requirements.txt
```

### Step 4: Configure API

1. **Backup the configuration template**
   ```bash
   cp OAI_CONFIG_LIST OAI_CONFIG_LIST.backup
   ```

2. **Edit OAI_CONFIG_LIST** (use TextEdit, nano, or your preferred editor)
   ```bash
   nano OAI_CONFIG_LIST
   ```
   
   Configure with your API details:
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

### Method 1: One-Click Launch (Easiest)
1. **Double-click** `start_mac.command` in Finder
2. If prompted about security, go to System Preferences → Security & Privacy → Allow

### Method 2: Terminal
```bash
# Navigate to project directory
cd /path/to/autogen_voice_agent

# Run with full checks
python3 start.py

# Run directly
python3 app.py

# Run tests only
python3 start.py --test
```

### Method 3: Shell Script
```bash
./run.sh
```

## 🧪 Testing

### Run All Tests
```bash
python3 start.py --test
```

### Individual Tests
```bash
python3 test_model_config.py
python3 unit_test.py
python3 test_web_search.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Permission Denied for .command File
**Error**: Cannot execute `start_mac.command`

**Solutions**:
```bash
# Make the file executable
chmod +x start_mac.command

# Or run from Terminal
./start_mac.command
```

#### 2. Python Command Not Found
**Error**: `python3: command not found`

**Solutions**:
- Install Python via Homebrew:
  ```bash
  brew install python
  ```
- Check if Python is installed:
  ```bash
  which python3
  ls -la /usr/bin/python*
  ```

#### 3. SSL Certificate Issues
**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions**:
```bash
# Update certificates
pip3 install --upgrade certifi

# For Python installed via Homebrew
brew reinstall ca-certificates

# Run the certificate update script
/Applications/Python\ 3.x/Install\ Certificates.command
```

#### 4. Xcode Command Line Tools
**Error**: `xcrun: error: invalid active developer path`

**Solution**:
```bash
xcode-select --install
```

#### 5. Homebrew Issues
**Error**: Homebrew-related errors

**Solutions**:
```bash
# Update Homebrew
brew update

# Fix permissions
sudo chown -R $(whoami) $(brew --prefix)/*

# Reinstall if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 6. M1/M2 Mac Compatibility
**For Apple Silicon Macs**:

```bash
# Use Rosetta if needed
arch -x86_64 pip3 install -r requirements.txt

# Or install native ARM versions
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### macOS-Specific Tips

1. **Use iTerm2** for better terminal experience
   ```bash
   brew install --cask iterm2
   ```

2. **Enable Developer Tools**
   ```bash
   xcode-select --install
   ```

3. **Gatekeeper Security**
   - If macOS blocks the application, go to System Preferences → Security & Privacy
   - Click "Allow Anyway" for the blocked application

4. **Environment Variables**
   Add to your shell profile (`~/.zshrc` or `~/.bash_profile`):
   ```bash
   export PATH="/opt/homebrew/bin:$PATH"  # For M1/M2 Macs
   export PATH="/usr/local/bin:$PATH"     # For Intel Macs
   ```

## 📁 File Management

### Making Scripts Executable
```bash
chmod +x start_mac.command
chmod +x run.sh
chmod +x start.py
```

### Creating Aliases
Add to your shell profile:
```bash
alias autogen='cd /path/to/autogen_voice_agent && python3 start.py'
```

## 🔄 Updates

### Using Git
```bash
git pull origin main
pip3 install -r requirements.txt --upgrade
```

### Manual Update
1. Download the latest release
2. Replace old files (keep your `OAI_CONFIG_LIST`)
3. Run `pip3 install -r requirements.txt --upgrade`

## 💡 Performance Tips

1. **Use SSD storage** for better performance
2. **Close unnecessary applications** to free up RAM
3. **Use Activity Monitor** to check resource usage
4. **Enable hardware acceleration** if available

## 🔐 Security Considerations

1. **Keep API keys secure**
   ```bash
   chmod 600 OAI_CONFIG_LIST
   ```

2. **Use environment variables** for sensitive data
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

3. **Regular updates**
   ```bash
   brew update && brew upgrade
   pip3 list --outdated
   ```

## 🆘 Getting Help

### Diagnostic Information
```bash
# System information
sw_vers
python3 --version
pip3 --version

# Check installation
python3 start.py --test

# Check permissions
ls -la start_mac.command
```

### Common Diagnostic Commands
```bash
# Check Python installation
which python3
python3 -c "import sys; print(sys.path)"

# Check pip packages
pip3 list | grep -E "(autogen|openai|requests)"

# Check network connectivity
curl -I https://api.openai.com/v1/models
```

## 📞 Support

If you encounter issues:

1. **Check this guide first**
2. **Run diagnostics**: `python3 start.py --test`
3. **Check system logs**: Console.app
4. **GitHub Issues**: [Report bugs](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/issues)
5. **Discussions**: [Ask questions](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/discussions)

When reporting issues, include:
- macOS version (`sw_vers`)
- Python version (`python3 --version`)
- Error messages
- Steps to reproduce

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Project downloaded
- [ ] Dependencies installed (`pip3 install -r requirements.txt`)
- [ ] API configured in `OAI_CONFIG_LIST`
- [ ] Scripts made executable (`chmod +x start_mac.command`)
- [ ] Test run successful (`python3 start.py --test`)

---

Enjoy your multi-agent assistant! 🎉
