# Hands-On YAML Exercise

Try these exercises to master YAML for Claude Skills!

## Exercise 1: Convert JSON to YAML

Convert this JSON skill configuration to YAML. Add comments explaining each section.

**JSON:**
```json
{
  "skill": "task-manager",
  "version": "1.0.0",
  "settings": {
    "max_tasks": 100,
    "auto_archive": true,
    "archive_days": 30
  },
  "priorities": ["low", "medium", "high", "urgent"]
}
```

**Your YAML (try before looking at answer):**
```yaml
# Write your YAML here!




```

<details>
<summary>Click to see answer</summary>

```yaml
# Task Manager Skill Configuration
skill: task-manager
version: 1.0.0

settings:
  max_tasks: 100        # Maximum active tasks allowed
  auto_archive: true    # Automatically archive completed tasks
  archive_days: 30      # Days before auto-archiving

# Task priority levels (lowest to highest)
priorities:
  - low
  - medium
  - high
  - urgent
```
</details>

---

## Exercise 2: Multi-line Strings

Create a YAML file for a "code-assistant" skill with a multi-line system prompt.

**Requirements:**
- Use literal block (`|`) for the system prompt
- Include at least 5 lines with proper formatting
- Add inline comments

**Try it:**
```yaml
# Write your solution here!




```

<details>
<summary>Click to see answer</summary>

```yaml
# Code Assistant Skill
skill: code-assistant
version: 2.0.0

# Main system prompt using literal block
system_prompt: |
  You are an expert coding assistant with knowledge of multiple programming languages.
  
  Your responsibilities:
  - Help debug code issues
  - Suggest improvements and optimizations
  - Explain complex concepts clearly
  - Follow language-specific best practices
  - Provide working code examples
  
  Always test your suggestions before providing them.

max_context_lines: 50  # Lines of code to analyze at once
```
</details>

---

## Exercise 3: Anchors & References

Create a YAML configuration for three skills that share common authentication settings.

**Requirements:**
- Define auth settings once using an anchor
- Three skills: `email-reader`, `calendar-sync`, `drive-manager`
- Each skill has different scopes but shares the auth config
- Use merge syntax (`<<:`)

**Try it:**
```yaml
# Write your solution here!




```

<details>
<summary>Click to see answer</summary>

```yaml
# Shared Configuration with Anchors

# Define common auth settings once
common_auth: &auth_base
  type: oauth2
  refresh_token: true
  token_expiry: 3600
  redirect_uri: http://localhost:8080/callback

# Skills using shared auth
skills:
  email_reader:
    name: Email Reader
    <<: *auth_base           # Merge all auth settings
    scope: email.read        # Specific to this skill
  
  calendar_sync:
    name: Calendar Sync
    <<: *auth_base
    scope: calendar.modify
  
  drive_manager:
    name: Drive Manager
    <<: *auth_base
    scope: drive.read drive.write
```
</details>

---

## Exercise 4: Complete Skill Configuration

Create a complete skill configuration for a "meeting-summarizer" that:

**Requirements:**
1. Has metadata (name, version, author, description)
2. Uses multi-line string for system prompt
3. Has configuration settings with comments
4. Includes output formatting options
5. Uses anchors for repeated settings
6. Has at least 10 inline comments explaining choices

**Try it:**
```yaml
# Write your complete skill here!




```

<details>
<summary>Click to see answer</summary>

