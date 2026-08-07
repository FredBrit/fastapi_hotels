from src.repos.base import BaseRepository
from src.models.rooms import RoomsORM
from src.models.bookings import BookingsORM
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import Room

from sqlalchemy import select, func
from src.database import engine


class RoomsRepository(BaseRepository):

    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(self, date_from, date_to):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))