from agents.agent_executor import create_agent
from tools.edit_content import edit_content


def get_editor_agent(llm):
    tools = [edit_content]
    system_prompt = "You are an editor. Edit a blog post for quality writing, readability, and proofreading."
    return create_agent(llm, tools, system_prompt)
