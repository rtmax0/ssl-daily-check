import click
from .config import ensure_config_files
from .checker import check_ssl
from .database import init_db, add_domain, get_all_domains, delete_domain, get_domain_info
from .notifier import send_notifications
from tabulate import tabulate
from datetime import datetime
import csv

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """SSL Daily Check Tool

    This tool helps you manage and monitor SSL certificates for multiple domains.

    Commands:
    add     Add a new domain to monitor
    list    List all monitored domains
    remove  Remove a domain from monitoring
    check   Check SSL certificates for all domains
    import  Import domains from a CSV file
    """
    ensure_config_files()
    init_db()
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command()
@click.argument('domain', required=True)
def add(domain):
    """Add a new domain to monitor"""
    port = click.prompt("Enter port (default is 443)", default=443, type=int)
    description = click.prompt("Enter description (optional)", default='')
    try:
        add_domain(domain, port, description)
        click.echo(f"Domain {domain} added successfully.")
    except ValueError as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
def list():
    """List all monitored domains"""
    domains = get_all_domains()
    table_data = []
    for domain, port, description, valid_until in domains:
        if valid_until:
            valid_until = datetime.fromisoformat(valid_until)
            days_to_expire = (valid_until - datetime.now()).days
            status = f"Expires in {days_to_expire} days"
        else:
            status = "Not checked yet"
        table_data.append([domain, port, description, status])
    click.echo(tabulate(table_data, headers=["Domain", "Port", "Description", "Status"], tablefmt="grid"))

@cli.command()
@click.argument('domain', required=True)
def remove(domain):
    """Remove a domain from monitoring"""
    domain_info = get_domain_info(domain)
    if domain_info:
        _, port, description, _, _, valid_until = domain_info
        if valid_until:
            days_to_expire = (valid_until - datetime.now()).days
            status = f"Expires in {days_to_expire} days"
        else:
            status = "Not checked yet"
        click.echo(f"Domain: {domain}")
        click.echo(f"Port: {port}")
        click.echo(f"Description: {description}")
        click.echo(f"Status: {status}")
        if click.confirm("Are you sure you want to remove this domain?"):
            delete_domain(domain)
            click.echo(f"Domain {domain} removed successfully.")
    else:
        click.echo(f"Domain {domain} not found.")

@cli.command()
def check():
    """Check SSL certificates for all domains"""
    expired_domains = check_ssl()
    if expired_domains:
        send_notifications(expired_domains)
        click.echo("Notifications sent for expired domains.")
    else:
        click.echo("No expired domains found.")

@cli.command(name='import')
@click.argument('csv_file', type=click.Path(exists=True))
def import_domains(csv_file):
    """Import domains from a CSV file"""
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            if len(row) >= 3:
                domain, port, description = row[0], int(row[1]), row[2]
            elif len(row) == 2:
                domain, port, description = row[0], int(row[1]), ''
            else:
                domain, port, description = row[0], 443, ''
            
            try:
                add_domain(domain, port, description)
                click.echo(f"Domain {domain} added successfully.")
            except ValueError as e:
                click.echo(f"Error adding {domain}: {str(e)}")

if __name__ == "__main__":
    cli()