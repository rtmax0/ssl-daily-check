import pytest
from click.testing import CliRunner
from ssl_daily_check.main import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_remove_command(runner):
    with patch('ssl_daily_check.main.get_domain_info') as mock_get_domain_info, \
         patch('ssl_daily_check.main.delete_domain') as mock_delete_domain:
        mock_get_domain_info.return_value = ('example.com', 443, 'Example Site', None, None, None)
        result = runner.invoke(cli, ['remove', 'example.com'], input='y\n')
        assert result.exit_code == 0
        assert 'Domain example.com removed successfully.' in result.output
        mock_delete_domain.assert_called_once_with('example.com')
