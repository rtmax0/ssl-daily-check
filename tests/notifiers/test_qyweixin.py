import pytest
from unittest.mock import patch, MagicMock
from ssl_daily_check.notifiers.qyweixin import QyWeixinNotifier

@pytest.fixture
def mock_requests_post():
    with patch('requests.post') as mock:
        mock.return_value = MagicMock(status_code=200)
        yield mock

def test_qyweixin_send_notification(mock_requests_post):
    notifier = QyWeixinNotifier("https://example.com/webhook")
    expired_domains = [
        ('example.com', 'Example Site', 10),
        ('test.com', 'Test Site', 5)
    ]

    notifier.send_notification(expired_domains)

    mock_requests_post.assert_called_once()
    args, kwargs = mock_requests_post.call_args
    assert args[0] == "https://example.com/webhook"
    assert "example.com" in kwargs['json']['text']['content']
    assert "test.com" in kwargs['json']['text']['content']
