# JIA Setup & Installation Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Detailed Installation](#detailed-installation)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Virtual Environments](#virtual-environments)

---

## Quick Start

### Minimum Setup (5 minutes)
```bash
# Clone repository
git clone https://github.com/your-username/JIA-VIRTUAL-ASSISTANT.git
cd JIA-VIRTUAL-ASSISTANT

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
cd CODE/CODE/AIAssistant
python JIA.py
```

---

## System Requirements

### Hardware
- **Processor**: Intel Core i5 or equivalent (quad-core minimum)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for application and venv
- **Audio**: Microphone and speakers
- **OS**: Windows 7+, Linux (Ubuntu 18.04+), macOS 10.14+
  - **Primary Support**: Windows 10/11
  - **Secondary Support**: Ubuntu 20.04 LTS

### Software
- **Python**: 3.8, 3.9, 3.10, 3.11, or 3.12
- **MySQL**: 5.7+ or 8.0+ (local or remote)
- **Git**: For version control
- **Internet**: Required for AI features, recommended for all

### Required Services
- **Google Gemini API Key**: Free from https://ai.google.dev/
- **MySQL Server**: Running locally or accessible remotely

---

## Detailed Installation

### Step 1: System Preparation

#### Windows
```bash
# Verify Python installation
python --version  # Should be 3.8 or higher

# Verify pip
pip --version

# Update pip (recommended)
python -m pip install --upgrade pip
```

#### Linux (Ubuntu/Debian)
```bash
# Install Python and dependencies
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv python3.10-dev

# Install system audio libraries (required for speech recognition)
sudo apt-get install portaudio19-dev

# Install MySQL client
sudo apt-get install mysql-client
```

#### macOS
```bash
# Install via Homebrew
brew install python@3.10
brew install portaudio
brew install mysql-client
```

### Step 2: Clone Repository

```bash
# Via HTTPS (recommended for CI/CD)
git clone https://github.com/your-username/JIA-VIRTUAL-ASSISTANT.git
cd JIA-VIRTUAL-ASSISTANT

# Via SSH (if configured)
git clone git@github.com:your-username/JIA-VIRTUAL-ASSISTANT.git
cd JIA-VIRTUAL-ASSISTANT
```

### Step 3: Create Virtual Environment

#### Standard Virtual Environment (venv)
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate

# Verify activation (should show venv prefix)
which python  # Linux/macOS
where python  # Windows
```

#### Advanced: Using conda (Alternative)
```bash
# Create conda environment
conda create -n jia python=3.10
conda activate jia
```

### Step 4: Install Dependencies

```bash
# Install all project dependencies
pip install -r requirements.txt

# Verify installation
pip check
```

**Note**: The `requirements.txt` includes all 170+ packages used in the project, extracted from the actual virtual environment with exact version pinning for reproducibility.

### Step 5: Database Configuration

#### MySQL Setup

```bash
# 1. Start MySQL server
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql

# macOS
brew services start mysql-community-server

# 2. Create database
mysql -u root -p
# Enter password when prompted
```

```sql
-- Inside MySQL CLI
CREATE DATABASE AIuser;
USE AIuser;

-- Import schema if available
SOURCE CODE/CODE/AIAssistant/aiuser.sql;

-- Create owner table if schema not imported
CREATE TABLE owner (
    username VARCHAR(100) PRIMARY KEY,
    email VARCHAR(100),
    phoneno VARCHAR(15),
    pasword VARCHAR(100)
);

-- Create test user
INSERT INTO owner VALUES ('testuser', 'test@example.com', '9999999999', 'password123');
```

#### Update Configuration in JIA.py

Edit `CODE/CODE/AIAssistant/JIA.py` around line 45:

```python
# Database configuration
host = 'localhost'         # or your remote DB host
port = '3306'             # MySQL default port
user = 'root'             # Your MySQL username
password = 'your_password' # Your MySQL password
database = 'AIuser'       # Database name
```

### Step 6: API Configuration

#### Google Gemini API

1. **Get Free API Key**
   - Visit: https://ai.google.dev/
   - Click "Get API Key"
   - Create or select a Google Cloud project
   - Copy your API key

2. **Configure in gemini.py**
   - Edit `CODE/CODE/AIAssistant/gemini.py`
   - Find line with `googleapi = "..."`
   - Replace with your API key:

```python
googleapi = "YOUR_API_KEY_HERE"
# Example: googleapi = "AIzaSyAjwv94NAt5SPCzqpNlT0Ye1kwwKV4AXhk"
```

**WARNING**: Never commit API keys to git. Use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()
googleapi = os.getenv('GEMINI_API_KEY')
```

