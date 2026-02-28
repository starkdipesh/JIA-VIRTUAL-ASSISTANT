# JIA Installation Quick Reference

## One-Liner Installation

```bash
# Clone, setup, and run in one go
git clone https://github.com/starkdipesh/JIA-VIRTUAL-ASSISTANT.git && cd JIA-VIRTUAL-ASSISTANT && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python verify_installation.py
```

## Quick Install (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/starkdipesh/JIA-VIRTUAL-ASSISTANT.git
cd JIA-VIRTUAL-ASSISTANT

# 2. Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python verify_installation.py

# 5. Configure (open in editor, replace YOUR_API_KEY)
cp .env.example .env
# Edit .env with your API key and database credentials

# 6. Run application
cd CODE/CODE/AIAssistant
python JIA.py
```

## Requirements File Summary

| File | Contents | Size |
|------|----------|------|
| `requirements.txt` | All project dependencies (170+ packages) | ~1.5GB |

## Installation by Use Case

### 🚀 **Just Want to Run It**
```bash
pip install -r requirements.txt
python verify_installation.py
```

## Configuration Steps

### 1. Database
```bash
# Start MySQL
mysql -u root -p

# Create database
CREATE DATABASE AIuser;

# Add test user
mysql -u root -p AIuser < CODE/CODE/AIAssistant/aiuser.sql
```

### 2. API Keys
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add:
# - DB_PASSWORD=your_mysql_password
# - GEMINI_API_KEY=your_api_key_from_https://ai.google.dev/
```

### 3. Verify
```bash
python verify_installation.py
```

## Troubleshooting

### "pip not found"
```bash
python -m pip install -r requirements.txt
```

### "No module named 'vosk'"
```bash
# Optional - comment out in offlineSTT.py if not needed
pip install vosk
```

### "MySQL connection refused"
```bash
# Check MySQL is running
mysqld --version
# On Windows: net start MySQL80
# On Linux: sudo systemctl start mysql
```

### "No microphones detected"
```bash
# Install audio libraries
# Windows: Download from http://portaudio.com
# Linux: sudo apt-get install portaudio19-dev
# macOS: brew install portaudio
```

## Common Commands

```bash
# Verify installation
python verify_installation.py

# Run application
python CODE/CODE/AIAssistant/JIA.py

# Check dependencies
pip check

# Update all packages
pip install --upgrade -r requirements.txt

# Export current environment (generate requirements.txt from .venv)
pip freeze > requirements.txt
```

## File Structure After Installation

```
JIA-VIRTUAL-ASSISTANT/
├── venv/                           # Virtual environment (large!)
│   ├── Lib/site-packages/         # Installed packages
│   └── Scripts/                   # Executables
├── CODE/CODE/AIAssistant/
│   ├── JIA.py                    # Main application
│   ├── gemini.py                 # AI integration
│   ├── stt.py & tts.py          # Speech processing
│   └── ...other modules
├── requirements.txt               # All project dependencies
├── .env                          # Configuration (don't commit!)
├── .env.example                  # Template
└── SETUP.md                      # Detailed guide
```

## Virtual Environment Tips

```bash
# Activate (required each terminal session)
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Check if activated (should show venv prefix)
(venv) $ python --version

# Deactivate
deactivate

# Delete virtual environment (to start fresh)
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

## Performance Tips

1. **Use SSD**: Faster pip installation
2. **Use Cache**: `pip install --cache-dir ~/.pip-cache`
3. **Upgrade pip**: `python -m pip install --upgrade pip`
4. **Parallel Install**: Use wheels instead of building from source
5. **Connection**: Use faster PyPI mirror if needed

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure .env file
3. ✅ Run verify_installation.py
4. 📖 Read SETUP.md for detailed guide
5. 📚 Read DEPENDENCIES.md to understand tech stack
6. 🚀 Run `python JIA.py`
7. 💬 Login with test credentials or create new account

## Support Resources

- **Installation Issues**: See SETUP.md → Troubleshooting section
- **Dependency Details**: See DEPENDENCIES.md for each package analysis
- **Main Documentation**: See README.md for architecture & features
- **Technical Setup**: See SETUP.md for detailed configuration

---

**Estimated Installation Time**: 5-10 minutes (varies by internet speed)  
**Disk Space Required**: 2-8 GB (depends on options)  
**Python Versions**: 3.8, 3.9, 3.10, 3.11

Good luck! 🎉
