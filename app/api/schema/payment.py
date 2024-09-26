from pydantic import BaseModel
from typing import Optional


class PaymentLogBase(BaseModel):
    user_id: int
    amount: float
    currency: str
    payment_method: str
    phone_number: Optional[str] = None


class PaymentLogCreate(PaymentLogBase):
    pass


class PaymentLogUpdate(PaymentLogBase):
    pass


class PaymentLogInDBBase(PaymentLogBase):
    id: int

    class Config:
        orm_mode = True


class PaymentLog(PaymentLogInDBBase):
    pass


class PaymentLogInDB(PaymentLogInDBBase):
    pass
