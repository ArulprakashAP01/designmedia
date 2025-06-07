#!/usr/bin/env python3

import os
import sys
import subprocess
import re
import json
import tempfile
from typing import List, Dict
from pathlib import Path
import shutil
import requests
import flask
from urllib.parse import urlparse

def is_git_available() -> bool:
    """Check if git is available in the system PATH."""
    return shutil.which('git') is not None

def validate_github_url(url: str) -> tuple:
    """Validate and extract information from GitHub URL."""
    try:
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL format")
        owner = path_parts[0]
        repo = path_parts[1]
        return owner, repo
    except Exception as e:
        print(f"Error parsing GitHub URL: {str(e)}")
        sys.exit(1)

def clone_repo(repo_url: str, temp_dir: str) -> None:
    """Clone or update a GitHub repository in a temporary directory."""
    if not is_git_available():
        print("Error: Git is not installed or not found in system PATH.")
        print("Please install Git from https://git-scm.com/downloads and ensure it's added to your system PATH.")
        sys.exit(1)

    print(f"\n🔍 Analyzing repository: {repo_url}")
    try:
        subprocess.run(['git', 'clone', '--depth', '1', repo_url, temp_dir], 
                      check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        sys.exit(1)

def detect_package_managers(temp_dir: str) -> Dict[str, str]:
    """Detect package managers based on dependency files."""
    package_files = {
        'package.json': 'npm',
        'requirements.txt': 'pip',
        'Pipfile': 'pipenv',
        'composer.json': 'composer',
        'pom.xml': 'maven',
        'build.gradle': 'gradle',
        'Gemfile': 'bundler',
        'go.mod': 'go',
        'Cargo.toml': 'cargo',
        '*.csproj': 'dotnet'
    }

    found_managers = {}
    
    for file_pattern, manager in package_files.items():
        if '*' in file_pattern:
            # Handle glob patterns
            matches = list(Path(temp_dir).rglob(file_pattern.replace('*', '*')))
            if matches:
                found_managers[manager] = str(matches[0])
        else:
            file_path = os.path.join(temp_dir, file_pattern)
            if os.path.exists(file_path):
                found_managers[manager] = file_path

    return found_managers

def parse_npm_dependencies(package_json_path: str) -> Dict:
    """Parse NPM dependencies from package.json."""
    try:
        with open(package_json_path, 'r') as f:
            data = json.load(f)
        deps = {}
        deps.update(data.get('dependencies', {}))
        deps.update(data.get('devDependencies', {}))
        return deps
    except Exception as e:
        print(f"Error parsing package.json: {e}")
        return {}

def parse_python_requirements(requirements_path: str) -> Dict:
    """Parse Python requirements from requirements.txt."""
    deps = {}
    try:
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle different requirement formats
                    if '==' in line:
                        name, version = line.split('==')
                        deps[name] = version
                    elif '>=' in line:
                        name, version = line.split('>=')
                        deps[name] = version
                    else:
                        deps[line] = "Not specified"
    except Exception as e:
        print(f"Error parsing requirements.txt: {e}")
    return deps

def check_outdated_packages(temp_dir: str, package_managers: Dict[str, str]) -> None:
    """Check for outdated packages based on detected package managers."""
    for manager, file_path in package_managers.items():
        try:
            print(f"\n=== {manager.upper()} Dependencies ===")
            print_package_header()
            
            if manager == 'npm':
                result = subprocess.run(['npm', 'outdated', '--json'], 
                                     cwd=temp_dir, capture_output=True, text=True)
                if result.stdout.strip():
                    packages = json.loads(result.stdout)
                    for pkg, info in packages.items():
                        current = info.get('current', 'N/A')
                        latest = info.get('latest', 'N/A')
                        print_package_info(pkg, current, latest)

            elif manager == 'pip':
                # First install requirements
                subprocess.run(['pip', 'install', '-r', file_path], capture_output=True)
                result = subprocess.run(['pip', 'list', '--outdated', '--format=json'],
                                     capture_output=True, text=True)
                if result.stdout.strip():
                    packages = json.loads(result.stdout)
                    for pkg in packages:
                        name = pkg['name']
                        current = pkg['version']
                        latest = pkg['latest_version']
                        print_package_info(name, current, latest)

            elif manager == 'composer':
                result = subprocess.run(['composer', 'outdated', '--direct', '--format=json'],
                                     cwd=temp_dir, capture_output=True, text=True)
                if result.stdout.strip():
                    data = json.loads(result.stdout)
                    for pkg in data.get('installed', []):
                        name = pkg.get('name', '')
                        current = pkg.get('version', '')
                        latest = pkg.get('latest', '')
                        print_package_info(name, current, latest)

            # Add more package manager checks as needed

        except subprocess.CalledProcessError as e:
            print(f"\nError checking {manager} packages: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected error checking {manager} packages: {str(e)}")

def print_package_header():
    """Print the header for package information."""
    header = "{:<40} {:<20} {:<20} {:<20}".format(
        "Package Name", "Current Version", "Latest Version", "Status"
    )
    print("\n" + header)
    print("-" * 100)

def print_package_info(name: str, current: str, latest: str, wanted: str = None):
    """Print package information in a consistent format."""
    status = "Update Available" if current != latest else "Up to date"
    
    # Ensure consistent formatting for version numbers
    current_ver = current if current != "N/A" else "-"
    latest_ver = latest if latest != "N/A" else "-"
    
    # Format the line with proper spacing
    line = "{:<40} {:<20} {:<20} {:<20}".format(
        name[:39],  # Limit package name length
        current_ver,
        latest_ver,
        status
    )
    print(line)

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_outdated.py <GitHub-repo-url>")
        print("Example: python check_outdated.py https://github.com/username/repo")
        sys.exit(1)

    repo_url = sys.argv[1]
    owner, repo = validate_github_url(repo_url)
    
    # Create a temporary directory for cloning
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Clone the repository
            clone_repo(repo_url, temp_dir)
            
            # Detect package managers
            package_managers = detect_package_managers(temp_dir)
            
            if not package_managers:
                print("\n⚠️ No recognized dependency files found in the repository.")
                sys.exit(0)
            
            print("\n📦 Found the following package managers:")
            for manager, file_path in package_managers.items():
                print(f"  - {manager.upper()}: {os.path.basename(file_path)}")
            
            # Check for outdated packages
            check_outdated_packages(temp_dir, package_managers)
            
        except Exception as e:
            print(f"\n❌ Error analyzing repository: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main() 
 if not package_managers:
                print("\n⚠️ No recognized dependency files found in the repository.")
                sys.exit(0)
