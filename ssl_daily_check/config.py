import os
import json

CONFIG_DIR = os.path.expanduser("~/.ssl-daily-check")
DOMAINS_FILE = os.path.join(CONFIG_DIR, "domains.txt")
NOTIFY_RULE_FILE = os.path.join(CONFIG_DIR, "notify-rule.json")

EXPIRY_THRESHOLD_DAYS = 15

def ensure_config_files():
    os.makedirs(CONFIG_DIR, exist_ok=True)

    if not os.path.exists(DOMAINS_FILE):
        with open(DOMAINS_FILE, "w") as f:
            f.write("# Add your domains here\n")

    if not os.path.exists(NOTIFY_RULE_FILE):
        default_rule = [
            {
                "id": "notify1",
                "type": "qyweixin",
                "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key-here"
            }
        ]
        with open(NOTIFY_RULE_FILE, "w") as f:
            json.dump(default_rule, f, indent=2)

def load_domains():
    with open(DOMAINS_FILE, "r") as f:
        return [line.strip().split(":") for line in f if line.strip() and not line.startswith("#")]

def load_notify_rules():
    with open(NOTIFY_RULE_FILE, "r") as f:
        return json.load(f)
