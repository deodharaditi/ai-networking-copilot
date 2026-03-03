from __future__ import annotations
from typing import Any, Dict
from anthropic import Anthropic
from app.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
import json
import re

def _extract_json(text: str) -> Dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in response: {text!r}")
    return json.loads(match.group())

def _fallback(name: str, persona: str, context: str) -> Dict[str, Any]:
    note = f"Hi {name} - noticed your work on {context}. Would love to connect."
    return{
        "persona": persona,
        "connection_note": note[:300],
        "follow_up_dm": f"Thanks for connection {name}. Would love to ask you 1-2 quick questions.",
        "reasoning_bullets": ["Template fallback - LLM unavailable"]
    }

def generate_messages(
        *,
        name: str,
        role_company: str,
        context: str,
        linkedin_url: str,
        persona: str,
        priority_score: int,
        tone: str = "warm",
) -> Dict[str, Any]:
    try:
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        system = (
            "You are a professional networking assistant. "
            "Output ONLY valid JSON — no markdown, no code fences, no extra text."
        )
        user = (
            f"Generate networking messages for this contact.\n\n"
            f"Name: {name}\n"
            f"Role/Company: {role_company}\n"
            f"Context: {context}\n"
            f"LinkedIn: {linkedin_url}\n"
            f"Persona: {persona}\n"
            f"Priority score: {priority_score}\n"
            f"Tone: {tone}\n\n"
            f"Return a JSON object with exactly these keys:\n"
            f"  connection_note  — LinkedIn connection request (≤300 characters)\n"
            f"  follow_up_dm     — follow-up DM after connecting (≤500 characters)\n"
            f"  reasoning_bullets — list of 2-4 short strings explaining why to reach out\n"
            f"  persona          — echo back \"{persona}\""
        )
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=400,
            temperature=0.4,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return _extract_json(response.content[0].text)
    except Exception:
        return _fallback(name, persona, context)