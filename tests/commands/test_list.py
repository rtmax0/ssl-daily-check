import pytest
from click.testing import CliRunner
from ssl_daily_check.main import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

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
