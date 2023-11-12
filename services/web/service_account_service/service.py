from typing import List, Optional

from project.logger import setup_logger
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import ServiceAccount, ServiceAccountCreateOrUpdate
from datetime import datetime

logger = setup_logger()


class ServiceAccountService:
    @staticmethod
    async def get_all(session: AsyncSession, page: int = 1, size: int = 10, **kwargs) -> List[ServiceAccount]:
        query = select(ServiceAccount)

        for key, value in kwargs.items():
            if hasattr(ServiceAccount, key) and value != "":
                query = query.where(getattr(ServiceAccount, key) == value)
        result = await session.execute(query.offset((page - 1) * size).limit(size))
        return result.scalars().all()

    @staticmethod
    async def count_all(session: AsyncSession, **kwargs) -> int:
        query = select(ServiceAccount)
        for key, value in kwargs.items():
            if hasattr(ServiceAccount, key):
                query = query.where(getattr(ServiceAccount, key) == value)

        result = await session.execute(query)
        return len(result.scalars().all())

    @staticmethod
    async def get(service_account_id: int, session: AsyncSession) -> Optional[ServiceAccount]:
        query = select(ServiceAccount).where(ServiceAccount.id == service_account_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create(session: AsyncSession, account: ServiceAccount) -> ServiceAccountCreateOrUpdate:
        session.add(account)
        await session.commit()
        await session.refresh(account)
        return account

    @staticmethod
    async def update(
        session: AsyncSession, account_id: int, account: ServiceAccountCreateOrUpdate
    ) -> Optional[ServiceAccountCreateOrUpdate]:
        query = select(ServiceAccount).where(ServiceAccount.id == account_id)
        result = await session.execute(query)
        service_account = result.scalars().first()
        if service_account:
            logger.info(f"update service account: {service_account.id}")
            for key, value in account.dict().items():
                if isinstance(value, datetime) and value.tzinfo is not None:
                    value = value.replace(tzinfo=None)
                setattr(service_account, key, value)
            session.add(service_account)
            await session.commit()
            await session.refresh(service_account)
            return service_account
        logger.info(f"No service account: {account_id} found")
        return None

    @staticmethod
    async def delete(
        session: AsyncSession,
        account_id: int,
    ):
        query = select(ServiceAccount).where(ServiceAccount.id == account_id)
        result = await session.execute(query)
        service_account = result.scalars().first()
        if service_account:
            await session.delete(service_account)
            await session.commit()
        return None
