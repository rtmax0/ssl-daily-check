import pytest
from click.testing import CliRunner
from ssl_daily_check.main import cli

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
    assert "import" in result.output
