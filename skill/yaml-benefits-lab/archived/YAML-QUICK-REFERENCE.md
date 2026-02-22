# YAML Quick Reference for Skills

## Basic Syntax

### Key-Value Pairs
```yaml
name: my-skill
version: 1.0.0
enabled: true
```

### Strings (quotes optional for simple strings)
```yaml
simple: no quotes needed
with_spaces: "use quotes if needed"
with_colon: "or if it contains: colons"
```

### Numbers and Booleans
```yaml
count: 42
price: 19.99
enabled: true
disabled: false
empty: null
```

### Lists/Arrays
```yaml
# Method 1: Dash notation
fruits:
  - apple
  - banana
  - orange

# Method 2: Inline (like JSON)
fruits: [apple, banana, orange]
```

### Objects/Dictionaries
```yaml
# Method 1: Indented
person:
  name: John
  age: 30
  city: London

# Method 2: Inline
person: {name: John, age: 30, city: London}
```

### Nested Structures
```yaml
skill:
  metadata:
    name: analyzer
    version: 1.0.0
  config:
    settings:
      timeout: 30
      retry: 3
```

## Comments

```yaml
# Full line comment
name: my-skill  # Inline comment
version: 1.0.0  # Another inline comment
```

## Multi-line Strings

### Literal Block (preserves newlines)
```yaml
description: |
  This is line one.
  This is line two.
  Newlines are preserved.
```

### Folded Block (folds into one line)
```yaml
description: >
  This long text
  will be folded into
  a single line with spaces.
```

### Multi-line with Chomping
```yaml
# Keep trailing newline
text: |
  Line 1
  Line 2

# Remove trailing newline  
text: |-
  Line 1
  Line 2

# Keep all trailing newlines
text: |+
  Line 1
  Line 2

```

## Anchors & References

### Define an Anchor
```yaml
default_settings: &defaults
  timeout: 30
  retry: 3
  log: true
```

### Reference an Anchor
```yaml
skill_a:
  name: processor
  settings: *defaults  # Uses all settings from &defaults
```

### Merge Anchors
```yaml
skill_b:
  name: analyzer
  <<: *defaults    # Merge all default settings
  timeout: 60      # Override just one value
```

## Advanced Features

### Multiple Documents in One File
```yaml
---
# Document 1
skill: first-skill
version: 1.0.0
---
# Document 2
skill: second-skill
version: 2.0.0
```

### Complex Anchors
```yaml
base_auth: &auth
  type: oauth2
  refresh: true

services:
  gmail:
    <<: *auth
    scope: email
  
  calendar:
    <<: *auth
    scope: calendar
```

### Lists of Objects
```yaml
skills:
  - name: analyzer
    version: 1.0.0
    enabled: true
  
  - name: processor
    version: 2.0.0
    enabled: false
```

## Common Gotchas

### ❌ Bad Indentation
```yaml
skill:
  name: test
   version: 1.0.0  # Mixed indentation - ERROR!
```

### ✅ Good Indentation
```yaml
skill:
  name: test
  version: 1.0.0  # Consistent indentation
```

### ❌ Colon in String Without Quotes
```yaml
title: My Skill: The Best One  # ERROR - colon confuses parser
```

### ✅ Quoted String
```yaml
title: "My Skill: The Best One"  # Good
```

### ❌ Tab Characters
```yaml
skill:
→ name: test  # Tab character - ERROR!
```

### ✅ Spaces Only
```yaml
skill:
  name: test  # Spaces only - Good
```

## YAML vs JSON Examples

### JSON
```json
{
  "skill": {
    "name": "analyzer",
    "settings": {
      "timeout": 30,
      "enabled": true
    }
  }
}
```

### Equivalent YAML
```yaml
skill:
  name: analyzer
  settings:
    timeout: 30
    enabled: true
```

## Best Practices for Skills

1. **Use comments liberally**
   ```yaml
   # Why this timeout value?
   timeout: 30  # Optimal for most API calls
   ```

2. **Use anchors for repeated settings**
   ```yaml
   default_config: &defaults
     timeout: 30
     retry: 3
   
   skill_a:
     <<: *defaults
   ```

3. **Use literal blocks for prompts**
   ```yaml
   prompt: |
     You are a helpful assistant.
     
     Focus on:
     - Clarity
     - Accuracy
     - Helpfulness
   ```

4. **Keep consistent indentation (2 spaces)**
   ```yaml
   skill:
     name: test
     config:
       setting: value
   ```

5. **Document complex configurations**
   ```yaml
   # Performance tuning parameters
   # Tested with 1000+ files, optimal values found:
   settings:
     batch_size: 50     # Files per batch
     timeout: 30        # Seconds per request
     max_retries: 3     # Before giving up
   ```

## Tools & Validation

- **Online Validators:**
  - https://www.yamllint.com/
  - https://jsonformatter.org/yaml-validator

- **VS Code Extensions:**
  - YAML by Red Hat
  - YAML Language Support

- **Command Line:**
  ```bash
  # Python
  python -c "import yaml; yaml.safe_load(open('file.yaml'))"
  
  # Node.js
  npm install -g yaml-cli
  yaml validate file.yaml
  ```

## Quick Tips

✅ **Do:**
- Use 2-space indentation
- Add comments for complex logic
- Quote strings with special characters
- Use anchors to reduce duplication
- Use literal blocks for multi-line text

❌ **Don't:**
- Mix tabs and spaces
- Forget to indent nested items
- Use inconsistent spacing
- Skip comments on non-obvious settings
- Create deeply nested structures (keep it simple)

---

**Remember:** YAML prioritizes human readability. When in doubt, choose the format that's easiest to read and understand!
