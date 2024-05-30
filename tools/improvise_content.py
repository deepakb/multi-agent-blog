from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("improvise_content", return_direct=False)
def improvise_content(input: str) -> str:
    """Enhance blog content to ensure optimal sentence structure, word choice, clarity, coherence, and engagement using ChatOpenAI."""
    prompt = f"Refine the following blog content to improve sentence structure, word choice, and overall clarity and coherence, making it highly engaging:\n\n{input}"
    response = llm.invoke(prompt)
    return response
