# Skill Composition Lab

**Created:** 2026-02-24  
**Purpose:** Learn how to build skills that call other skills (skill composition/orchestration)  
**Example:** A "markdown-to-pdf" workflow where one skill reads `.md` files and calls another skill to generate PDFs

---

## 📚 What You'll Learn

1. **Skill Composition Patterns** - Different ways one skill can invoke another
2. **Orchestration Strategies** - When to use each pattern
3. **Practical Examples** - Real-world skill chains (Markdown → PDF conversion)
4. **Best Practices** - Progressive disclosure, separation of concerns

---

## 🎯 Core Concepts

### What is Skill Composition?

**Skill composition** is when one skill orchestrates or invokes another skill to accomplish a larger workflow. Think of it like function composition in programming, but for AI workflows.

**Example:** A "document-publisher" skill that:
1. Reads markdown files (could use a "markdown-reader" skill)
2. Converts to PDF (calls a "pdf-generator" skill)
3. Uploads to cloud storage (calls an "upload-to-s3" skill)

### Why Compose Skills?

**Benefits:**
- ✅ **Reusability** - Write PDF generation once, use it everywhere
- ✅ **Modularity** - Each skill has one clear responsibility
- ✅ **Maintainability** - Update PDF logic in one place
- ✅ **Separation of Concerns** - Reading files vs. generating PDFs are different domains

---

## 🔧 Three Skill Composition Patterns

### Pattern 1: Direct Invocation via Instructions

**How it works:** Skill A's instructions tell Claude to invoke Skill B using `/skill-name`

**When to use:**
- Linear workflows (A → B → C)
- Clear handoff points
- When Skill B needs to run in isolation

**Example:**

```markdown
# Skill A: markdown-to-pdf (SKILL.md)
---
name: markdown-to-pdf
description: Convert markdown files to professional PDFs
---

# Markdown to PDF Converter

## Workflow
1. Read all markdown files in the specified directory
2. For each markdown file:
   - Extract the content and metadata
   - Invoke the PDF generator: `/generate-pdf [filename.md]`
3. Collect all generated PDFs in `/output/pdfs/`
```

```markdown
# Skill B: generate-pdf (SKILL.md)
---
name: generate-pdf
description: Generate a PDF from markdown content
disable-model-invocation: true
---

# PDF Generator

Generate a professional PDF from $ARGUMENTS:

1. Read the markdown file: $ARGUMENTS
2. Convert markdown to HTML with proper styling
3. Use a PDF library (e.g., `wkhtmltopdf` or Python's `pdfkit`)
4. Apply styling:
   - Font: Georgia for body, Helvetica for headings
   - Margins: 1 inch all around
   - Page numbers at bottom center
5. Save to `output/pdfs/[original-filename].pdf`
```

**Key features:**
- ✅ Skill B is `disable-model-invocation: true` (only invoked explicitly)
- ✅ Clear separation: Skill A orchestrates, Skill B executes
- ✅ Reusable: Other skills can also call `/generate-pdf`

---

### Pattern 2: Implicit Composition via Triggers

**How it works:** Skill A does work that naturally triggers Skill B's description

**When to use:**
- Flexible workflows where Claude should decide the best approach
- When multiple skills might apply to the same task
- Knowledge-based skills that complement each other

**Example:**

```markdown
# Skill A: document-analyzer (SKILL.md)
---
name: document-analyzer
description: Analyze markdown documents for structure, readability, and quality
---

# Document Analyzer

Analyze the provided markdown files:

1. Check document structure (headings, sections)
2. Measure readability (Flesch-Kincaid score)
3. Identify missing elements (TOC, summary, examples)
4. **If the document meets quality standards**, suggest converting to PDF for distribution
```

```markdown
# Skill B: generate-pdf (SKILL.md)
---
name: generate-pdf
description: Generate a PDF from markdown content. Use when user wants to convert markdown to PDF or when suggesting PDF generation for distribution.
---

# PDF Generator
[... same as before ...]
```

