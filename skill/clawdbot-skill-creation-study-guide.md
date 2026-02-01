# Clawdbot Skill Creation Study Guide

**Created:** 2026-02-01  
**Goal:** Master creating custom Skills for Clawdbot (SKILL.md format)  
**Time:** 60-75 minutes  

---

## 📋 What You'll Learn

1. What Clawdbot Skills are and why they matter
2. Skill anatomy (SKILL.md + resources)
3. Progressive disclosure pattern
4. The 6-step creation process
5. Real-world examples
6. Best practices and common patterns
7. Hands-on: Build your first skill

---

## 🎯 Part 1: Core Concepts (10 min)

### What Are Clawdbot Skills?

**Skills** = Modular packages that extend Clawdbot's capabilities with specialized knowledge, workflows, and tools.

**Think of them as:** "Onboarding guides" for specific domains or tasks.

**Without skills:**
- Clawdbot relies on general knowledge
- Repeats the same research every time
- No access to domain-specific tools
- No reusable workflows

**With skills:**
- Domain expertise loaded on demand
- Bundled scripts execute reliably
- Workflows guide multi-step processes
- Reference docs available when needed

**Example:**
- User: "What's the weather in London?"
- Without skill: Clawdbot has no way to fetch weather
- With `weather` skill: Clawdbot uses curl + wttr.in API automatically

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for file formats, APIs, systems
3. **Domain expertise** - Company knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, assets for complex tasks

**Key insight:** Skills transform Clawdbot from generalist → specialist when needed.

---

## 🏗️ Part 2: Skill Anatomy (15 min)

### Required Structure

Every skill has this structure:

```
skill-name/
├── SKILL.md          (REQUIRED)
│   ├── YAML frontmatter (name, description)
│   └── Markdown body (instructions)
└── Bundled Resources (OPTIONAL)
    ├── scripts/      - Executable code (Python, Bash, etc.)
    ├── references/   - Docs loaded on demand
    └── assets/       - Files used in output (templates, icons)
```

### SKILL.md (Required)

Every SKILL.md contains:

**1. YAML Frontmatter** (required):
```yaml
---
name: skill-name
description: What this skill does and WHEN to use it
---
```

**2. Markdown Body** (required):
- Instructions for using the skill
- How to use bundled resources
- Workflows and examples

**Example - Weather Skill:**
```markdown
---
name: weather
description: Get current weather and forecasts (no API key required).
---

# Weather

Two free services, no API keys needed.

## wttr.in (primary)

Quick one-liner:
\```bash
curl -s "wttr.in/London?format=3"
# Output: London: ⛅️ +8°C
\```

Format codes: `%c` condition · `%t` temp · `%h` humidity
```

### Bundled Resources (Optional)

#### 1. Scripts (`scripts/`)

**Purpose:** Executable code for deterministic, repeatable tasks

**When to include:**
- Same code is rewritten repeatedly
- Deterministic reliability needed
- Complex operations (image processing, PDF manipulation)

**Example:**
```
pdf-editor/
└── scripts/
    ├── rotate_pdf.py
    ├── merge_pdfs.py
    └── extract_text.py
```

**Usage in SKILL.md:**
```markdown
## Rotating PDFs

Use the bundled script:
\```bash
python scripts/rotate_pdf.py input.pdf output.pdf --angle 90
\```
```

**Benefits:**
- Token efficient (execute without loading into context)
- Deterministic (same inputs → same outputs)
- Reusable (tested once, works everywhere)

#### 2. References (`references/`)

**Purpose:** Documentation loaded on demand to inform Clawdbot's thinking

**When to include:**
- Database schemas
- API documentation
- Company policies
- Domain knowledge
- Detailed workflow guides

**Example:**
```
bigquery-skill/
└── references/
    ├── schema.md         - Database tables/relationships
    ├── finance.md        - Revenue, billing metrics
    ├── sales.md          - Opportunities, pipeline
    └── marketing.md      - Campaigns, attribution
```

**Usage in SKILL.md:**
```markdown
## Querying User Data

For table schemas, see [schema.md](references/schema.md)

For finance-specific queries, see [finance.md](references/finance.md)
```

**Benefits:**
- Keeps SKILL.md lean
- Loaded only when needed
- Avoids context window bloat

