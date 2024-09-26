from fastapi import FastAPI
import uvicorn
from app.config import settings
from app.utils.logging_config import setup_logging
from app.db.session import get_db
from app.api.v1.router import router as api_router

# Initialize logging
setup_logging()

# # Initialize the database
get_db()


app = FastAPI()
app.include_router(api_router, prefix="/api")

# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(events.router, prefix="/events", tags=["events"])

# Print settings to verify
print(f"Host: {settings.HOST}, Port: {settings.PORT}")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level="info")
