# Example Skill: API Helper

**Purpose:** Demonstrates WHY YAML is used for `knowledge/` files in skills.

---

## Structure

```
example-skill/
├── SKILL.md                    # ← Markdown: Human documentation
├── README.md                   # ← Markdown: You are here
├── scripts/                    # ← Python: Scripts that DO work
│   ├── api_client.py           # Reads knowledge/api-endpoints.yaml
│   └── error_handler.py        # Reads knowledge/error-codes.yaml
└── knowledge/                  # ← YAML: Structured data for scripts
    ├── api-endpoints.yaml      # API endpoint definitions
    └── error-codes.yaml        # Error code mappings
```

---

## The Key Insight

**Markdown** = For **humans** to read (documentation, guides)  
**YAML** = For **scripts** to read (structured data, configuration)

The Python scripts in `scripts/` need to **programmatically** access the data in `knowledge/`. YAML makes this trivial!

---

## Try It Yourself

### 1. Run the API Client Demo

```bash
cd example-skill
python scripts/api_client.py
```

**You'll see:**
- How easily Python loads YAML (2 lines!)
- Dictionary-based access to endpoints
- Type-safe boolean values (`requires_auth`)
- Easy querying (list services, list actions)

### 2. Run the Error Handler Demo

```bash
python scripts/error_handler.py
```

**You'll see:**
- Clean error code lookup
- Filtering by severity/category
- Formatted error messages
- Statistics generation

---

## Compare: YAML vs Markdown

### ❌ If `knowledge/` used Markdown

**api-endpoints.md:**
```markdown
## User Service
- Base URL: https://api.example.com/v1
- Get user: GET /users/{id}
- Create user: POST /users
```

**scripts/api_client.py (nightmare parsing):**
```python
import re

def get_endpoint(service, action):
    with open('knowledge/api-endpoints.md') as f:
        content = f.read()
    
    # Brittle regex - breaks if format changes!
    pattern = rf"## {service}.*?- {action}: (\w+) (/[^\n]+)"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return {"method": match.group(1), "path": match.group(2)}
    return None

# Fragile! Hard to maintain! 😱
```

**Problems:**
- ❌ Complex regex required
- ❌ Fragile (any markdown formatting change breaks it)
- ❌ No type safety (everything is a string)
- ❌ Hard to query/filter
- ❌ Manual parsing for every field

---

### ✅ With YAML (current implementation)

**knowledge/api-endpoints.yaml:**
```yaml
user_service:
  base_url: https://api.example.com/v1
  endpoints:
    get_user:
      method: GET
      path: /users/{id}
      requires_auth: true
```

**scripts/api_client.py (clean and simple):**
```python
import yaml

def get_endpoint(service, action):
    with open('knowledge/api-endpoints.yaml') as f:
        data = yaml.safe_load(f)
    return data[service]['endpoints'][action]

# Clean! Reliable! Easy! ✅
```

**Benefits:**
- ✅ Simple parsing (2 lines)
- ✅ Robust (structure is guaranteed)
- ✅ Type-safe (`requires_auth` is boolean, not string)
- ✅ Easy to query/filter
- ✅ Dictionary access (no regex!)

---

## Key Takeaways

### Use YAML in `knowledge/` when:
1. **Scripts need to read it** programmatically
2. Data is **structured** (lists, hierarchies, key-value pairs)
3. Multiple scripts **share** the same knowledge
4. You need **validation** or **querying**
5. Data changes **frequently**

### Use Markdown for:
1. **Human-readable** documentation (SKILL.md, README.md)
2. **Explanatory** content (guides, tutorials)
3. **Free-form** prose
4. Content that **doesn't need parsing**

---

## Code Highlights

### API Client (scripts/api_client.py)

**YAML Loading (2 lines!):**
```python
with open('knowledge/api-endpoints.yaml') as f:
    data = yaml.safe_load(f)
```

**Accessing Endpoint (simple dictionary lookup!):**
```python
endpoint = data['user_service']['endpoints']['get_user']
method = endpoint['method']  # "GET"
requires_auth = endpoint['requires_auth']  # True (boolean, not string!)
```

### Error Handler (scripts/error_handler.py)

**YAML Loading:**
```python
with open('knowledge/error-codes.yaml') as f:
    data = yaml.safe_load(f)
```

**Filtering by Severity (list comprehension!):**
```python
critical = {
    code: info
    for code, info in error_codes.items()
    if info['severity'] == 'critical'
}
```

**Statistics (because structure is guaranteed!):**
```python
stats = {
    'total': len(error_codes),
    'by_severity': count_by_field('severity'),
    'by_category': count_by_field('category')
}
```

---

## Real-World Benefits

### Benefit 1: Update Knowledge Without Code Changes

**Change `knowledge/api-endpoints.yaml`:**
```yaml
# Add new endpoint
new_service:
  base_url: https://api.new.com
  endpoints:
    new_action:
      method: POST
      path: /action
```

**Scripts automatically see it** - no code changes needed!

### Benefit 2: Type Safety

**YAML:**
```yaml
requires_auth: true  # Boolean
timeout: 30          # Integer
```

**In Python:**
```python
if endpoint['requires_auth']:  # Works correctly!
    # This is boolean True, not string "true"
```

**Markdown:**
```markdown
- Requires auth: true
```

**In Python:**
```python
# After regex parsing, you get string "true"
# Need manual conversion: bool(value == "true")
```

### Benefit 3: Easy Validation

**YAML Schema Validation:**
```python
# Can validate YAML structure
schema = {
    'type': 'object',
    'properties': {
        'method': {'enum': ['GET', 'POST', 'PUT', 'DELETE']},
        'path': {'type': 'string'},
        'requires_auth': {'type': 'boolean'}
    }
}
```

**Markdown:** No standard schema validation possible!

---

## Summary

**The Pattern:**
- `SKILL.md` / `README.md` → Markdown (human docs)
- `knowledge/*.yaml` → YAML (structured data)
- `scripts/*.py` → Python (reads YAML easily)

**The Benefit:**
- Scripts are **simple** (no complex parsing)
- Knowledge is **maintainable** (update YAML without touching code)
- Data is **type-safe** (booleans, numbers, structures)
- Everything is **queryable** (filter, search, analyze)

**The Result:**
- ✅ Clean code
- ✅ Reliable parsing
- ✅ Easy maintenance
- ✅ Happy developers! 🎉

---

## Next Steps

1. ✅ Run both demo scripts (`api_client.py`, `error_handler.py`)
2. ✅ Try modifying the YAML files and re-running scripts
3. ✅ Compare complexity: imagine parsing this as Markdown!
4. ✅ Read `../YAML-KNOWLEDGE-LAB.md` for more details

**Now you know WHY skills use YAML in `knowledge/` folders!** 🎯
