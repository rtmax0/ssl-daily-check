import pytest
import tempfile
import csv
from click.testing import CliRunner
from ssl_daily_check.main import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_import_command(runner):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        csv_writer = csv.writer(temp_file)
        csv_writer.writerow(['Domain', 'Port', 'Description'])
        csv_writer.writerow(['example.com', '443', 'Example Site'])
        csv_writer.writerow(['test.com', '8443', 'Test Site'])
        temp_file_name = temp_file.name

    with patch('ssl_daily_check.main.add_domain') as mock_add_domain:
        result = runner.invoke(cli, ['import', temp_file_name])
        assert result.exit_code == 0
        assert 'Domain example.com added successfully.' in result.output
        assert 'Domain test.com added successfully.' in result.output
        mock_add_domain.assert_any_call('example.com', 443, 'Example Site')
        mock_add_domain.assert_any_call('test.com', 8443, 'Test Site')
        assert mock_add_domain.call_count == 2
