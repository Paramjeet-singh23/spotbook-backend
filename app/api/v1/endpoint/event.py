from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.schema.event import (
    EventCreate,
    EventUpdate,
    Event,
    EventAccessCreate,
    EventAccess,
)
from app.crud.event import (
    create_event,
    get_event,
    update_event,
    delete_event,
    create_event_access,
    get_event_access,
    update_event_access,
    delete_event_access,
    check_is_user_admin,
)
from app.utils.security import get_user_id_from_token
from app.crud.event import check_user_access_to_event

router = APIRouter()


@router.post("/", response_model=None)
def create_event_endpoint(
    event: EventCreate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id_from_token),
):
    return create_event(db, event, user_id)


@router.get("/{event_id}", response_model=Event)
def get_event_endpoint(
    event_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id_from_token),
):
    if not check_user_access_to_event(db, user_id, event_id):
        raise HTTPException(status_code=403, detail="Access forbidden")
    db_event = get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.put("/{event_id}", response_model=Event)
def update_event_endpoint(
    event_id: UUID,
    event: EventUpdate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id_from_token),
):
    if not check_user_access_to_event(db, user_id, event_id):
        raise HTTPException(status_code=403, detail="Access forbidden")
    db_event = update_event(db, event_id, event, user_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.delete("/{event_id}", response_model=Event)
def delete_event_endpoint(
    event_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id_from_token),
):
    if not check_user_access_to_event(db, user_id, event_id):
        raise HTTPException(status_code=403, detail="Access forbidden")

    db_event = delete_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.post("/event_accesses/", response_model=EventAccess)
def create_event_access_endpoint(
    event_access: EventAccessCreate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id_from_token),
):
    return create_event_access(db, event_access, user_id)


@router.get("/event_accesses/{event_access_id}", response_model=EventAccess)
def get_event_access_endpoint(event_access_id: UUID, db: Session = Depends(get_db)):
    db_event_access = get_event_access(db, event_access_id)
    if db_event_access is None:
        raise HTTPException(status_code=404, detail="Event access not found")
    return db_event_access


@router.put("/event_accesses/{event_access_id}", response_model=EventAccess)
def update_event_access_endpoint(
    event_access_id: UUID,
    event_id: UUID,
    event_access: EventAccessCreate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id_from_token),
):
    if not check_is_user_admin(db, user_id, event_id):
        raise HTTPException(status_code=403, detail="Access forbidden")

    db_event_access = update_event_access(db, event_access_id, event_access, user_id)
    if db_event_access is None:
        raise HTTPException(status_code=404, detail="Event access not found")
    return db_event_access


@router.delete("/event_accesses/{event_access_id}", response_model=EventAccess)
def delete_event_access_endpoint(
    event_access_id: UUID,
    event_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id_from_token),
):
    if not check_is_user_admin(db, user_id, event_id):
        raise HTTPException(status_code=403, detail="Access forbidden")

    db_event_access = delete_event_access(db, event_access_id)
    if db_event_access is None:
        raise HTTPException(status_code=404, detail="Event access not found")
    return db_event_access
