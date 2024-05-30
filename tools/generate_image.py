from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("generate_image", return_direct=False)
def generate_image(input: str) -> str:
    """Generates an outline for a given research data using ChatOpenAI."""
    prompt = f"Generate an outline for the following research data:\n\n{input}"
    response = llm.invoke(prompt)
    return response
