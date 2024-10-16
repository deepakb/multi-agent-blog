from langchain_openai import ChatOpenAI
from app.core.config import settings


async def get_fast_llm():
    return ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)


async def get_long_context_llm():
    return ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
