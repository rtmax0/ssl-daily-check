# Changelog

All notable changes to this project will be documented in this file.

## [0.2.1] - 2024-07-18

### Added
- New 'export' command to export domains to a CSV file
- 'import' command to import domains from a CSV file
- Unit tests for both import and export functionalities
- Updated README.md with information about new commands

### Changed
- Refactored main.py to include new import and export commands
- Updated CLI help text to include new commands

## [0.2.0] - 2024-07-13

### Added
- New 'remove' command to replace 'delete' command
- Help text for CLI commands

### Changed
- Refactored main.py to include new 'remove' command and help text
- Updated README.md with new command structure and usage instructions

### Fixed
- Various issues in database and config modules
- Improved overall test coverage and error handling

## [0.1.1] - 2024-06-15

### Added
- Initial release of SSL Daily Check tool
- Basic CLI interface with add, list, and delete commands
- SSL certificate checking functionality
- SQLite database for storing domain information
- WeChat Work notification system for expiring certificates
- Configuration file support for notify rules
