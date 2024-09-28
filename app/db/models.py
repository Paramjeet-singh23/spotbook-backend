import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


# Role model
class Role(Base):
    __tablename__ = "role"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String)

    # Relationships
    event_accesses = relationship("EventAccess", back_populates="role")


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
    name = Column(String)
    create_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime)

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
    name = Column(String)
    create_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    event_type = Column(UUID(as_uuid=True), ForeignKey("event_type.id"))
    is_repetitive = Column(Boolean)
    event_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    field = Column(String)

    # Relationships
    creator = relationship(
        "Users", foreign_keys=[create_by], back_populates="created_events"
    )
    updater = relationship("Users", foreign_keys=[updated_by])
    event_type_obj = relationship("EventType", back_populates="events")
    accesses = relationship("EventAccess", back_populates="event")


# Users model
class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    sex = Column(String)
    created_at = Column(DateTime)
    last_login = Column(DateTime)
    updated_at = Column(DateTime)
    hashed_password = Column(String)

    # Relationships
    created_events = relationship(
        "Event", foreign_keys="Event.create_by", back_populates="creator"
    )
    managed_events = relationship(
        "EventAccess", foreign_keys="EventAccess.managed_by", back_populates="manager"
    )
    event_access = relationship("EventAccess", back_populates="user")
    payment_logs = relationship("PaymentLog", back_populates="user")


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
    event_id = Column(UUID(as_uuid=True), ForeignKey("event.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id"))
    managed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime)

    # Relationships
    event = relationship("Event", back_populates="accesses")
    user = relationship("Users", back_populates="event_access")
    manager = relationship(
        "Users", foreign_keys=[managed_by], back_populates="managed_events"
    )
    role = relationship("Role", back_populates="event_accesses")


# PaymentLog model
class Payment(Base):
    __tablename__ = "payment"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String)
    payment_method = Column(String)
    phone_number = Column(String)

    # Relationships
    user = relationship("Users", back_populates="payment")
