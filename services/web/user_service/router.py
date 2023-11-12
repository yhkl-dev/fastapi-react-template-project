from auth.exceptions import AuthorizationException, exception_handling
from auth.model import (
    ExternalAuthToken,
    InternalAccessTokenData,
    InternalAuthToken,
    InternalUser,
)
from auth.provider import AzureAuthProvider
from auth.service import AuthSerive
from auth.util import (
    create_internal_access_token,
    create_internal_auth_token,
)
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from project.config import settings
from project.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import RedirectResponse

from auth.schemes import CSRFTokenRedirectCookieBearer, AccessTokenCookieBearer, AuthTokenBearer

router = APIRouter()


csrf_token_redirect_cookie_scheme = CSRFTokenRedirectCookieBearer()
auth_token_scheme = AuthTokenBearer()
access_token_cookie_scheme = AccessTokenCookieBearer()


@router.get("/login")
async def login(
    response: JSONResponse,
    internal_user: str = Depends(auth_token_scheme),
) -> JSONResponse:
    access_token = await create_internal_access_token(
        InternalAccessTokenData(
            sub=internal_user.internal_sub_id,
        )
    )

    response = JSONResponse(
        content=jsonable_encoder(
            {
                "userLoggedIn": True,
                "userName": internal_user.username,
            }
        ),
    )

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

    return response


@router.get("/login-redirect")
async def login_rediret():
    provider = AzureAuthProvider()
    request_uri, state_csrf_token = await provider.get_request_uri()
    response = RedirectResponse(url=request_uri)
    response.set_cookie(key="state", value=f"Bearer {state_csrf_token}", httponly=True)
    return response


@router.get("/azure-login-callback/")
async def azure_login_callback(
    request: Request,
    _=Depends(csrf_token_redirect_cookie_scheme),
    session: AsyncSession = Depends(get_session),
):
    """Callback triggered when the user logs in to Azure's pop-up.

    Receives an authentication_token from Azure which then
    exchanges for an access_token. The latter is used to
    gain user information from Azure's userinfo_endpoint.

    Args:
            request: The incoming request as redirected by Azure
    """
    code = request.query_params.get("code")

    if not code:
        raise AuthorizationException("Missing external authentication token")

    provider = AzureAuthProvider()

    external_user = await provider.get_user(auth_token=ExternalAuthToken(code=code))
    print(external_user)
    # # Get or create the internal user
    internal_user = await AuthSerive.get_user_by_external_sub_id(session, external_user)

    if not internal_user:
        internal_user = await AuthSerive.create_internal_user(session, external_user)

    internal_auth_token: InternalAuthToken = await create_internal_auth_token(internal_user)
    # Redirect the user to the home page
    redirect_url = f"{settings.FRONTEND_URL}?authToken={internal_auth_token}"
    response = RedirectResponse(url=redirect_url)

    # Delete state cookie. No longer required
    response.delete_cookie(key="state")

    return response


@router.get("/user-session-status/")
async def user_session_status(internal_user: InternalUser = Depends(access_token_cookie_scheme)) -> JSONResponse:
    """User status endpoint for checking whether the user currently holds
    an HTTPOnly cookie with a valid access token.

    Args:
        internal_user: A user object that has meaning in this application

    Returns:
        response: A JSON response with the status of the user's session
    """
    async with exception_handling():
        logged_id = True if internal_user else False

        response = JSONResponse(
            content=jsonable_encoder(
                {
                    "userLoggedIn": logged_id,
                    "userName": internal_user.username,
                }
            ),
        )

        return response
