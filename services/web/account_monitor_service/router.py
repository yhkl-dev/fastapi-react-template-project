from fastapi import APIRouter, Depends
from project.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import AccountMonitorService


router = APIRouter()


@router.get("/tasks")
async def get_accounts(
    session: AsyncSession = Depends(get_session),
):
    id = AccountMonitorService.run_task()
    return {"data": id, "code": 200, "message": "REQUEST SUCCESS"}
