from agents.agent_executor import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser


class IdeaResponse(BaseModel):
    title: str = Field(...,
                       description="This is the Title of the blog idea", min_length=10)
    description: str = Field(
        ..., description="This is the description of the blog idea", min_length=10)


class Ideas(BaseModel):
    ideas: List[IdeaResponse]


parser = PydanticOutputParser(pydantic_object=Ideas)


def get_topic_agent(llm):
    tools = [TavilySearchResults(search_depth="advanced")]
    system_prompt = "Act as an experienced SEO copywriter, tasked with brainstorming a list of 5 compelling article ideas based on [topic]. The goal is to generate content that not only resonates with your target audience but also ranks well on search engines. Use your expertise to identify keywords and trends that align with [topic] and the interests of your readers. Each article idea should be designed to offer valuable insights, answer common questions, or solve specific problems related to [topic]. Focus on creating headlines that are SEO-friendly and compelling enough to drive clicks and engagement. Additionally, consider the potential for backlinks and social shares, which can further enhance the visibility of your content. Rteurn this in json format as \n{format_instructions}"
    return create_agent(llm, tools, system_prompt, parser)