**Best practice:** If files are large (>10k words), include grep search patterns in SKILL.md

#### 3. Assets (`assets/`)

**Purpose:** Files used in output (not loaded into context)

**When to include:**
- Templates (HTML, React, PowerPoint)
- Brand assets (logos, icons, fonts)
- Boilerplate code
- Sample documents

**Example:**
```
frontend-builder/
└── assets/
    ├── templates/
    │   ├── react-app/      - React boilerplate
    │   └── html-template/  - Static HTML
    ├── logo.png
    └── fonts/
```

**Usage in SKILL.md:**
```markdown
## Creating a New App

Copy the React template:
\```bash
cp -r assets/templates/react-app ./my-new-app
cd my-new-app && npm install
\```
```

**Benefits:**
- Separates output resources from docs
- Clawdbot uses files without loading them
- Faster, more efficient

---

## 🧠 Part 3: Progressive Disclosure Pattern (10 min)

### The Three-Level Loading System

Skills use progressive disclosure to manage context efficiently:

**Level 1: Metadata (Always loaded)**
- Name + description (~100 words)
- Clawdbot reads this to decide IF skill applies

**Level 2: SKILL.md body (When skill triggers)**
- Loaded only after skill is selected (<5k words)
- Core workflows and instructions

**Level 3: Bundled resources (As needed)**
- Loaded only when Clawdbot determines they're needed
- Unlimited size (scripts can execute without reading)

**Example Flow:**

```
User: "What's the weather in London?"
  ↓
Level 1: Clawdbot scans all skill descriptions
         → "weather: Get current weather..." ✓ MATCH
  ↓
Level 2: Load weather SKILL.md body
         → Instructions: Use wttr.in with curl
  ↓
Execute: curl -s "wttr.in/London?format=3"
  ↓
Result: "London: ⛅️ +8°C"
```

### Why This Matters

**Without progressive disclosure:**
- All skill docs loaded always = context bloat
- Slow, expensive, hits token limits

**With progressive disclosure:**
- Only relevant content loaded
- Fast, efficient, scalable

**Key principle:** Keep SKILL.md lean (<500 lines). Split content into references when approaching this limit.

---

## 🛠️ Part 4: The 6-Step Creation Process (20 min)

### Step 1: Understand with Concrete Examples

**Goal:** Clearly understand how the skill will be used

**Questions to ask:**
- What functionality should this skill support?
- Can you give examples of how it would be used?
- What would trigger this skill?

**Example - Image Editor Skill:**
- "Remove red-eye from this image"
- "Rotate this image 90 degrees"
- "Crop this photo to 1:1 ratio"

**Output:** Clear list of use cases

### Step 2: Plan Reusable Contents

**Goal:** Identify scripts, references, and assets to include

**For each example, ask:**
1. How would I execute this from scratch?
2. What would make this easier when repeating?

**Example - PDF Editor Skill:**

| Use Case | Resource Needed |
|----------|----------------|
| "Rotate this PDF" | `scripts/rotate_pdf.py` |
| "Merge these PDFs" | `scripts/merge_pdfs.py` |
| "Extract text from PDF" | `scripts/extract_text.py` |

**Example - BigQuery Skill:**

| Use Case | Resource Needed |
|----------|----------------|
| "How many users logged in today?" | `references/schema.md` (table definitions) |
| "Show revenue by region" | `references/finance.md` (metrics guide) |

**Output:** List of scripts/, references/, assets/ to create

### Step 3: Initialize the Skill

**Goal:** Create skill directory with proper structure

**Command:**
```bash
scripts/init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets] [--examples]
```

**Examples:**
```bash
# Basic skill
scripts/init_skill.py weather-helper --path ./skills

# With scripts and references
scripts/init_skill.py pdf-tools --path ./skills --resources scripts,references

# With example files
scripts/init_skill.py my-skill --path ./skills --resources scripts --examples
```

**What it creates:**
```
skill-name/
├── SKILL.md (with TODO placeholders)
└── [optional directories based on --resources flag]
```

**Note:** If you use `--examples`, delete placeholder files you don't need.

### Step 4: Edit the Skill

**Goal:** Implement scripts/references/assets and write SKILL.md

#### 4a. Create Bundled Resources

