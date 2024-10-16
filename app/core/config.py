from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LLM Research API"
    PROJECT_DESCRIPTION: str = "API for conducting LLM research and generating articles"
    VERSION: str = "1.0.0"
    ALLOWED_HOSTS: list = ["*"]
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
