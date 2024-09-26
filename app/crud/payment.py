from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models import Payment
from app.schema.payment import PaymentCreate, PaymentUpdate


def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_payments(db: Session, skip: int = 0, limit: int = 100) -> List[Payment]:
    return db.query(Payment).offset(skip).limit(limit).all()


def create_payment(db: Session, payment_in: PaymentCreate) -> Payment:
    db_payment = Payment(
        user_id=payment_in.user_id,
        amount=payment_in.amount,
        currency=payment_in.currency,
        payment_method=payment_in.payment_method,
        phone_number=payment_in.phone_number,
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def update_payment(
    db: Session, payment_id: int, payment_in: PaymentUpdate
) -> Optional[Payment]:
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        return None
    for key, value in payment_in.dict(exclude_unset=True).items():
        setattr(db_payment, key, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def delete_payment(db: Session, payment_id: int) -> Optional[Payment]:
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        return None
    db.delete(db_payment)
    db.commit()
    return db_payment
