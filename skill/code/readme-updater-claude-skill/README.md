# README Updater - Claude Code SKILL

A Claude Code skill for creating and updating professional README.md files.

## Installation

### In Claude Desktop

1. Copy the `readme-updater-claude-skill` folder to your Claude skills directory
2. Restart Claude or reload skills

### In Claude Code

```bash
# Add this folder to your skills directory
cp -r readme-updater-claude-skill ~/.claude/skills/
```

## Usage

Just ask Claude to work on your README:

```
Create a README for my Python CLI tool
```

```
Update my README with installation and usage sections
```

```
Improve my project's README following best practices
```

```
Add API documentation section to the README
```

## What It Does

The skill will:
- ✅ Analyze your project structure to understand what it does
- ✅ Create properly formatted sections in standard order
- ✅ Include working code examples from your actual code
- ✅ Follow industry best practices for your project type
- ✅ Preserve existing style when updating
- ✅ Add missing sections and fix common issues

## Project Types Supported

- Python packages (pip, poetry, requirements.txt)
- Node.js projects (npm, yarn, package.json)
- CLI tools
- Web applications
- Libraries and frameworks
- Rust crates
- Go modules

## Created

2026-02-11 by Helpful Bob for Master Yang

Based on Claude Code SKILL format from anthropics/skills
