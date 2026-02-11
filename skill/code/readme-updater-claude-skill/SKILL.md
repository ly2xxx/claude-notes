---
name: readme-updater
description: Create, update, or enhance project README.md files with proper structure and documentation best practices. Use when user asks to create a new README, update an existing README, improve documentation, add missing sections, or restructure README content.
version: 1.0
license: MIT
---

# README Updater

Professional README.md creation and enhancement following industry best practices.

## Instructions

### 1. Assess Current State

**If README.md exists:**
- Read the entire file
- Identify existing sections
- Note missing or incomplete content
- Check for outdated information

**If no README exists:**
- Examine project files (package.json, requirements.txt, pyproject.toml, etc.)
- Determine project type (library, CLI tool, web app, framework)
- Identify key features from source code

### 2. Gather Essential Information

Collect before writing:
- **Installation method**: pip, npm, git clone, cargo, etc.
- **Dependencies**: Required software and minimum versions
- **Basic usage**: Minimal working example from actual code
- **Key features**: Main capabilities (from code/config)
- **Configuration**: Environment variables, config files
- **License**: From LICENSE file or user specification

### 3. Write/Update Content

Follow these principles:
- **30-second rule**: User should understand the project in 30 seconds
- **Show, don't tell**: Code examples > lengthy descriptions
- **Imperative voice**: "Run `npm install`" not "You should run npm install"
- **Present tense**: "This tool processes..." not "will process"
- **Copy-pasteable**: All commands should run as-is

### 4. Standard README Structure

Use this section order (adjust for project type):

1. **Title & one-line description** (always first)
2. **Demo/Screenshot** (if applicable - especially for UIs/CLIs)
3. **Features** (bullet list - key capabilities only)
4. **Installation** (step-by-step with prerequisites)
5. **Quick Start** (minimal working example)
6. **Usage** (common use cases with code)
7. **Configuration** (if applicable)
8. **API Documentation** (for libraries)
9. **Development** (for contributors)
10. **License** (always include)

### 5. Project-Specific Patterns

**For Libraries/Packages:**
```markdown
## Installation
\`\`\`bash
pip install package-name
\`\`\`

## Quick Start
\`\`\`python
from package import main_function

result = main_function("input")
print(result)  # Output: expected result
\`\`\`

## API
### `main_function(input: str) -> str`
Description of what it does.

**Parameters:**
- `input` (str): Description of input

**Returns:**
- str: Description of return value
```

**For CLI Tools:**
```markdown
## Installation
\`\`\`bash
pip install tool-name
\`\`\`

## Usage
\`\`\`bash
# Basic usage
tool-name input.txt

# With options
tool-name input.txt --output result.txt --format json
\`\`\`

### Options
- `--output, -o`: Specify output file
- `--format, -f`: Output format (json|csv|txt)
```

**For Web Applications:**
```markdown
## Quick Start

\`\`\`bash
# Clone and install
git clone https://github.com/user/app.git
cd app
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run development server
npm run dev
\`\`\`

Visit http://localhost:3000

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `DATABASE_URL` | Database connection | Required |
```

### 6. Quality Checks

Before finishing, verify:
- [ ] Project name and description are clear
- [ ] Installation steps are complete and testable
- [ ] At least one working code example included
- [ ] All code examples use correct syntax highlighting
- [ ] Links are valid (especially to LICENSE, docs)
- [ ] Minimum version requirements specified (Python 3.8+, Node 16+, etc.)
- [ ] License information included

### 7. Common Improvements

When updating existing READMEs, look for:
- **Outdated dependencies**: Update version requirements
- **Broken examples**: Fix code that no longer works
- **Missing badges**: Add if appropriate (build status, version, license)
- **Unclear installation**: Add prerequisite steps
- **No examples**: Add working code samples
- **Dead links**: Update or remove
- **Inconsistent formatting**: Standardize code blocks and headings

## Examples

### Minimal README (for simple scripts):
```markdown
# Project Name

One-line description of what this does.

## Installation

\`\`\`bash
pip install project-name
\`\`\`

## Usage

\`\`\`python
from project import function
result = function()
\`\`\`

## License

MIT
```

### Full README (for complex projects):
Includes all sections from Standard Structure above with detailed examples.

## Tips

- **Match existing style**: When updating, preserve the project's tone
- **Use badges sparingly**: Only add meaningful ones (build status, version, license)
- **Include screenshots**: For UIs, CLIs with visual output, or complex workflows
- **Link to full docs**: Keep README concise, link to detailed documentation
- **Show realistic examples**: Use actual use cases, not toy examples
- **Update regularly**: When features change, update README same time

## When Not to Include

Avoid these in README:
- Changelog (use CHANGELOG.md)
- Detailed API docs (link to full docs)
- Every single feature (highlight key ones only)
- Implementation details (save for architecture docs)
- Personal blog-style content (keep professional)
