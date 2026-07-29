from fastapi import APIRouter
from database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.repos.users import UsersRepository

import bcrypt

router = APIRouter(prefix='/auth', tags=['Аутентификация и авторизация'])


@router.post('/register')
async def register_user(data: UserRequestAdd):
    # Кодируем пароль в байты, генерируем соль и хешируем
    pwd_bytes = data.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {'status': 'OK'}    