**Start with scripts:**
```python
# scripts/rotate_pdf.py
import sys
from PyPDF2 import PdfReader, PdfWriter

def rotate_pdf(input_path, output_path, angle=90):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        page.rotate(angle)
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)

if __name__ == "__main__":
    rotate_pdf(sys.argv[1], sys.argv[2], int(sys.argv[3]))
```

**Test your scripts!** Actually run them to ensure they work.

**Create references:**
```markdown
# references/schema.md

## Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR | User email |
| created_at | TIMESTAMP | Registration date |

## Queries

### Active users today:
\```sql
SELECT COUNT(*) FROM users
WHERE DATE(last_login_at) = CURRENT_DATE
\```
```

**Add assets:**
```
assets/
└── templates/
    └── react-app/
        ├── package.json
        ├── src/
        │   └── App.jsx
        └── public/
            └── index.html
```

#### 4b. Write SKILL.md

**Frontmatter (critical for triggering):**
```yaml
---
name: pdf-tools
description: Comprehensive PDF manipulation including rotation, merging, splitting, and text extraction. Use when working with PDF files for: (1) Rotating pages, (2) Merging multiple PDFs, (3) Splitting PDFs, (4) Extracting text or metadata.
---
```

**Description best practices:**
- Include WHAT the skill does
- Include WHEN to use it (specific triggers)
- Be comprehensive (this is what Clawdbot reads to decide)
- Don't include "when to use" in the body (loaded after triggering!)

**Body structure:**
```markdown
# PDF Tools

Bundled scripts for reliable PDF operations.

## Rotating PDFs

Use the bundled script:
\```bash
python scripts/rotate_pdf.py input.pdf output.pdf 90
\```

Angles: 90, 180, 270 (clockwise)

## Merging PDFs

\```bash
python scripts/merge_pdfs.py output.pdf file1.pdf file2.pdf file3.pdf
\```

## Advanced: Custom Operations

For complex workflows, see [advanced.md](references/advanced.md)
```

**Writing guidelines:**
- Use imperative form ("Use the script", not "You should use")
- Be concise (assume Clawdbot is smart)
- Provide examples over explanations
- Link to references for details

### Step 5: Package the Skill

**Goal:** Create distributable .skill file

**Command:**
```bash
scripts/package_skill.py <path/to/skill-folder>

# Optional: specify output directory
scripts/package_skill.py <path/to/skill-folder> ./dist
```

**What it does:**
1. **Validates:**
   - YAML frontmatter format
   - Required fields (name, description)
   - Naming conventions
   - Directory structure
   - File organization

2. **Packages:**
   - Creates `skill-name.skill` file (zip with .skill extension)
   - Includes all files
   - Maintains directory structure

**If validation fails:**
- Fix errors
- Run packaging again
- Repeat until successful

**Output:**
```
dist/
└── pdf-tools.skill  (ready to share!)
```

### Step 6: Iterate

**Goal:** Improve based on real usage

**Workflow:**
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify improvements needed
4. Implement changes
5. Test again
6. Package updated version

**Common iterations:**
- Add missing examples
- Create new reference docs
- Improve script error handling
- Clarify ambiguous instructions
- Add more bundled resources

---

## 💡 Part 5: Real-World Examples (15 min)

### Example 1: Simple Skill (No Bundled Resources)

**Use case:** Weather lookups

**Structure:**
```
weather/
└── SKILL.md
```

**SKILL.md:**
```markdown
---
name: weather
description: Get current weather and forecasts (no API key required).
---

# Weather

Two free services, no API keys needed.

## wttr.in (primary)

Quick one-liner:
\```bash
curl -s "wttr.in/London?format=3"
# Output: London: ⛅️ +8°C
\```

Full forecast:
\```bash
curl -s "wttr.in/London?T"
\```

Format codes: `%c` condition · `%t` temp · `%h` humidity

## Open-Meteo (fallback, JSON)

\```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
\```
```

**Why no bundled resources?** The curl commands are simple enough to include inline.

### Example 2: Medium Skill (Scripts)

**Use case:** PDF manipulation

**Structure:**
```
pdf-tools/
├── SKILL.md
└── scripts/
    ├── rotate_pdf.py
    ├── merge_pdfs.py
    └── extract_text.py
```

