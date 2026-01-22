from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from pydantic import BaseModel, Field, field_validator


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationStatus(str, Enum):
    applied = ("applied",)
    screeening = ("screening",)
    interviwer = ("interviwer",)
    offer = ("offer",)
    rejected = ("rejected",)


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1)
    role: str = Field(min_length=1)
    link: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.applied
    applied_date: Optional[date] = None

    @field_validator("company", "role")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty or blank")
        return value.strip()


class Application(BaseModel):
    id: UUID
    company: str
    role: str
    link: Optional[str] = None
    status: ApplicationStatus
    applied_date: date
