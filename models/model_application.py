from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    applied = ("applied",)
    screeening = ("screeening",)
    interviwer = ("interviwer",)
    offer = ("offer",)
    rejected = ("rejected",)


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1)
    role: str = Field(min_length=1)
    link: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.applied
    applied_date: Optional[date] = None


class Application(BaseModel):
    id: UUID
    company: str
    role: str
    link: Optional[str] = None
    status: ApplicationStatus
    applied_date: date
