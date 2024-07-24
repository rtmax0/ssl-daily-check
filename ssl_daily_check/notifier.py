from .notifiers.qyweixin import QyWeixinNotifier
from .config import load_notify_rules

def get_notifier(rule):
    if rule['type'] == 'qyweixin':
        return QyWeixinNotifier(rule['url'])  # Changed 'webhook_url' to 'url'
    else:
        raise ValueError(f"Unsupported notifier type: {rule['type']}")

def send_notifications(expired_domains):
    rules = load_notify_rules()
    for rule in rules:
        notifier = get_notifier(rule)
        notifier.send_notification(expired_domains)
