# SSL Checker

SSL Checker is a Python-based tool that monitors SSL certificates for specified domains and sends notifications when certificates are nearing expiration.

## Features

- Checks SSL certificates for multiple domains
- Stores certificate information in a SQLite database
- Sends notifications via WeChat Work (企业微信) when certificates are close to expiration
- Configurable through simple text files
- Designed to run as a cron job on Linux systems

## Requirements

- Python 3.8+
- Poetry for dependency management

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ssl-checker.git
   cd ssl-checker
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Configuration

1. Create a `~/.ssl-checker/domains.txt` file with the domains you want to monitor:
   ```
   example.com:Example Website
   yourdomain.com:Your Website
   ```

2. Create a `~/.ssl-checker/notify-rule.json` file with your WeChat Work webhook URL:
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

Run the SSL Checker manually:

```
poetry run ssl-checker
```

To set up automatic checking, add a cron job:

```
0 0 * * * /path/to/your/poetry/environment/bin/ssl-checker
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
