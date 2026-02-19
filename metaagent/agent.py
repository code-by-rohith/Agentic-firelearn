from google.adk.agents import Agent

print("Initializing the agent...")

root_agent = Agent(
        name="metaagent",
        model="gemini-3-flash-preview",
        description="My ADK agent",
        instruction="You are a helpful AI assistant."
)