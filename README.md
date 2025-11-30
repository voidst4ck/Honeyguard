# 🍯 HoneyGuard

Multi-service honeypot for threat intelligence gathering and SOC training.

## 🎯 Features

- **SSH Honeypot** - Captures credentials with Paramiko
- **Modular Architecture** - Easy to add HTTP, FTP, Telnet services
- **JSON Logging** - SIEM-ready structured logs
- **YAML Configuration** - Simple service management
- **Configurable Limits** - Max auth attempts, timeouts
- **Custom SSH Banners** - Realistic service emulation

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Pipenv

### Installation
```bash
# Clone the repository
git clone https://github.com/voidst4ck/Honeyguard.git
cd Honeyguard

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Run the honeypot
python -m honeyguard.main
```

## ⚙️ Configuration

Edit `config/default.yml`

## 🔍 Testing
```bash
# Terminal 1: Start honeypot
python -m honeyguard.main

# Terminal 2: Test connection
ssh admin@127.0.0.1 -p 2222
# Try any username/password - all attempts are logged
```

## 📊 Log Output

Logs are saved in JSON format in `logs/honeyguard.log`:
```json
{
  "timestamp": "2025-01-15T23:12:45Z",
  "level": "WARNING",
  "service": "ssh",
  "message": "auth_attempt",
  "source_ip": "192.168.1.100",
  "session_id": "20250115231245",
  "username": "admin",
  "password": "P@ssw0rd123",
  "auth_method": "password",
  "attempt": 1,
  "success": false
}
```

## 🛡️ Security Warning

**This is a honeypot - DO NOT expose to production networks!**

- Run in isolated environment (VM, separate VLAN)
- Monitor resource usage (DoS attacks possible)
- Regularly review logs for reconnaissance patterns
- Use non-standard ports in production (not 22)

## 🔧 Development
```bash
# Install dev dependencies
pipenv install --dev

# Run with debug logging
python -m honeyguard.main  # Edit config to set level: "DEBUG"
```

## 🗺️ Roadmap

- [x] SSH honeypot with Paramiko
- [x] JSON structured logging
- [x] YAML configuration
- [x] Max auth attempts limiting
- [ ] HTTP honeypot service
- [ ] FTP honeypot service
- [ ] Geo-IP lookup integration
- [ ] Slack/Discord alerting
- [ ] Rate limiting per IP

## 📜 License

MIT License

## 🎓 Educational Purpose

This project is for **educational and research purposes only**.

Developed as part of BTLO1 certification training for SOC analyst skills.

## 📧 Contact

[@voidst4ck](https://github.com/voidst4ck)

---

**⚠️ Deploy responsibly. Monitor actively. Learn continuously.**