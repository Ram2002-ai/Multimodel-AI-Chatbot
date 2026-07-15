"""Health check endpoint for readiness/liveness probes."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}