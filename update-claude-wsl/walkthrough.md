# Walkthrough: WSL2 Claude Code Update Script

I have implemented a Bash script to manage updates for Claude Code on WSL2. This script checks your current version against the latest version available on npm and performs an update if necessary.

## Changes Made

### Update Script
- Created [update-claude.sh](file:///h:/code/yl/claude-notes/update-claude.sh) in the workspace.
- Added logic to check for `node` and `npm` dependencies.
- Added version comparison logic using `npm list` and `npm info`.
- Added a `--dry-run` flag for safe verification of the script's logic.

## Verification Results

### Logic Verification (Dry Run)
I verified the script's logic by running it with the `--dry-run` flag.

**Command:**
```bash
wsl ./update-claude.sh --dry-run
```

**Output:**
```text
Running in DRY RUN mode. No changes will be made.
Checking for Claude Code updates...
Claude Code is not currently installed.
Fetching latest version from npm...
Latest version:  2.1.49
Installing @anthropic-ai/claude-code@latest...
[DRY RUN] Would execute: sudo npm install -g @anthropic-ai/claude-code@latest
```

## How to Use

1. **Open your WSL2 terminal.**
2. **Navigate to the workspace:**
   ```bash
   cd /mnt/h/code/yl/claude-notes
   ```
3. **Run the script:**
   ```bash
   ./update-claude.sh
   ```
   *Note: The script uses `sudo` for the global npm installation, so you may be prompted for your WSL password.*

4. **Verify installation:**
   ```bash
   claude --version
   ```
