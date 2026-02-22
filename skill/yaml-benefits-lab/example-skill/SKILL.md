# API Helper Skill

**Purpose:** Simplify API interactions by managing endpoints and error handling through structured knowledge files.

## What This Skill Does

- ✅ Manages API endpoint configurations
- ✅ Handles error codes and provides actionable guidance
- ✅ Validates requests before sending
- ✅ Provides consistent error messaging

## How It Works

### Architecture

```
api-helper-skill/
├── SKILL.md                    # ← You are here (human documentation)
├── scripts/                    # ← Python tools that DO the work
│   ├── api_client.py           # Makes API calls using knowledge/
│   └── error_handler.py        # Handles errors using knowledge/
└── knowledge/                  # ← YAML data that scripts READ
    ├── api-endpoints.yaml      # API endpoint definitions
    └── error-codes.yaml        # Error code mappings
```

### Why YAML in knowledge/?

The Python scripts in `scripts/` need to **programmatically read** endpoint and error data. YAML is perfect for this because:

1. **Easy to parse** - 2 lines of Python code
2. **Structured** - Guaranteed data format
3. **Type-safe** - Numbers stay numbers, booleans stay booleans
4. **Queryable** - Dictionary access, not regex parsing
5. **Maintainable** - Update knowledge without changing scripts

## Usage

### Making an API Call

```python
from scripts.api_client import APIClient

client = APIClient()

# Get a user (endpoint definition comes from knowledge/api-endpoints.yaml)
response = client.call('user_service', 'get_user', user_id=123)

# Create a user
response = client.call('user_service', 'create_user', data={'name': 'Alice'})
```

### Handling Errors

```python
from scripts.error_handler import ErrorHandler

handler = ErrorHandler()

# Get error information (from knowledge/error-codes.yaml)
error_info = handler.get_error_info(1002)
print(f"Error: {error_info['message']}")
print(f"Severity: {error_info['severity']}")
print(f"Action: {error_info['action']}")
```

## Adding New Endpoints

Just update `knowledge/api-endpoints.yaml`:

```yaml
new_service:
  base_url: https://api.example.com/new
  endpoints:
    my_action:
      method: POST
      path: /do-something
      description: Does something cool
```

**No code changes needed!** The scripts automatically read the updated YAML.

## Adding New Error Codes

Just update `knowledge/error-codes.yaml`:

```yaml
error_codes:
  3001:
    message: New error type
    severity: warning
    action: Do this to fix it
```

**No code changes needed!** The error handler automatically reads the updated YAML.

## Benefits Over Markdown

If we stored this knowledge in markdown files instead:

- ❌ Scripts would need complex regex parsing
- ❌ Fragile - any formatting change breaks scripts
- ❌ No type safety (everything is a string)
- ❌ Hard to validate data structure
- ❌ Difficult to query programmatically

With YAML:

- ✅ Simple parsing (2 lines)
- ✅ Robust - structure is guaranteed
- ✅ Type-safe (numbers, booleans, lists)
- ✅ Easy validation
- ✅ Dictionary access

## See Also

- `knowledge/api-endpoints.yaml` - API endpoint definitions
- `knowledge/error-codes.yaml` - Error code mappings
- `scripts/api_client.py` - API client implementation
- `scripts/error_handler.py` - Error handler implementation

---

**This is a working example demonstrating why YAML is used for structured knowledge that scripts need to read!**
