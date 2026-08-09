from src.repos.base import BaseRepository
from src.models.rooms import RoomsORM
from src.models.bookings import BookingsORM
from src.repos.utils import rooms_ids_for_booking
from src.repos.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.schemas.rooms import Room, RoomWithRels

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload
from src.database import engine


class RoomsRepository(BaseRepository):

    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .where(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]


    async def get_one_or_none(self, id, hotel_id):

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .where(RoomsORM.hotel_id == hotel_id, RoomsORM.id == id)
        )

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return RoomDataWithRelsMapper.map_to_domain_entity(model)