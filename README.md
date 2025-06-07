# GitHub Dependency Version Checker

This GitHub Action automatically checks for outdated dependencies in your pull requests and provides a detailed report as a PR comment.

## Features

- 🔍 Automatically detects multiple package managers in your repository
- 📦 Currently supports:
  - NPM (package.json)
  - Python (requirements.txt)
  - More package managers coming soon!
- 💬 Posts results directly as a PR comment
- ⚡ Runs automatically on PR creation and updates
- 🎯 Clear visual indicators for outdated packages

## Setup

1. Add this GitHub Action to your repository by creating the following file structure:
   ```
   .github/
   ├── workflows/
   │   └── dependency-check.yml
   └── scripts/
       └── check_dependencies.py
   ```

2. The action will automatically run on all pull requests.

3. You can also manually trigger the action using the "Actions" tab in your GitHub repository.

## Example Output

The action will comment on your PR with a table like this:

### NPM Dependencies
| Package | Current Version | Latest Version | Status |
|---------|----------------|----------------|--------|
| react | 17.0.2 | 18.2.0 | ⚠️ Update Available |
| typescript | 4.5.4 | 4.5.4 | ✅ Up to date |

### Python Dependencies
| Package | Current Version | Latest Version | Status |
|---------|----------------|----------------|--------|
| requests | 2.26.0 | 2.31.0 | ⚠️ Update Available |
| pytest | 7.1.1 | 7.1.1 | ✅ Up to date |

## Permissions

The action requires the following permissions:
- `pull-requests: write` - To comment on pull requests
- `contents: read` - To read repository contents

These permissions are automatically configured in the workflow file.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests to add support for more package managers or improve existing functionality. 