import pytest
from click.testing import CliRunner
from ssl_daily_check.main import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "SSL Daily Check Tool" in result.output
    assert "add" in result.output
    assert "list" in result.output
    assert "remove" in result.output
    assert "check" in result.output

def test_add_command(runner):
    with patch('ssl_daily_check.main.add_domain') as mock_add_domain:
        result = runner.invoke(cli, ['add', 'example.com'], input='443\nExample Site\n')
        assert result.exit_code == 0
        assert 'Domain example.com added successfully.' in result.output
        mock_add_domain.assert_called_once_with('example.com', 443, 'Example Site')

def test_list_command(runner):
    with patch('ssl_daily_check.main.get_all_domains') as mock_get_all_domains:
        mock_get_all_domains.return_value = [
            ('example.com', 443, 'Example Site', '2024-01-01T00:00:00')
        ]
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert 'example.com' in result.output
        assert '443' in result.output
        assert 'Example Site' in result.output

def test_remove_command(runner):
    with patch('ssl_daily_check.main.get_domain_info') as mock_get_domain_info, \
         patch('ssl_daily_check.main.delete_domain') as mock_delete_domain:
        mock_get_domain_info.return_value = ('example.com', 443, 'Example Site', None, None, None)
        result = runner.invoke(cli, ['remove', 'example.com'], input='y\n')
        assert result.exit_code == 0
        assert 'Domain example.com removed successfully.' in result.output
        mock_delete_domain.assert_called_once_with('example.com')

def test_check_command(runner):
    with patch('ssl_daily_check.main.check_ssl') as mock_check_ssl, \
         patch('ssl_daily_check.main.send_notifications') as mock_send_notifications:
        mock_check_ssl.return_value = [('example.com', 'Example Site', 5)]
        result = runner.invoke(cli, ['check'])
        assert result.exit_code == 0
        assert 'Notifications sent for expired domains.' in result.output
        mock_send_notifications.assert_called_once_with([('example.com', 'Example Site', 5)])
