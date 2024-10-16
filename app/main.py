from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import research
from app.core.config import settings
from app.core.logging import setup_logging

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
setup_logging()

# Include routers
app.include_router(
    research.router, prefix="/api/v1/research", tags=["research"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
