from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.db.model.event import Event, EventAccess, RoleEnum
from app.schema.event import EventCreate, EventUpdate, EventAccessCreate


def create_event(db: Session, event: EventCreate, user_id: UUID):
    db_event = Event(
        name=event.name,
        event_type=event.event_type,
        is_repetitive=event.is_repetitive,
        event_date=event.event_date,
        create_by=user_id,
        updated_by=user_id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Automatically create EventAccess with ADMIN role
    db_event_access = EventAccess(
        event_id=db_event.id,
        user_id=user_id,
        role=RoleEnum.ADMIN,
        managed_by=user_id,
        updated_by=user_id,
    )
    db.add(db_event_access)
    db.commit()
    db.refresh(db_event_access)

    return db_event


def get_event(db: Session, event_id: UUID):
    return db.query(Event).filter(Event.id == event_id).first()


def update_event(db: Session, event_id: UUID, event: EventUpdate, user_id: UUID):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.name = event.name
        db_event.event_type = event.event_type
        db_event.is_repetitive = event.is_repetitive
        db_event.event_date = event.event_date
        db_event.updated_by = user_id
        db.commit()
        db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: UUID):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event


def create_event_access(db: Session, event_access: EventAccessCreate, user_id: UUID):
    db_event_access = EventAccess(
        event_id=event_access.event_id,
        user_id=event_access.user_id,
        role=event_access.role,
        managed_by=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        updated_by=user_id,
    )
    db.add(db_event_access)
    db.commit()
    db.refresh(db_event_access)
    return db_event_access


def get_event_access(db: Session, event_access_id: UUID):
    return db.query(EventAccess).filter(EventAccess.id == event_access_id).first()


def update_event_access(
    db: Session, event_access_id: UUID, event_access: EventAccessCreate, user_id: UUID
):
    db_event_access = (
        db.query(EventAccess).filter(EventAccess.id == event_access_id).first()
    )
    if db_event_access:
        db_event_access.event_id = event_access.event_id
        db_event_access.user_id = event_access.user_id
        db_event_access.role = event_access.role
        db_event_access.updated_at = datetime.utcnow()
        db_event_access.updated_by = user_id
        db.commit()
        db.refresh(db_event_access)
    return db_event_access


def delete_event_access(db: Session, event_access_id: UUID):
    db_event_access = (
        db.query(EventAccess).filter(EventAccess.id == event_access_id).first()
    )
    if db_event_access:
        db.delete(db_event_access)
        db.commit()
    return db_event_access


def check_user_access_to_event(db: Session, user_id: UUID, event_id: UUID) -> bool:
    # Implement your logic to check if the user has access to the event
    # For example, you can query the database to see if the user is associated with the event
    event_access = (
        db.query(EventAccess).filter_by(user_id=user_id, event_id=event_id).first()
    )
    return event_access is not None


def check_is_user_admin(db: Session, user_id: UUID, event_id: UUID) -> bool:
    roles = (
        db.query(EventAccess.role)
        .filter(EventAccess.user_id == user_id, EventAccess.event_id == event_id)
        .all()
    )
    role_names = [
        role[0] for role in roles
    ]  # Extract the role names from the query result
    return RoleEnum.ADMIN.value in role_names