**How it works:**
- When Skill A suggests "converting to PDF", Claude sees Skill B's description
- If the context matches ("wants to convert markdown to PDF"), Claude may auto-invoke Skill B
- More flexible than Pattern 1, but less deterministic

---

### Pattern 3: Script-Based Orchestration

**How it works:** Skill A includes a script that orchestrates multiple skills

**When to use:**
- Complex workflows with conditional logic
- Need precise control over execution order
- When skills need to exchange data between steps

**Example:**

```markdown
# Skill: publish-documentation (SKILL.md)
---
name: publish-documentation
description: Full documentation publishing workflow
disable-model-invocation: true
---

# Documentation Publisher

Run the documentation publishing workflow:

1. Execute the orchestration script:
   ```bash
   python scripts/publish_workflow.py $ARGUMENTS
   ```

The script handles:
- Reading markdown files
- Converting to PDF (calls `/generate-pdf`)
- Validating output
- Uploading to S3 (calls `/upload-to-s3`)
```

```python
# scripts/publish_workflow.py
import subprocess
import os

def publish_docs(input_dir):
    # Step 1: Find all markdown files
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    # Step 2: Convert each to PDF using the generate-pdf skill
    for md_file in md_files:
        print(f"Converting {md_file} to PDF...")
        result = subprocess.run([
            'claude-code', 'skill', 'generate-pdf', md_file
        ], capture_output=True)
        
        if result.returncode != 0:
            print(f"Error converting {md_file}: {result.stderr}")
            continue
    
    # Step 3: Upload PDFs using upload-to-s3 skill
    pdf_dir = 'output/pdfs'
    subprocess.run(['claude-code', 'skill', 'upload-to-s3', pdf_dir])
    
    print("✅ Documentation published successfully!")

if __name__ == "__main__":
    import sys
    publish_docs(sys.argv[1])
```

**Key features:**
- ✅ Full control via Python/Bash
- ✅ Can handle errors and retries
- ✅ Can pass data between skills
- ⚠️ Requires Claude Code CLI access

---

## 🧪 Hands-On Example: Markdown → PDF Workflow

Let's build a complete example with two composable skills.

### Directory Structure

```
.claude/skills/
├── markdown-to-pdf/
│   ├── SKILL.md
│   └── scripts/
│       └── orchestrate.py
└── generate-pdf/
    ├── SKILL.md
    └── scripts/
        └── convert.py
```

### Skill 1: generate-pdf (The Worker)

This skill does ONE thing well: converts a single markdown file to PDF.

**File:** `.claude/skills/generate-pdf/SKILL.md`

```markdown
---
name: generate-pdf
description: Generate a professional PDF from a markdown file
disable-model-invocation: true
argument-hint: [filename.md]
---

# PDF Generator

Convert $ARGUMENTS to a professional PDF:

1. Read the markdown file
2. Run the conversion script:
   ```bash
   python scripts/convert.py "$ARGUMENTS"
   ```
3. Report the output location

The script handles:
- Markdown → HTML conversion
- Professional styling (fonts, margins, page numbers)
- Output to `output/pdfs/[filename].pdf`
```

**File:** `.claude/skills/generate-pdf/scripts/convert.py`

```python
import sys
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def convert_md_to_pdf(md_file):
    """Convert a markdown file to a styled PDF"""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown.markdown(
        md_content, 
        extensions=['extra', 'codehilite', 'toc']
    )
    
    # Add professional styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 1in;
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                }}
            }}
            body {{
                font-family: Georgia, serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
            }}
            h1, h2, h3 {{
                font-family: Helvetica, sans-serif;
                color: #2c3e50;
            }}
            code {{
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
            }}
            pre {{
                background: #f8f8f8;
                padding: 12px;
                border-left: 3px solid #3498db;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generate PDF
    output_dir = Path('output/pdfs')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_filename = Path(md_file).stem + '.pdf'
    pdf_path = output_dir / pdf_filename
    
    HTML(string=styled_html).write_pdf(pdf_path)
    
    print(f"✅ PDF generated: {pdf_path}")
    return str(pdf_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert.py <markdown-file>")
        sys.exit(1)
    
    convert_md_to_pdf(sys.argv[1])
```

