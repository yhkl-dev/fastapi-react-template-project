from auth.util import validate_internal_access_token
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from auth.exceptions import UnauthorizedUser


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        token = request.headers.get("Authorization")
        if (
            request.url.path
            not in [
                "/login",
                "/login-redirect",
                "/azure-login-callback/",
                "/user-session-status/",
                "/docs",
                "/openapi.json",
            ]
            and request.method != "OPTIONS"
        ):  # 跳过登录接口
            if not token:
                return JSONResponse(
                    content="Could not validate credentials",
                    status_code=HTTP_401_UNAUTHORIZED,
                    headers={
                        "Access-Control-Allow-Origin": "http://localhost:3000",
                        "Access-Control-Allow-Credentials": "true",
                    },
                )
            else:
                token = token.split(" ")[1]
                try:
                    await validate_internal_access_token(
                        None,
                        token,
                    )
                except UnauthorizedUser as e:
                    print(e)
                    return JSONResponse(
                        content="Could not validate credentials",
                        status_code=HTTP_401_UNAUTHORIZED,
                        headers={
                            "Access-Control-Allow-Origin": "http://localhost:3000",
                            "Access-Control-Allow-Credentials": "true",
                        },
                    )
        response: Response = await call_next(request)
        return response
