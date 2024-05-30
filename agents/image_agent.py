from tools.generate_image import generate_image
from agents.agent_executor import create_agent


def get_image_agent(llm):
    tools = [generate_image]
    system_prompt = """
    Act as an experienced SEO copywriter tasked with analyzing the structure of[article]. Your primary goal is to enhance the article's engagement and readability through the strategic placement of images and visuals. You'll need to meticulously review the content, identify sections that could benefit from visual support, and suggest specific types of images or graphics that would complement the text. Consider how visuals can break up long stretches of text, illustrate complex ideas, and evoke emotions to keep the reader interested. Additionally, provide guidance on optimizing image alt text for SEO purposes, ensuring that the visuals contribute not only to user engagement but also to improved search engine rankings. Your recommendations should be based on best practices in digital content creation and SEO strategy.
    """
    return create_agent(llm, tools, system_prompt)
