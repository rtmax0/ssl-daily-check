import sqlite3
import os
from datetime import datetime, timedelta

DB_FILE = os.path.expanduser("~/.ssl-checker/data.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ssl_checks
                 (domain TEXT PRIMARY KEY, description TEXT, check_time TEXT,
                  valid_from TEXT, valid_until TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(domain, description, valid_from, valid_until):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO ssl_checks
                 (domain, description, check_time, valid_from, valid_until)
                 VALUES (?, ?, ?, ?, ?)''',
              (domain, description, datetime.now().isoformat(),
               valid_from.isoformat(), valid_until.isoformat()))
    conn.commit()
    conn.close()

def get_domain_info(domain):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM ssl_checks WHERE domain = ?", (domain,))
    result = c.fetchone()
    conn.close()
    if result:
        return (result[0], result[1],
                datetime.fromisoformat(result[2]),
                datetime.fromisoformat(result[3]),
                datetime.fromisoformat(result[4]))
    return None
