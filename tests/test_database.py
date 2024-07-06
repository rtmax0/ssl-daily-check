import os
import pytest
from datetime import datetime, timedelta
from ssl_daily_check.database import init_db, save_to_db, get_domain_info, DB_FILE

@pytest.fixture
def temp_db(tmp_path):
    original_db_file = DB_FILE
    os.environ['HOME'] = str(tmp_path)
    yield
    os.environ['HOME'] = original_db_file

def test_init_db(temp_db):
    init_db()
    assert os.path.exists(DB_FILE)

def test_save_and_get_domain_info(temp_db):
    init_db()
    domain = "example.com"
    description = "Example Site"
    valid_from = datetime.now()
    valid_until = datetime.now() + timedelta(days=30)

    save_to_db(domain, description, valid_from, valid_until)

    info = get_domain_info(domain)
    assert info is not None
    assert info[0] == domain
    assert info[1] == description
    assert isinstance(info[2], datetime)  # check_time
    assert info[3] == valid_from
    assert info[4] == valid_until
