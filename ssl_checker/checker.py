import ssl
import socket
from datetime import datetime, timedelta
from .config import load_domains
from .database import save_to_db, get_domain_info

def check_ssl():
    domains = load_domains()
    expired_domains = []
    for domain, description in domains:
        domain_info = get_domain_info(domain)
        if domain_info:
            _, _, _, _, valid_until = domain_info
            valid_until = datetime.fromisoformat(valid_until)
            if valid_until - datetime.now() > timedelta(days=15):
                continue  # Skip SSL check if expiration is more than 15 days away

        try:
            cert = get_ssl_cert(domain)
            valid_from = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
            valid_until = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            days_to_expire = (valid_until - datetime.now()).days

            save_to_db(domain, description, valid_from, valid_until)

            if days_to_expire <= 15:
                expired_domains.append((domain, description, days_to_expire))
        except Exception as e:
            print(f"Error checking {domain}: {str(e)}")

    return expired_domains

def get_ssl_cert(domain):
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
            return secure_sock.getpeercert()
