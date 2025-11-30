# Mirage V3: Cyberpunk Edition 🌐💻

A single-file, LLM-driven Cyber Range & Honeypot Simulator designed for safe Red Team practice. Features dynamic response generation, real-time terminal dashboard, and Burp Suite integration.

## 🎯 Features

- **AI-Powered Responses**: Uses Kimi/Moonshot AI to dynamically generate TCP/HTTP responses
- **Multi-Protocol Support**: SSH, FTP, HTTP/HTTPS on ports 21, 22, 80, 443, 8080
- **Real-time TUI**: Cyberpunk-themed terminal dashboard with live metrics
- **Burp Suite Integration**: Specialized handling for web vulnerability testing
- **Asset Fabrication**: Generates fake documents (Excel, Word) for realistic scenarios
- **Difficulty Modes**: EASY (vulnerable) vs HARD (security-conscious) responses
- **Network Simulation**: Visual network topology and connection monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- sudo/admin privileges (for privileged ports)
- Kimi API key

### Installation

1. **Clone/Setup**:
```bash
cd mirage-v3-cyberpunk
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure Environment**:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Kimi API key
nano .env
```

4. **Run with sudo** (required for ports 22, 80, 443):
```bash
sudo python3 mirage_v3_cyberpunk.py
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```bash
LLM_API_KEY=your_kimi_api_key_here
```

### Key Settings in Python Script
- `ACTIVE_PORTS`: List of ports to listen on
- `DIFFICULTY`: "EASY" or "HARD" 
- `MODEL_NAME`: AI model to use
- `WORLD_CONTEXT`: Global state dictionary

## 🎮 Usage

### Terminal UI
- **Dashboard**: Real-time system metrics and connection logs
- **Network Map**: Visual topology of simulated infrastructure
- **Virtual Assets**: Browse fabricated file system
- **Web Config**: Toggle vulnerability settings
- **Burp Logs**: View intercepted web traffic

### Network Testing
Once running, you can test with:
```bash
# SSH testing
ssh root@localhost -p 22

# Web testing  
curl http://localhost:80
curl http://localhost:8080

# FTP testing
ftp localhost 21
```

### Web Interface
Open `index.html` in your browser for a visual dashboard (simulated data).

## 🛡️ Security Features

- **Safe Environment**: All responses are AI-generated, no real system access
- **Configurable Difficulty**: EASY mode for learning, HARD for advanced testing
- **Vulnerability Simulation**: SQL injection, XSS, directory traversal
- **Realistic Banners**: Convincing service responses for each protocol

## 📊 Dashboard Components

1. **CPU/Memory Gauges**: Simulated system load
2. **Connection History**: Recent network connections
3. **AI Kernel Log**: Real-time AI decision logging
4. **Threat Level**: Dynamic security status
5. **Active Modules**: Service monitoring status

## 🔍 AI Integration

The system uses Kimi AI to:
- Generate protocol-appropriate responses
- Simulate vulnerable web applications
- Create realistic file system content
- Adapt responses based on difficulty setting

## 🚨 Important Notes

- **Run with sudo**: Required for privileged ports (22, 80, 443, 8080)
- **Firewall**: May need to allow incoming connections
- **API Limits**: Monitor your Kimi API usage
- **Terminal Size**: Maximize terminal for best TUI experience

## 🐛 Troubleshooting

### Permission Denied
```bash
sudo python3 mirage_v3_cyberpunk.py
```

### Port Binding Issues
- Check if ports are already in use: `sudo lsof -i :22`
- Try different ports in `ACTIVE_PORTS` list

### API Errors
- Verify `LLM_API_KEY` in `.env` file
- Check API quota/limitations
- Ensure base URL is correct for your region

## 🎨 Customization

### Changing Colors
Edit the color constants at the top of the Python script:
```python
C_CB = "bright_cyan"      # Main borders
C_GN = "bright_green"     # Success/Go
C_RD = "bright_red"       # Alerts/Errors
```

### Adding New Vulnerabilities
Modify the `SYSTEM_PROMPT` to include new attack patterns and responses.

### Custom Assets
Extend the `Fabricator` class to generate additional file types.

## 📚 Use Cases

- **Red Team Training**: Practice against AI-generated targets
- **Penetration Testing**: Safe environment for tool testing
- **Security Education**: Learn vulnerability patterns
- **CTF Preparation**: Practice with simulated challenges
- **Tool Development**: Test security tools safely

## 🤝 Contributing

This is a research/educational tool. Feel free to:
- Report bugs and issues
- Suggest new features
- Share your testing scenarios
- Contribute improvements

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Always ensure you have permission before testing any systems. The authors are not responsible for misuse.

---

**Mirage V3** - Where AI meets cybersecurity training in a cyberpunk aesthetic. Happy hacking! 🚀
