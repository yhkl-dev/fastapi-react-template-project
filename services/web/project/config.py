from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str
    OPENAPI_CLIENT_ID: str = ""
    APP_CLIENT_ID: str = ""
    TENANT_ID: str = ""
    SCOPE_DESCRIPTION: str = "user_impersonation"
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_TENANT_ID: str
    AZURE_REDIRECT_URL: str
    FRONTEND_URL: str
    AUTH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str
    ALGORITHM: str

    @property
    def AZURE_AUTHORITY(self) -> str:
        return f"https://login.microsoftonline.com/{self.AZURE_TENANT_ID}"

    @property
    def AZURE_DISCOVERY_URL(self) -> str:
        return f"{self.AZURE_AUTHORITY}/v2.0/.well-known/openid-configuration"

    @property
    def SCOPE_NAME(self) -> str:
        return f"api://{self.APP_CLIENT_ID}/{self.SCOPE_DESCRIPTION}"

    @property
    def SCOPES(self) -> dict:
        return {
            self.SCOPE_NAME: self.SCOPE_DESCRIPTION,
        }

    @property
    def OPENAPI_AUTHORIZATION_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.AZURE_TENANT_ID}/oauth2/v2.0/authorize"

    @property
    def OPENAPI_TOKEN_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.AZURE_TENANT_ID}/oauth2/v2.0/token"


settings = Settings()
