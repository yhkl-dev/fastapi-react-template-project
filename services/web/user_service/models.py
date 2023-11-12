from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class LoginPayLoad(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# class UserTable(SQLModel, table=True):
#     id: int = Field(default=None, nullable=False, primary_key=True)
