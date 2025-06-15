# Linux Installation and Usage Guide

This guide provides detailed instructions for Linux users to install and run the AutoGen Multi-Agent Voice Assistant.

## 📋 Prerequisites

### System Requirements
- Linux distribution (Ubuntu 18.04+, CentOS 7+, Debian 10+, Fedora 30+, etc.)
- Python 3.8 or higher
- Internet connection
- At least 4GB RAM (8GB recommended)

## 🛠️ Installation

### Step 1: Install Python

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install development tools
sudo apt install build-essential python3-dev
```

#### CentOS/RHEL/Fedora
```bash
# For CentOS/RHEL 7
sudo yum install python3 python3-pip python3-devel gcc

# For CentOS/RHEL 8+ or Fedora
sudo dnf install python3 python3-pip python3-devel gcc
```

#### Arch Linux
```bash
sudo pacman -S python python-pip base-devel
```

#### openSUSE
```bash
sudo zypper install python3 python3-pip python3-devel gcc
```

**Verify Installation**
```bash
python3 --version
pip3 --version
```

### Step 2: Download the Project

**Option A: Using Git**
```bash
# Install git if not available
sudo apt install git  # Ubuntu/Debian
# sudo dnf install git  # Fedora
# sudo yum install git  # CentOS

# Clone repository
git clone https://github.com/RRiiiccckkk/X-program-autogen_voice_agent.git
cd autogen_voice_agent
```

**Option B: Download ZIP**
```bash
# Using wget
wget https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/archive/main.zip
unzip main.zip
cd autogen_voice_agent-main

# Using curl
curl -L https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/archive/main.zip -o main.zip
unzip main.zip
cd autogen_voice_agent-main
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# If you encounter issues, try:
pip install --user -r requirements.txt
```

### Step 5: Configure API

1. **Backup the configuration template**
   ```bash
   cp OAI_CONFIG_LIST OAI_CONFIG_LIST.backup
   ```

2. **Edit OAI_CONFIG_LIST** (use nano, vim, or your preferred editor)
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

### Method 1: Shell Script (Recommended)
```bash
# Make script executable
chmod +x run.sh

# Run the application
./run.sh
```

### Method 2: Python Launcher
```bash
# Run with full checks
python3 start.py

# Run directly
python3 app.py

# Run tests only
python3 start.py --test
```

### Method 3: With Virtual Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Run application
python start.py

# Deactivate when done
deactivate
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

#### 1. Python Not Found
**Error**: `python3: command not found`

**Solutions**:
```bash
# Check if python is installed as 'python'
which python
python --version

# Install Python
sudo apt install python3  # Ubuntu/Debian
sudo dnf install python3  # Fedora
```

#### 2. Permission Denied
**Error**: `Permission denied` when running scripts

**Solutions**:
```bash
# Make scripts executable
chmod +x run.sh start.py

# Or run with python directly
python3 start.py
```

#### 3. SSL Certificate Issues
**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions**:
```bash
# Update certificates
sudo apt update && sudo apt install ca-certificates  # Ubuntu/Debian
sudo dnf update ca-certificates  # Fedora

# Update pip certificates
pip install --upgrade certifi
```

#### 4. Build Dependencies Missing
**Error**: `error: Microsoft Visual C++ 14.0 is required` or similar

**Solutions**:
```bash
# Install build tools
sudo apt install build-essential python3-dev  # Ubuntu/Debian
sudo dnf install gcc python3-devel  # Fedora
sudo yum groupinstall "Development Tools"  # CentOS
```

#### 5. Virtual Environment Issues
**Error**: `venv: command not found`

**Solutions**:
```bash
# Install venv module
sudo apt install python3-venv  # Ubuntu/Debian
sudo dnf install python3-venv  # Fedora

# Alternative: use virtualenv
pip3 install virtualenv
virtualenv venv
```

#### 6. Network/Firewall Issues
**Error**: Connection timeouts or blocked requests

**Solutions**:
```bash
# Check firewall
sudo ufw status  # Ubuntu
sudo firewall-cmd --state  # CentOS/Fedora

# Test connectivity
curl -I https://api.openai.com/v1/models

