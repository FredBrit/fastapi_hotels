from sqlalchemy import select, insert, update, delete
from src.schemas.hotels import Hotel
from pydantic import BaseModel
from src.repos.mappers.base import DataMapper


class BaseRepository:

    model = None
    mapped: DataMapper = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self, *expressions, **filters):

        conditions = [getattr(self.model, key) == value for key, value in filters.items()]
        conditions.extend(expressions)

        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, **filters):
        return await self.get_filtered(**filters)
   
    async def get_one_or_none(self, **filters):

        conditions = [getattr(self.model, key) == value for key, value in filters.items()]

        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model) 

    async def add(self, data: BaseModel):

        
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)

        result = await self.session.execute(add_data_stmt)

        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)    


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filters) -> None:

        conditions = [getattr(self.model, key) == value for key, value in filters.items()]

        stmt = (
            update(self.model)
            .where(*conditions)
            .values(**data.model_dump(exclude_unset=exclude_unset)).returning(self.model)
        )

        result = await self.session.execute(stmt)

        return result.scalars().one()
        
                


    async def delete(self, *expressions, **filters) -> None:
        conditions = [getattr(self.model, key) == value for key, value in filters.items()]
        conditions.extend(expressions)

        stmt = (
            delete(self.model)
            .where(*conditions)
            .returning(self.model)
        )

        result = await self.session.execute(stmt)

        