### Skill 2: markdown-to-pdf (The Orchestrator)

This skill handles the workflow: finding files, calling the PDF generator, summarizing results.

**File:** `.claude/skills/markdown-to-pdf/SKILL.md`

```markdown
---
name: markdown-to-pdf
description: Convert all markdown files in a directory to professional PDFs
disable-model-invocation: true
argument-hint: [directory-path]
---

# Markdown to PDF Batch Converter

Convert all markdown files in $ARGUMENTS to PDFs:

## Workflow

1. **Find markdown files**:
   - List all `.md` files in the directory
   - Exclude CLAUDE.md, AGENTS.md, MEMORY.md (special files)

2. **Convert each file**:
   - For each markdown file, invoke:
     ```
     /generate-pdf [filename]
     ```
   - Track success/failures

3. **Summary**:
   - Report total files processed
   - List generated PDFs
   - Report any errors

## Example

```bash
/markdown-to-pdf ./docs
```

This will convert all `.md` files in `./docs/` to PDFs in `output/pdfs/`.
```

---

## 🎯 When to Use Each Pattern

| Pattern | Best For | Pros | Cons |
|---------|----------|------|------|
| **Direct Invocation** | Linear workflows, clear steps | Simple, predictable | Less flexible |
| **Implicit Composition** | Flexible workflows, knowledge skills | Claude decides best approach | Less deterministic |
| **Script-Based** | Complex logic, conditional flows | Full control, error handling | Requires scripting |

---

## ✅ Best Practices

### 1. Progressive Disclosure

Don't load all skill content upfront. Use references:

```markdown
# Main Skill (SKILL.md)
---
name: advanced-pdf-workflow
description: Advanced PDF generation with custom templates
---

# Advanced PDF Workflow

For template documentation, see [templates.md](templates.md)
For styling options, see [styling-guide.md](styling-guide.md)
```

### 2. Single Responsibility

Each skill should do ONE thing well:
- ✅ `generate-pdf` - converts markdown to PDF
- ✅ `upload-to-s3` - uploads files to S3
- ✅ `markdown-to-pdf` - orchestrates the workflow
- ❌ `generate-and-upload-pdf` - does too much (split it)

### 3. Clear Triggering

Use descriptive `description` fields:

```yaml
# Good
description: Generate a PDF from markdown content. Use when converting .md files to .pdf or when user says "make a PDF".

# Bad
description: PDF stuff
```

### 4. Error Handling

Orchestrator skills should handle failures gracefully:

```markdown
2. **Convert each file**:
   - For each markdown file, invoke `/generate-pdf [filename]`
   - If conversion fails, log the error and continue
   - Track failed files for summary report
```

---

## 🚀 Advanced: Multi-Skill Chains

You can chain multiple skills together:

```
/document-pipeline ./docs
  ├─> /analyze-markdown (check quality)
  ├─> /generate-pdf (convert to PDF)
  ├─> /optimize-images (compress images in PDFs)
  └─> /upload-to-s3 (publish to cloud)
```

**Pattern:** Create a "pipeline" skill that orchestrates multiple specialized skills.

---

## 📖 Further Reading

- **Progressive Disclosure**: Keep SKILL.md lean, use reference files
- **Subagents**: Run skills in isolated contexts with `context: fork`
- **Dynamic Context**: Use `!`command`` to inject live data
- **Skill Arguments**: Use `$ARGUMENTS`, `$0`, `$1` for parameterization

---

## 🎓 Exercise

**Challenge:** Build a "blog-publisher" skill that:
1. Reads markdown blog posts from `/posts/`
2. Generates PDFs for each post (`/generate-pdf`)
3. Creates an HTML index page
4. Uploads everything to S3 (`/upload-to-s3`)

**Bonus:** Add a skill that sends a Slack notification when publishing completes.

---

*Created by Helpful Bob for Master Yang - 2026-02-24*
