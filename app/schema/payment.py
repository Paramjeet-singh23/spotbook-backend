from pydantic import BaseModel
from typing import Optional


class PaymentBase(BaseModel):
    user_id: int
    amount: float
    currency: str
    payment_method: str
    phone_number: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    pass


class PaymentInDBBase(PaymentBase):
    id: int

    class Config:
        orm_mode = True


class Payment(PaymentInDBBase):
    pass


class PaymentInDB(PaymentInDBBase):
    pass
