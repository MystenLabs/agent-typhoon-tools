#!/bin/bash

# Check if repos.txt exists
if [ ! -f "repos.txt" ]; then
    echo "Error: repos.txt file not found"
    exit 1
fi

# Create/clear private_repos.txt
> private_repos.txt

# Read each line from repos.txt
while IFS= read -r repo; do
    # Skip empty lines
    [ -z "$repo" ] && continue
    
    echo "Checking repository: $repo"
    
    # Extract repo name from URL
    repo_name=$(basename "$repo" .git)
    
    # Check if repo is private by attempting to get info without authentication
    if ! git ls-remote --heads "$repo" &>/dev/null; then
        echo "$repo" >> private_repos.txt
        echo "Repository $repo is private"
        echo "Skipping clone for private repository"
        echo "----------------------------------------"
        continue
    fi
    
    # Check if repo already exists locally
    if [ -d "$repo_name" ]; then
        echo "Repository $repo_name already exists locally"
    else
        echo "Cloning repository $repo"
        if git clone "$repo" 2>/dev/null; then
            echo "Successfully cloned $repo"
        else
            echo "Failed to clone $repo"
        fi
    fi
    
    echo "----------------------------------------"
done < repos.txt

echo "Process completed!"
echo "Private repositories have been logged to private_repos.txt"

