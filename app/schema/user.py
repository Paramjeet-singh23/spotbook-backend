from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.schema.event import Event, EventAccess
from app.schema.payment import Payment
import uuid
from app.db.model.user import GenderEnum


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    sex: GenderEnum


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    sex: Optional[str] = None


class UserInDBBase(UserBase):
    id: uuid.UUID
    created_at: datetime
    last_login: Optional[datetime] = None
    updated_at: datetime
    password: str

    class Config:
        orm_mode = True


class User(UserInDBBase):
    created_events: List[Event] = []
    managed_events: List[EventAccess] = []
    event_access: List[EventAccess] = []
    payment: List[Payment] = []


class UserInDB(UserInDBBase):
    pass
