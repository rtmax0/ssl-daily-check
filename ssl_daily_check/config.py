import os
import json

CONFIG_DIR = os.path.expanduser("~/.ssl-daily-check")
NOTIFY_RULE_FILE = os.path.join(CONFIG_DIR, "notify-rule.json")
DOMAINS_JSON = os.path.join(CONFIG_DIR, "domains.json")

EXPIRY_THRESHOLD_DAYS = 15

def ensure_config_files():
    """Ensure that necessary configuration files exist."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

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

    if not os.path.exists(DOMAINS_JSON):
        with open(DOMAINS_JSON, "w") as f:
            json.dump([], f, indent=2)

def load_notify_rules():
    """Load notification rules from the configuration file."""
    with open(NOTIFY_RULE_FILE, "r") as f:
        return json.load(f)

def save_domains_to_json(domains):
    """Save the list of domains to the JSON file."""
    with open(DOMAINS_JSON, "w") as f:
        json.dump(domains, f, indent=2)

def load_domains_from_json():
    """Load the list of domains from the JSON file."""
    if os.path.exists(DOMAINS_JSON):
        with open(DOMAINS_JSON, "r") as f:
            return json.load(f)
    return []
