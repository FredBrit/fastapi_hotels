from sqlalchemy import select
from pydantic import EmailStr
from src.repos.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):

    model = UsersORM
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):

        

        query = select(self.model).where(self.model.email==email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        # Чтобы сработал кастомный Exception
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model, from_attributes=True) 