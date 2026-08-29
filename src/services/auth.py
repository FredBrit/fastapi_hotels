from fastapi import Request
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from src.config import settings
from src.services.base import BaseService
from src.schemas.users import UserAdd, UserRequestAdd, UserWithHashedPassword
from src.exceptions import (
    IncorrectTokenException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
)


class AuthService(BaseService):
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        # Стандарт JWT рекомендует использовать claim 'sub' (subject) для ID пользователя
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserRequestAdd) -> str:
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token 

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one(id=user_id)   
        