# Configure proxy if needed
export https_proxy=http://proxy:port
export http_proxy=http://proxy:port
```

### Distribution-Specific Tips

#### Ubuntu/Debian
```bash
# Install additional dependencies
sudo apt install curl wget git vim

# For older versions, use deadsnakes PPA for newer Python
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9 python3.9-pip
```

#### CentOS/RHEL
```bash
# Enable EPEL repository
sudo yum install epel-release

# For Python 3.8+ on CentOS 7
sudo yum install python38 python38-pip
```

#### Fedora
```bash
# Install development tools
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

#### Arch Linux
```bash
# Install AUR helper (yay) for additional packages
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si
```

## 📁 File Management

### Making Scripts Executable
```bash
chmod +x run.sh start.py start_mac.command
```

### Creating Desktop Shortcut
```bash
# Create desktop entry
cat > ~/.local/share/applications/autogen-assistant.desktop << EOF
[Desktop Entry]
Name=AutoGen Assistant
Comment=Multi-Agent Voice Assistant
Exec=/path/to/autogen_voice_agent/run.sh
Icon=/path/to/autogen_voice_agent/icon.png
Terminal=true
Type=Application
Categories=Development;
EOF
```

### Setting Up Aliases
Add to your shell profile (`~/.bashrc`, `~/.zshrc`):
```bash
alias autogen='cd /path/to/autogen_voice_agent && python3 start.py'
alias autogen-test='cd /path/to/autogen_voice_agent && python3 start.py --test'
```

## 🔄 Updates

### Using Git
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Manual Update
```bash
# Backup configuration
cp OAI_CONFIG_LIST OAI_CONFIG_LIST.backup

# Download new version
wget https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/archive/main.zip
unzip main.zip

# Restore configuration
cp OAI_CONFIG_LIST.backup autogen_voice_agent-main/OAI_CONFIG_LIST

# Update dependencies
cd autogen_voice_agent-main
pip install -r requirements.txt --upgrade
```

## 💡 Performance Tips

1. **Use SSD storage** for better I/O performance
2. **Monitor resources** with `htop` or `top`
3. **Use virtual environments** to avoid conflicts
4. **Enable swap** if you have limited RAM:
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

## 🔐 Security Considerations

1. **Secure API keys**
   ```bash
   chmod 600 OAI_CONFIG_LIST
   ```

2. **Use environment variables**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
   ```

3. **Regular updates**
   ```bash
   sudo apt update && sudo apt upgrade  # Ubuntu/Debian
   sudo dnf update  # Fedora
   ```

## 🆘 Getting Help

### System Information
```bash
# Distribution info
cat /etc/os-release
lsb_release -a

# Python info
python3 --version
pip3 --version

# System resources
free -h
df -h
```

### Diagnostic Commands
```bash
# Check Python installation
which python3
python3 -c "import sys; print(sys.path)"

# Check installed packages
pip3 list | grep -E "(autogen|openai|requests)"

# Check network
ping -c 4 google.com
curl -I https://api.openai.com/v1/models

# Check logs
journalctl -f  # System logs
dmesg | tail   # Kernel messages
```

### Log Files
```bash
# Application logs (if any)
tail -f ~/.local/share/autogen/logs/*.log

# System logs
sudo tail -f /var/log/syslog  # Ubuntu/Debian
sudo tail -f /var/log/messages  # CentOS/RHEL
```

## 📞 Support

If you encounter issues:

1. **Check this guide first**
2. **Run diagnostics**: `python3 start.py --test`
3. **Check system logs**: `journalctl -f`
4. **GitHub Issues**: [Report bugs](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/issues)
5. **Discussions**: [Ask questions](https://github.com/RRiiiccckkk/X-program-autogen_voice_agent/discussions)

When reporting issues, include:
- Linux distribution and version
- Python version
- Error messages
- Output of `python3 start.py --test`

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed (optional)
- [ ] Project downloaded
- [ ] Virtual environment created (recommended)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API configured in `OAI_CONFIG_LIST`
- [ ] Scripts made executable (`chmod +x run.sh`)
- [ ] Test run successful (`python3 start.py --test`)

---

Happy coding on Linux! 🐧
