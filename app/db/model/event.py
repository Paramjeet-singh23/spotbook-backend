import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

import enum


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


# Define the Enum class
import enum


class EventTypeEnum(enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"


# Event model
class Event(Base):
    __tablename__ = "event"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    create_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    event_type = Column(Enum(EventTypeEnum), nullable=False)
    is_repetitive = Column(Boolean, default=False)
    event_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    updated_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # Relationships
    creator = relationship(
        "User", foreign_keys=[create_by], back_populates="created_events"
    )
    updater = relationship("User", foreign_keys=[updated_by])
    accesses = relationship("EventAccess", back_populates="event")


# EventAccess model
class EventAccess(Base):
    __tablename__ = "event_access"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    event_id = Column(UUID(as_uuid=True), ForeignKey("event.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    managed_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    updated_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # Relationships
    event = relationship("Event", back_populates="accesses")
    user = relationship(
        "User",
        primaryjoin="User.id == EventAccess.user_id",
        foreign_keys=[user_id],
        back_populates="event_access",
    )
    manager = relationship(
        "User",
        primaryjoin="User.id == EventAccess.managed_by",
        foreign_keys=[managed_by],
        back_populates="managed_events",
    )
