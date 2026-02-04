# Git Worktrees - Quick Reference Card

**Print this or keep it open while practicing!**

---

## 🎯 The Big Idea

**One repo, multiple working directories, parallel work**

```
Instead of: Switch branches → lose context → frustration
Do this:    Multiple worktrees → parallel Claude sessions → productivity
```

---

## ⚡ Essential Commands

```bash
# CREATE worktree
git worktree add <path> <branch>              # Use existing branch
git worktree add -b <new-branch> <path>       # Create new branch
git worktree add ../my-app-feature feature-x  # Example

# LIST worktrees
git worktree list                             # Simple list
git worktree list --porcelain                 # Detailed

# REMOVE worktree
git worktree remove <path>                    # Clean removal
git worktree remove --force <path>            # Force it

# CLEANUP
git worktree prune                            # Remove orphaned metadata
```

---

## 🚀 Tonight's Quick Start

**Step 1: Create practice repo**
```bash
cd C:\code
mkdir wt-test && cd wt-test
git init
echo "test" > README.md
git add . && git commit -m "init"
```

**Step 2: Create your first worktree**
```bash
git worktree add -b feature-1 ../wt-test-f1
cd ../wt-test-f1
ls  # You're in a new directory with feature-1 checked out!
```

**Step 3: Work in parallel**
```bash
# Terminal 1: Main worktree
cd C:\code\wt-test
echo "main work" > main.txt
git add . && git commit -m "main work"

# Terminal 2: Feature worktree  
cd C:\code\wt-test-f1
echo "feature work" > feature.txt
git add . && git commit -m "feature work"

# Both tracked independently!
```

---

## 💡 Claude Code Team Pattern

```
project/
├── main/              # Main worktree (stable)
├── wt-auth/           # Claude session 1 → Auth feature
├── wt-refactor/       # Claude session 2 → Refactoring
├── wt-experiment/     # Claude session 3 → Experiments
└── wt-hotfix/         # Manual → Emergency fixes

Each directory = independent Claude context!
```

---

## ✅ Checklist for Tonight

- [ ] Create first worktree (Exercise 1)
- [ ] List worktrees (`git worktree list`)
- [ ] Create 3 worktrees for parallel tasks
- [ ] Run 2 Claude sessions in different worktrees
- [ ] Remove a worktree cleanly
- [ ] Apply to one real project

---

## ⚠️ Remember

1. **Can't check out same branch twice** (use different branches)
2. **Always commit before removing** (don't lose work)
3. **Use descriptive names** (`../app-auth` not `../temp`)
4. **One Claude session per worktree** (context isolation)

---

## 🎓 When to Use Worktrees

✅ **USE when**:
- Running parallel AI sessions
- Comparing different approaches
- Long-running tasks + urgent fixes
- PR review while developing
- Testing without disrupting dev

❌ **DON'T USE when**:
- Simple feature branches (regular checkout is fine)
- Very short-lived work (overhead not worth it)
- Single-task workflow (no parallel work)

---

## 🔥 Pro Tips

```bash
# Naming convention
../my-app-feature    # Feature work
../my-app-hotfix     # Bug fixes  
../my-app-exp-api    # Experiments

# Quick cleanup
git worktree list | grep feature | xargs git worktree remove

# Create + start work immediately
git worktree add -b feat ../app-feat && cd ../app-feat

# List with colors (easier to read)
git worktree list --verbose
```

---

**Main Guide**: `C:\Users\vl\clawd\study\git-worktrees-claude-guide.md`

**Start here**: Exercise 1 in the main guide (page 3)

---

🚀 **You got this!** Worktrees will change your workflow tonight.