**SKILL.md:**
```markdown
---
name: pdf-tools
description: PDF manipulation including rotation, merging, and text extraction. Use when working with PDF files.
---

# PDF Tools

## Rotating PDFs

\```bash
python scripts/rotate_pdf.py input.pdf output.pdf 90
\```

## Merging PDFs

\```bash
python scripts/merge_pdfs.py output.pdf file1.pdf file2.pdf
\```

## Extracting Text

\```bash
python scripts/extract_text.py input.pdf output.txt
\```
```

**Why scripts?** Same PDF operations repeated often, deterministic reliability needed.

### Example 3: Complex Skill (All Resources)

**Use case:** Company-specific BigQuery analytics

**Structure:**
```
company-analytics/
├── SKILL.md
├── scripts/
│   ├── run_query.py
│   └── export_csv.py
├── references/
│   ├── schema.md          - Database structure
│   ├── finance.md         - Revenue metrics
│   ├── sales.md           - Sales queries
│   └── product.md         - Product analytics
└── assets/
    └── templates/
        └── dashboard.html
```

**SKILL.md:**
```markdown
---
name: company-analytics
description: Query company BigQuery datasets for finance, sales, and product analytics. Use when analyzing company data, generating reports, or answering business questions about users, revenue, or products.
---

# Company Analytics

## Schema Overview

For complete table schemas, see [schema.md](references/schema.md)

## Domain-Specific Queries

- **Finance metrics**: See [finance.md](references/finance.md)
- **Sales pipeline**: See [sales.md](references/sales.md)
- **Product usage**: See [product.md](references/product.md)

## Running Queries

\```bash
python scripts/run_query.py --query "SELECT * FROM users LIMIT 10"
\```

## Exporting Results

\```bash
python scripts/export_csv.py --query-file query.sql --output report.csv
\```

## Creating Dashboards

Copy the template:
\```bash
cp assets/templates/dashboard.html ./my-dashboard.html
\```
```

**Why all resource types?**
- Scripts: Reliable query execution
- References: Domain knowledge (schemas, metrics)
- Assets: Dashboard templates for output

---

## 🎓 Part 6: Best Practices (10 min)

### 1. Concise is Key

**❌ Bad:**
```markdown
This skill provides comprehensive functionality for working with PDF files. It includes
various utilities and helper scripts that can be used in multiple different scenarios when
you need to perform operations on PDF documents such as rotating pages, merging files,
or extracting text content. The skill uses the PyPDF2 library which is a robust and
well-tested Python library for PDF manipulation...
```

**✅ Good:**
```markdown
# PDF Tools

Bundled scripts for PDF manipulation.

## Rotate
\```bash
python scripts/rotate_pdf.py input.pdf output.pdf 90
\```
```

**Why:** Assume Clawdbot is smart. Only provide what it doesn't already know.

### 2. Write Clear Descriptions

**The description is your PRIMARY triggering mechanism!**

**❌ Bad:**
```yaml
description: PDF tools
```

**✅ Good:**
```yaml
description: PDF manipulation including rotation, merging, splitting, and text extraction. Use when working with PDF files for: (1) Rotating pages, (2) Merging multiple PDFs, (3) Splitting documents, (4) Extracting text.
```

**Include:**
- What the skill does
- When to use it (specific triggers)
- Key capabilities

### 3. Progressive Disclosure

**Keep SKILL.md under 500 lines. Split into references when approaching limit.**

**Pattern:**
```markdown
# Main Skill Instructions

Quick start guide here...

## Advanced Topics

For detailed workflows, see:
- [Complex Queries](references/advanced-queries.md)
- [Performance Tuning](references/performance.md)
- [Error Handling](references/errors.md)
```

Clawdbot loads references only when needed.

### 4. Organize Multi-Domain Skills

**For skills with multiple variants:**

```
cloud-deploy/
├── SKILL.md (overview + provider selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

When user chooses AWS, only aws.md is loaded.

### 5. Test Your Scripts

**Always test scripts before packaging:**

```bash
# Test rotation
python scripts/rotate_pdf.py test.pdf output.pdf 90
# Verify output.pdf is rotated correctly

