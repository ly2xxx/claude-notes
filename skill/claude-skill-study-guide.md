# Claude Skill Creation Study Guide

**Created:** 2026-02-01  
**Goal:** Build a functional Claude Skill and ensure it is recognized by Claude Code  
**Time:** 15-30 minutes  

---

## 📋 What You'll Learn

1. What a "Skill" is and why it's different from just a prompt
2. The strict technical requirements for Claude to detect your skill
3. How to structure your `SKILL.md` and frontmatter
4. Patterns for connecting Skills to MCP servers
5. Common reasons why skills fail to load (Gotchas)

---

## 🎯 Part 1: Core Concepts (5 min)

### What is a Skill?

A skill is a **folder** containing instructions that teach Claude how to handle specific tasks or workflows. It is the "brain" (knowledge) that directs the "hands" (MCP tools).

**Key distinction:**
- **MCP Server:** Provides the tools (connectivity).
- **Skill:** Provides the recipe (knowledge/workflow) on *how* to use those tools.

### Progressive Disclosure (The 3 Levels)

To save tokens and context, Claude doesn't read everything at once:

1.  **Level 1: YAML Frontmatter** acts as the "index card". Claude reads *only* this to decide if the skill is relevant.
2.  **Level 2: SKILL.md Body** is loaded *only* when the skill is triggered.
3.  **Level 3: Linked Files** in `references/` are read *only* if the skill explicitly looks them up.

---

## 🔧 Part 2: Technical Details (10 min)

### ⚠️ Critical Rules for Recognition

If you violate these, Claude **will not see** your skill.

| Component | Rule | Example |
| :--- | :--- | :--- |
| **Folder Name** | **Kebab-case only**. No spaces, no capitals. | `project-setup` ✅ <br> `Project Setup` ❌ |
| **File Name** | Must be exactly **`SKILL.md`**. Case-sensitive. | `SKILL.md` ✅ <br> `skill.md` ❌ |
| **Frontmatter** | Must match folder name. No XML tags. | `name: project-setup` |

### File Structure

```text
your-skill-name/              # Kebab-case folder
├── SKILL.md                  # REQUIRED: Main instructions
├── scripts/                  # Optional: Helper scripts (py/bash)
├── references/               # Optional: Documentation docs
└── assets/                   # Optional: Templates/Icons
```

### The All-Important YAML Frontmatter

This is the gatekeeper. Use this exact format at the top of `SKILL.md`:

```yaml
---
name: your-skill-name        # Must match folder name exactly
description: Action-oriented summary. Triggers + Capabilities.
---
```

**Good Description Formula:** `[What it does] + [When to use it (Trigger Phrases)] + [Key capabilities]`

**Example:**
> "Manages Linear project workflows. Use when user says 'plan sprint', 'create tickets', or 'check project status'. Creates tasks with proper labeling."

---

## 💡 Part 3: Patterns & Use Cases (10 min)

### Pattern 1: Sequential Workflow
**Best for:** Onboarding, Setup, Reports.

*Structure:*
1.  **Trigger:** User says "Onboard new client".
2.  **Step 1:** Create folder (Drive MCP).
3.  **Step 2:** Create contract (Doc creation).
4.  **Step 3:** Slack notification (Slack MCP).

### Pattern 2: Context-Aware Tool Selection
**Best for:** "Fix this" or "Store this" generic requests.

*Structure:*
- Logic tree in `SKILL.md`:
    - IF file > 10MB -> Use S3 MCP.
    - IF file < 10MB -> Use Local File MCP.

### Pattern 3: Document & Asset Creation
**Best for:** Standardizing output without external tools.

*Structure:*
- Embedded templates in `assets/`.
- Style guides in `references/`.
- Skill enforces "Always use H2 for headers" or "Follow Brand Palette X".

---

## ⚠️ Part 4: Gotchas & Troubleshooting (5 min)

### Why didn't my skill load?

1.  **Folder/Name Mismatch:** Folder is `my-skill`, YAML name is `My Skill`. (Must be `my-skill`).
2.  **Wrong Case:** File is named `skill.md` instead of `SKILL.md`.
3.  **Vague Description:** Description says "Helps with tasks". (Claude ignores this). Needs specific triggers.
4.  **XML in Frontmatter:** Used `<tool>` tags in the description block. (Forbidden).

### Why is it hallucinating steps?

- **Instructions too verbose:** Claude got lost in text. Use **numbered lists** and **headers**.
- **Missing "References":** You put 20 pages of docs in `SKILL.md`. Move them to `references/api-docs.md` and tell Claude to read it *only if needed*.

---

## 🛠️ Part 5: Your Implementation Plan (5 min)

### Quick Start: Create Your First Skill

1.  **Create Directory:**
    ```bash
    mkdir -p my-first-skill
    ```

2.  **Create SKILL.md:**
    ```markdown
    ---
    name: my-first-skill
    description: A tutorial skill. Use when user says "teach me skills" or "test skill".
    ---

    # My First Skill
    
    ## Instructions
    1.  Greet the user.
    2.  Explain that this text is coming from a loaded skill.
    3.  Ask if they want to see a magic trick (optional script execution).
    ```

3.  **Load the Skill:**
    - **Claude Code:** Ensure it's in your configured skills directory (e.g. `.claude/skills` or via settings).
    - **Claude.ai:** Settings -> Capabilities -> Add Skill -> Upload standard zip of the folder.

---

## 📊 Success Metrics

1.  **Trigger Rate:** Does it load automatically when you say the trigger phrase? (Target: >90%)
2.  **Accuracy:** Does it follow the step-by-step logic without skipping?
3.  **Latency:** Is it faster than typing out the full prompt context every time?

---

## 📚 Resources

- **Official Guide:** `The-Complete-Guide-to-Building-Skill-for-Claude.pdf` (in your workspace)
- **Skill Creator Skill:** Ask Claude to "Help me build a skill" (uses built-in bootstrap skill).
