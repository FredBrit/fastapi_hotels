from sqlalchemy import select, insert, update, delete
from src.schemas.hotels import Hotel
from pydantic import BaseModel


class BaseRepository:

    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self, **filters):

        conditions = [getattr(self.model, key) == value for key, value in filters.items()]

        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()
   
    async def get_one_or_none(self, **filters):

        conditions = [getattr(self.model, key) == value for key, value in filters.items()]

        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True) 

    async def add(self, data: BaseModel):

        
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)

        result = await self.session.execute(add_data_stmt)

        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True) 


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filters) -> None:

        conditions = [getattr(self.model, key) == value for key, value in filters.items()]

        stmt = (
            update(self.model)
            .where(*conditions)
            .values(**data.model_dump(exclude_unset=exclude_unset)).returning(self.model)
        )

        result = await self.session.execute(stmt)

        return result.scalars().one()
        
                


    async def delete(self, **filters) -> None:
        conditions = [getattr(self.model, key) == value for key, value in filters.items()]

        stmt = (
            delete(self.model)
            .where(*conditions)
            .returning(self.model)
        )

        result = await self.session.execute(stmt)

        return result.scalars().one()