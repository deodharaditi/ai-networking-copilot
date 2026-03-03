from __future__ import annotations
from typing import List
from app.schemas import ContactInput

def parse_contacts(raw_text: str) -> List[ContactInput]:
    contacts = []
    for i, line in enumerate(raw_text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        fields = [f.strip() for f in line.split("|")]
        if len(fields) != 4:
            raise ValueError(
                f"Line {i} has {len(fields)} field(s), expected 4 (name | role_company | context | linkedin_url):\n  {line!r}"
            )
        name, role_company, context, linkedin_url = fields
        contacts.append(ContactInput(name=name, role_company=role_company, context=context, linkedin_url=linkedin_url))
    return contacts

def classify_persona(contact: ContactInput) -> str:
    text = f"{contact.role_company} {contact.context}".lower()
    if any(kw in text for kw in ("founder", "ceo", "cofounder", "co-founder")):
        return "founder"
    if any(kw in text for kw in ("recruiter", "talent", "hr", "sourcer")):
        return "recruiter"
    if any(kw in text for kw in ("engineer", "ml", "infra", "platform", "devops")):
        return "engineer"
    return "community"

def compute_priority_score(contact: ContactInput, persona: str) -> int:
    text = f"{contact.role_company} {contact.context}".lower()
    score = 0

    if persona == "founder":
        score += 3
    elif persona == "recruiter":
        score += 2

    if any(kw in text for kw in ("hiring", "looking for", "open role", "join our team", "we're hiring")):
        score += 2

    if any(kw in text for kw in ("agent", "infra", "devtools", "observability", "mlops")):
        score += 2

    if any(kw in text for kw in ("yc", "y combinator", "techstars", "on deck", "ondeck")):
        score += 1

    if len(contact.context.strip()) < 12:
        score -= 2

    return score