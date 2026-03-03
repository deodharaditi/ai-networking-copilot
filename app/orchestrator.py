from __future__ import annotations
from typing import List
from app.schemas import ContactResult
from app.logic import parse_contacts, classify_persona, compute_priority_score
from app.compose import generate_messages

def analyze_contacts(raw_text: str, tone: str = "warm") -> List[ContactResult]:
    contacts = parse_contacts(raw_text)
    results = []

    for c in contacts:
        persona = classify_persona(c)
        score = compute_priority_score(c, persona)
        msg = generate_messages(
            name=c.name,
            role_company=c.role_company,
            context=c.context,
            linkedin_url=str(c.linkedin_url),
            persona=persona,
            priority_score=score,
            tone=tone
        )
        results.append(ContactResult(
            name=c.name,
            role_company=c.role_company,
            context=c.context,
            linkedin_url=str(c.linkedin_url),
            persona=persona,
            priority_score=score,
            connection_note=msg["connection_note"],
            follow_up_dm=msg["follow_up_dm"],
            reasoning_bullets=msg.get("reasoning_bullets", []),
        ))

    return sorted(results, key=lambda r: r.priority_score, reverse=True)