# Coding Agent (Claude Code) Study Guide

**Created:** 2026-02-01  
**Goal:** Master using Claude Code and other coding agents via Clawdbot  
**Time:** 30-40 minutes  

---

## 📋 What You'll Learn

1. What coding agents are and when to use them
2. How to run Claude Code, Codex, and Pi agents
3. PTY mode (critical for success)
4. Background mode for long-running tasks
5. Real-world workflows (building, reviewing, parallel work)
6. Best practices and common pitfalls

---

## 🎯 Part 1: Core Concepts (10 min)

### What Are Coding Agents?

Coding agents are **AI-powered terminal tools** that can:
- Write code autonomously
- Fix bugs
- Review PRs
- Refactor codebases
- Run tests and iterate

**Available in Clawdbot:**
- **Claude Code** - Anthropic's official coding agent
- **Codex** - Uses GPT-5.2-codex (default model)
- **OpenCode** - Open-source alternative
- **Pi** - Multi-provider coding agent

### Why Use Them?

**Instead of:**
1. Asking Clawdbot to generate code
2. Manually copying/pasting
3. Manually running tests
4. Manually fixing errors

**You get:**
1. Agent autonomously codes in your project
2. Agent runs tests, sees errors, iterates
3. Agent commits and pushes when done
4. You review the final result

**Key insight:** Orchestrator mode > manual coding. Let agents do the heavy lifting.

---

## 🔧 Part 2: Critical Concept - PTY Mode (5 min)

### What is PTY?

PTY (Pseudo-Terminal) = Simulated terminal for interactive programs.

**The Problem:**
Coding agents are **interactive terminal applications**. Without PTY:
- Output breaks (garbled text)
- Colors missing
- Agent may hang waiting for input
- Commands fail mysteriously

### The Solution: Always Use `pty:true`

**❌ Wrong:**
```bash
bash command:"claude 'Build a todo app'"
```

**✅ Correct:**
```bash
bash pty:true command:"claude 'Build a todo app'"
```

**Rule:** If it's Claude Code, Codex, Pi, or any coding agent → **pty:true**

---

## 🚀 Part 3: Basic Usage (10 min)

### Pattern 1: One-Shot Tasks

**Use case:** Quick edits, single files, small features

**Claude Code:**
```bash
bash pty:true workdir:~/project command:"claude 'Add error handling to auth.js'"
```

**Codex:**
```bash
bash pty:true workdir:~/project command:"codex exec 'Fix the TypeScript errors'"
```

**Pi:**
```bash
bash pty:true workdir:~/project command:"pi 'Refactor the API module'"
```

**Key parameters:**
- `pty:true` - Enable terminal mode
- `workdir:~/project` - Set working directory (agent only sees this folder)
- `command:"..."` - What to run

### Pattern 2: Background Mode

**Use case:** Long-running tasks (building apps, complex refactors)

**Start in background:**
```bash
bash pty:true workdir:~/project background:true command:"claude 'Build a REST API for todos'"
# Returns: sessionId (e.g., "abc123")
```

**Monitor progress:**
```bash
process action:log sessionId:abc123
```

**Check if still running:**
```bash
process action:poll sessionId:abc123
```

**Kill if needed:**
```bash
process action:kill sessionId:abc123
```

**Why background mode?**
- Long tasks don't block you
- Can run multiple agents in parallel
- Monitor progress without interrupting
- Continue other work

---

## 💡 Part 4: Real-World Workflows (15 min)

### Workflow 1: Building a Feature

**Goal:** Build a complete feature end-to-end

**Steps:**
```bash
# 1. Start agent in background (with PTY!)
bash pty:true workdir:~/myproject background:true command:"codex exec --full-auto 'Build a dark mode toggle component. Include tests.'"

# Returns sessionId: "xyz789"

# 2. Check progress every few minutes
process action:log sessionId:xyz789

# 3. Agent will:
#    - Create component files
#    - Write tests
#    - Run tests, fix failures
#    - Commit when done

# 4. Review the changes
cd ~/myproject
git log -1 --stat
git diff HEAD~1
```

**Flags explained:**
- `exec` - One-shot mode (exits when done)
- `--full-auto` - Auto-approves changes in workspace (safe)
- `--yolo` - No sandbox, no approvals (fastest, use with caution)

### Workflow 2: Reviewing PRs

**⚠️ CRITICAL:** Never review PRs in Clawdbot's own project folder!

