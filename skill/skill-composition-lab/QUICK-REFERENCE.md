# Skill Composition - Quick Reference

## 🎯 Three Patterns for Skill Composition

### Pattern 1: Direct Invocation
**Orchestrator skill explicitly calls worker skill**

```markdown
# orchestrator/SKILL.md
For each file:
  1. Process the file
  2. Invoke: `/worker-skill [filename]`
  3. Track results
```

✅ Best for: Linear workflows, clear handoffs  
✅ Pros: Predictable, debuggable  
❌ Cons: Less flexible

---

### Pattern 2: Implicit Composition
**Skill descriptions naturally trigger each other**

```markdown
# analyzer/SKILL.md
description: Analyze documents. When quality is good, suggest PDF generation.

# generator/SKILL.md  
description: Generate PDFs. Use when suggesting PDF generation or user requests conversion.
```

✅ Best for: Flexible workflows, knowledge skills  
✅ Pros: Claude decides best approach  
❌ Cons: Less deterministic

---

### Pattern 3: Script-Based
**Python/Bash script orchestrates multiple skills**

```python
# scripts/orchestrate.py
import subprocess

# Call skill 1
subprocess.run(['claude-code', 'skill', 'analyze', file])

# Call skill 2  
subprocess.run(['claude-code', 'skill', 'generate-pdf', file])
```

✅ Best for: Complex logic, conditionals, error handling  
✅ Pros: Full control, can pass data between skills  
❌ Cons: Requires scripting, needs CLI access

---

## 📋 Checklist: Creating Composable Skills

### Worker Skill (The Tool)
- [ ] Does ONE thing well
- [ ] Has `disable-model-invocation: true` (only called explicitly)
- [ ] Clear `argument-hint` showing expected input
- [ ] Handles errors gracefully
- [ ] Reports success/failure clearly

**Example:** `generate-pdf` - converts ONE markdown file to PDF

### Orchestrator Skill (The Coordinator)
- [ ] Discovers what needs processing
- [ ] Calls worker skills with proper arguments
- [ ] Tracks success/failures
- [ ] Provides summary report
- [ ] Continues on errors (batch processing)

**Example:** `markdown-to-pdf` - finds files, calls `generate-pdf` for each

---

## 🔧 Key Frontmatter Fields

```yaml
---
name: my-skill              # Becomes /my-skill command
description: What it does and when to use it
disable-model-invocation: true   # Only called explicitly (orchestrators may leave false)
argument-hint: [input]     # Shown in autocomplete
context: fork              # Run in isolated subagent (optional)
allowed-tools: Read, Grep  # Restrict tool access (optional)
---
```

---

## 💡 Design Tips

### 1. Single Responsibility
❌ `generate-and-upload-pdf` (does too much)  
✅ `generate-pdf` + `upload-to-s3` (compose them)

### 2. Progressive Disclosure
Don't load all content upfront:

```markdown
# Main skill
For detailed API docs, see [api-reference.md](api-reference.md)
For examples, see [examples.md](examples.md)
```

### 3. Clear Triggers
```yaml
# Good
description: Generate PDF from markdown. Use when converting .md to .pdf or user says "make a PDF"

# Bad  
description: PDF stuff
```

### 4. Error Handling
Orchestrators should continue on errors:

```markdown
For each file:
  - Try to convert with `/generate-pdf`
  - If it fails, log error and continue
  - Track failures for summary report
```

---

## 🚀 Common Patterns

### Sequential Chain
```
/workflow
  ├─> /step-1
  ├─> /step-2  
  └─> /step-3
```

### Parallel Processing
```
/batch-processor
  ├─> /process file1.md
  ├─> /process file2.md
  └─> /process file3.md
```

### Conditional Flow
```python
if condition:
    subprocess.run(['claude-code', 'skill', 'option-a'])
else:
    subprocess.run(['claude-code', 'skill', 'option-b'])
```

---

## 📖 Example: Our Markdown → PDF System

### Architecture

```
markdown-to-pdf (Orchestrator)
    ↓
    Discovers: guide.md, tutorial.md
    ↓
    For each file:
    ├─> /generate-pdf guide.md
    └─> /generate-pdf tutorial.md
        ↓
        scripts/convert.py
        ↓
        output/pdfs/guide.pdf ✅
```

### File Structure

```
.claude/skills/
├── generate-pdf/           # Worker
│   ├── SKILL.md           # Instructions
│   └── scripts/
│       └── convert.py     # PDF generation logic
│
└── markdown-to-pdf/       # Orchestrator
    └── SKILL.md           # Batch workflow
```

### Usage

```bash
# Orchestrator (batch)
/markdown-to-pdf ./docs

# Worker (single file)
/generate-pdf docs/guide.md
```

---

## ⚠️ Common Mistakes

### ❌ Circular Dependencies
Skill A calls Skill B calls Skill A → Infinite loop

### ❌ Too Much in One Skill
One monolithic skill instead of composable pieces

### ❌ Poor Error Handling
Orchestrator fails completely if one worker fails

### ❌ Unclear Descriptions
Claude can't auto-invoke because description is vague

---

## ✅ Best Practices Summary

1. **Worker skills** = `disable-model-invocation: true`
2. **Orchestrators** = call workers explicitly with `/skill-name`
3. **Single responsibility** = one skill, one job
4. **Progressive disclosure** = use reference files for large content
5. **Error handling** = continue on failures, report at end
6. **Clear naming** = descriptive skill names and arguments

---

*Quick reference for skill composition patterns - 2026-02-24*
