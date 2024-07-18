import pytest
import tempfile
import csv
import os
from click.testing import CliRunner
from ssl_daily_check.main import cli
from unittest.mock import patch

@pytest.fixture
def runner():
    return CliRunner()

def test_export_command(runner):
    with patch('ssl_daily_check.main.get_all_domains') as mock_get_all_domains:
        mock_get_all_domains.return_value = [
            ('example.com', 443, 'Example Site', None),
            ('test.com', 8443, 'Test Site', None)
        ]
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
            temp_file_name = temp_file.name

        result = runner.invoke(cli, ['export', temp_file_name])
        assert result.exit_code == 0
        assert f'Domains exported to {temp_file_name} successfully.' in result.output

        with open(temp_file_name, 'r') as f:
            csv_reader = csv.reader(f)
            rows = list(csv_reader)
            assert rows[0] == ['Domain', 'Port', 'Description']
            assert rows[1] == ['example.com', '443', 'Example Site']
            assert rows[2] == ['test.com', '8443', 'Test Site']

        os.unlink(temp_file_name)
