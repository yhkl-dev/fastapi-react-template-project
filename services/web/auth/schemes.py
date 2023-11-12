from typing import Optional

from auth.exceptions import UnauthorizedUser, exception_handling
from auth.model import InternalUser
from auth.util import (
    validate_internal_access_token,
    validate_internal_auth_token,
    validate_state_csrf_token,
)
from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param
from project.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


class CSRFTokenRedirectCookieBearer:
    """Scheme that checks the validity of the state parameter
    returned by the Authentication provider when it redirects
    the user to the application after a successful sing in.
    """

    async def __call__(self, request: Request):
        async with exception_handling():
            # State token from redirect
            state_csrf_token: str = request.query_params.get("state")
            # State token from cookie
            state_csrf_token_cookie: str = request.cookies.get("state")

            if not state_csrf_token_cookie:
                raise UnauthorizedUser("Invalid state token")

            # Remove Bearer
            state_csrf_token_cookie = state_csrf_token_cookie.split()[1]

            await validate_state_csrf_token(state_csrf_token, state_csrf_token_cookie)


class AuthTokenBearer:
    """Scheme that checks the validity of the authorization token
    that is exchanged prior to authenticating the user in the
    service and issuing the final access token.
    """

    async def __call__(self, request: Request, session: AsyncSession = Depends(get_session)) -> Optional[str]:
        async with exception_handling():
            authorization: str = request.headers.get("Authorization")
            scheme, internal_auth_token = get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "bearer":
                raise UnauthorizedUser("Invalid authentication token")

            internal_user = await validate_internal_auth_token(session, internal_auth_token)

            return internal_user


class AccessTokenCookieBearer:
    """Scheme that checks the validity of the access token
    that is stored to an HTTPOnly secure cookie in order
    to authorize the user.
    """

    async def __call__(self, request: Request, session: AsyncSession = Depends(get_session)) -> InternalUser:
        async with exception_handling():
            internal_access_token: str = request.cookies.get("access_token")
            if not internal_access_token:
                raise UnauthorizedUser("Invalid access token cookie")

            internal_access_token = internal_access_token.split()[1]
            print("internal_access_token", internal_access_token)

            internal_user = await validate_internal_access_token(session, internal_access_token)

            return internal_user
