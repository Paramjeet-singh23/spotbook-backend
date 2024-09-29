from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from app.utils.security import verify_token
from app.db.session import get_db
from app.crud.user import get_user_by_email
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/api/user/token", "/docs", "/openapi.json"]:
            response = await call_next(request)
            return response

        authentication: str = request.headers.get("Authentication")
        if authentication:
            try:
                scheme, token = authentication.split()
                if scheme.lower() != "bearer":
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication scheme",
                    )
                credentials_exception = HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                token_data = verify_token(token, credentials_exception)

                # Use context manager for database session
                with next(get_db()) as db:
                    print(token_data.email)
                    user = get_user_by_email(db, email=token_data.email)
                    if user is None:
                        raise credentials_exception
                    request.state.user = user
            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Token has expired"
                )
            except jwt.InvalidTokenError:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authentication header missing",
            )

        response = await call_next(request)
        return response
