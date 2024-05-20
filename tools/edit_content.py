from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


@tool("edit_content", return_direct=False)
def edit_content(input: str) -> str:
    """Edits a blog post for quality writing, readability, and proofreading using ChatOpenAI."""
    prompt = f"Edit the following blog post for quality writing, readability, and proofreading:\n\n{input}"
    print(prompt)
    response = llm.invoke(prompt)
    return response
