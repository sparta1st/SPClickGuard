import time
import psutil
import os
import re
import requests
import socket
from pynput import mouse
from collections import deque
from colorama import init, Fore, Style
from pynput import keyboard
import base64
from cryptography.fernet import Fernet
init(autoreset=True)

# Configurații
WEBHOOK_URL = "YOUR_WEBHOOK"  
CPS_THRESHOLD = 12
CONSTANCY_THRESHOLD = 4
CONSTANCY_DEVIATION_MS = 3
MIN_IMPOSSIBLE_PRECISION = [100.0, 125.0, 133.33, 200.0]
SUSPECT_KEYWORDS = [
    "auto", "macro", "clicker", "tiny", "pulover", "op_", "logitech", "glorious", "bloody",
    "razer", "xmouse", "recorder", "corsair", "steel", "hotkey", "keyran", "binder",
    "clickermann", "ghost", "mouse", "enhanced", "key", "rapid", "autohotkey"
]

click_times = deque(maxlen=20)
click_intervals = deque(maxlen=20)
suspect_logs = []
all_logs = []
last_click = None
special_clicks = []


# Funcții
def remove_ansi_codes(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def get_pc_name():
    return socket.gethostname()

def get_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"


key_source = "SPARTA.1st".ljust(32)[:32].encode()  
KEY = base64.urlsafe_b64encode(key_source)
cipher = Fernet(KEY)

HIDDEN_LOG_PATH = os.path.join(os.getenv("APPDATA"), ".hidden_log.dat")

def log(msg):
    clean = remove_ansi_codes(msg)
    print(msg)
    all_logs.append(clean)

    try:
        encrypted = cipher.encrypt(clean.encode())
        with open(HIDDEN_LOG_PATH, "ab") as f:
            f.write(encrypted + b"\n")
    except Exception as e:
        print(Fore.RED + f"[!] Eroare la scrierea logului criptat: {e}")

def send_webhook_summary():
    pc = get_pc_name()
    ip = get_ip()

    total_clicks = len(all_logs)
    total_suspect = len(suspect_logs)
    total_ok = total_clicks - total_suspect
    total_special = len(special_clicks)

    entries = "\n".join([f"• {log}" for log in suspect_logs[-1000:]]) or "*Nimic suspect.*"
    specials = "\n".join([f"• {line}" for line in special_clicks[-1000:]]) or "*Nimic.*"

    embed = {
        "title": "📊 Raport Clickuri Final",
        "description": (
            f"🖥️ **PC:** {pc}\n"
            f"🌐 **IP:** {ip}\n"
            f"✅ **Clickuri normale:** {total_ok}\n"
            f"❌ **Clickuri suspecte:** {total_suspect}\n"
            f"🔍 **Clickuri speciale:** {total_special}\n\n"
            f"🔁 **Clickuri speciale (jitter/butterfly):**\n{specials}\n\n"
            f"🚨 **Clickuri suspecte:**\n{entries}"
        ),
        "color": 0xffaa00 if special_clicks else (0xff4444 if suspect_logs else 0x00ff88)
    }

    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    except Exception as e:
        print(f"[!] Webhook error: {e}")

def get_suspect_process_name():
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name'].lower()
            if any(k in name for k in SUSPECT_KEYWORDS):
                return name
        except:
            continue
    return "Unknown software"

def calculate_cps():
    if len(click_times) < 2:
        return 0
    duration = click_times[-1] - click_times[0]
    return round((len(click_times) - 1) / duration, 2) if duration > 0 else 0

def is_constant_clicking():
    if len(click_intervals) < CONSTANCY_THRESHOLD:
        return False
    base = round(click_intervals[-1], 2)
    for i in range(1, CONSTANCY_THRESHOLD):
        if abs(round(click_intervals[-i - 1], 2) - base) > CONSTANCY_DEVIATION_MS:
            return False
    return True

def detect_click_type(interval):
    if interval < 60:
        return "jitterclick"
    elif 60 <= interval < 90:
        return "butterfly"
    return None

def on_click(x, y, button, pressed):
    global last_click

    if pressed:
        now = time.time()
        click_times.append(now)

        if last_click:
            interval = (now - last_click) * 1000
            click_intervals.append(interval)
            cps = calculate_cps()
            click_type = detect_click_type(interval)

            if click_type:
                msg = f"[!] {click_type} click | Interval: {round(interval, 2)}ms | CPS: {cps}"
                special_clicks.append(msg)
                log(Fore.YELLOW + msg)

            is_suspect = False
            reason = ""

            if round(interval, 2) in MIN_IMPOSSIBLE_PRECISION:
                is_suspect = True
                reason = "Perfect interval - known macro"
            elif cps > CPS_THRESHOLD:
                is_suspect = True
                reason = f"High CPS: {cps}"
            elif is_constant_clicking():
                is_suspect = True
                reason = "Low CPS but consistent delay"

            if is_suspect:
                proc = get_suspect_process_name()
                msg = f"[SUSPECT] {round(interval,2)}ms | {reason} | Source: {proc}"
                suspect_logs.append(msg)
                log(Fore.RED + msg)
            else:
                log(Fore.GREEN + f"[✓] {round(interval,2)} ms | CPS: {cps}")

        last_click = now

def on_key_press(key):
    if key == keyboard.Key.f8:
        send_webhook_summary()
        os._exit(0)

keyboard.Listener(on_press=on_key_press).start()
# Start monitor
print(Fore.YELLOW + " Monitorizarea a inceput. Apasă f8 pentru a opri.")
try:
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
except KeyboardInterrupt:
    print(Fore.CYAN + "\n Monitorizare oprită.")
    send_webhook_summary()



