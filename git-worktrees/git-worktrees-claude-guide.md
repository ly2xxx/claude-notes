# Git Worktrees + Claude Code: Hands-On Practice Guide

**Context**: From Paolo Rosson (Head of Applied AI at Dext) sharing Claude Code team tips:
> "Git worktrees in parallel - Spin up 3-5 worktrees, each running its own Claude session. The team says it's their single biggest productivity unlock."

---

## 🎯 What You'll Learn Tonight

By the end of this guide, you'll:
1. ✅ Understand what git worktrees are and why they're powerful
2. ✅ Create and manage multiple worktrees
3. ✅ Run parallel Claude sessions in different worktrees
4. ✅ Practice the Claude Code team's workflow
5. ✅ Know when to use worktrees vs branches

**Time Estimate**: 45-60 minutes

---

## 📚 Part 1: Understanding Git Worktrees (10 min)

### What is a Git Worktree?

**Traditional Git**:
```
repo/
└── .git/          # Git data
└── main/          # Working directory (ONE branch at a time)
```

You switch branches → files change → context lost.

**Git Worktrees**:
```
repo/
├── .git/                    # Shared Git data
├── main/                    # Worktree 1 (main branch)
├── worktrees/
│   ├── feature-auth/        # Worktree 2 (feature branch)
│   ├── bugfix-db/           # Worktree 3 (another branch)
│   └── experiment-api/      # Worktree 4 (experimental)
```

**Each worktree** = Separate directory with its own checked-out branch.

### Why This Changes Everything for AI Development

#### The Problem
```
You: "Claude, refactor the auth module"
Claude: *starts work*
Urgent bug appears → You switch branches
Claude: *loses context, files changed underneath*
You: "Nevermind, start over..."
```

#### The Solution (Worktrees)
```
Worktree 1 (main):        Claude Desktop → "Refactor auth"
Worktree 2 (hotfix):      VS Code → Fix urgent bug
Worktree 3 (experiment):  Claude CLI → "Try new API design"
Worktree 4 (review):      Browser → Review PR

Each stays in its own space. No conflicts. No context loss.
```

### Key Benefits

✅ **Parallel AI sessions**: Each worktree = independent Claude context  
✅ **No branch switching**: Keep all work visible simultaneously  
✅ **Fast context switching**: `cd` between directories, not `git checkout`  
✅ **Compare implementations**: See different approaches side-by-side  
✅ **Reduced cognitive load**: Physical separation = mental separation  

---

## 🛠️ Part 2: Hands-On Setup (15 min)

### Prerequisites Check

```bash
# Verify Git version (need 2.5+, recommend 2.30+)
git --version

# Expected: git version 2.x.x (if 2.30+, great!)
```

### Exercise 1: Create Your First Worktree

We'll use a practice repository to learn safely.

#### Step 1: Create Practice Repo

```bash
# Navigate to your code directory
cd C:\code

# Create test repo
mkdir worktree-practice
cd worktree-practice
git init
echo "# Worktree Practice" > README.md
git add .
git commit -m "Initial commit"
```

#### Step 2: Create a Feature Branch (Traditional Way)

```bash
# Create and switch to feature branch
git checkout -b feature-1
echo "Feature 1 work" > feature1.txt
git add .
git commit -m "Add feature 1"

# Switch back to main
git checkout main
# Notice: feature1.txt disappears
```

#### Step 3: Create Your First Worktree

```bash
# We're on main branch
pwd
# Output: C:\code\worktree-practice

# Create a worktree for feature-1
git worktree add ../worktree-practice-feature1 feature-1

# What happened?
# 1. New directory created: C:\code\worktree-practice-feature1
# 2. feature-1 branch checked out there
# 3. Main directory (worktree-practice) stays on main
```

#### Step 4: Explore Both Worktrees

```bash
# Main worktree
cd C:\code\worktree-practice
ls
# Output: README.md (no feature1.txt)

# Feature worktree
cd C:\code\worktree-practice-feature1
ls
# Output: README.md, feature1.txt (both present!)

# They're independent but share Git history
```

#### Step 5: Work in Parallel

```bash
# In main worktree (C:\code\worktree-practice)
echo "Main branch work" > main-work.txt
git add .
git commit -m "Work on main"

# In feature worktree (C:\code\worktree-practice-feature1)
cd C:\code\worktree-practice-feature1
echo "Feature 1 progress" >> feature1.txt
git add .
git commit -m "Continue feature 1"

# Both changes tracked independently!
```

