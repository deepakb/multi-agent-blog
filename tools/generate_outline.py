from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("generate_outline", return_direct=False)
def generate_outline(input: str) -> str:
    """Generates an outline for a given research data using ChatOpenAI."""
    prompt = f"Generate an outline for the following research data:\n\n{input}"
    print(prompt)
    response = llm.invoke(prompt)
    return response
