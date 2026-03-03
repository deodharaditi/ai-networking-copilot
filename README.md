# AI Networking Copilot

> Built as a 1-hour live coding challenge for [Azentic AI](https://azentic.com)

**Live Demo:** [ai-networking-copilot.streamlit.app](https://ai-networking-copilot.streamlit.app)

A lightweight AI-powered networking assistant that helps you prioritize outreach, personalize messages, and track contacts — without a bloated CRM.

---

## What It Does

- Scores who to message first using deterministic heuristics
- Classifies contact persona (founder / recruiter / engineer / community)
- Generates tailored LinkedIn connection notes (≤300 chars)
- Generates follow-up DMs for after acceptance
- Persists results as a reusable JSON mini-CRM

---

## Problem

When networking at scale, it's hard to decide who to prioritize, how to tailor outreach, how to follow up consistently, and how to track conversations.

This tool combines deterministic heuristics with LLM-powered language generation to produce structured, reusable outreach data.

---

## Architecture

    User Input (Streamlit)
            ↓
       Orchestrator
            ↓
     ┌─────────────────────┐
     │ logic               │
     │  ├─ ingest          │
     │  ├─ classify        │
     │  └─ score           │
     │ compose (LLM)       │
     └─────────────────────┘
            ↓
      JSON CRM Output

### Design Principles

- **Deterministic heuristics** for scoring and persona — transparent and debuggable
- **LLM used only for language generation** — not decision control
- **Modular, tool-like components** — each file has one responsibility
- **Graceful fallback** — app never crashes if LLM call fails

---

## Tech Stack

- Python
- Streamlit (UI + execution layer)
- Pydantic (data contracts)
- Anthropic Claude API (language generation)
- JSON persistence (lightweight mini-CRM)

---

## Run Locally

    git clone https://github.com/deodharaditi/ai-networking-copilot
    cd ai-networking-copilot
    pip install -r requirements.txt

Create a `.env` file:

    ANTHROPIC_API_KEY=your-key-here
    ANTHROPIC_MODEL=claude-sonnet-4-5

Run:

    streamlit run ui_streamlit.py

---

## Input Format

Paste contacts as pipe-separated lines:

    Name | Role/Company | Context | LinkedIn URL

---

## Future Extensions

- Follow-up cadence planning (3 / 7 / 14 day intervals)
- Status tracking (new → messaged → accepted → replied)
- Email + subject line generation
- Graph-based orchestration for multi-step workflows