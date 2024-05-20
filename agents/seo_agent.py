from agents.agent_executor import create_agent
from tools.optimize_seo import optimize_seo


def get_seo_agent(llm):
    tools = [optimize_seo]
    system_prompt = "You are an SEO expert. Optimize a blog post for SEO by incorporating keyword integration and linking strategies."
    return create_agent(llm, tools, system_prompt)
