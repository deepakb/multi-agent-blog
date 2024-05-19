import random
from langchain_core.tools import tool


@tool("sum_numbers", return_direct=False)
def sum_numbers(input: str) -> str:
    """Returns the sum of the given numbers input."""
    return sum(map(int, input.split()))
