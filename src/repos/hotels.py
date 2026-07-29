from sqlalchemy import select, insert
from src.repos.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):

    model = HotelsORM
    schema = Hotel



    async def get_all1(self, title, location, limit, offset):

        query = select(HotelsORM)

        if title:
            query = query.where(HotelsORM.title.ilike(f"%{title.strip()}%"))

        if location:
            query = query.where(HotelsORM.location.ilike(f"%{location.strip()}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )        

        result = await self.session.execute(query)
        
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


        
    