```yaml
# ==========================================
# Meeting Summarizer Skill
# ==========================================
# Automatically generates summaries from meeting transcripts
# Author: Master Yang
# Last Updated: 2026-02-22

# Skill Metadata
metadata:
  name: meeting-summarizer
  version: 1.5.0
  author: Master Yang
  description: >
    Analyzes meeting transcripts and generates concise summaries
    with action items, key decisions, and participant contributions.
  tags:
    - meetings
    - productivity
    - summarization

# System Prompt - defines AI behavior
system_prompt: |
  You are a professional meeting summarizer with expertise in extracting key information.
  
  Your summaries should include:
  - Meeting overview (date, attendees, duration)
  - Key discussion points
  - Decisions made
  - Action items with owners
  - Follow-up topics
  
  Format output in clear sections using markdown.
  Be concise but capture all important details.

# Common settings anchor for reuse
default_limits: &limits
  max_transcript_length: 50000  # Characters
  max_participants: 20
  timeout_seconds: 60

# Configuration Settings
configuration:
  <<: *limits  # Merge default limits
  
  # Input processing
  accepted_formats:
    - txt          # Plain text transcripts
    - vtt          # Video subtitle format
    - srt          # Subtitle format
    - json         # Structured meeting data
  
  # Analysis depth
  analysis_level: detailed  # detailed | brief | executive
  
  # Language support
  languages:
    - en           # English
    - es           # Spanish
    - fr           # French
  
  # Feature toggles
  features:
    extract_action_items: true      # Identify action items
    identify_decisions: true        # Highlight decisions
    sentiment_analysis: false       # Analyze meeting tone
    speaker_attribution: true       # Attribute quotes to speakers

# Output Configuration
output:
  format: markdown                  # markdown | html | json
  include_timestamps: true          # Link to original timestamps
  include_participant_stats: true   # Who spoke most, etc.
  highlight_urgent_items: true      # Flag time-sensitive actions
  
  # Template structure
  sections:
    - overview
    - key_points
    - decisions
    - action_items
    - next_steps
  
  # Export options
  export:
    save_to_file: true
    filename_pattern: "meeting-summary-{date}.md"
    notify_participants: false      # Email summary to attendees

# Quality Settings
quality:
  min_transcript_quality: 0.8       # Skip poor quality transcripts (0-1)
  require_participant_names: true   # Reject if no names found
  verify_action_items: true         # Double-check extracted tasks

# ==========================================
# Usage Notes:
# - Optimized for English business meetings
# - Works best with clear audio transcriptions
# - Action items require explicit language ("will", "should", "must")
# - Adjust analysis_level based on meeting importance
# ==========================================
```
</details>

---

## Exercise 5: Debug YAML Errors

Find and fix the errors in this YAML:

```yaml
# Broken YAML - Find the errors!
skill: data-processor
version: 1.0.0
settings:
  timeout: 30
   max_retries: 3
  log_level: "info
description: This is a skill: it processes data
features:
  - feature1
  - feature2
	- feature3
nested:
  level1:
    level2:
      value: test
```

<details>
<summary>Click to see errors and fixes</summary>

**Errors Found:**

1. **Line 5:** Mixed indentation (3 spaces vs 2)
   ```yaml
   # ❌ Wrong
     timeout: 30
      max_retries: 3
   
   # ✅ Fixed
     timeout: 30
     max_retries: 3
   ```

2. **Line 6:** Unclosed quote
   ```yaml
   # ❌ Wrong
   log_level: "info
   
   # ✅ Fixed
   log_level: "info"
   # OR
   log_level: info
   ```

3. **Line 7:** Unquoted string with colon
   ```yaml
   # ❌ Wrong
   description: This is a skill: it processes data
   
   # ✅ Fixed
   description: "This is a skill: it processes data"
   ```

4. **Line 11:** Tab character instead of spaces
   ```yaml
   # ❌ Wrong (has tab)
   	- feature3
   
   # ✅ Fixed (spaces only)
     - feature3
   ```

**Corrected YAML:**
```yaml
# Fixed YAML
skill: data-processor
version: 1.0.0

settings:
  timeout: 30
  max_retries: 3
  log_level: info

description: "This is a skill: it processes data"

features:
  - feature1
  - feature2
  - feature3

nested:
  level1:
    level2:
      value: test
```
</details>

---

## Exercise 6: Real-World Skill

Create a YAML configuration for a skill you actually need! 

**Ideas:**
- Email sorter/filter
- Code documentation generator
- Research paper summarizer
- Social media post scheduler
- Budget analyzer

**Your Custom Skill:**
```yaml
# Create your own skill here!
# Include:
# - Metadata
# - System prompt (multi-line)
# - Configuration with comments
# - At least one anchor/reference
# - Multiple sections




```

---

## Challenge: Convert Your Existing Skills

If you have any existing JSON configuration files:

1. Pick one
2. Convert it to YAML
3. Add helpful comments
4. Use anchors where appropriate
5. Format multi-line strings properly

Compare the before/after readability!

---

## Validation Tips

**Online Tools:**
- https://www.yamllint.com/
- https://jsonformatter.org/yaml-validator

**VS Code:**
- Install "YAML" extension by Red Hat
- Get instant syntax validation
- Auto-formatting with Shift+Alt+F

**Python Quick Check:**
```bash
python -c "import yaml; yaml.safe_load(open('your-file.yaml'))"
```

---

## Next Steps

1. ✅ Complete all exercises
2. ✅ Convert one existing JSON config to YAML
3. ✅ Add this lab to your bookmarks
4. ✅ Use YAML for all future skill configurations
5. ✅ Share your best YAML practices with the team!

Happy YAML learning! 🎉
