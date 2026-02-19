from google.adk.agents import Agent

root_agent = Agent(
        name="metaagent",
        model="gemini-3-flash-preview",
        description="My ADK agent",
        instruction="You are a helpful AI assistant."
)