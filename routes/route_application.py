from __future__ import annotations

from uuid import UUID
from fastapi import HTTPException, status
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from models.model_application import (
    Application,
    ApplicationCreate,
    ApplicationStatusUpdate,
)
from services.service_application import (
    create_application,
    list_application,
    get_application,
    update_status,
    get_metrics,
)


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=Application, status_code=status.HTTP_201_CREATED)
def create(pyload: ApplicationCreate) -> Application:
    """
    Cria uma candidatura.
    - payload vem do body (JSON)
    - retorna Application (com id preenchido)
    """
    return create_application(pyload)


@router.get("", response_model=list[Application])
def list_all() -> list[Application]:

    return list_application()


@router.get("/metrics")
def metrics() -> dict[str, int]:
    return get_metrics()


@router.get("/{app_id}", response_model=Application)
def get_by_id(app_id: UUID) -> Application:

    application = get_application(app_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not Found"
        )
    return application


@router.patch("/{app_id}", response_model=Application)
def patch_status(app_id: UUID, payload: ApplicationStatusUpdate) -> Application:
    updated = update_status(app_id, payload.status)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Applicaiton no Found"
        )
    return updated
