from sqlalchemy import select,insert
from pydantic import EmailStr
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import UserDataMapper
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword, UserAdd


class UsersRepository(BaseRepository):

    model = UsersORM
    mapper = UserDataMapper


    async def get_user_with_hashed_password(self, email: EmailStr):

        

        query = select(self.model).where(self.model.email==email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        # Чтобы сработал кастомный Exception
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model, from_attributes=True)


    async def add(self, data: UserAdd):

        check_existing_users = await self.session.execute(
            select(self.model).where(self.model.email==data.email)
            )

        result_check = check_existing_users.scalars().one_or_none()

        if result_check:
            raise ValueError('Такой пользователь уже существует!')

        query = insert(self.model).values(**data.model_dump()).returning(self.model)


        result = await self.session.execute(query)

        new_user = result.scalars().one()

        return self.mapper.map_to_domain_entity(new_user)        