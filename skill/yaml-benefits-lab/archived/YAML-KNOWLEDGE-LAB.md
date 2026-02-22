# YAML Knowledge Files Lab

## The Real Question

**Why use YAML files in `knowledge/` folder instead of markdown (.md) for everything?**

---

## The Pattern You Saw

```
my-skill/
├── SKILL.md              # Main skill definition (humans read)
├── scripts/              # Python tools (machines run)
│   ├── analyzer.py
│   └── processor.py
└── knowledge/            # Structured data (scripts READ)
    ├── api-endpoints.yaml
    ├── error-codes.yaml
    └── rules.yaml
```

**Key insight:** The Python scripts in `scripts/` need to **programmatically read** the knowledge files!

---

## The Core Difference

### Markdown = Human Documentation
- ✅ Great for explanations, guides, READMEs
- ✅ Free-form, natural language
- ❌ **Hard for scripts to parse**
- ❌ No standard structure
- ❌ Brittle when scripts try to extract data

### YAML = Machine-Readable Data
- ✅ **Easy for scripts to parse** (1-2 lines of code)
- ✅ Standard structure
- ✅ Type-safe (strings, numbers, lists, objects)
- ✅ Validate data schemas
- ❌ Less flexible for prose

---

## Real-World Example: API Helper Skill

### ❌ Bad: Markdown Knowledge (Hard to Parse)

**knowledge/endpoints.md**
```markdown
# API Endpoints

## User Service
- Base URL: https://api.example.com/v1
- Get user: GET /users/{id}
- Create user: POST /users
- Update user: PUT /users/{id}

## Payment Service  
- Base URL: https://api.example.com/payments
- Process payment: POST /process
- Refund: POST /refund/{transaction_id}
```

**scripts/call_api.py** (parsing nightmare!)
```python
# How do you parse this reliably? 😱
import re

def get_endpoint(service, action):
    with open('../knowledge/endpoints.md') as f:
        content = f.read()
    
    # Fragile regex parsing - breaks if format changes
    # What if someone adds extra spaces?
    # What if the markdown structure changes?
    # This is a MESS!
    pattern = rf"## {service}.*?- {action}: (\w+) (/[^\n]+)"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return {"method": match.group(1), "path": match.group(2)}
    return None

# Fragile! Hard to maintain!
endpoint = get_endpoint("User Service", "Get user")
```

---

### ✅ Good: YAML Knowledge (Easy to Parse)

**knowledge/endpoints.yaml**
```yaml
# API Endpoints Knowledge Base
# Scripts can easily read this structured data

user_service:
  base_url: https://api.example.com/v1
  endpoints:
    get_user:
      method: GET
      path: /users/{id}
      description: Retrieve user by ID
    
    create_user:
      method: POST
      path: /users
      description: Create new user
    
    update_user:
      method: PUT
      path: /users/{id}
      description: Update existing user

payment_service:
  base_url: https://api.example.com/payments
  endpoints:
    process_payment:
      method: POST
      path: /process
      description: Process a payment
    
    refund:
      method: POST
      path: /refund/{transaction_id}
      description: Refund a transaction
```

**scripts/call_api.py** (clean and simple!)
```python
import yaml

def load_endpoints():
    """Load API endpoints from YAML - clean and reliable!"""
    with open('../knowledge/endpoints.yaml') as f:
        return yaml.safe_load(f)

def get_endpoint(service, action):
    """Get endpoint details - simple dictionary access!"""
    endpoints = load_endpoints()
    return endpoints[service]['endpoints'][action]

# Clean! Easy! Reliable!
endpoint = get_endpoint('user_service', 'get_user')
print(f"{endpoint['method']} {endpoint['path']}")
# Output: GET /users/{id}
```

---

## More Examples: Why YAML Wins

### Example 1: Error Code Lookup

**❌ Markdown (hard to parse)**
```markdown
# Error Codes
- 1001: Invalid user ID
- 1002: User not found
- 2001: Payment failed
- 2002: Insufficient funds
```

**✅ YAML (easy to parse)**
```yaml
error_codes:
  1001:
    message: Invalid user ID
    severity: warning
    action: Validate input format
  
  1002:
    message: User not found
    severity: error
    action: Check user exists before operation
  
  2001:
    message: Payment failed
    severity: critical
    action: Contact payment provider
  
  2002:
    message: Insufficient funds
    severity: error
    action: Notify user to add funds
```

**Python script**:
```python
import yaml

def get_error_info(code):
    with open('../knowledge/error_codes.yaml') as f:
        errors = yaml.safe_load(f)
    return errors['error_codes'][code]

# Usage
error = get_error_info(1002)
print(f"Error: {error['message']}")
print(f"Action: {error['action']}")
```

---

### Example 2: Business Rules

**❌ Markdown (ambiguous, hard to validate)**
```markdown
# Discount Rules
- If cart total > $100, apply 10% discount
- If user is premium member, apply 15% discount
- If items > 5, free shipping
```

