from fastapi import APIRouter
from app.api.v1.endpoint import event, user, payment

router = APIRouter()

# Include individual routers
router.include_router(event.router, prefix="/event", tags=["Event"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(payment.router, prefix="/payment", tags=["Payment"])
