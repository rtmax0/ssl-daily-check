import requests
from .base import BaseNotifier

class QyWeixinNotifier(BaseNotifier):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_notification(self, expired_domains):
        message = "以下域名的SSL证书即将过期:\n"
        for domain, description, days in expired_domains:
            message += f"- {domain} ({description}): {days}天后过期\n"

        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        response = requests.post(self.webhook_url, json=data)
        if response.status_code != 200:
            print(f"Failed to send notification: {response.text}")
