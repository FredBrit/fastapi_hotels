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
        
        hotels_ids_to_get = select(HotelsORM.id.label('id'))

        if title:
            hotels_ids_to_get = hotels_ids_to_get.where(HotelsORM.title.ilike(f"%{title.strip()}%"))

        if location:
            hotels_ids_to_get = hotels_ids_to_get.where(HotelsORM.location.ilike(f"%{location.strip()}%"))

        
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        result = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .where(
                RoomsORM.id.in_(rooms_ids_to_get),
                RoomsORM.hotel_id.in_(hotels_ids_to_get)
            )
            .limit(limit)
            .offset(offset)    
        )

        return await self.get_filtered(HotelsORM.id.in_(result))    


        
    