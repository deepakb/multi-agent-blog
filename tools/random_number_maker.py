import random
from langchain_core.tools import tool


@tool("random_number", return_direct=False)
def random_number_maker(input: str) -> str:
    """Returns a random number between 0-100. input the word 'random'"""
    return random.randint(0, 100)
