from langchain_core.tools import tool


@tool("lower_case", return_direct=False)
def to_lower_case(input: str) -> str:
    """Returns the input as all lower case."""
    return input.lower()
