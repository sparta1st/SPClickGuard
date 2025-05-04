# 🖱️ ClickGuard

**ClickGuard** is an advanced Windows-based click monitoring tool for personal and educational use. It detects unnatural clicking patterns such as autoclickers, jitterclicks, and butterfly clicks with high precision, while also identifying suspicious background software.

---

## 🔍 Features

- ✅ Real-time click monitoring with CPS (Clicks Per Second)
- 🚨 Detects:
  - Jitterclicking
  - Butterfly clicking
  - Autoclickers and macro patterns
- 🔐 Encrypted and hidden local logging (Fernet AES)
- 📤 Sends a full report to a Discord webhook on shutdown
- 🧠 Identifies constant timing intervals or known macro delays
- 🖥️ Includes PC name and public IP in the final report
- 🛑 Exits cleanly using the `F8` key
- 🕵️ Lists suspicious background processes (ex: `razer`, `xmouse`, `autohotkey`)

---

## 🛡️ Security

All logs are encrypted and saved to a hidden file in the system using a fixed encryption key (`SPARTA.1st`) for local-only usage. This ensures privacy and tamper protection.

---

## ⚙️ How to Use

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ClickGuard.git
