import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from ssl_daily_check.checker import check_ssl, get_ssl_cert

@pytest.fixture
def mock_get_all_domains():
    with patch('ssl_daily_check.checker.get_all_domains') as mock:
        mock.return_value = [
            ('example.com', 443, 'Example Site', None),
            ('test.com', 443, 'Test Site', None)
        ]
        yield mock

@pytest.fixture
def mock_get_domain_info():
    with patch('ssl_daily_check.checker.get_domain_info') as mock:
        mock.return_value = None
        yield mock

@pytest.fixture
def mock_get_ssl_cert():
    with patch('ssl_daily_check.checker.get_ssl_cert') as mock:
        mock.return_value = {
            'notBefore': 'Jan 1 00:00:00 2023 GMT',
            'notAfter': 'Jan 1 00:00:00 2024 GMT'
        }
        yield mock

@pytest.fixture
def mock_save_ssl_check():
    with patch('ssl_daily_check.checker.save_ssl_check') as mock:
        yield mock

def test_check_ssl(mock_get_all_domains, mock_get_domain_info, mock_get_ssl_cert, mock_save_ssl_check):
    with patch('ssl_daily_check.checker.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 12, 20)
        mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(*args, **kw)

        expired_domains = check_ssl()

        assert len(expired_domains) == 2
        assert expired_domains[0][0] == 'example.com'
        assert expired_domains[0][2] == 12  # days to expire
        assert expired_domains[1][0] == 'test.com'
        assert expired_domains[1][2] == 12  # days to expire

def test_get_ssl_cert():
    mock_cert = {'notBefore': 'Jan 1 00:00:00 2023 GMT', 'notAfter': 'Jan 1 00:00:00 2024 GMT'}

    with patch('ssl_daily_check.checker.socket.create_connection') as mock_connection:
        mock_sock = MagicMock()
        mock_connection.return_value = mock_sock

        with patch('ssl_daily_check.checker.ssl.create_default_context') as mock_context:
            mock_secure_sock = MagicMock()
            mock_secure_sock.getpeercert.return_value = mock_cert
            mock_context.return_value.wrap_socket.return_value.__enter__.return_value = mock_secure_sock

            cert = get_ssl_cert('example.com', 443)

            assert cert == mock_cert
            assert cert['notBefore'] == 'Jan 1 00:00:00 2023 GMT'
            assert cert['notAfter'] == 'Jan 1 00:00:00 2024 GMT'
