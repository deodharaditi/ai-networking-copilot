# AI Networking Copilot

A lightweight AI-powered networking assistant that:

- Scores outreach priority
- Classifies contact persona (founder / recruiter / engineer / community)
- Generates tailored LinkedIn connection notes (≤300 chars)
- Generates follow-up messages
- Persists results as a reusable JSON mini-CRM

---

## Problem

When networking at scale, it’s hard to decide:
- Who to prioritize
- How to tailor outreach
- How to follow up consistently
- How to track conversations

This tool combines deterministic heuristics with LLM-powered language generation to produce structured, reusable outreach data.

---

## Architecture

```text
User Input (Streamlit)
        ↓
   Orchestrator
        ↓
 ┌─────────────────────┐
 │ ingest              │
 │ classify            │
 │ score               │
 │ compose (LLM)       │
 │ store               │
 └─────────────────────┘
        ↓
  JSON CRM Output
```

### Design Principles

- Deterministic heuristics for transparency
- LLM used only for language generation
- Modular, tool-like components
- Extendable orchestration layer

---

## Tech Stack

- Python
- Streamlit (UI + execution layer)
- Pydantic (contracts)
- Hosted LLM provider (configurable)
- JSON persistence

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run ui_streamlit.py
