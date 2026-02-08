from anthropic import Anthropic
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define schema
class Contact(BaseModel):
    name: str
    email: str
    phone: str | None = None

# Extract from text
# Extract from text
tool_definition = {
    "name": "Contact",
    "description": "Extract contact information from text",
    "input_schema": Contact.model_json_schema()
}

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": """Extract contact info:
        Hi, I'm Dr. Sarah Chen. You can reach me at sarah.chen@hospital.org 
        or call +44-20-1234-5678."""
    }],
    tools=[tool_definition],
    tool_choice={"type": "tool", "name": "Contact"}
)

# Parse result
if message.content and message.content[-1].type == 'tool_use':
    tool_use = message.content[-1]
    contact = Contact(**tool_use.input)
    print(f"Name: {contact.name}")
    print(f"Email: {contact.email}")
    print(f"Phone: {contact.phone}")
else:
    print("No contact information extracted.")