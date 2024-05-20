from agents.agent_executor import create_agent
from tools.generate_content import generate_content


def get_content_writer_agent(llm):
    tools = [generate_content]
    system_prompt = "You are a content writer. Generate a detailed and engaging blog post based on a given outline."
    return create_agent(llm, tools, system_prompt)
