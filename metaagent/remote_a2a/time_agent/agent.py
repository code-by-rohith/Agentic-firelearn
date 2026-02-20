from datetime import datetime

from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.llm_agent import Agent

# Ensure API credentials from project .env are available when run via uvicorn.
load_dotenv()


def get_current_time() -> dict:
    """Get the current time in the format YYYY-MM-DD HH:MM:SS."""
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


root_agent = Agent(
    name="time_agent",
    model="gemini-3-flash-preview",
    description="A time agent that returns the current date and time.",
    instruction=(
        "You are a time assistant. "
        "When users ask for current date/time, call get_current_time."
    ),
    tools=[get_current_time],
)

# Expose this ADK agent via A2A and auto-generate the well-known agent card.
a2a_app = to_a2a(root_agent, port=8001)
