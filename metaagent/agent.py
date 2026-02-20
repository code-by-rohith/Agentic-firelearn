from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

print("Initializing ADK A2A-consuming root agent...")


chat_agent = Agent(
    name="chat_agent",
    model="gemini-3-flash-preview",
    description="Handles general conversation requests.",
    instruction="You are a helpful AI assistant for general questions.",
)

time_agent = RemoteA2aAgent(
    name="time_agent",
    description="Remote A2A agent that provides current date/time.",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

root_agent = Agent(
    name="metaagent",
    model="gemini-3-flash-preview",
    description="Coordinator agent that delegates chat and time requests.",
    instruction=(
        "You are the coordinator. "
        "Delegate current date/time requests to time_agent. "
        "Delegate all other requests to chat_agent."
    ),
    sub_agents=[chat_agent, time_agent],
)
