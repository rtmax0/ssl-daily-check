import sqlite3
import os
import json
import re
from datetime import datetime

DB_FILE = os.path.expanduser("~/.ssl-daily-check/data.db")
DOMAINS_JSON = os.path.expanduser("~/.ssl-daily-check/domains.json")

def init_db():
    """Initialize the SQLite database with necessary tables."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Create domains table
    c.execute('''CREATE TABLE IF NOT EXISTS domains
                 (domain TEXT PRIMARY KEY, port INTEGER, description TEXT)''')

    # Create SSL checks table with DATETIME type for time fields
    c.execute('''CREATE TABLE IF NOT EXISTS ssl_checks
                 (domain TEXT PRIMARY KEY,
                  check_time DATETIME,
                  valid_from DATETIME,
                  valid_until DATETIME,
                  FOREIGN KEY(domain) REFERENCES domains(domain))''')

    conn.commit()
    conn.close()

def is_valid_domain(domain):
    """Check if the given domain is valid."""
    pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    return re.match(pattern, domain) is not None

def add_domain(domain, port, description):
    """Add a new domain to the database."""
    if not is_valid_domain(domain):
        raise ValueError("Invalid domain name")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO domains (domain, port, description) VALUES (?, ?, ?)",
              (domain, port, description))
    conn.commit()
    conn.close()
    update_domains_json()

def get_all_domains():
    """Retrieve all domains from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT d.domain, d.port, d.description, s.valid_until FROM domains d LEFT JOIN ssl_checks s ON d.domain = s.domain")
    domains = c.fetchall()
    conn.close()
    return domains

def delete_domain(domain):
    """Delete a domain from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM domains WHERE domain = ?", (domain,))
    c.execute("DELETE FROM ssl_checks WHERE domain = ?", (domain,))
    conn.commit()
    conn.close()
    update_domains_json()

def update_domains_json():
    """Update the domains.json file with current database content."""
    domains = get_all_domains()
    domain_list = [{"domain": d[0], "port": d[1], "description": d[2]} for d in domains]
    with open(DOMAINS_JSON, 'w') as f:
        json.dump(domain_list, f, indent=2)

def save_ssl_check(domain, valid_from, valid_until):
    """Save SSL check results to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO ssl_checks
                 (domain, check_time, valid_from, valid_until)
                 VALUES (?, ?, ?, ?)''',
              (domain, datetime.now().isoformat(), valid_from.isoformat(), valid_until.isoformat()))
    conn.commit()
    conn.close()

def get_domain_info(domain):
    """Retrieve information for a specific domain."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT d.domain, d.port, d.description, s.check_time, s.valid_from, s.valid_until FROM domains d LEFT JOIN ssl_checks s ON d.domain = s.domain WHERE d.domain = ?", (domain,))
    result = c.fetchone()
    conn.close()
    if result:
        return (result[0], result[1], result[2],
                datetime.fromisoformat(result[3]) if result[3] else None,
                datetime.fromisoformat(result[4]) if result[3] else None,
                datetime.fromisoformat(result[5]) if result[5] else None)
    return None

def get_expiring_domains(days):
    """Retrieve domains with SSL certificates expiring within the specified number of days."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT d.domain, d.description, s.valid_until
        FROM domains d
        JOIN ssl_checks s ON d.domain = s.domain
        WHERE s.valid_until <= date('now', '+' || ? || ' days')
    ''', (days,))
    expiring_domains = c.fetchall()
    conn.close()
    return expiring_domains
