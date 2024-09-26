from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class EventBase(BaseModel):
    name: str
    create_by: int
    event_type: int
    is_repetitive: bool
    event_date: datetime
    field: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    updated_by: int


class EventInDBBase(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Event(EventInDBBase):
    pass


class EventInDB(EventInDBBase):
    pass


class EventAccessBase(BaseModel):
    event_id: int
    user_id: int
    role_id: int
    managed_by: int


class EventAccessCreate(EventAccessBase):
    pass


class EventAccessUpdate(EventAccessBase):
    pass


class EventAccessInDBBase(EventAccessBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class EventAccess(EventAccessInDBBase):
    pass


class EventAccessInDB(EventAccessInDBBase):
    pass
