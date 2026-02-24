# Skill Composition Lab - Index

**Created:** 2026-02-24  
**Purpose:** Master the art of composing Claude skills  
**Level:** Intermediate to Advanced

---

## 📚 Contents

### 🎓 Learning Materials

1. **[README.md](README.md)** - Start here!
   - Core concepts of skill composition
   - Three main patterns (Direct, Implicit, Script-based)
   - When to use each pattern
   - Best practices and guidelines
   - Hands-on example walkthrough

2. **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** - Cheat sheet
   - Pattern comparison at a glance
   - Checklist for creating composable skills
   - Key frontmatter fields
   - Common mistakes to avoid
   - Design tips

3. **[ADVANCED-EXAMPLE.md](ADVANCED-EXAMPLE.md)** - Deep dive
   - Complete publishing pipeline (6 skills)
   - Multi-skill orchestration
   - Conditional workflows
   - Data passing between skills
   - Error handling and rollback strategies

---

## 🛠️ Example Skills

Located in `example-skills/`

### Worker Skills

**[generate-pdf](example-skills/generate-pdf/)**
- **What it does:** Converts a single markdown file to a styled PDF
- **Pattern:** Worker skill (does one thing well)
- **Invocation:** Manual only (`disable-model-invocation: true`)
- **Usage:** `/generate-pdf docs/guide.md`

### Orchestrator Skills

**[markdown-to-pdf](example-skills/markdown-to-pdf/)**
- **What it does:** Batch converts all markdown files in a directory
- **Pattern:** Orchestrator (calls `generate-pdf` for each file)
- **Invocation:** Manual only (batch operation)
- **Usage:** `/markdown-to-pdf ./docs`

---

## 🗺️ Learning Path

### Level 1: Understanding (30 min)
1. Read [README.md](README.md) → Core concepts
2. Review [QUICK-REFERENCE.md](QUICK-REFERENCE.md) → Patterns summary
3. Understand the three composition patterns

**Goal:** Know when to use each pattern

---

### Level 2: Building (1 hour)
1. Study `example-skills/generate-pdf/` → Worker skill anatomy
2. Study `example-skills/markdown-to-pdf/` → Orchestrator skill anatomy
3. Identify how they work together
4. Try modifying them:
   - Change PDF styling
   - Add new file exclusions
   - Customize output directory

**Goal:** Understand skill structure and composition

---

### Level 3: Creating (2 hours)
1. Build your own worker skill (e.g., `optimize-images`)
2. Build an orchestrator that uses it (e.g., `prepare-blog-post`)
3. Test the composition
4. Handle errors gracefully

**Goal:** Create your first skill pair

---

### Level 4: Mastering (4 hours)
1. Read [ADVANCED-EXAMPLE.md](ADVANCED-EXAMPLE.md) → Complex pipeline
2. Understand multi-skill orchestration (6 skills working together)
3. Build a 3+ skill pipeline for your use case
4. Implement error handling and rollback
5. Add conditional logic

**Goal:** Build production-ready skill pipelines

---

## 🎯 Quick Examples

### Example 1: Simple Chain
```
User: /markdown-to-pdf ./docs

markdown-to-pdf:
  ├─> Find: guide.md, tutorial.md
  ├─> /generate-pdf guide.md → ✅
  ├─> /generate-pdf tutorial.md → ✅
  └─> Summary: 2 PDFs created
```

### Example 2: Conditional Flow
```
User: /publish-docs ./documentation

publish-docs:
  ├─> /analyze-markdown ./documentation
  │   └─> Quality scores: guide=88, draft=60
  ├─> Filter: guide.md only (≥70)
  ├─> /generate-pdf guide.md → ✅
  ├─> /create-index output/pdfs → ✅
  ├─> /upload-to-s3 output → ✅
  └─> /send-slack "Published 1 doc" → ✅
```

---

## 🔑 Key Concepts Summary

### Composition = Modularity

**Bad (Monolithic):**
```
generate-and-upload-pdf-and-notify-slack
└─> Does everything (600 lines)
```

**Good (Modular):**
```
publish-pipeline
├─> /generate-pdf
├─> /upload-to-s3
└─> /send-slack
```

### Worker vs Orchestrator

| Aspect | Worker | Orchestrator |
|--------|--------|--------------|
| **Purpose** | Do one thing well | Coordinate multiple workers |
| **Invocation** | Usually `disable-model-invocation: true` | Can allow auto-invocation |
| **Complexity** | Simple, focused | Complex, manages workflow |
| **Reusability** | High (called by many) | Lower (specific workflow) |
| **Example** | `generate-pdf` | `markdown-to-pdf` |

