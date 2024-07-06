import requests

from ssl_daily_check.config import load_notify_rules

def send_notifications(expired_domains):
    rules = load_notify_rules()
    for rule in rules:
        if rule['type'] == 'qyweixin':
            send_qyweixin_notification(rule['url'], expired_domains)

def send_qyweixin_notification(webhook_url, expired_domains):
    message = "以下域名的SSL证书即将过期:\n"
    for domain, description, days in expired_domains:
        message += f"- {domain} ({description}): {days}天后过期\n"

    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    print(webhook_url)
    response = requests.post(webhook_url, json=data)
    if response.status_code != 200:
        print(f"Failed to send notification: {response.text}")
