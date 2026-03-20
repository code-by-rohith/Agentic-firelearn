from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

from agentic_rag.src.rag_tools import (
    list_knowledge_sources,
    plan_query,
    refine_query_if_needed,
    retrieve_context,
)

load_dotenv()


root_agent = Agent(
    name="agentic_rag_agent",
    model="gemini-3-flash-preview",
    description="Agentic RAG assistant over local Firebase docs.",
    instruction=(
        "You are an agentic RAG assistant. Always ground answers in retrieval results. "
        "Workflow: (1) call plan_query, (2) call retrieve_context with planned_query, "
        "(3) if weak/no context, call refine_query_if_needed and retrieve_context again, "
        "(4) answer with concise summary and explicit citations like [source]. "
        "Never claim facts that are not in retrieved context. "
        "If no evidence is found, clearly say it and suggest what document is missing."
    ),
    tools=[
        plan_query,
        retrieve_context,
        refine_query_if_needed,
        list_knowledge_sources,
    ],
)
