from faker import Faker
from fastapi import APIRouter, Depends, Request
from project.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import (
    ServiceAccount,
    ServiceAccountCreateOrUpdate,
    ServiceAccountCreateOrUpdateResponse,
    ServiceAccountListResponse,
    ServiceAccountResponse,
    ServiceAccountDeleteResponse,
)
from .service import ServiceAccountService

router = APIRouter()


@router.get("/accounts", response_model=ServiceAccountListResponse)
async def get_accounts(
    session: AsyncSession = Depends(get_session),
    page: int = 1,
    size: int = 10,
    request: Request = None,
):
    query_params = dict(request.query_params)
    query_params.pop("page", None)
    query_params.pop("size", None)
    items = await ServiceAccountService.get_all(session, page, size, **query_params)
    counts = await ServiceAccountService.count_all(session, **query_params)
    return {"total": counts, "items": items, "code": 200, "message": "REQUEST SUCCESS"}


@router.get("/accounts/{service_account_id}", response_model=ServiceAccountResponse)
async def get_account(
    service_account_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await ServiceAccountService.get(service_account_id=int(service_account_id), session=session)
    return {"data": result, "code": 200, "message": "REQUEST SUCCESS"}


@router.post(
    "/accounts",
    response_model=ServiceAccountCreateOrUpdateResponse,
)
async def create_account(
    payload: ServiceAccount,
    session: AsyncSession = Depends(get_session),
) -> ServiceAccountCreateOrUpdateResponse:
    result = await ServiceAccountService.create(session, payload)
    return {"data": result, "code": 201, "message": "REQUEST SUCCESS"}


@router.put(
    "/accounts/{service_account_id}",
    response_model=ServiceAccountCreateOrUpdateResponse,
)
async def update_account(
    service_account_id: int,
    payload: ServiceAccountCreateOrUpdate,
    session: AsyncSession = Depends(get_session),
) -> ServiceAccountCreateOrUpdateResponse:
    result = await ServiceAccountService.update(session, service_account_id, payload)
    if result:
        return {"data": result, "code": 200, "message": "REQUEST SUCCESS"}
    return {"data": None, "code": 400, "message": "RESOURCE NOT FOUND"}


@router.delete("/accounts/{service_account_id}", response_model=ServiceAccountDeleteResponse)
async def delete_account(
    service_account_id: int,
    session: AsyncSession = Depends(get_session),
) -> ServiceAccountDeleteResponse:
    await ServiceAccountService.delete(session, service_account_id)
    return {"message": "Account deleted", "code": 200}


@router.get("/fake")
async def fake_data(
    session: AsyncSession = Depends(get_session),
):
    fake = Faker()
    for _ in range(100):
        fake_account = ServiceAccount(
            account_name=fake.name(),
            domain=fake.domain_name(),
            account_expiration_date=fake.future_datetime(),
            email_address=fake.email(),
            abi_password_rule=fake.boolean(),
            password_expiration_date=fake.future_datetime(),
            owner_email=fake.email(),
            applicant_email=fake.email(),
            end_user_email=fake.email(),
            group=fake.word(),
            role=fake.word(),
            account_permission=fake.word(),
            server_name=fake.hostname(),
            ip=fake.ipv4(),
            service_name=fake.word(),
            application_name=fake.word(),
            save_the_password_in_script=fake.boolean(),
            script_name=fake.file_name(),
            account_for_different_application=fake.boolean(),
            multiple_apps=fake.word(),
            managed_system_description=fake.sentence(),
            managed_account_description=fake.sentence(),
            change_the_password_periodically=fake.boolean(),
            account_automanage=fake.boolean(),
        )
        session.add(fake_account)
    await session.commit()
    await session.flush()
    return {"message": "success"}
