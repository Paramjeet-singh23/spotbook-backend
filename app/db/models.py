from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from app.db.session import Base


# Role model
class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationships
    event_accesses = relationship("EventAccess", back_populates="role")


# EventType model
class EventType(Base):
    __tablename__ = "event_type"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)

    # Relationships
    events = relationship("Event", back_populates="event_type_obj")


# Event model
class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_by = Column(Integer, ForeignKey("users.id"))
    event_type = Column(Integer, ForeignKey("event_type.id"))
    is_repetitive = Column(Boolean)
    event_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    updated_by = Column(Integer, ForeignKey("users.id"))
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
    id = Column(Integer, primary_key=True)
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
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("role.id"))
    managed_by = Column(Integer, ForeignKey("users.id"))
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
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String)
    payment_method = Column(String)
    phone_number = Column(String)

    # Relationships
    user = relationship("Users", back_populates="payment")
