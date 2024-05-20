from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("optimize_seo", return_direct=False)
def optimize_seo(input: str) -> str:
    """Optimizes a blog post for SEO by incorporating keyword integration and linking strategies using ChatOpenAI."""
    prompt = f"Optimize the following blog post for SEO, incorporating keyword integration and linking strategies:\n\n{input}"
    print(prompt)
    response = llm.invoke(prompt)
    return response