Create `.env` file in project root:
```
GEMINI_API_KEY=your_api_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=AIuser
```

### Step 7: Verify Installation

```bash
# Check all imports
python -c "import kivy; import speech_recognition; import pyttsx3; print('All imports successful!')"

# Test database connection
python -c "import mysql.connector; print('MySQL connector OK')"

# Run the application
cd CODE/CODE/AIAssistant
python JIA.py
```

---

## Configuration

### Environment Variables (.env file)

Create `.env` in project root:

```bash
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=AIuser

# APIs
GEMINI_API_KEY=your_api_key
WOLFRAM_ALPHA_APP_ID=your_app_id

# Application
DEBUG=False
LOG_LEVEL=INFO
MAX_RESPONSE_WORDS=500
```

### Audio Configuration

Edit `CODE/CODE/AIAssistant/stt.py` for microphone settings:

```python
energy_threshold = 300        # Noise level (higher = less sensitive)
pause_threshold = 1           # Pause duration (seconds)
language = 'en-IN'           # Language code
```

---

## Troubleshooting

### Installation Issues

#### "pip is not recognized as an internal or external command"
```bash
# Windows: Use Python module
python -m pip install -r requirements.txt

# Or add Python to PATH
# Control Panel > System > Environment Variables > Add Python to PATH
```

#### "No module named 'kivy'"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall
pip install --force-reinstall kivy==2.3.1
```

#### "ModuleNotFoundError: No module named 'mysql'"
```bash
pip install mysql-connector-python==8.2.0
```

### Runtime Issues

#### "No module named '_ctypes'"
```bash
# Linux: Install required development files
sudo apt-get install python3-dev libffi-dev

# Reinstall kivy
pip install --force-reinstall kivy
```

#### "Could not find PortAudio"
```bash
# Install system audio libraries
# Linux
sudo apt-get install portaudio19-dev

# macOS
brew install portaudio

# Windows: Install from http://www.portaudio.com/download.html
```

#### "Connection refused (MySQL)"
```bash
# Verify MySQL is running
mysql -u root -p -e "SELECT VERSION();"

# Check credentials in JIA.py
# Restart MySQL service if needed
```

#### "No module named 'vosk' | Vosk model not found"
```bash
# Vosk is for offline speech recognition (optional)
# Comment it out if not needed in offlineSTT.py

# Or download vosk model:
# https://alphacephei.com/vosk/models
pip install vosk
```

### Audio Issues

#### "No microphone detected"
```bash
# Test microphone
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"

# Change microphone in stt.py
with sr.Microphone(device_index=1) as source:  # Use device 1 instead of 0
```

#### "Audio playback not working"
```bash
# Test speakers
from playsound import playsound
playsound('path/to/audio.mp3')

# Verify system audio is not muted
```

---

## Virtual Environments

### Comparison of Options

| Tool | Pros | Cons | Use When |
|------|------|------|----------|
| **venv** | Built-in, lightweight, simple | No conda support | Standard Python projects |
| **conda** | Package management, binary wheels | Larger, slower | Using ML/scientific packages |
| **poetry** | Lock files, dependency graphs | Requires poetry.lock setup | Production deployments |
| **pipenv** | Automatic lock files, Pipfile | Can be slow | Team projects |

### Best Practices

```bash
# 1. Always use virtual environment
python -m venv venv

# 2. Document Python version
echo "python=3.10" > .python-version

# 3. Keep requirements.txt updated
pip freeze > requirements.txt

# 4. Use .gitignore to exclude venv
echo "venv/" >> .gitignore
```

---

## Next Steps

1. **Start the Application**: `python JIA.py`
2. **Read Documentation**: Check `/DOC` folder
3. **Explore Features**: Login with test credentials
4. **Configure APIs**: Add your Gemini API key
5. **Customize Voice**: Adjust TTS settings in `tts.py`

---

## Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: See `/DOC` folder
- **Examples**: Check test files in repository
- **Community**: Star the project if helpful!

---

**Last Updated**: February 28, 2026
**Status**: Production Ready
