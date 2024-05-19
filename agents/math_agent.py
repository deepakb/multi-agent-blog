from agents.agent_executor import create_agent
from tools.sum_numbers import sum_numbers


def get_math_agent(llm):
    tools = [sum_numbers]
    system_prompt = "You are a math majesto who can sum the given numbers"
    return create_agent(llm, tools, system_prompt)
