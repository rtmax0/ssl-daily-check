import click
from .config import ensure_config_files
from .checker import check_ssl
from .database import init_db
from .notifier import send_notifications

@click.command()
def main():
    """SSL Checker Tool"""
    ensure_config_files()
    init_db()
    expired_domains = check_ssl()
    if expired_domains:
        send_notifications(expired_domains)
    click.echo("SSL check completed.")

if __name__ == "__main__":
    main()
