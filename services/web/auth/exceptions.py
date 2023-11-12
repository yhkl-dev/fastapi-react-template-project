from contextlib import asynccontextmanager

from fastapi import HTTPException, status
from project.logger import logging

logger = logging.getLogger(__name__)


class DatabaseException(Exception):
    pass


class UnknownDatabaseType(DatabaseException):
    pass


class DatabaseConnectionError(DatabaseException):
    pass


class AuthenticationException(Exception):
    pass


class UnknownAuthenticationProvider(AuthenticationException):
    pass


class AuthorizationException(Exception):
    pass


class UnauthorizedUser(AuthorizationException):
    pass


class DiscoveryDocumentError(AuthorizationException):
    pass


class ProviderConnectionError(AuthorizationException):
    pass


@asynccontextmanager
async def exception_handling():
    try:
        yield
    except DatabaseConnectionError as exc:
        print(1)
        raise HTTPException(status_code=500, detail="Cannot serve results at the moment. Please try again.")
    except UnauthorizedUser as exc:
        print(2)
        print(f"unauthrized: {exc}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    except Exception as exc:
        print(3, exc)
        logger.error(f"Got error {exc}")
        raise HTTPException(status_code=500, detail="An error has occurred. Please try again.")
