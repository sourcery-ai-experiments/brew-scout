from fastapi import APIRouter, Response, Depends, status

from ...libs.dependencies.common import settings_factory
from ...libs.settings import AppSettings


router = APIRouter(tags=["Common API's"])


@router.get("/health", response_class=Response)
async def health(settings: AppSettings = Depends(settings_factory)) -> Response:
    if settings.database_dsn:
        return Response(status_code=status.HTTP_200_OK)
    
    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
