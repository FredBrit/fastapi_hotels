from sqlalchemy import select, insert
from src.repos.base import BaseRepository
from src.repos.utils import rooms_ids_for_booking
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.schemas.hotels import Hotel

from datetime import date


class HotelsRepository(BaseRepository):

    model = HotelsORM
    schema = Hotel





    async def get_filtered_by_time(
            self,
            title: str,
            location: str,
            date_from: date,
            date_to: date,
            limit: int, 
            offset: int
    ):

        
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        query = (
            select(HotelsORM)
            .where(
                HotelsORM.id.in_(hotels_ids_to_get),
                HotelsORM.id.in_(
                    select(RoomsORM.hotel_id)
                    .where(RoomsORM.id.in_(rooms_ids_to_get))
                )
            )
            .limit(limit)
            .offset(offset)
        )

        if title:
            query = query.where(HotelsORM.title.ilike(f"%{title.strip()}%"))

        if location:
            query = query.where(HotelsORM.location.ilike(f"%{location.strip()}%"))


        result = await self.session.execute(query)


        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()] 


        
    