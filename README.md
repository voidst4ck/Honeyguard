# 🍯 HoneyGuard

Multi-service SSH honeypot for threat intelligence gathering and attacker profiling.

## 🎯 Features

- **SSH Honeypot** - Captures credentials and commands
- **Native Asyncio** - High-performance async architecture
- **Real-time Alerts** - Log all authentication attempts
- **Statistics Dashboard** - Top IPs, credentials, and attack patterns

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Pipenv

## 🔍 Testing

Test the honeypot from another machine:
```bash
ssh anyuser@<honeypot-ip> -p 2222
# Try any username/password - all attempts are logged
```

## 📈 Statistics

View attack statistics:
```python
from core.database import HoneyDatabase

db = HoneyDatabase()
stats = db.get_stats()

print(f"Total attacks: {stats['total_attacks']}")
print(f"Top IPs: {stats['top_ips']}")
print(f"Top credentials: {stats['top_usernames']}")
```

## 🛡️ Security Warning

**This is a honeypot - DO NOT expose to production networks!**

- Run in isolated environment (VM, separate VLAN)
- Monitor resource usage (DoS attacks possible)
- Regularly review logs for reconnaissance patterns

## 📝 Project Structure
```
Honeyguard/
├── core/
│   ├── ssh_server.py    # SSH protocol implementation
│   ├── logger.py        # Logging system
│   └── database.py      # SQLite persistence
├── data/                # SQLite database
├── logs/                # Log files
└── main.py             # Entry point
```

## 🔧 Configuration

Edit `main.py` to configure:

- **Port**: Change `port=2222` 
- **Host**: Change `host='0.0.0.0'`
- **Log Level**: Modify `HoneyLogger(log_level=10)` (10=DEBUG, 20=INFO)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📜 License

MIT License - see LICENSE file

## 🎓 Educational Purpose

This project is for **educational and research purposes only**. 

Developed as part of BTLO1 certification training for SOC analyst skills.

## 📧 Contact

[@voidst4ck](https://github.com/voidst4ck)

---

**⚠️ Deploy responsibly. Monitor actively. Learn continuously.**