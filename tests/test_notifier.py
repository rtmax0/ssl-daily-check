import pytest
from unittest.mock import patch, MagicMock
from ssl_daily_check.notifier import send_notifications, send_qyweixin_notification

@pytest.fixture
def mock_load_notify_rules():
    with patch('ssl_daily_check.notifier.load_notify_rules') as mock:
        mock.return_value = [
            {
                "id": "notify1",
                "type": "qyweixin",
                "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key"
            }
        ]
        yield mock

@pytest.fixture
def mock_requests_post():
    with patch('ssl_daily_check.notifier.requests.post') as mock:
        mock.return_value = MagicMock(status_code=200)
        yield mock

def test_send_notifications(mock_load_notify_rules, mock_requests_post):
    expired_domains = [
        ('example.com', 'Example Site', 10),
        ('test.com', 'Test Site', 5)
    ]

    send_notifications(expired_domains)

    mock_requests_post.assert_called_once()
    args, kwargs = mock_requests_post.call_args
    assert args[0] == "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key"
    assert "example.com" in kwargs['json']['text']['content']
    assert "test.com" in kwargs['json']['text']['content']

def test_send_qyweixin_notification(mock_requests_post):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key"
    expired_domains = [
        ('example.com', 'Example Site', 10),
        ('test.com', 'Test Site', 5)
    ]

    send_qyweixin_notification(webhook_url, expired_domains)

    mock_requests_post.assert_called_once()
    args, kwargs = mock_requests_post.call_args
    assert args[0] == webhook_url
    assert "example.com" in kwargs['json']['text']['content']
    assert "test.com" in kwargs['json']['text']['content']
