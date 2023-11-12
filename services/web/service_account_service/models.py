from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class CustomDateTime(datetime):
    def json(self):
        return self.strftime("%Y-%m-%d %H:%M:%S")


class ServiceAccountBase(SQLModel):
    account_name: str
    domain: str
    email_address: str
    account_expiration_date: CustomDateTime
    abi_password_rule: bool
    password_expiration_date: CustomDateTime
    owner_email: str
    applicant_email: str
    end_user_email: str
    group: str
    role: str
    account_permission: str
    server_name: str
    ip: str
    applicant_email: str
    service_name: str
    application_name: str
    save_the_password_in_script: bool
    script_name: str
    account_for_different_application: bool
    multiple_apps: str
    managed_system_description: str
    managed_account_description: str
    change_the_password_periodically: bool
    account_automanage: bool

    class Config:
        json_encoders = {
            CustomDateTime: lambda v: v.json(),
        }


class ServiceAccount(ServiceAccountBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class ServiceAccountCreateOrUpdate(ServiceAccountBase):
    pass


class ServiceAccountCreateOrUpdateResponse(BaseModel):
    code: int
    message: str
    data: Optional[ServiceAccountCreateOrUpdate]


class ServiceAccountDeleteResponse(BaseModel):
    code: int
    message: str


class ServiceAccountResponse(BaseModel):
    code: int
    message: str
    data: Optional[ServiceAccount]


class ServiceAccountListResponse(BaseModel):
    code: int
    message: str
    total: int
    items: List[ServiceAccount]
