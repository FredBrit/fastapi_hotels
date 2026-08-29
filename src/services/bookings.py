from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.base import BaseService


class BookingService(BaseService):
    async def add_booking(self, user_id: int, booking_data: BookingAddRequest):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.dict(),
        )
        booking = await self.db.bookings.add_booking(_booking_data)
        await self.db.commit()
        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_current_user_bookings(self, user_id: int):
        return await self.db.bookings.get_all(user_id=user_id)