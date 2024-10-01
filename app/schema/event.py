from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.db.model.event import EventTypeEnum, RoleEnum


class EventCreate(BaseModel):
    name: str
    event_type: EventTypeEnum
    is_repetitive: bool = False
    event_date: datetime


class EventUpdate(BaseModel):
    name: str
    event_type: EventTypeEnum
    is_repetitive: bool = False
    event_date: datetime


class Event(BaseModel):
    id: UUID
    name: str
    event_type: EventTypeEnum
    is_repetitive: bool
    event_date: datetime
    create_by: UUID
    created_at: datetime
    updated_at: datetime
    updated_by: UUID

    class Config:
        orm_mode = True


class EventAccessCreate(BaseModel):
    event_id: UUID
    user_id: UUID
    role: RoleEnum


class EventAccess(BaseModel):
    id: UUID
    event_id: UUID
    user_id: UUID
    role: RoleEnum
    managed_by: UUID
    created_at: datetime
    updated_at: datetime
    updated_by: UUID

    class Config:
        orm_mode = True