### Exercise 2: List and Manage Worktrees

```bash
# List all worktrees
git worktree list

# Output:
# C:/code/worktree-practice         abc1234 [main]
# C:/code/worktree-practice-feature1 def5678 [feature-1]

# Detailed view
git worktree list --porcelain

# Remove a worktree (when done)
git worktree remove ../worktree-practice-feature1
# Or: rm -rf ../worktree-practice-feature1 && git worktree prune
```

---

## 🤖 Part 3: Claude Code Workflow (20 min)

### The Claude Code Team's Setup

According to the post, they run **3-5 worktrees**, each with its own Claude session.

**Typical Layout**:
```
project/
├── main/                  # Worktree 1: Main branch (stable)
├── wt-feature-x/          # Worktree 2: New feature (Claude Desktop)
├── wt-refactor-y/         # Worktree 3: Refactoring (Claude CLI)
├── wt-experiment-z/       # Worktree 4: Experiments (Claude Desktop)
└── wt-bugfix/             # Worktree 5: Hot fixes (manual)
```

### Exercise 3: Set Up Multi-Worktree Project

Let's simulate a real project with multiple parallel tasks.

#### Step 1: Create a Realistic Project

```bash
cd C:\code
mkdir my-app
cd my-app
git init

# Create initial structure
echo "# My App" > README.md
mkdir src
echo "console.log('Hello');" > src/app.js
git add .
git commit -m "Initial project"
```

#### Step 2: Create Multiple Worktrees

```bash
# Main worktree is at: C:\code\my-app

# Create worktree for authentication feature
git worktree add -b feature/auth ../my-app-auth
# New branch 'feature/auth' created
# Directory: C:\code\my-app-auth

# Create worktree for database refactor
git worktree add -b refactor/database ../my-app-db-refactor
# Directory: C:\code\my-app-db-refactor

# Create worktree for API experiments
git worktree add -b experiment/new-api ../my-app-api-experiment
# Directory: C:\code\my-app-api-experiment

# Create worktree for bug fixes
git worktree add -b hotfix/critical-bug ../my-app-hotfix
# Directory: C:\code\my-app-hotfix

# Check setup
git worktree list
```

#### Step 3: Simulate Parallel Claude Sessions

**Worktree 1: Feature Development (Claude Desktop)**
```bash
cd C:\code\my-app-auth

# Create a .clawdbot context file
echo "# Task: Implement JWT authentication
- Add login endpoint
- Add token validation middleware
- Add user session management" > TASK.md

# Start Claude Desktop pointed here
# Ask: "Read TASK.md and implement the authentication system"
```

**Worktree 2: Refactoring (Claude CLI or separate session)**
```bash
cd C:\code\my-app-db-refactor

echo "# Task: Refactor database layer
- Extract database logic from controllers
- Add connection pooling
- Implement repository pattern" > TASK.md

# Start another Claude session here
# Ask: "Read TASK.md and refactor the database layer"
```

**Worktree 3: Experiments (Third Claude session)**
```bash
cd C:\code\my-app-api-experiment

echo "# Task: Prototype GraphQL API
- Experiment with GraphQL instead of REST
- Compare performance
- Document findings" > TASK.md

# Third Claude session
# Ask: "Read TASK.md and create a GraphQL prototype"
```

**Worktree 4: Bug Fixes (Manual work or fourth session)**
```bash
cd C:\code\my-app-hotfix

echo "# Critical Bug: Memory leak in image processing
- Reproduce issue
- Find root cause
- Fix and test" > TASK.md

# Handle manually or with a focused Claude session
```

### Exercise 4: Context Management

**Key Insight**: Each worktree has its own:
- Files and folders
- Branch checkout
- Working directory state
- `.git` metadata (shared, but worktree-specific)

**Best Practice for Claude**:
```bash
# In each worktree, create context files:
cd C:\code\my-app-auth
echo "# Authentication Module
Current status: Implementing JWT
Dependencies: jsonwebtoken, bcrypt
Next: Add refresh token logic" > CONTEXT.md

# Tell Claude: "Read CONTEXT.md before starting"
# Update CONTEXT.md as work progresses
```

---

## 🎓 Part 4: Advanced Patterns (15 min)

### Pattern 1: The "Compare Implementations" Workflow

**Scenario**: You want to try two different approaches to the same problem.

