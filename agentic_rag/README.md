# Agentic RAG with Google ADK

This folder now uses **Google ADK** to implement an agentic RAG pattern.

## ADK Agent
- `agentic_rag/agent.py` exposes `root_agent` (ADK-compatible)
- The agent is instructed to run this loop:
  1. `plan_query`
  2. `retrieve_context`
  3. `refine_query_if_needed` + second retrieval when needed
  4. grounded answer with citations

## Tools
- `agentic_rag/src/rag_tools.py`
- Tool functions:
  - `plan_query`
  - `retrieve_context`
  - `refine_query_if_needed`
  - `list_knowledge_sources`

## Knowledge Base
- `agentic_rag/data/firebase_overview.txt`
- `agentic_rag/data/security_rules.txt`
- `agentic_rag/data/cost_optimization.txt`

## Quick Local Tool Test
```bash
python3 agentic_rag/main.py
```

## ADK Integration
Use `agentic_rag/agent.py` and its `root_agent` in your ADK runtime the same way as your `metaagent/agent.py`.
