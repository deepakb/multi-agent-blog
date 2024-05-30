from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("write_content", return_direct=False)
def write_content(input: str) -> str:
    """Write blog content for a given outline using ChatOpenAI."""
    prompt = f"Write blog content for the following outline data:\n\n{input}"
    response = llm.invoke(prompt)
    return response