```bash
# Create two experimental worktrees from same starting point
git checkout main
git worktree add -b experiment/approach-a ../my-app-exp-a
git worktree add -b experiment/approach-b ../my-app-exp-b

# Claude in worktree A: "Implement using Redis"
# Claude in worktree B: "Implement using PostgreSQL"

# Compare results side-by-side
# Keep the winner, delete the loser
```

### Pattern 2: The "Review While Building" Workflow

```bash
# Worktree 1: Active development
cd C:\code\my-app-feature

# Worktree 2: PR review (main branch for reference)
cd C:\code\my-app-main

# Open both in split VS Code windows
# Claude builds in worktree 1
# You review in worktree 2 simultaneously
```

### Pattern 3: The "Long-Running Task" Workflow

```bash
# Start a massive refactor in a worktree
cd C:\code\my-app-big-refactor
# Claude: "Refactor entire codebase to TypeScript" (takes hours)

# Meanwhile, fix urgent bugs in another worktree
cd C:\code\my-app-hotfix
# Work continues without interrupting the refactor
```

### Pattern 4: The "Isolated Testing" Workflow

```bash
# Create a worktree specifically for running tests
git worktree add -b test-runner ../my-app-test

cd C:\code\my-app-test
# Run long test suites here
npm test -- --watch

# Development continues uninterrupted in main worktree
```

---

## 🚀 Part 5: Real-World Practice Exercise (10 min)

### Mission: Set Up Your Actual Project

**Goal**: Create a worktree setup for one of your real projects tonight.

#### Option A: Molt Kanban Board

```bash
cd C:\code\molt

# Create worktree for new feature
git worktree add -b feature/advanced-filters ../molt-filters
cd C:\code\molt-filters

# Tell Claude: "Add advanced filtering to Molt board"
```

#### Option B: aidev MCP Crew

```bash
cd C:\code\aidev  # (or wherever your MCP project is)

# Create experimental worktree
git worktree add -b experiment/new-agent ../aidev-experiment
cd C:\code\aidev-experiment

# Tell Claude: "Experiment with adding a new agent type"
```

#### Option C: Any Active Project

```bash
cd C:\code\your-project

# Create 3 worktrees for parallel work
git worktree add -b feature/task1 ../your-project-task1
git worktree add -b feature/task2 ../your-project-task2  
git worktree add -b feature/task3 ../your-project-task3

# Assign different Claude sessions to each
```

---

## 📋 Worktree Command Cheatsheet

### Essential Commands

```bash
# Create new worktree
git worktree add <path> <branch>
git worktree add -b <new-branch> <path>  # Create branch + worktree

# List all worktrees
git worktree list
git worktree list --porcelain  # Detailed output

# Remove worktree
git worktree remove <path>
git worktree remove --force <path>  # Force removal

# Clean up deleted worktrees
git worktree prune

# Move worktree
git worktree move <old-path> <new-path>

# Lock/unlock worktree (prevent deletion)
git worktree lock <path>
git worktree unlock <path>
```

### Common Workflows

```bash
# Quick worktree for bug fix
git worktree add ../project-hotfix -b hotfix/issue-123

# Create worktree from specific commit
git worktree add ../project-old abc1234

# Create worktree for PR review
git worktree add ../project-pr-456 pr/456

# Cleanup after merge
cd main-worktree
git worktree remove ../project-feature
git branch -d feature/name
```

---

## 💡 Pro Tips from Experience

### Naming Conventions

```bash
# Good: Descriptive, short, consistent
../my-app-auth          # Feature work
../my-app-hotfix        # Bug fixes
../my-app-exp-graphql   # Experiments

# Bad: Confusing, inconsistent
../app-copy
../temp123
../new-folder-2
```

### Directory Organization

**Option 1: Sibling Directories** (Recommended)
```
C:\code\
├── my-app/              # Main worktree
├── my-app-feature1/     # Worktree 1
├── my-app-feature2/     # Worktree 2
└── my-app-hotfix/       # Worktree 3
```

**Option 2: Nested Worktrees**
```
C:\code\my-app\
├── .git/
├── main/                # Main worktree moved
└── worktrees/
    ├── feature1/
    ├── feature2/
    └── hotfix/
```

### Claude Session Management

**Best Practice**:
1. One VS Code window per worktree
2. One Claude Desktop instance per worktree (if possible)
3. Or: Use Claude CLI for secondary worktrees
4. Label terminal tabs: "Worktree: Auth", "Worktree: DB"

### Cleanup Strategy

