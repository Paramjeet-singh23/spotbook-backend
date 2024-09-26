from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone
from app.db.models import Event
from app.schema.event import EventCreate, EventUpdate


def get_event(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).offset(skip).limit(limit).all()


def create_event(db: Session, event_in: EventCreate) -> Event:
    db_event = Event(
        name=event_in.name,
        create_by=event_in.create_by,
        event_type=event_in.event_type,
        is_repetitive=event_in.is_repetitive,
        event_date=event_in.event_date,
        field=event_in.field,
        created_at=datetime.utcnow(),
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_id: int, event_in: EventUpdate) -> Optional[Event]:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None
    for key, value in event_in.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    db_event.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int) -> Optional[Event]:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None
    db.delete(db_event)
    db.commit()
    return db_event
