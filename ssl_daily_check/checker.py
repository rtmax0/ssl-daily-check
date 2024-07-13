import ssl
import socket
from datetime import datetime, timedelta
from .config import EXPIRY_THRESHOLD_DAYS
from .database import get_all_domains, get_domain_info, save_ssl_check

def check_ssl():
    """
    Check SSL certificates for all domains in the database.

    Returns:
    list: A list of tuples containing information about expired or soon-to-expire domains.
    """
    domains = get_all_domains()
    expired_domains = []
    for domain, port, description, _ in domains:
        domain_info = get_domain_info(domain)
        if domain_info:
            _, _, _, _, _, valid_until = domain_info
            if valid_until and datetime.now() + timedelta(days=EXPIRY_THRESHOLD_DAYS) < valid_until:
                continue  # Skip SSL check if expiration is more than EXPIRY_THRESHOLD_DAYS days away

        try:
            cert = get_ssl_cert(domain, port)
            valid_from = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
            valid_until = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            days_to_expire = (valid_until - datetime.now()).days

            save_ssl_check(domain, valid_from, valid_until)

            if days_to_expire <= EXPIRY_THRESHOLD_DAYS:
                expired_domains.append((domain, description, days_to_expire))
        except Exception as e:
            print(f"Error checking {domain}: {str(e)}")

    return expired_domains

def get_ssl_cert(domain, port):
    """
    Retrieve the SSL certificate for a given domain and port.

    Args:
    domain (str): The domain to check.
    port (int): The port to connect to.

    Returns:
    dict: A dictionary containing the certificate information.
    """
    context = ssl.create_default_context()
    with socket.create_connection((domain, port)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
            return secure_sock.getpeercert()
