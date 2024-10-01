from fastapi import FastAPI
import uvicorn
from app.config import settings
from app.utils.logging_config import setup_logging
from app.db.session import get_db
from app.api.v1.router import router as api_router
from app.middleware.auth import AuthMiddleware
from fastapi.openapi.utils import get_openapi

# Initialize logging
setup_logging()

# # Initialize the database
get_db()


app = FastAPI()


# Custom OpenAPI schema generation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API description",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authentication",
            "in": "header",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Assign the custom OpenAPI function
app.openapi = custom_openapi

app.include_router(api_router, prefix="/api")
app.add_middleware(AuthMiddleware)

# Print settings to verify
print(f"Host: {settings.HOST}, Port: {settings.PORT}")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level="info")
