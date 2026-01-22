from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

from models.model_application import Application, ApplicationCreate, ApplicationStatus

_APPLICATIONS_DB: dict[UUID, Application] = {}


def create_application(data: ApplicationCreate) -> Application:
    """
    Cria uma candidatura e guarda em memória.

    Regras:
    - gera um UUID novo
    - se applied_date não veio, usa a data de hoje
    - salva no storage em memória
    """

    new_id = uuid4()
    applied = data.applied_date or date.today()

    application = Application(
        id=new_id,
        company=data.company,
        role=data.role,
        link=data.link,
        status=data.status,
        applied_date=applied,
    )

    _APPLICATIONS_DB[new_id] = application
    return application


def list_application() -> list[Application]:
    """Retorna todas as candidaturas cadastradas."""
    return list(_APPLICATIONS_DB.values())


def get_application(app_id: UUID) -> Application | None:
    """
    Busca uma candidatura pelo id.

    Retorna:
    - Application se existir
    - None se não existir (a rota converte isso para 404)
    """
    return _APPLICATIONS_DB.get(app_id)


def rest_storage() -> None:
    """Usado apenas em testes para limpar o storage em memória."""
    _APPLICATIONS_DB.clear()


def update_status(app_id: UUID, new_status: ApplicationStatus) -> Application | None:
    application = _APPLICATIONS_DB.get(app_id)
    if application is None:
        return None
    updated = application.model_copy(update={"status": new_status})
    _APPLICATIONS_DB[app_id] = updated
    return updated


def get_metrics() -> dict[str, int]:
    metrics: dict[str, int] = {status.value: 0 for status in ApplicationStatus}

    for app in _APPLICATIONS_DB.values():
        metrics[app.status.value] += 1
    return metrics
