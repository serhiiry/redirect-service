from fastapi import APIRouter
from ..responses import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    return HealthCheckResponse(status="healthy")
