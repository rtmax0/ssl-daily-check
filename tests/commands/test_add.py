import pytest
from click.testing import CliRunner
from ssl_daily_check.main import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_add_command(runner):
    with patch('ssl_daily_check.main.add_domain') as mock_add_domain:
        result = runner.invoke(cli, ['add', 'example.com'], input='443\nExample Site\n')
        assert result.exit_code == 0
        assert 'Domain example.com added successfully.' in result.output
        mock_add_domain.assert_called_once_with('example.com', 443, 'Example Site')
