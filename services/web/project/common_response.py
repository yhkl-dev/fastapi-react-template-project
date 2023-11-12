from pydantic import BaseModel


class CommonResponseModel(BaseModel):
    code: int
    message: str
    data: dict = None
