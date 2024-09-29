import uuid
from sqlalchemy import Column, String, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from enum import Enum as PyEnum

import enum


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class GenderEnum(PyEnum):
    MALE = "Male"
    FEMALE = "Female"


# User model
class User(Base):
    __tablename__ = "user"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    sex = Column(Enum(GenderEnum), nullable=False)
    last_login = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    password = Column(String, nullable=False)

    # Relationships
    created_events = relationship(
        "Event", foreign_keys="Event.create_by", back_populates="creator"
    )
    managed_events = relationship(
        "EventAccess",
        primaryjoin="User.id == EventAccess.managed_by",
        foreign_keys="EventAccess.managed_by",
        back_populates="manager",
    )
    event_access = relationship(
        "EventAccess",
        primaryjoin="User.id == EventAccess.user_id",
        foreign_keys="EventAccess.user_id",
        back_populates="user",
    )
    payment = relationship("Payment", back_populates="user")
