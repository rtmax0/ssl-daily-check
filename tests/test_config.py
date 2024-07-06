import os
import json
import pytest
from ssl_daily_check.config import ensure_config_files, load_domains, load_notify_rules, CONFIG_DIR, DOMAINS_FILE, NOTIFY_RULE_FILE

@pytest.fixture
def temp_config_dir(tmp_path):
    original_config_dir = CONFIG_DIR
    os.environ['HOME'] = str(tmp_path)
    yield
    os.environ['HOME'] = original_config_dir

def test_ensure_config_files(temp_config_dir):
    ensure_config_files()
    assert os.path.exists(DOMAINS_FILE)
    assert os.path.exists(NOTIFY_RULE_FILE)

def test_load_domains(temp_config_dir):
    with open(DOMAINS_FILE, 'w') as f:
        f.write("example.com:Example Site\n")
        f.write("# comment\n")
        f.write("test.com:Test Site\n")

    domains = load_domains()
    assert domains == [
        ['example.com', 'Example Site'],
        ['test.com', 'Test Site']
    ]

def test_load_notify_rules(temp_config_dir):
    rules = [
        {
            "id": "notify1",
            "type": "qyweixin",
            "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key"
        }
    ]
    with open(NOTIFY_RULE_FILE, 'w') as f:
        json.dump(rules, f)

    loaded_rules = load_notify_rules()
    assert loaded_rules == rules