**Safe approach - Clone to temp:**
```bash
# 1. Clone PR to temp directory
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR

# 2. Checkout the PR
gh pr checkout 130

# 3. Run review (with PTY!)
bash pty:true workdir:$REVIEW_DIR command:"codex review --base origin/main"

# 4. Clean up
trash $REVIEW_DIR
```

**Alternative - Git worktree:**
```bash
# 1. Create worktree for PR branch
git worktree add /tmp/pr-130-review pr-130-branch

# 2. Review in isolated worktree
bash pty:true workdir:/tmp/pr-130-review command:"codex review --base main"

# 3. Remove worktree after review
git worktree remove /tmp/pr-130-review
```

**Why?** Keeps your main project clean, prevents agent from wandering into sensitive files.

### Workflow 3: Parallel Issue Fixing

**Goal:** Fix multiple issues simultaneously

**Setup:**
```bash
# 1. Create worktrees for each issue
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 2. Launch Codex in each (background + PTY!)
bash pty:true workdir:/tmp/issue-78 background:true command:"pnpm install && codex --yolo 'Fix issue #78: Login timeout error. Commit and push.'"

bash pty:true workdir:/tmp/issue-99 background:true command:"pnpm install && codex --yolo 'Fix issue #99: Memory leak in WebSocket. Commit and push.'"

# 3. Monitor all sessions
process action:list

# 4. Check progress on each
process action:log sessionId:abc123
process action:log sessionId:def456

# 5. Create PRs after fixes
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --title "fix: Login timeout error" --body "Fixes #78"

cd /tmp/issue-99 && git push -u origin fix/issue-99
gh pr create --title "fix: WebSocket memory leak" --body "Fixes #99"

# 6. Cleanup worktrees
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

**Result:** Fixed 2 issues in parallel, created 2 PRs, all in <30 minutes.

### Workflow 4: Batch PR Reviews

**Goal:** Review multiple PRs quickly

**Setup:**
```bash
# 1. Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# 2. Launch review army (all with PTY!)
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #86. git diff origin/main...origin/pr/86'"

bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #87. git diff origin/main...origin/pr/87'"

bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #88. git diff origin/main...origin/pr/88'"

# 3. Monitor all reviews
process action:list

# 4. Collect reviews and post to GitHub
process action:log sessionId:abc123 > review-86.txt
gh pr comment 86 --body-file review-86.txt
```

---

## 🎓 Part 5: Agent-Specific Tips (5 min)

### Claude Code

**Best for:**
- General coding tasks
- Modern frameworks (React, Next.js)
- TypeScript/JavaScript projects

**Usage:**
```bash
bash pty:true workdir:~/project command:"claude 'Your task'"
```

**No special flags** - Claude Code is straightforward.

### Codex (GPT-5.2)

**Best for:**
- Complex refactoring
- Large codebases
- Python/Django/Flask
- PR reviews

**Requires git repo:**
```bash
# Quick scratch work
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init
bash pty:true workdir:$SCRATCH command:"codex exec 'Your task'"
```

**Flags:**
- `exec "task"` - One-shot execution
- `--full-auto` - Auto-approve in workspace
- `--yolo` - No approvals (fastest)

### Pi Coding Agent

**Best for:**
- Multi-provider flexibility
- Custom model selection
- Non-interactive tasks

**Installation:**
```bash
npm install -g @mariozechner/pi-coding-agent
```

**Usage:**
```bash
# Default provider/model
bash pty:true workdir:~/project command:"pi 'Your task'"

# Custom provider
bash pty:true command:"pi --provider openai --model gpt-4o-mini -p 'Your task'"

