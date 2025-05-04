# 🛡️ ClickGuard - Advanced Click Behavior Monitor

Welcome to **ClickGuard**, a powerful and privacy-conscious tool designed to detect abnormal mouse activity such as autoclickers, jitterclicks, butterfly clicks, and scripted macros.

ClickGuard is ideal for gamers, developers, and curious tinkerers who want to analyze click behavior, test hardware, or investigate external input automation — all while ensuring your logs are encrypted, hidden, and optionally reported via Discord webhooks.

## 🚀 Features

- 🔍 **Real-time Click Monitoring** – Tracks click intervals, CPS (Clicks Per Second), and patterns.
- ⚠️ **Suspicious Behavior Detection** – Identifies:
  - Abnormally high CPS
  - Consistent click delays (potential macro usage)
  - Common automation intervals (e.g., 100.0 ms)
  - Special clicking patterns like *butterfly* and *jitterclick*
- 🔐 **Encrypted and Hidden Logs** – All logs are encrypted using a custom key (`SPARTA.1st`) and stored in a hidden file under `%APPDATA%`.
- 🌐 **Webhook Integration** – Summarized logs are sent via Discord webhook with machine name, IP address, and suspicious data.
- 🧪 **Offline Analysis Ready** – Log files can be decrypted and reviewed later.
- 🔒 **Keybind Controlled** – Application exit is triggered using `F8` to prevent accidental termination.

## 📝 Requirements

- Python 3.8+
- Modules:
  - `pynput`
  - `colorama`
  - `psutil`
  - `cryptography`
  - `requests`

## ▶️ How to Run

```bash
python bot.py
```

To build an executable:

```bash
pyinstaller --onefile --noconsole --icon=icon.ico bot.py
```

## 📁 Encrypted Logs

Logs are saved in:
```
%APPDATA%\.hidden_log.dat
```

To decrypt logs, use the same `SPARTA.1st` key with the included decryptor script.

## 🤖 Disclaimer

> This tool is intended **for educational, personal testing, and debugging purposes only.**  
> Any misuse for violating terms of service, spying, or cheating in games is strongly discouraged.

## 📥 License

MIT License – you're free to use, modify, and distribute, with proper credit.
