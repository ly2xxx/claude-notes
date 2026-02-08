# Claude Code Agent Teams - Hands-On Lab (30-60 min)

**Created:** 2026-02-08  
**Topic:** Agent Teams (announced Feb 5, 2026)  
**Duration:** 30-60 minutes  
**Prerequisites:** Claude Code VSCode extension installed

---

## 📋 What You'll Learn

- The difference between **subagents** and **Agent Teams**
- How to enable and configure Agent Teams
- When to use teams vs. single agents
- Practical parallel workflows (code review, multi-module development)

---

## 🎯 What Are Agent Teams?

**Key Innovation (Feb 2026):** Multiple *independent* Claude Code instances that:
- Run in parallel with separate context windows
- Communicate directly with each other (not just back to main agent)
- Coordinate via shared task lists
- Self-organize work distribution

### Agent Teams vs Subagents

| Feature | Subagents | Agent Teams |
|---------|-----------|-------------|
| Context | Inside main session | Each has own context window |
| Communication | Results return to main only | Direct peer-to-peer messaging |
| Coordination | Main agent orchestrates | Self-coordinate via task list |
| Token cost | Moderate | Scales with team size |
| Best for | Sequential subtasks | Parallel independent work |

---

## 🚀 Lab Setup (5 minutes)

### Step 1: Update Claude Code

```bash
# VSCode: Open Command Palette (Ctrl+Shift+P)
# Type: "Extensions: Check for Extension Updates"
# Update "Claude Code" if available
```

Or install/update via:
```bash
code --install-extension anthropic.claude-code
```

### Step 2: Enable Agent Teams (Experimental)

Create/edit `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "tmux"
}
```

**Windows location:** `C:\Users\<username>\.claude\settings.json`

**Note:** 
- `teammateMode` options: `"in-process"`, `"tmux"`, `"iTerm2"`, `"auto"` (default)
- For Windows without tmux, use `"in-process"` and navigate with Shift+↑/↓

### Step 3: Restart VSCode

Close and reopen VSCode to load the new settings.

---

## 🧪 Exercise 1: Your First Agent Team (15 min)

**Goal:** Create a 2-person team to review a codebase in parallel.

### Scenario
You have a small Python project with multiple modules. You want:
- Agent A: Review `utils.py` and `config.py`
- Agent B: Review `main.py` and `tests/`

### Setup a Test Project

```bash
mkdir ~/claude-teams-lab
cd ~/claude-teams-lab
```

Create sample files:

**main.py:**
```python
from utils import calculate_total, format_output
from config import settings

def process_data(items):
    total = calculate_total(items)
    return format_output(total, settings['currency'])

if __name__ == "__main__":
    data = [100, 200, 300]
    result = process_data(data)
    print(result)
```

**utils.py:**
```python
def calculate_total(items):
    return sum(items)

def format_output(value, currency='USD'):
    return f"{currency} {value:.2f}"
```

**config.py:**
```python
settings = {
    'currency': 'USD',
    'tax_rate': 0.2,
    'debug': True
}
```

**tests/test_utils.py:**
```python
from utils import calculate_total

def test_calculate_total():
    assert calculate_total([1, 2, 3]) == 6
```

### Task: Launch Agent Team

Open Claude Code in VSCode (Cmd/Ctrl+Shift+P → "Claude Code: Start")

**Prompt:**
```
Create an agent team with 2 teammates:
1. "reviewer-utils" - Review utils.py and config.py for code quality, edge cases, and best practices
2. "reviewer-main" - Review main.py and tests/ for logic errors and test coverage

Each teammate should:
- Document findings in a markdown file (findings-utils.md / findings-main.md)
- Suggest specific improvements
- Run in parallel

Use the Sonnet model for both.
```

### What to Observe

✅ **Team spawning:** Watch Claude create 2 independent agents  
✅ **Parallel execution:** Both agents work simultaneously  
✅ **Task completion:** Each produces a findings file  
✅ **Self-coordination:** Agents claim tasks from shared list  

### Expected Outcome