# Non-interactive mode (still use PTY!)
bash pty:true command:"pi -p 'Summarize src/'"
```

**Bonus:** Pi has Anthropic prompt caching enabled (90% cost savings on repetitive work)!

---

## ⚠️ Part 6: Common Pitfalls & Best Practices (5 min)

### ❌ Common Mistakes

1. **Forgetting pty:true**
   - Result: Broken output, hanging agent
   - Fix: Always include `pty:true`

2. **Running Codex outside git repo**
   - Result: "not a git repository" error
   - Fix: `git init` in scratch dirs

3. **Checking out branches in ~/Projects/clawdbot/**
   - Result: Breaking your LIVE Clawdbot instance
   - Fix: Use temp dirs or worktrees

4. **Spawning agent in ~/clawd/**
   - Result: Agent reads SOUL.md, gets confused about org chart
   - Fix: Use specific project directories

5. **Not monitoring background tasks**
   - Result: Don't know if agent succeeded/failed
   - Fix: Regularly check with `process action:log`

6. **Killing sessions too early**
   - Result: Incomplete work
   - Fix: Be patient, agents iterate slowly but thoroughly

### ✅ Best Practices

1. **Use workdir to constrain scope**
   - Agent only sees relevant files
   - Faster analysis, less distraction

2. **Background mode for >5 min tasks**
   - Don't block your workflow
   - Run multiple agents in parallel

3. **Auto-notify on completion**
   - Add wake trigger to prompt:
   ```bash
   bash pty:true background:true command:"codex exec 'Build feature.
   
   When done, run: clawdbot gateway wake --text \"Done: Built feature\" --mode now'"
   ```
   - Get instant notification instead of waiting for heartbeat

4. **Progress updates**
   - Tell user when you start background task
   - Update only on milestones/questions/completion
   - If you kill a session, say why immediately

5. **Respect tool choice**
   - User asks for Codex? Use Codex.
   - Don't silently take over coding yourself
   - Orchestrator mode > manual coding

6. **Git worktrees for parallel work**
   - Safe isolation
   - Keep main branch clean
   - Easy cleanup

---

## 🛠️ Part 7: Your Action Plan (5 min)

### Quick Win: Try Claude Code

**Goal:** Experience the workflow with a simple task

**Steps:**
1. Pick a project with a small TODO item
2. Run Claude Code:
   ```bash
   bash pty:true workdir:~/yourproject command:"claude 'Add TypeScript types to config.js'"
   ```
3. Watch the output
4. Review the changes: `git diff`
5. If good, commit: `git add . && git commit -m "feat: add TypeScript types"`

**Time:** 5-10 minutes

### Next Level: Background Task

**Goal:** Build a small feature end-to-end

**Steps:**
1. Start in background:
   ```bash
   bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Build a /health endpoint for the API'"
   ```
2. Monitor progress:
   ```bash
   process action:log sessionId:XXX
   ```
3. Review when done
4. Test the feature
5. Create PR

**Time:** 20-30 minutes

### Advanced: Parallel PR Reviews

**Goal:** Review 3+ PRs simultaneously

**Steps:**
1. Fetch PR refs
2. Launch parallel Codex reviewers
3. Monitor all sessions
4. Post reviews to GitHub

**Time:** 30-45 minutes for 3 PRs

---

## 📊 Success Metrics

Track these to measure impact:

1. **Time savings**
   - Before: Manual coding time
   - After: Agent coding time
   - Target: 50-70% reduction

2. **Code quality**
   - Tests included?
   - Error handling added?
   - Edge cases covered?

3. **Iteration speed**
   - How many fix/test cycles?
   - Agent autonomy (did it self-correct?)

4. **Parallel capacity**
   - How many agents running simultaneously?
   - Workload distribution

---

## 🎓 Key Takeaways

1. **pty:true is mandatory** - Never forget it for coding agents
2. **workdir constrains scope** - Keeps agents focused
3. **Background mode for long tasks** - Don't block your workflow
4. **Orchestrator > manual** - Let agents code, you review
5. **Git worktrees for safety** - Isolate risky work
6. **Monitor, don't interfere** - Trust the process

---

## 📚 Resources

- **Coding Agent skill:** `C:\Users\vl\AppData\Roaming\npm\node_modules\clawdbot\skills\coding-agent\SKILL.md`
- **Process tool docs:** Check Clawdbot docs for process management
- **Claude Code:** https://www.anthropic.com/claude/code
- **Codex:** Your ~/.codex/config.toml

---

## 🚀 Quick Reference Card

**One-shot task:**
```bash
bash pty:true workdir:~/project command:"claude 'Task'"
```

**Background task:**
```bash
bash pty:true workdir:~/project background:true command:"codex exec 'Task'"
# Returns sessionId
```

**Monitor:**
```bash
process action:log sessionId:XXX
```

**Kill:**
```bash
process action:kill sessionId:XXX
```

**Review PR safely:**
```bash
git worktree add /tmp/pr-review pr-branch
bash pty:true workdir:/tmp/pr-review command:"codex review"
git worktree remove /tmp/pr-review
```

---

**Study time:** ~40 minutes  
**First hands-on:** ~10 minutes  
**ROI:** 50-70% faster coding, autonomous iteration, parallel workflows ✨

Ready to try it? Start with the "Quick Win" section above!
