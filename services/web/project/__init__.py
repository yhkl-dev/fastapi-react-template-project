from contextlib import asynccontextmanager

from account_monitor_service.router import router as account_monitor_router
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from service_account_service.router import router as service_account_router
from user_service.router import router as user_router
from fastapi.openapi.docs import get_swagger_ui_html
from .database import init_db
from .middleware import JWTMiddleware


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("init lifespan")
    await init_db()
    yield
    print("clean up lifespan")


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=app_lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(JWTMiddleware)
    app.include_router(service_account_router, prefix="/api")
    app.include_router(account_monitor_router, prefix="/api")
    app.include_router(user_router, prefix="")

    @app.get("/docs", include_in_schema=False)
    async def custom_docs():
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

    return app


app = create_app()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )
