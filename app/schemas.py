from __future__ import annotations
from pydantic import BaseModel, Field, HttpUrl
from typing import List
from datetime import datetime, timezone
import uuid


class ContactInput(BaseModel):
    name: str
    role_company: str
    context: str
    linkedin_url: HttpUrl

class ContactResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role_company: str
    context: str
    linkedin_url: HttpUrl
    persona: str
    priority_score: int
    connection_note: str
    follow_up_dm: str
    reasoning_bullets: List[str] = Field(default_factory=list)
    status: str = "new"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    