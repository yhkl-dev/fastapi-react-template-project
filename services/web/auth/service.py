import hashlib

from passlib.hash import bcrypt
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.model import ExternalUser, InternalUser, User
import datetime
from uuid import uuid4
from sqlmodel import select
from typing import Optional


class AuthSerive:
    @staticmethod
    async def create_internal_user(session: AsyncSession, external_user: ExternalUser) -> InternalUser:
        encrypted_external_sub_id = await encrypt_external_sub_id(external_user)
        unique_identifier = str(uuid4())
        i_user = User(
            internal_sub_id=unique_identifier,
            external_sub_id=encrypted_external_sub_id,
            username=external_user.username,
            created_at=datetime.datetime.utcnow(),
        )

        session.add(i_user)
        await session.commit()
        await session.refresh(i_user)
        return i_user

    @staticmethod
    async def get_user(session: AsyncSession, id: str) -> Optional[User]:
        query = select(User).where(User.external_sub_id == id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_internal_id(session: AsyncSession, id: str) -> Optional[User]:
        query = select(User).where(User.internal_sub_id == id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_external_sub_id(session: AsyncSession, external_user: ExternalUser) -> InternalUser:
        internal_user = None
        encrypted_external_sub_id = await encrypt_external_sub_id(external_user)

        db_user = await AuthSerive.get_user(session, encrypted_external_sub_id)

        if db_user:
            internal_user = InternalUser(
                internal_sub_id=db_user.internal_sub_id,
                external_sub_id=db_user.external_sub_id,
                username=db_user.username,
                created_at=db_user.created_at,
            )

        return internal_user

    @staticmethod
    async def get_user_by_internal_sub_id(session: AsyncSession, internal_sub_id: str) -> InternalUser:
        internal_user = None
        user: User = await AuthSerive.get_user_by_internal_id(session, internal_sub_id)

        if user:
            internal_user = InternalUser(
                internal_sub_id=user.internal_sub_id,
                external_sub_id=user.external_sub_id,
                username=user.username,
                created_at=user.created_at,
            )

        return internal_user


async def encrypt_external_sub_id(external_user: ExternalUser) -> str:
    """It encrypts the subject id received from the external provider. These ids are
    used to uniquely identify a user in the system of the external provider and
    are usually public. However, it is better to be stored encrypted just in case.

    Args:
            external_user: An object representing a user with information
                                            based on the external provider's service.

    Returns:
            encrypted_external_sub_id: The encrypted external subject id
    """
    salt = external_user.email.lower()
    salt = salt.replace(" ", "")
    # Hash the salt so that the email is not plain text visible in the database
    salt = hashlib.sha256(salt.encode()).hexdigest()
    # bcrypt requires a 22 char salt
    if len(salt) > 21:
        salt = salt[:21]

    # As per passlib the last character of the salt should always be one of [.Oeu]
    salt = salt + "O"

    encrypted_external_sub_id = bcrypt.using(salt=salt).hash(external_user.external_sub_id)
    return encrypted_external_sub_id
