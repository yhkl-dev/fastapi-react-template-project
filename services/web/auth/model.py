from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class InternalAuthToken(BaseModel):
    code: str


class ExternalAuthToken(BaseModel):
    code: str


class InternalAccessTokenData(BaseModel):
    sub: str


class ExternalUser(SQLModel):
    email: str
    username: str
    external_sub_id: str


class InternalUser(SQLModel):
    external_sub_id: str
    internal_sub_id: str
    username: str
    created_at: datetime


class User(InternalUser, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
