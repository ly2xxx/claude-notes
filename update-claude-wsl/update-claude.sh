#!/bin/bash

# Configuration
PACKAGE_NAME="@anthropic-ai/claude-code"
DRY_RUN=false

if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "Running in DRY RUN mode. No changes will be made."
fi

echo "Checking for Claude Code updates..."

# Check for node/npm
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js/npm first."
    exit 1
fi

# Get current version
CURRENT_VERSION=$(npm list -g $PACKAGE_NAME --depth=0 2>/dev/null | grep $PACKAGE_NAME | cut -d'@' -f3)

if [ -z "$CURRENT_VERSION" ]; then
    echo "Claude Code is not currently installed."
else
    echo "Current version: $CURRENT_VERSION"
fi

# Get latest version
echo "Fetching latest version from npm..."
LATEST_VERSION=$(npm info $PACKAGE_NAME version)

if [ -z "$LATEST_VERSION" ]; then
    echo "Error: Could not fetch latest version from npm."
    exit 1
fi

echo "Latest version:  $LATEST_VERSION"

# Compare and update
if [ "$CURRENT_VERSION" == "$LATEST_VERSION" ]; then
    echo "Claude Code is already up to date."
else
    if [ -z "$CURRENT_VERSION" ]; then
        echo "Installing $PACKAGE_NAME@latest..."
    else
        echo "Updating $PACKAGE_NAME to $LATEST_VERSION..."
    fi
    
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would execute: sudo npm install -g $PACKAGE_NAME@latest"
        exit 0
    fi
    
    sudo npm install -g "$PACKAGE_NAME@latest"
    
    if [ $? -eq 0 ]; then
        echo "Update successful!"
        claude --version
    else
        echo "Update failed. Please check permissions or network connection."
        exit 1
    fi
fi