**✅ YAML (structured, queryable)**
```yaml
discount_rules:
  cart_value_discount:
    condition:
      field: cart_total
      operator: greater_than
      value: 100
    action:
      type: percentage
      value: 10
  
  premium_member_discount:
    condition:
      field: user_tier
      operator: equals
      value: premium
    action:
      type: percentage
      value: 15
  
  free_shipping:
    condition:
      field: item_count
      operator: greater_than
      value: 5
    action:
      type: free_shipping
      value: true
```

**Python script**:
```python
import yaml

def apply_discounts(cart_total, user_tier, item_count):
    with open('../knowledge/discount_rules.yaml') as f:
        rules = yaml.safe_load(f)['discount_rules']
    
    discounts = []
    
    for rule_name, rule in rules.items():
        condition = rule['condition']
        # Programmatically evaluate conditions
        if evaluate_condition(condition, locals()):
            discounts.append(rule['action'])
    
    return discounts
```

---

## Key Benefits Summary

| Aspect | Markdown Knowledge | YAML Knowledge |
|--------|-------------------|----------------|
| **Parsing** | Complex regex, fragile | 2 lines: open + yaml.load() |
| **Validation** | No schema | Can validate structure |
| **Querying** | String searching | Dictionary access |
| **Updating** | Breaks scripts | Scripts auto-update |
| **Type Safety** | Everything is strings | Proper types (int, bool, list) |
| **Nesting** | Hard to represent | Natural hierarchies |
| **Comments** | Mixed with content | Clear separation |
| **Script Complexity** | High (custom parsers) | Low (standard library) |

---

## When to Use Each

### Use YAML in `knowledge/` when:
- ✅ Scripts need to **read** the data programmatically
- ✅ Data is **structured** (lists, hierarchies, key-value)
- ✅ Multiple scripts **share** the same knowledge
- ✅ You need **validation** or **querying**
- ✅ Data changes **frequently**
- ✅ **Example:** API endpoints, error codes, rules, configs, lookup tables

### Use Markdown in docs/ when:
- ✅ **Humans** are the primary readers
- ✅ Content is **explanatory** (guides, READMEs, tutorials)
- ✅ You need **formatting** (bold, links, code blocks)
- ✅ Natural language **prose**
- ✅ No script parsing needed
- ✅ **Example:** SKILL.md, README.md, USAGE.md, GUIDE.md

---

## Real Skill Structure

```
data-analyzer-skill/
├── SKILL.md                    # ← Markdown: Human-readable skill definition
├── README.md                   # ← Markdown: Usage guide
├── scripts/                    # ← Python tools
│   ├── analyze.py              # Reads from knowledge/
│   ├── validate.py             # Reads from knowledge/
│   └── report.py               # Reads from knowledge/
├── knowledge/                  # ← YAML: Machine-readable structured data
│   ├── data-sources.yaml       # Scripts parse this
│   ├── validation-rules.yaml   # Scripts parse this
│   └── output-formats.yaml     # Scripts parse this
└── docs/                       # ← Markdown: Human documentation
    ├── INSTALLATION.md
    ├── EXAMPLES.md
    └── TROUBLESHOOTING.md
```

**The pattern:**
- `SKILL.md` + `docs/` = **Humans read** (Markdown)
- `knowledge/` = **Scripts read** (YAML)
- `scripts/` = **Use knowledge** to do work

---

## Code Comparison

### Parsing Markdown (Don't Do This!)

```python
# Fragile, error-prone, hard to maintain
import re

def get_api_endpoint(file_path, service_name):
    with open(file_path) as f:
        content = f.read()
    
    # Brittle regex - breaks easily
    pattern = rf"## {service_name}.*?URL: ([^\n]+)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1) if match else None

# Hope the markdown format never changes! 🤞
```

### Parsing YAML (Do This!)

```python
# Clean, reliable, maintainable
import yaml

def get_api_endpoint(file_path, service_name):
    with open(file_path) as f:
        data = yaml.safe_load(f)
    return data['services'][service_name]['base_url']

# Structure is guaranteed! ✅
```

---

## Research Findings

**Quote from GitHub Issue #23:**
> "Markdown is not meant to be used for structured data. It is great to output simple files, mostly for mixed-content documents (rich text, different headings, tables), but hard to parse it back."

**StackShare comparison:**
> "Markdown is a lightweight markup language used for content formatting, while YAML is primarily used for data serialization and configuration files."

**Tech4Teaching Blog:**
> "Markdown provides readability and natural structure for human writers, while YAML adds the precision and hierarchy that AI systems rely on for retrieval, linking, and reasoning."

**X (Twitter) on YAML for LLMs:**
> "YAML is easier to read and edit than JSON while still being machine-parseable. You want to reduce the prompt size, especially when sending long structured context (like a knowledge base) to the model."

---

## Bottom Line

**Markdown = Human Documentation**  
**YAML = Machine Data**

If your `scripts/` need to **read** it → use YAML  
If your **humans** need to **read** it → use Markdown

**Both have their place in a well-designed skill!**

---

## Try It Yourself

See the practical examples in:
- `yaml-benefits-lab/skill-with-knowledge/` (coming next!)

Where I'll build a complete example skill showing:
- `SKILL.md` (markdown documentation)
- `knowledge/*.yaml` (structured data for scripts)
- `scripts/*.py` (reading and using the YAML knowledge)

This will make the benefit crystal clear! 🎯