### Progressive Disclosure

Don't load everything into context:

```markdown
# SKILL.md (500 lines max)
For detailed templates, see [templates.md](templates.md)
For API reference, see [api-docs.md](api-docs.md)
```

---

## 🚀 Common Use Cases

### Documentation Pipelines
```
/publish-docs
├─> Analyze quality
├─> Generate PDFs
├─> Create index
└─> Upload to S3
```

### Code Quality Workflows
```
/code-review
├─> Run linter
├─> Run tests
├─> Generate coverage report
└─> Post to PR
```

### Content Publishing
```
/publish-blog
├─> Optimize images
├─> Generate thumbnails
├─> Convert to HTML
└─> Deploy to website
```

### Data Processing
```
/process-dataset
├─> Validate data
├─> Transform formats
├─> Generate visualizations
└─> Export results
```

---

## ⚠️ Common Pitfalls

### 1. Circular Dependencies
❌ Skill A → Skill B → Skill A (infinite loop)  
✅ Clear hierarchy: Orchestrator → Workers

### 2. Too Much Coupling
❌ Worker skill assumes specific orchestrator  
✅ Worker skill is generic, reusable

### 3. Poor Error Handling
❌ Pipeline fails completely on first error  
✅ Log errors, continue processing, report at end

### 4. Unclear Triggers
❌ Vague descriptions, skills don't know when to activate  
✅ Specific, descriptive triggers in frontmatter

---

## 📖 Further Reading

### Claude Code Documentation
- [Skills Overview](https://code.claude.com/docs/en/skills)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent Skills Standard](https://agentskills.io)

### Related Labs
- `/skill-creator` - Built-in skill for creating new skills
- `yaml-benefits-lab/` - YAML configuration patterns
- `code/readme-updater-claude-skill/` - Real-world skill example

---

## 🎓 Exercises

### Beginner
1. Modify `generate-pdf` styling (change fonts/colors)
2. Add a new file exclusion to `markdown-to-pdf`
3. Create a simple worker skill that counts words in markdown files

### Intermediate
1. Build an `optimize-images` worker skill
2. Create an orchestrator that calls both `optimize-images` and `generate-pdf`
3. Add error handling to report which images failed

### Advanced
1. Build a 3-skill pipeline: analyze → process → notify
2. Add conditional logic (only process files meeting criteria)
3. Implement rollback on failure
4. Create a dashboard skill that summarizes pipeline runs

---

## 📊 Skill Composition Decision Tree

```
Do you need to compose multiple operations?
├─ NO → Single skill is fine
└─ YES → Composition needed
    │
    ├─ Linear workflow (A → B → C)?
    │   └─ Use Pattern 1: Direct Invocation
    │
    ├─ Need conditional logic or data passing?
    │   └─ Use Pattern 3: Script-Based
    │
    └─ Flexible, context-dependent workflow?
        └─ Use Pattern 2: Implicit Composition
```

---

## 🔧 Tools & Templates

### Skill Template (Worker)
```markdown
---
name: my-worker
description: Does X. Use when Y.
disable-model-invocation: true
argument-hint: [input]
---

# Worker Skill

Process $ARGUMENTS:

1. Validate input
2. Execute main logic
3. Report result or error
```

### Skill Template (Orchestrator)
```markdown
---
name: my-orchestrator
description: Coordinates X workflow
disable-model-invocation: true
---

# Orchestrator Skill

Run workflow on $ARGUMENTS:

1. Discover inputs
2. For each input:
   - Call: `/worker-skill [input]`
   - Track result
3. Generate summary
```

---

## 📞 Support

**Questions?** Review the examples in this lab:
1. Start with simple examples in README
2. Check QUICK-REFERENCE for patterns
3. Study ADVANCED-EXAMPLE for complex cases

**Debugging?** Common issues:
- Skill not loading → Check frontmatter YAML
- Skill not triggering → Review `description` field
- Errors in composition → Check argument passing

---

## ✅ Completion Checklist

After completing this lab, you should be able to:

- [ ] Explain the three skill composition patterns
- [ ] Identify when to use each pattern
- [ ] Create a worker skill with single responsibility
- [ ] Create an orchestrator that calls multiple workers
- [ ] Handle errors in skill pipelines
- [ ] Pass data between skills
- [ ] Use progressive disclosure effectively
- [ ] Write clear skill descriptions for triggering
- [ ] Build a 3+ skill pipeline for a real use case

---

**Lab created for Master Yang - 2026-02-24**  
*Happy composing! 🎼*
