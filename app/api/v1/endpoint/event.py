from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schema.event import Event, EventCreate, EventUpdate
from app.db.session import get_db
from app.crud.event import (
    get_event,
    get_events,
    create_event,
    update_event,
    delete_event,
)

router = APIRouter()


@router.get("/", response_model=List[Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = get_events(db, skip=skip, limit=limit)
    return events


@router.post("/", response_model=Event)
def create_new_event(event: EventCreate, db: Session = Depends(get_db)):
    return create_event(db=db, event_in=event)


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.put("/{event_id}", response_model=Event)
def update_existing_event(
    event_id: int, event: EventUpdate, db: Session = Depends(get_db)
):
    db_event = update_event(db=db, event_id=event_id, event_in=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.delete("/{event_id}", response_model=Event)
def delete_existing_event(event_id: int, db: Session = Depends(get_db)):
    db_event = delete_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event
