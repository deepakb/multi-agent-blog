from agents.agent_executor import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults


def get_research_agent(llm):
    tools = [TavilySearchResults(max_results=5)]
    system_prompt = "You are a research assistant. Conduct research on a given topic."
    return create_agent(llm, tools, system_prompt)
