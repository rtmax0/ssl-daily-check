# SSL Daily Check

SSL Daily Check is a Python-based tool that monitors SSL certificates for specified domains and sends notifications when certificates are nearing expiration.

## Features

- Checks SSL certificates for multiple domains
- Stores domain and certificate information in a SQLite database
- Sends notifications via WeChat Work (企业微信) when certificates are close to expiration
- Configurable through JSON files
- Provides command-line interface for managing domains
- Designed to run as a cron job on Linux systems
- Supports importing domains from a CSV file

## Requirements

- Python 3.8+
- Poetry for dependency management

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ssl-daily-check.git
   cd ssl-daily-check
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Configuration

Create a `~/.ssl-daily-check/notify-rule.json` file with your WeChat Work webhook URL:
```json
[
  {
    "id": "notify1",
    "type": "qyweixin",
    "url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key-here"
  }
]
```

## Usage

The SSL Daily Check tool provides several commands:

```
Usage: ssl-daily-check [OPTIONS] COMMAND [ARGS]...

  SSL Daily Check Tool

  This tool helps you manage and monitor SSL certificates for multiple domains.

Commands:
  add     Add a new domain to monitor
  list    List all monitored domains
  remove  Remove a domain from monitoring
  check   Check SSL certificates for all domains
  import  Import domains from a CSV file
```

1. Add a new domain:
   ```
   poetry run ssl-daily-check add example.com
   ```

2. List all monitored domains:
   ```
   poetry run ssl-daily-check list
   ```

3. Remove a domain:
   ```
   poetry run ssl-daily-check remove example.com
   ```

4. Check SSL certificates:
   ```
   poetry run ssl-daily-check check
   ```

5. Import domains from a CSV file:
   ```
   poetry run ssl-daily-check import domains.csv
   ```
   
   The CSV file should have the following format:
   ```
   domain,port,description
   example.com,443,Example website
   example.org,8443,Another example
   ```
   
   The 'port' and 'description' fields are optional. If not provided, the default port (443) will be used, and the description will be left empty.

To set up automatic checking, add a cron job:

```
0 0 * * * /path/to/your/poetry/environment/bin/ssl-daily-check check
```

This will run the SSL Checker daily at midnight.

## Development

This project uses:
- Poetry for dependency management
- Black for code formatting
- Flake8 for linting
- Pytest for testing

To set up the development environment:

1. Install development dependencies:
   ```
   poetry install --dev
   ```

2. Run tests:
   ```
   poetry run pytest
   ```

3. Format code:
   ```
   poetry run black .
   ```

4. Run linter:
   ```
   poetry run flake8
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.