import json
from chat.llm import ask_llm

PROMPT = """
You are an intent parser for an engineering knowledge graph.

Return ONLY valid JSON.

Possible intents:
- ownership
- dependencies
- blast_radius
- list

JSON format:
{
  "intent": "<intent>",
  "entity_type": "service|database|cache|team|null",
  "entity_name": "<name or null>"
}

Examples:
User: Who owns payment-service?
{"intent":"ownership","entity_type":"service","entity_name":"payment-service"}

User: What breaks if redis-main goes down?
{"intent":"blast_radius","entity_type":"cache","entity_name":"redis-main"}

User: List all services
{"intent":"list","entity_type":"service","entity_name":null}

User: 
"""

def parse_intent(user_input: str) -> dict:
    raw = ask_llm(PROMPT + user_input)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "intent": "unknown",
            "entity_type": None,
            "entity_name": None
        }