- `findings-utils.md` with utils/config review
- `findings-main.md` with main/tests review
- Total time < 5 min (vs. 8-10 min sequential)

---

## 🔬 Exercise 2: Task Dependencies (15 min)

**Goal:** Create a 3-agent team with dependent tasks.

### Scenario
Refactor a module with these steps:
1. Agent A: Analyze current code structure
2. Agent B: Write refactoring plan (depends on #1)
3. Agent C: Implement tests (depends on #2)

### Setup

Create `legacy_code.py`:

```python
def process(data, type):
    if type == 'sum':
        r = 0
        for i in data:
            r = r + i
        return r
    elif type == 'avg':
        r = 0
        for i in data:
            r = r + i
        return r / len(data)
    elif type == 'max':
        r = data[0]
        for i in data:
            if i > r:
                r = i
        return r
    else:
        return None
```

### Task: Dependent Workflow

**Prompt:**
```
Create 3-agent team for refactoring legacy_code.py:

Task list:
1. [analyzer] Analyze current code - identify code smells, duplication, edge cases
2. [architect] Design refactored version (→ depends on #1) - propose clean structure
3. [tester] Write comprehensive tests (→ depends on #2) - cover edge cases

Use dependency order. Enable "plan approval" for architect and tester.
Use delegate mode (Shift+Tab) - team lead coordinates only.
```

### What to Observe

✅ **Sequential execution:** Task 2 waits for task 1  
✅ **Plan approval:** You review architect's plan before execution  
✅ **Delegate mode:** Lead doesn't code, only coordinates  

### Expected Outcome

- Analysis document
- Refactoring proposal (requiring your approval)
- Test suite (pytest format)

---

## 🎮 Exercise 3: Real-World Scenario (20 min)

**Goal:** Multi-module feature implementation.

### Scenario
Add a "user authentication" feature across 3 modules:
- Backend API endpoint
- Database schema
- Frontend form component

### Create Starter Project

```bash
mkdir auth-feature
cd auth-feature
mkdir backend frontend database
```

**backend/api.py:**
```python
# Existing API
def get_users():
    return {"users": []}
```

**database/schema.sql:**
```sql
-- Existing schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT
);
```

**frontend/app.js:**
```javascript
// Existing app
function fetchUsers() {
    fetch('/api/users').then(r => r.json()).then(console.log);
}
```

### Task: Parallel Feature Development

**Prompt:**
```
Create 3-agent team to add login/authentication feature:

1. backend-dev: Add POST /auth/login endpoint to backend/api.py
   - Accept username/password
   - Return JWT token
   - Handle errors

2. db-dev: Add password_hash column to database/schema.sql
   - Migration script
   - Indexing for username lookups

3. frontend-dev: Create login form in frontend/login.js
   - Username/password fields
   - Call /auth/login endpoint
   - Store token in localStorage

Work in parallel. Each module is independent (no file conflicts).
Document integration points in INTEGRATION.md.
```

### What to Observe

✅ **Parallel development:** All 3 agents work simultaneously  
✅ **No conflicts:** Separate directories prevent collisions  
✅ **Integration doc:** Agents coordinate contract (API spec)  

### Expected Outcome

- Working backend endpoint
- Database migration
- Frontend login component
- Integration documentation

**Bonus:** Ask the team lead to create a 4th agent for integration testing.

---

## 🧠 Best Practices (Learned from Research)

### ✅ DO Use Agent Teams For:
- **Code reviews** across multiple modules
- **Parallel exploration** (e.g., testing 3 different approaches)
- **Multi-module features** with clear boundaries
- **Documentation sprints** (API docs, README, guides)

### ❌ DON'T Use Agent Teams For:
- **Simple tasks** (use single agent or subagents)
- **Sequential workflows** (dependencies negate parallelism)
- **Single-file editing** (conflict risk)
- **Token-constrained work** (cost scales linearly with team size)

### 🛡️ Prevent File Conflicts:
1. Assign clear directory/file ownership per agent
2. Use task dependencies for shared files
3. Review `.claude/teams/` config if conflicts occur

### 💰 Token Management:
- 5-person team = 5× token cost minimum
- Use subagents for simple subtasks
- Reserve teams for discussions, reviews, parallel exploration

---

## 🎓 Advanced Techniques

### 1. Competing Hypotheses
```
Create 3 agents to solve the same algorithm challenge using different approaches:
- Agent A: Brute force
- Agent B: Dynamic programming
- Agent C: Greedy algorithm

Each documents time/space complexity. Team lead compares results.
```

### 2. Multi-Language Documentation
```
Create 4 agents to translate README.md:
- Agent A: Japanese
- Agent B: Korean
- Agent C: Chinese
- Agent D: Spanish

Maintain consistent technical terminology across all versions.
```

### 3. Architecture Review Panel
```
Create 3 senior-engineer agents to review proposed system architecture:
- Agent A: Security perspective
- Agent B: Scalability perspective
- Agent C: Maintainability perspective

Discuss trade-offs and vote on approach.
```

---

## 🔍 Debugging & Troubleshooting

### Teams Not Spawning?
```bash
# Check settings loaded:
cat ~/.claude/settings.json

# Verify experimental flag:
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS

# Restart VSCode completely
```

### High Token Usage?
- Switch to Haiku/Sonnet instead of Opus
- Reduce team size
- Use subagents for simpler tasks
- Check if delegate mode is enabled (Shift+Tab)

### File Conflicts?
- Review task assignments in team prompt
- Add explicit "do not modify X.py" instructions
- Use `.claude/teams/team-name.json` to check config

---

## 📊 Comparing Your Results

**Single Agent Baseline:**
- Exercise 1 (code review): ~8-10 minutes
- Exercise 2 (refactor): ~12-15 minutes
- Exercise 3 (feature): ~20-25 minutes

**Agent Teams Target:**
- Exercise 1: ~3-5 minutes (60% faster)
- Exercise 2: ~8-10 minutes (33% faster, dependencies limit)
- Exercise 3: ~8-12 minutes (60% faster, high parallelism)

**Trade-off:** Speed gain vs. 2-5× token cost

---

## 🎁 Bonus Challenge (If Time Permits)

**Task:** Combine Agent Teams with Checkpoints

1. Create a 3-agent team to refactor a complex module
2. Enable checkpoints (automatic via Opus 4.6)
3. Let agents explore 3 different refactoring approaches in parallel
4. Use Esc+Esc to rewind if an approach fails
5. Compare all 3 approaches and pick the best

**Why:** Checkpoints let you safely explore multiple parallel paths and rewind individually.

---

## 📚 Further Reading

- [Official Agent Teams Docs](https://code.claude.com/docs/en/agent-teams)
- [Claude Opus 4.6 Announcement](https://www.anthropic.com/news/claude-opus-4-6)
- [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview)
- [Checkpoints & Autonomous Work](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)

---

## ✅ Lab Completion Checklist

- [ ] Enabled experimental agent teams flag
- [ ] Created first 2-agent team (Exercise 1)
- [ ] Tested task dependencies (Exercise 2)
- [ ] Built real multi-module feature (Exercise 3)
- [ ] Compared speed: teams vs. single agent
- [ ] Identified use cases for your own projects

---

## 🎯 Key Takeaways

1. **Agent Teams ≠ Subagents:** Separate contexts, direct communication, self-coordination
2. **Best for parallel work:** Code reviews, multi-module features, competing approaches
3. **Token cost scales:** 1 lead + N teammates = (N+1)× cost minimum
4. **Prevent conflicts:** Clear ownership boundaries per agent
5. **Combine with checkpoints:** Safe exploration of multiple paths

**Production-ready?** Still experimental (as of Feb 2026), but powerful for the right use cases.

---

**Next Steps:**
- Apply to your current projects (identify parallelizable work)
- Experiment with team sizes (2-5 agents optimal)
- Track token costs vs. time savings
- Report bugs/feedback to Anthropic

**Happy teaming! 🤖🤖🤖**
