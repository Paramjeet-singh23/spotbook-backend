import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


# EventType model
class EventType(Base):
    __tablename__ = "event_type"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    create_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    updated_by = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    # Relationships
    events = relationship("Event", back_populates="event_type_obj")


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
    event_type = Column(UUID(as_uuid=True), ForeignKey("event_type.id"), nullable=False)
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
    event_type_obj = relationship("EventType", back_populates="events")
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
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"), nullable=False)
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
    role = relationship("Role", back_populates="event_accesses")
