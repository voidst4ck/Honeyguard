# 🍯 HoneyGuard

Multi-service SSH honeypot for threat intelligence gathering and attacker profiling.

## 🎯 Features

- **SSH Honeypot** - Captures credentials and commands
- **Real-time Alerts** - Log all authentication attempts
- **Statistics Dashboard** - Top IPs, credentials, and attack patterns

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Pipenv

## 🔍 Testing

Test the honeypot from another machine:
```bash
ssh anyuser@<honeypot-ip> -p 2222
# Try any username/password - all attempts are logged
```

## 🛡️ Security Warning

**This is a honeypot - DO NOT expose to production networks!**

- Run in isolated environment (VM, separate VLAN)
- Monitor resource usage (DoS attacks possible)
- Regularly review logs for reconnaissance patterns

## 📜 License

MIT License - see LICENSE file

## 🎓 Educational Purpose

This project is for **educational and research purposes only**. 

Developed as part of BTLO1 certification training for SOC analyst skills.

## 📧 Contact

[@voidst4ck](https://github.com/voidst4ck)

---

**⚠️ Deploy responsibly. Monitor actively. Learn continuously.**