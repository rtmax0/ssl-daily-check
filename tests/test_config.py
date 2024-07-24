import os
import json
import pytest
from ssl_daily_check import config
from ssl_daily_check.config import (
    ensure_config_files, load_notify_rules, save_domains_to_json,
    load_domains_from_json
)

@pytest.fixture
def temp_config_dir(tmp_path):
    test_config_dir = tmp_path / '.ssl-daily-check'
    test_config_dir.mkdir(parents=True, exist_ok=True)

    original_config_dir = config.CONFIG_DIR
    original_notify_rule_file = config.NOTIFY_RULE_FILE
    original_domains_json = config.DOMAINS_JSON

    config.CONFIG_DIR = str(test_config_dir)
    config.NOTIFY_RULE_FILE = str(test_config_dir / 'notify-rule.json')
    config.DOMAINS_JSON = str(test_config_dir / 'domains.json')

    yield

    config.CONFIG_DIR = original_config_dir
    config.NOTIFY_RULE_FILE = original_notify_rule_file
    config.DOMAINS_JSON = original_domains_json

def test_ensure_config_files(temp_config_dir):
    ensure_config_files()
    assert os.path.exists(config.NOTIFY_RULE_FILE)
    assert os.path.exists(config.DOMAINS_JSON)

def test_load_notify_rules(temp_config_dir):
    ensure_config_files()
    rules = load_notify_rules()
    assert isinstance(rules, list)
    assert len(rules) == 1
    assert rules[0]['id'] == 'notify1'
    assert rules[0]['type'] == 'qyweixin'
    assert 'webhook_url' in rules[0]

def test_save_and_load_domains_json(temp_config_dir):
    ensure_config_files()
    domains = [
        {"domain": "example.com", "port": 443, "description": "Example Site"},
        {"domain": "test.com", "port": 443, "description": "Test Site"}
    ]
    save_domains_to_json(domains)

    loaded_domains = load_domains_from_json()
    assert loaded_domains == domains

def test_load_domains_from_json_empty(temp_config_dir):
    ensure_config_files()
    # Ensure the file is empty
    with open(config.DOMAINS_JSON, 'w') as f:
        json.dump([], f)
    domains = load_domains_from_json()
    assert domains == []

def test_load_domains_from_json_nonexistent(temp_config_dir):
    # Ensure the file doesn't exist
    if os.path.exists(config.DOMAINS_JSON):
        os.remove(config.DOMAINS_JSON)
    domains = load_domains_from_json()
    assert domains == []
