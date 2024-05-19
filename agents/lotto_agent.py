from agents.agent_executor import create_agent
from tools.random_number_maker import random_number_maker


def get_lotto_agent(llm):
    tools = [random_number_maker]
    system_prompt = "You are a senior lotto manager. you run the lotto and get random numbers"
    return create_agent(llm, tools, system_prompt)
