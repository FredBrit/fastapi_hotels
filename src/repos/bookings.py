from src.models.bookings import BookingsORM
from src.repos.base import BaseRepository
from src.schemas.bookings import Booking
from src.repos.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper