# Claude Structured Output Study Guide
**Master Yang's Practice Session - 2026-02-06**

## 🎯 Tonight's Goal
Master structured outputs with Claude to build reliable AI components for production systems.

---

## 📋 Prerequisites

```bash
pip install anthropic pydantic python-dotenv
```

**Setup `.env`:**
```bash
ANTHROPIC_API_KEY=your_key_here
```

---

## 🏗️ Core Concepts

### Why Pydantic?
Anthropic uses **Pydantic models** for schema definition - same as OpenAI, FastAPI, etc.

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str = Field(description="Clear task title")
    priority: Priority
    deadline: Optional[str] = Field(None, description="ISO date format")
    subtasks: List[str] = Field(default_factory=list)
```

**Key features:**
- Type validation (str, int, float, bool, List, Optional)
- Enums for controlled vocabularies
- Field descriptions guide the model
- Nested structures supported

---

## 🚀 Level 1: Basic Extraction

**Goal:** Extract structured data from unstructured text.

```python
from anthropic import Anthropic
from pydantic import BaseModel
from typing import List
import os

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define schema
class Contact(BaseModel):
    name: str
    email: str
    phone: str | None = None

# Extract from text
message = client.messages.create(
    model="claude-sonnet-4",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": """Extract contact info:
        Hi, I'm Dr. Sarah Chen. You can reach me at sarah.chen@hospital.org 
        or call +44-20-1234-5678."""
    }],
    # 🔑 The magic parameter
    response_format=Contact
)

# Parse result
contact = Contact.model_validate_json(message.content[0].text)
print(f"Name: {contact.name}")
print(f"Email: {contact.email}")
print(f"Phone: {contact.phone}")
```

**Practice exercises:**
1. Extract product details (name, price, category) from Amazon listing
2. Parse meeting notes into attendees, decisions, action items
3. Extract recipe (ingredients, steps, cooking time) from blog post

---

## 🎓 Level 2: Multi-Entity Extraction

**Goal:** Extract multiple items at once.

```python
from typing import List
from pydantic import BaseModel

class Email(BaseModel):
    sender: str
    subject: str
    priority: str  # "urgent", "normal", "low"
    has_attachment: bool
    action_required: bool

class InboxSummary(BaseModel):
    total_emails: int
    emails: List[Email]
    urgent_count: int

# Process inbox
inbox_text = """
1. From: boss@company.com - Subject: URGENT: Q4 Report Due Tomorrow
2. From: newsletter@tech.com - Subject: Weekly AI News
3. From: client@bigcorp.com - Subject: Contract Review (attachment)
"""

message = client.messages.create(
    model="claude-sonnet-4",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": f"Analyze this inbox:\n{inbox_text}"
    }],
    response_format=InboxSummary
)

summary = InboxSummary.model_validate_json(message.content[0].text)
print(f"📧 {summary.urgent_count} urgent emails out of {summary.total_emails}")
for email in summary.emails:
    if email.urgent:
        print(f"⚠️ {email.subject}")
```

**Practice exercises:**
1. Extract all GitHub issues from project discussion
2. Parse invoice (line items, totals, tax, vendor info)
3. Extract entities from news article (people, organizations, locations, dates)

---

## 🔥 Level 3: RAG + Structured Metadata

**Goal:** Extract metadata for vector database indexing.

```python
from datetime import datetime
from typing import List, Optional

class DocumentMetadata(BaseModel):
    title: str
    author: Optional[str] = None
    date_published: Optional[str] = None  # ISO format
    document_type: str  # "article", "report", "email", "documentation"
    topics: List[str]  # Max 5 key topics
    entities: List[str]  # Named entities (people, orgs, products)
    summary: str  # 1-2 sentence summary
    relevance_score: int = Field(ge=1, le=10, description="How important/useful is this?")

def process_document_for_rag(document_text: str) -> DocumentMetadata:
    """Extract metadata for vector DB storage"""
    message = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Extract structured metadata:\n\n{document_text}"
        }],
        response_format=DocumentMetadata
    )
    return DocumentMetadata.model_validate_json(message.content[0].text)

# Example usage
doc = """
Building AI Agents: A Technical Deep Dive
By Dr. Emily Zhang, Jan 15 2026

This report examines the architecture of production AI agents using 
LangChain, CrewAI, and AutoGPT frameworks. Key findings show that 
structured outputs reduce hallucination rates by 40%...
"""

metadata = process_document_for_rag(doc)
print(f"📄 {metadata.title}")
print(f"🏷️ Topics: {', '.join(metadata.topics)}")
print(f"⭐ Relevance: {metadata.relevance_score}/10")

# Now store in your vector DB with this metadata
# chromadb.add(document_text, metadata=metadata.model_dump())
```

**Practice exercises:**
1. Build metadata extractor for your code documentation
2. Process email threads into structured conversation logs
3. Extract structured data from PDF research papers

---

## 🤖 Level 4: Agent Decision-Making

**Goal:** Structured outputs for agent tool selection and reasoning.

```python
from enum import Enum
from typing import List, Optional

class ActionType(str, Enum):
    SEARCH_WEB = "search_web"
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    EXECUTE_CODE = "execute_code"
    ASK_USER = "ask_user"
    COMPLETE = "complete"

class AgentAction(BaseModel):
    action: ActionType
    reasoning: str  # Why this action?
    parameters: dict  # Action-specific params
    confidence: float = Field(ge=0.0, le=1.0)

class AgentPlan(BaseModel):
    goal_understood: str  # Restate the user's goal
    steps: List[AgentAction]  # Ordered action sequence
    estimated_time_seconds: int
    risks: List[str]  # Potential failure points

def plan_task(user_request: str) -> AgentPlan:
    """Agent planning with structured reasoning"""
    message = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""You are an AI agent. Create an execution plan for:
            
            USER REQUEST: {user_request}
            
            Break down into concrete actions with reasoning."""
        }],
        response_format=AgentPlan
    )
    return AgentPlan.model_validate_json(message.content[0].text)

# Example
plan = plan_task("Find all Python files in my repo that use deprecated APIs and create a fix plan")

print(f"🎯 Goal: {plan.goal_understood}")
print(f"⏱️ Est. time: {plan.estimated_time_seconds}s")
print(f"\n📋 Steps:")
for i, step in enumerate(plan.steps, 1):
    print(f"{i}. {step.action.value}")
    print(f"   Why: {step.reasoning}")
    print(f"   Confidence: {step.confidence:.0%}")
```

**Practice exercises:**
1. Build a structured planning agent for your MCP crew
2. Create code review agent with structured findings
3. Build research agent that outputs structured citations

---

## 🏭 Level 5: Production Patterns

### Pattern 1: Multi-Stage Processing Pipeline

```python
from typing import List
from pydantic import BaseModel

# Stage 1: Extract raw data
class RawEmail(BaseModel):
    sender: str
    subject: str
    body: str

# Stage 2: Classify and prioritize
class EmailClassification(BaseModel):
    category: str  # "support", "sales", "hr", "spam"
    priority: int  # 1-5
    sentiment: str  # "positive", "neutral", "negative"
    requires_response: bool

# Stage 3: Generate action
class EmailAction(BaseModel):
    action_type: str  # "respond", "forward", "archive", "flag"
    suggested_response: str | None = None
    forward_to: str | None = None
    notes: str

def process_email_pipeline(email_text: str):
    """Multi-stage structured processing"""
    
    # Stage 1: Parse
    raw = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Extract email structure:\n{email_text}"}],
        response_format=RawEmail
    ).content[0].text
    
    # Stage 2: Classify
    classification = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Classify:\n{raw}"}],
        response_format=EmailClassification
    ).content[0].text
    
    # Stage 3: Action
    action = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Suggest action for {classification}"}],
        response_format=EmailAction
    ).content[0].text
    
    return {
        "raw": RawEmail.model_validate_json(raw),
        "classification": EmailClassification.model_validate_json(classification),
        "action": EmailAction.model_validate_json(action)
    }
```

### Pattern 2: Self-Correcting with Validation

```python
from pydantic import BaseModel, field_validator
from typing import List

class CodeReview(BaseModel):
    file_path: str
    issues: List[str]
    severity: str  # "critical", "warning", "info"
    suggested_fix: str
    
    @field_validator('severity')
    def validate_severity(cls, v):
        if v not in ['critical', 'warning', 'info']:
            raise ValueError('Invalid severity level')
        return v

def review_code_with_retry(code: str, max_retries=3):
    """Structured output with validation and retry"""
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-sonnet-4",
                max_tokens=1024,
                messages=[{"role": "user", "content": f"Review this code:\n{code}"}],
                response_format=CodeReview
            )
            review = CodeReview.model_validate_json(message.content[0].text)
            return review
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Retry {attempt + 1}: {e}")
    
```

### Pattern 3: Streaming Structured Output

```python
# Note: Anthropic doesn't support streaming structured output yet
# But you can use a hybrid approach:

class StreamingAnalysis(BaseModel):
    thinking: str  # Claude's reasoning
    result: dict  # Final structured output

# Stream thinking, then get structured result
with client.messages.stream(
    model="claude-sonnet-4",
    max_tokens=2048,
    messages=[{"role": "user", "content": "Analyze this complex dataset..."}]
) as stream:
    thinking = ""
    for text in stream.text_stream:
        print(text, end="", flush=True)
        thinking += text

