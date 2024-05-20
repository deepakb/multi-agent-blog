from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("generate_content", return_direct=False)
def generate_content(input: str) -> str:
    """Generates a detailed and engaging blog post based on a given outline using ChatOpenAI."""
    prompt = f"Generate a detailed and engaging blog post based on the following outline:\n\n{input}"
    print(prompt)
    response = llm.invoke(prompt)
    return response
