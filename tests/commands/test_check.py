import pytest
from click.testing import CliRunner
from ssl_daily_check.main import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_check_command(runner):
    with patch('ssl_daily_check.main.check_ssl') as mock_check_ssl, \
         patch('ssl_daily_check.main.send_notifications') as mock_send_notifications:
        mock_check_ssl.return_value = [('example.com', 'Example Site', 5)]
        result = runner.invoke(cli, ['check'])
        assert result.exit_code == 0
        assert 'Notifications sent for expired domains.' in result.output
        mock_send_notifications.assert_called_once_with([('example.com', 'Example Site', 5)])
