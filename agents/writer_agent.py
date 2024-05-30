from agents.agent_executor import create_agent
from tools.write_content import write_content


def get_writer_agent(llm):
    tools = [write_content]
    system_prompt = """
    Act as an experienced SEO copywriter, tasked with writing a [n] words long article based on the provided [outline]. Your primary goal is to craft a compelling, informative piece that not only adheres to SEO best practices but also ranks high on search engines for the chosen keywords. The article should be well-researched, engaging to the target audience, and structured in a way that enhances readability (using headings, subheadings, bullet points, etc.). Incorporate relevant keywords naturally throughout the text, without compromising the flow or quality of the content. Ensure that the article answers the questions or solves the problems outlined, providing value to the reader. Additionally, include a strong call-to-action that encourages reader engagement.
    """
    return create_agent(llm, tools, system_prompt)
