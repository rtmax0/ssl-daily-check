import pytest
import os
from datetime import datetime, timedelta
from ssl_daily_check.database import (
    init_db, add_domain, get_all_domains, delete_domain,
    get_domain_info, get_expiring_domains, is_valid_domain,
)
from ssl_daily_check import database

@pytest.fixture
def temp_db(tmp_path):
    test_config_dir = tmp_path / '.ssl-daily-check'
    test_config_dir.mkdir(parents=True, exist_ok=True)

    original_db_file = database.DB_FILE
    original_domains_json = database.DOMAINS_JSON

    database.DB_FILE = str(test_config_dir / 'data.db')
    database.DOMAINS_JSON = str(test_config_dir / 'domains.json')

    yield

    database.DB_FILE = original_db_file
    database.DOMAINS_JSON = original_domains_json

def test_init_db(temp_db):
    init_db()
    assert os.path.exists(database.DB_FILE)

def test_add_and_get_domain(temp_db):
    init_db()
    add_domain("example.com", 443, "Example Site")
    domains = get_all_domains()
    assert len(domains) == 1
    assert domains[0][0] == "example.com"
    assert domains[0][1] == 443
    assert domains[0][2] == "Example Site"

def test_delete_domain(temp_db):
    init_db()
    add_domain("example.com", 443, "Example Site")
    delete_domain("example.com")
    domains = get_all_domains()
    assert len(domains) == 0

def test_get_domain_info(temp_db):
    init_db()
    add_domain("example.com", 443, "Example Site")
    info = get_domain_info("example.com")
    assert info[0] == "example.com"
    assert info[1] == 443
    assert info[2] == "Example Site"

def test_get_expiring_domains(temp_db):
    init_db()
    add_domain("example.com", 443, "Example Site")
    # Simulate an SSL check
    from ssl_daily_check.database import save_ssl_check
    valid_from = datetime.now()
    valid_until = datetime.now() + timedelta(days=10)
    save_ssl_check("example.com", valid_from, valid_until)

    expiring = get_expiring_domains(15)
    assert len(expiring) == 1
    assert expiring[0][0] == "example.com"

def test_is_valid_domain():
    assert is_valid_domain("example.com")
    assert is_valid_domain("sub.example.com")
    assert not is_valid_domain("invalid")
    assert not is_valid_domain("invalid.com.")
    assert not is_valid_domain(".invalid.com")

def test_domains_json_update(temp_db):
    init_db()
    add_domain("example.com", 443, "Example Site")
    assert os.path.exists(database.DOMAINS_JSON)
    with open(database.DOMAINS_JSON, 'r') as f:
        content = f.read()
        assert "example.com" in content
        assert "443" in content
        assert "Example Site" in content
