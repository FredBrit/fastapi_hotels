from fastapi import Depends, Query, Request, HTTPException
from src.services.auth import AuthService
from pydantic import BaseModel
from typing import Annotated
from src.database import async_session_maker
from src.utils.db_manager import DBManager

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description='Номер страницы')]
    per_page: Annotated[int | None, Query(None, ge=1, lt=5, description='Количество отелей на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail='Не предоставлен токен')
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]    

