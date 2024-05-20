from agents.agent_executor import create_agent
from tools.generate_outline import generate_outline


def get_outliner_agent(llm):
    tools = [generate_outline]
    system_prompt = "You are an outliner. Generate an outline for a given research data."
    return create_agent(llm, tools, system_prompt)
