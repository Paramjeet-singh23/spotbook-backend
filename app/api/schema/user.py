from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.api.schema.event import Event, EventAccess
from app.api.schema.payment import Payment


class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    sex: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    sex: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    updated_at: datetime
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserInDBBase):
    created_events: List[Event] = []
    managed_events: List[EventAccess] = []
    event_access: List[EventAccess] = []
    payment_logs: List[Payment] = []


class UserInDB(UserInDBBase):
    pass
