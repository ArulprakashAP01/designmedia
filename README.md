# 📦 Dependency Update Checker

A command-line tool to check for outdated dependencies in GitHub repositories. This tool supports multiple package managers and provides a clean, formatted output of outdated packages.

## Features

- 🔍 Analyzes any public GitHub repository
- 📊 Clean, formatted output
- 🛠️ Supports multiple package managers:
  - npm (Node.js)
  - pip (Python)
  - composer (PHP)
  - maven (Java)
  - gradle (Java)
  - bundler (Ruby)
  - go modules (Go)
  - cargo (Rust)
  - dotnet (C#/.NET)
- 🚀 Easy to use
- 🔒 Safe temporary directory handling
- ⚡ Fast repository analysis

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/dependency-update-checker
cd dependency-update-checker
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Make sure you have Git installed on your system.

## Usage

Run the script with a GitHub repository URL:
```bash
python check_outdated.py https://github.com/username/repo
```

Example output:
```
🔍 Analyzing repository: https://github.com/username/repo

📦 Found the following package managers:
  - NPM: package.json
  - PIP: requirements.txt

=== NPM Dependencies ===
Package Name                             Current Version      Latest Version       Status              
----------------------------------------------------------------------------------------------------
express                                  4.17.1              4.18.2               Update Available    
lodash                                  4.17.20             4.17.21              Update Available    

=== PIP Dependencies ===
Package Name                             Current Version      Latest Version       Status              
----------------------------------------------------------------------------------------------------
requests                                 2.26.0              2.28.2               Update Available    
flask                                    2.0.1               2.3.3                Update Available    
```

## Requirements

- Python 3.7 or higher
- Git
- Package managers for the languages you want to check:
  - npm for Node.js packages
  - pip for Python packages
  - composer for PHP packages
  - maven for Java packages
  - etc.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all package managers and their communities
- Inspired by various dependency checking tools

## Support

If you encounter any problems or have suggestions, please open an issue in the GitHub repository.
