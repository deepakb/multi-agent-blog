from langchain_community.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings


async def get_retriever():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY)
    vectorstore = InMemoryVectorStore(embedding=embeddings)
    return vectorstore.as_retriever(k=3)
