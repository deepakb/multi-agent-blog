# utils/helpers.py

import re
from typing import List, Dict, Any
from langchain_core.documents import Document


def format_doc(doc: Document, max_length: int = 1000) -> str:
    """
    Format a Document object into a string representation.

    Args:
    doc (Document): The document to format.
    max_length (int): Maximum length of the formatted string.

    Returns:
    str: Formatted string representation of the document.
    """
    related = "- ".join(doc.metadata.get("categories", []))
    formatted = f"### {doc.metadata.get('title', 'Untitled')}\n\nSummary: {doc.page_content}\n\nRelated\n{related}"
    return formatted[:max_length]


def format_docs(docs: List[Document]) -> str:
    """
    Format a list of Document objects into a single string.

    Args:
    docs (List[Document]): List of documents to format.

    Returns:
    str: Formatted string representation of all documents.
    """
    return "\n\n".join(format_doc(doc) for doc in docs)


def clean_text(text: str) -> str:
    """
    Clean and normalize text.

    Args:
    text (str): The text to clean.

    Returns:
    str: Cleaned text.
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters except punctuation
    text = re.sub(r'[^a-zA-Z0-9\s\.,!?]', '', text)
    return text


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
    text (str): The text to chunk.
    chunk_size (int): The size of each chunk.
    overlap (int): The number of characters to overlap between chunks.

    Returns:
    List[str]: List of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.

    Args:
    d (Dict): The dictionary to flatten.
    parent_key (str): The parent key for nested dictionaries.
    sep (str): Separator for keys.

    Returns:
    Dict: Flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning a default value if the denominator is zero.

    Args:
    numerator (float): The numerator.
    denominator (float): The denominator.
    default (float): The default value to return if the denominator is zero.

    Returns:
    float: The result of the division or the default value.
    """
    return numerator / denominator if denominator != 0 else default
