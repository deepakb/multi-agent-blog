from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("edit_content", return_direct=False)
def edit_content(input: str) -> str:
    """Refine blog content to ensure clarity, coherence, and engagement using ChatOpenAI."""
    prompt = f"Refine the following blog content to make it clear, coherent, and engaging:\n\n{input}"
    response = llm.invoke(prompt)
    return response