# Test merging
python scripts/merge_pdfs.py merged.pdf file1.pdf file2.pdf
# Verify merged.pdf contains both files
```

### 6. Use Imperative Form

**❌ Wrong:**
```markdown
You should use the rotate script when you want to rotate a PDF.
```

**✅ Right:**
```markdown
Rotate PDFs:
\```bash
python scripts/rotate_pdf.py input.pdf output.pdf 90
\```
```

### 7. Avoid Extraneous Files

**DO NOT include:**
- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- QUICK_REFERENCE.md

**Only include files Clawdbot needs to do the job.**

### 8. Skill Naming Conventions

**Rules:**
- Lowercase letters, digits, hyphens only
- Under 64 characters
- Descriptive, verb-led ("pdf-tools", not "pdfs")
- Namespace by tool when needed ("gh-pr-review", "linear-issue-tracker")

**Examples:**
- ✅ `weather-lookup`
- ✅ `pdf-editor`
- ✅ `gh-pr-review`
- ❌ `Weather Lookup` (no caps/spaces)
- ❌ `pdf` (too vague)

---

## 🚀 Part 7: Hands-On Exercise (20 min)

### Build Your First Skill: Calculator

**Goal:** Create a simple calculator skill with Python script

#### Step 1: Initialize

```bash
scripts/init_skill.py calculator --path ./my-skills --resources scripts
```

#### Step 2: Create the Script

**Create `scripts/calc.py`:**
```python
import sys
import operator

ops = {
    'add': operator.add,
    'subtract': operator.sub,
    'multiply': operator.mul,
    'divide': operator.truediv
}

operation = sys.argv[1]
a = float(sys.argv[2])
b = float(sys.argv[3])

result = ops[operation](a, b)
print(f"{a} {operation} {b} = {result}")
```

**Test it:**
```bash
python scripts/calc.py multiply 15 23
# Output: 15.0 multiply 23.0 = 345.0
```

#### Step 3: Write SKILL.md

```markdown
---
name: calculator
description: Performs basic arithmetic operations (add, subtract, multiply, divide). Use when calculations are needed.
---

# Calculator

Bundled script for reliable arithmetic.

## Usage

\```bash
python scripts/calc.py <operation> <number1> <number2>
\```

Operations: `add`, `subtract`, `multiply`, `divide`

## Examples

\```bash
python scripts/calc.py add 10 5
# 10.0 add 5.0 = 15.0

python scripts/calc.py multiply 15 23
# 15.0 multiply 23.0 = 345.0
\```
```

#### Step 4: Package

```bash
scripts/package_skill.py ./my-skills/calculator
```

#### Step 5: Test

Install the skill in Clawdbot and try:
- "What's 123 times 456?"
- "Add 789 and 321"

Clawdbot should use your calculator skill!

---

## 📚 Quick Reference

### Skill Structure Template

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter
│   │   ├── name: skill-name
│   │   └── description: What + When
│   └── Markdown body
└── Optional resources
    ├── scripts/        - Executable code
    ├── references/     - Docs loaded on demand
    └── assets/         - Templates, images
```

### Creation Checklist

- [ ] Step 1: Understand with concrete examples
- [ ] Step 2: Plan scripts/references/assets
- [ ] Step 3: Initialize skill directory
- [ ] Step 4a: Create bundled resources
- [ ] Step 4b: Write SKILL.md
- [ ] Step 5: Package skill
- [ ] Step 6: Test and iterate

### Validation Checklist

Before packaging:
- [ ] YAML frontmatter has `name` and `description`
- [ ] Description includes what + when
- [ ] SKILL.md body is concise (<500 lines)
- [ ] Scripts are tested and work
- [ ] No extraneous files (README, etc.)
- [ ] Skill name follows conventions

---

## 🎓 Key Takeaways

1. **Skills extend Clawdbot** with domain expertise
2. **Progressive disclosure** keeps context efficient
3. **SKILL.md is required**, resources are optional
4. **Description is critical** for triggering
5. **Concise is better** - assume Clawdbot is smart
6. **Test scripts** before packaging
7. **Split large content** into references
8. **Iterate based on usage** to improve

---

**Study time:** ~75 minutes  
**First skill creation:** ~20-30 minutes  
**ROI:** Transform Clawdbot into a domain expert for your specific needs ✨

Ready to build your first skill? Start with the calculator exercise above!