# Then get structured output
final_result = client.messages.create(
    model="claude-sonnet-4",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Analyze this complex dataset..."},
        {"role": "assistant", "content": thinking},
        {"role": "user", "content": "Now format your analysis as structured JSON"}
    ],
    response_format=YourStructuredModel
)
```

---

## 🎯 Your Use Cases

### 1. MCP Crew Orchestration

```python
class MCPTask(BaseModel):
    assigned_to: str  # "claude", "gemini", "docker"
    task_type: str  # "code_generation", "analysis", "execution"
    input_data: dict
    expected_output_schema: str
    timeout_seconds: int

class MCPOrchestrationPlan(BaseModel):
    tasks: List[MCPTask]
    dependencies: dict  # task_id -> [dependent_task_ids]
    parallel_groups: List[List[str]]  # Which tasks can run concurrently
```

### 2. RAG Document Processing

```python
class RAGChunk(BaseModel):
    text: str
    metadata: DocumentMetadata  # From earlier example
    embedding_hint: str  # Key concepts for embedding
    chunk_type: str  # "introduction", "technical", "conclusion"
    links_to: List[str]  # Related chunk IDs
```

### 3. Browser Automation Results

```python
class ScrapedData(BaseModel):
    url: str
    title: str
    main_content: str
    extracted_data: dict
    images: List[str]
    links: List[str]
    metadata: dict
    confidence_score: float
```

---

## ⚠️ Common Gotchas

### 1. Optional vs Required Fields
```python
# ❌ Bad: Everything optional = garbage output
class BadSchema(BaseModel):
    name: str | None = None
    email: str | None = None

# ✅ Good: Required core fields, optional extras
class GoodSchema(BaseModel):
    name: str  # Required
    email: str  # Required
    phone: str | None = None  # Truly optional
```

### 2. Enum vs String
```python
# ❌ Bad: Freeform strings
class BadTask(BaseModel):
    priority: str  # Could be "high", "HIGH", "urgent", "ASAP"...

# ✅ Good: Controlled vocabulary
class GoodTask(BaseModel):
    priority: Priority  # Enum from earlier
```

### 3. Descriptions Matter
```python
# ❌ Bad: No guidance
class BadModel(BaseModel):
    value: int

# ✅ Good: Clear expectations
class GoodModel(BaseModel):
    relevance_score: int = Field(
        ge=1, 
        le=10, 
        description="Rate 1-10 where 10 is most relevant to user query"
    )
```

---

## 🧪 Practice Projects for Tonight

### Project 1: Email Triage Bot (30 min)
Build a system that:
1. Reads Gmail inbox (use mock data)
2. Extracts structured email data
3. Classifies by urgency/category
4. Generates response suggestions

### Project 2: Code Documentation Extractor (45 min)
1. Read Python files from your repos
2. Extract function signatures, docstrings, dependencies
3. Build structured API documentation
4. Output as structured JSON for search

### Project 3: Mini RAG Pipeline (60 min)
1. Take 10 documents from your projects
2. Extract structured metadata
3. Generate embeddings (use any service)
4. Build search that returns structured results

---

## 📚 Reference

### Quick Pydantic Cheat Sheet
```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from enum import Enum
from datetime import datetime

class ExampleModel(BaseModel):
    # Basic types
    name: str
    age: int
    score: float
    active: bool
    
    # Optional
    nickname: Optional[str] = None
    
    # Lists
    tags: List[str]
    
    # Enums
    status: Literal["draft", "published", "archived"]
    
    # Nested
    metadata: dict
    
    # With constraints
    rating: int = Field(ge=1, le=5, description="1-5 stars")
    
    # Validator
    @field_validator('age')
    def check_age(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
```

### Model Selection
- **claude-sonnet-4**: Best balance (use this for practice)
- **claude-opus-4**: Maximum accuracy (expensive)
- **claude-haiku-4**: Fast/cheap (good for simple extractions)

---

## 🎓 Next Steps After Tonight

1. **Build your MCP crew structured interfaces**
2. **Add structured output to your RAG pipelines**
3. **Replace all string-based agent responses with schemas**
4. **Benchmark: structured vs unstructured accuracy**

---

## 💡 Pro Tips

1. **Start simple, iterate**: Begin with flat models, add nesting later
2. **Test with bad inputs**: How does it handle garbage data?
3. **Version your schemas**: Track changes for compatibility
4. **Use Field descriptions**: They guide Claude's understanding
5. **Validate early**: Catch schema issues before prod

---

**Ready to practice!** 🚀

Start with Level 1, work through to Level 4 tonight. Tomorrow you'll be writing production-grade structured output pipelines.
