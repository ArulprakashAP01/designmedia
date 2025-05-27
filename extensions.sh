#!/bin/bash

# Function to clone the GitHub repository
clone_repo() {
    REPO_URL=$1
    REPO_NAME=$(basename "$REPO_URL" .git)

    if [ -d "$REPO_NAME" ]; then
        echo "Repository $REPO_NAME already exists, pulling latest changes..."
        cd $REPO_NAME && git pull
    else
        echo "Cloning repository $REPO_URL..."
        git clone $REPO_URL
    fi
    cd $REPO_NAME
}

# Function to detect programming language based on common dependency files
detect_language() {
    LANGUAGES=()

    if [ -f "package.json" ]; then
        LANGUAGES+=("JavaScript/Node.js")
    fi
    if [ -f "requirements.txt" ] || [ -f "Pipfile" ]; then
        LANGUAGES+=("Python")
    fi
    if [ -f "pom.xml" ]; then
        LANGUAGES+=("Java (Maven)")
    fi
    if [ -f "Gemfile" ]; then
        LANGUAGES+=("Ruby")
    fi
    if [ -f "composer.json" ]; then
        LANGUAGES+=("PHP")
    fi
    if [ -f "go.mod" ]; then
        LANGUAGES+=("Go")
    fi
    if [ -f "Cargo.toml" ]; then
        LANGUAGES+=("Rust")
    fi
    if [ -f ".csproj" ] || [ -f ".sln" ]; then
        LANGUAGES+=(".NET")
    fi

    if [ ${#LANGUAGES[@]} -eq 0 ]; then
        echo "No recognized dependency files found. Could not detect languages."
        exit 1
    else
        echo "Detected the following languages in the repository:"
        for LANG in "${LANGUAGES[@]}"; do
            echo "  - $LANG"
        done
    fi
}

# Function to run the corresponding outdated command based on detected language
check_outdated() {
    LANGUAGES=$1

    for LANG in $LANGUAGES; do
        case $LANG in
            "JavaScript/Node.js")
                echo -e "\nChecking for outdated Node.js plugins..."
                npm outdated --long | awk 'NR>1 { 
                    if ($2 != $3) { 
                        printf "%-40s %-20s %-20s %-20s\n", $1, $2, $3, $4;
                        print $1 " is outdated!";
                    }
                }'
                ;;
            "Python")
                echo -e "\nChecking for outdated Python libraries..."
                pip list --outdated | awk 'NR>2 { 
                    if ($2 != $3) { 
                        printf "%-40s %-20s %-20s\n", $1, $2, $3;
                        print $1 " is outdated!";
                    }
                }'
                ;;
            "Java (Maven)")
                echo -e "\nChecking for outdated Java dependencies (Maven)..."
                mvn versions:display-dependency-updates | grep "The following dependencies are outdated:" -A 10 | awk '
                /outdated/ { 
                    print $1 " is outdated!";
                }'
                ;;
            "Ruby")
                echo -e "\nChecking for outdated Ruby gems..."
                bundle outdated | awk 'NR>1 { 
                    if ($2 != $3) { 
                        printf "%-40s %-20s %-20s %-20s\n", $1, $2, $3, $4;
                        print $1 " is outdated!";
                    }
                }'
                ;;
            "PHP")
                echo -e "\nChecking for outdated PHP plugins..."
                composer outdated --direct | awk 'NR>1 { 
                    if ($2 != $3) { 
                        printf "%-40s %-20s %-20s %-20s\n", $1, $2, $3, $4;
                        print $1 " is outdated!";
                    }
                }'
                echo -e "\nRunning composer audit to check for security vulnerabilities..."
                composer audit
                ;;
            "Go")
                echo -e "\nChecking for outdated Go modules..."
                go list -u -m all | awk '{ 
                    split($0, a, "@"); 
                    if (a[2] != "latest") { 
                        print $0 " is outdated!";
                    }
                }'
                ;;
            "Rust")
                echo -e "\nChecking for outdated Rust dependencies..."
                cargo outdated | awk 'NR>1 { 
                    if ($2 != $3) { 
                        printf "%-40s %-20s %-20s\n", $1, $2, $3;
                        print $1 " is outdated!";
                    }
                }'
                ;;
            ".NET")
                echo -e "\nChecking for outdated .NET NuGet packages..."
                dotnet list package --outdated | awk 'NR>2 { 
                    if ($2 != $3) { 
                        printf "%-40s %-20s %-20s\n", $1, $2, $3;
                        print $1 " is outdated!";
                    }
                }'
                ;;
            *)
                echo "No outdated plugin/library check for language: $LANG"
                ;;
        esac
    done
}

# Main script logic
if [ -z "$1" ]; then
    echo "Usage: ./check_outdated.sh <GitHub-repo-url>"
    exit 1
fi

REPO_URL=$1

# Step 1: Clone the repository
clone_repo $REPO_URL

# Step 2: Detect the languages used in the repository
detect_language

# Step 3: Check for outdated dependencies based on detected languages
check_outdated "${LANGUAGES[@]}"
