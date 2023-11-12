import datetime
import hashlib
import os
from typing import Optional

from auth.service import AuthSerive
from jwt import PyJWTError
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode
from project.cache import cache
from project.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession

from .exceptions import UnauthorizedUser
from .model import InternalAccessTokenData, InternalAuthToken, InternalUser


async def create_state_csrf_token() -> str:
    """Creates a CSRF token to mitigate CSRF attacks on redirects from
    from the Authentication provider.

    The token is added in an HTTPOnly, secure cookie on the browser
    and also passed to the Auth provider as a "state" parameter.
    When the Auth provider redirects the user back to our service,
    we check that the HTTPOnly cookie value matches the "state" value
    returned by the Auth provider. We also check that we did add this
    token in the cache at some time in the past.

    Returns:
            state_csrf_token: The csrf token
    """
    state_csrf_token = hashlib.sha256(os.urandom(1024)).hexdigest()

    # Values not necessary. We only need to check for existence
    await cache.set(state_csrf_token, {"valid": True})

    return state_csrf_token


async def validate_state_csrf_token(state_csrf_token: str, state_csrf_token_cookie: str):
    """Checks the validity of a state token received by the redirect url,
    against the state token that the server added in the browser cookie.

    Args:
            state_csrf_token: The token returned in the redirect url
            state_csrf_token_cookie: The token saved previously in the cookie
    """
    if state_csrf_token != state_csrf_token_cookie:
        raise UnauthorizedUser("Failed to validate state token")

    # Also, check that we 100% cached that token in the past
    cached_token = await cache.get(state_csrf_token)

    if not cached_token:
        raise UnauthorizedUser("Failed to validate against cached state token")

    await cache.delete(state_csrf_token)


async def create_internal_auth_token(internal_user: InternalUser) -> InternalAuthToken:
    """Creates a one time JWT authentication token to return to the user.
    The token is used as a key to cache the user's internal id until
    he requests for an access token when it is removed from the cache.

    Args:
            internal_user: A user object that has meaning in this application

    Returns:
            encoded_jwt: The encoded JWT authentication token

    """
    expires_delta = datetime.timedelta(minutes=int(settings.AUTH_TOKEN_EXPIRE_MINUTES))

    expire = datetime.datetime.utcnow() + expires_delta

    to_encode = dict(exp=expire, sub=internal_user.internal_sub_id)

    encoded_jwt = jwt_encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

    # Add token/user pair in the cache
    await cache.set(encoded_jwt, internal_user.internal_sub_id)

    return encoded_jwt


async def validate_internal_access_token(session: AsyncSession, internal_access_token: str) -> Optional[InternalUser]:
    """Checks the validity of an internal access token. If the token
    is valid it also checks whether there is an associated user
    in the database, and returns it.

    Args:
        internal_access_token: Internal access token

    Returns:
        internal_user: A user object as defined in this application
    """
    try:
        payload = jwt_decode(internal_access_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        internal_sub_id: str = payload.get("sub")
        if internal_sub_id is None:
            raise UnauthorizedUser("Missing 'sub' id from access token")

    except PyJWTError as exc:
        raise UnauthorizedUser(f"Failed to validate access token: {exc}")
    if session:
        internal_user = await AuthSerive.get_user_by_internal_sub_id(session, internal_sub_id)
        if not internal_user:
            raise UnauthorizedUser(f"User {internal_sub_id} does not exist")

        return internal_user
    return None


async def validate_state_csrf_token(state_csrf_token: str, state_csrf_token_cookie: str):
    """Checks the validity of a state token received by the redirect url,
    against the state token that the server added in the browser cookie.

    Args:
            state_csrf_token: The token returned in the redirect url
            state_csrf_token_cookie: The token saved previously in the cookie
    """
    if state_csrf_token != state_csrf_token_cookie:
        raise UnauthorizedUser(f"Failed to validate state token")

    # Also, check that we 100% cached that token in the past
    cached_token = await cache.get(state_csrf_token)

    if not cached_token:
        raise UnauthorizedUser(f"Failed to validate against cached state token")

    await cache.delete(state_csrf_token)


async def validate_internal_auth_token(session: AsyncSession, internal_auth_token: str) -> InternalUser:
    """Checks the validity of an internal authentication token.
    If the token is valid it also checks whether there is an
    associated user in the cache, and returns it.

    Args:
            internal_auth_token: Internal authentication token

    Returns:
            internal_user: A user object as defined in this application
    """
    try:
        jwt_decode(internal_auth_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except PyJWTError as exc:
        raise UnauthorizedUser(f"Failed to validate auth token: {exc}")

    internal_sub_id = await cache.get(internal_auth_token)

    if not internal_sub_id:
        raise UnauthorizedUser(f"User {internal_sub_id} not cached")

    # Invalidate cache. Authentication token can only be used once
    await cache.delete(internal_auth_token)

    internal_user = await AuthSerive.get_user_by_internal_sub_id(session, internal_sub_id)

    return internal_user


async def create_internal_access_token(access_token_data: InternalAccessTokenData) -> str:
    """Creates a JWT access token to return to the user.

    Args:
            access_token_data: The data to be included in the JWT access token

    Returns:
            encoded_jwt: The encoded JWT access token
    """
    expires_delta = datetime.timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = access_token_data.dict()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update(dict(exp=expire))
    encoded_jwt = jwt_encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt
