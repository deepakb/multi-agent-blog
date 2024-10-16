from fastapi import APIRouter, HTTPException
from app.models.research import ResearchRequest, ResearchResponse
from app.services.research import conduct_research
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ResearchResponse)
async def create_research(request: ResearchRequest):
    try:
        logger.info(f"Starting research on topic: {request.topic}")
        result = await conduct_research(request.topic)
        logger.info(f"Research completed for topic: {request.topic}")
        return result
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occurred during the research process")