```bash
# Weekly cleanup ritual
git worktree list  # Review active worktrees
git worktree remove <merged-worktrees>
git worktree prune
git branch -d <merged-branches>
```

---

## ⚠️ Common Pitfalls & Solutions

### Pitfall 1: Checking Out Same Branch in Multiple Worktrees

**Problem**:
```bash
git worktree add ../wt1 feature-x  # OK
git worktree add ../wt2 feature-x  # ERROR!
```

**Why**: Git prevents same branch in multiple worktrees (would cause conflicts).

**Solution**: Use different branches or create from commits:
```bash
git worktree add ../wt2 -b feature-x-copy abc1234
```

### Pitfall 2: Forgetting Uncommitted Changes

**Problem**: You have uncommitted work in a worktree, delete the directory manually, and lose work.

**Solution**: Always commit or stash before removing:
```bash
cd worktree
git add .
git commit -m "WIP: Save progress"
# OR
git stash
cd ..
git worktree remove worktree
```

### Pitfall 3: Mixing Up Worktree Contexts

**Problem**: You run commands in wrong worktree, confuse Claude with wrong context.

**Solution**: 
- Always check `pwd` before commands
- Use terminal labels/tabs
- Create CONTEXT.md file in each worktree root

### Pitfall 4: Large Binary Files

**Problem**: Worktrees duplicate working directory. With large binaries, this wastes disk space.

**Solution**:
- Use `.gitignore` for build artifacts, `node_modules`, etc.
- Each worktree only duplicates tracked files
- Consider sparse-checkout for monorepos

---

## 🎯 Tonight's Practice Plan

### Phase 1: Foundation (20 min)
- [ ] Complete Exercise 1: Create first worktree
- [ ] Complete Exercise 2: List and manage worktrees
- [ ] Create and delete 3 practice worktrees

### Phase 2: Claude Integration (20 min)
- [ ] Complete Exercise 3: Multi-worktree setup
- [ ] Start 2 parallel Claude sessions in different worktrees
- [ ] Test context isolation

### Phase 3: Real Project (20 min)
- [ ] Choose one of your active projects
- [ ] Create 2-3 worktrees for different tasks
- [ ] Run at least one Claude session in a worktree
- [ ] Practice switching between worktrees

---

## 📊 Success Criteria

By the end of tonight, you should:
- ✅ Feel comfortable creating/removing worktrees
- ✅ Understand when to use worktrees vs branches
- ✅ Have set up at least 2 parallel Claude sessions in separate worktrees
- ✅ Know how to list and manage your worktrees
- ✅ Have a real project configured with worktrees

---

## 🔗 Additional Resources

### Official Documentation
- Git Worktree Docs: https://git-scm.com/docs/git-worktree
- Pro Git Book (Worktrees): https://git-scm.com/book/en/v2

### Advanced Topics
- Sparse checkout with worktrees
- Worktrees in monorepos
- CI/CD with worktrees
- Worktrees + Git LFS

### VS Code Integration
- Open each worktree in separate window
- Use "File > Open Folder" for each worktree
- Multi-root workspaces (experimental)

---

## 🧪 Bonus Challenge

**For After Tonight**: Try the full Claude Code team stack:

1. ✅ Git worktrees (tonight)
2. ⬜ CLAUDE.md auto-rules ("Update your CLAUDE.md so you don't make that mistake again")
3. ⬜ Plan mode workflow (re-plan when things go sideways)
4. ⬜ Subagents for focus (offload tasks to keep main context clean)
5. ⬜ Voice dictation (fn fn on macOS)

---

## 📝 Quick Reference Card

```bash
# CREATE
git worktree add <path> <branch>          # From existing branch
git worktree add -b <new> <path>          # Create new branch + worktree
git worktree add <path> HEAD              # Detached HEAD

# MANAGE  
git worktree list                         # Show all
git worktree remove <path>                # Delete
git worktree prune                        # Clean orphaned metadata

# TYPICAL WORKFLOW
cd my-project
git worktree add ../my-project-feature feature/new-thing
cd ../my-project-feature
# Work here with Claude
git add . && git commit -m "Feature work"
cd ../my-project
git worktree remove ../my-project-feature
git merge feature/new-thing
```

---

**Ready to start?** Begin with Exercise 1 above! 🚀

**Questions during practice?** Document them in a `worktree-questions.md` file and we'll review tomorrow.

**Have fun** - This is going to change how you work with Claude!
