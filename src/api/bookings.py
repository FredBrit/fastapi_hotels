from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_current_user_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_current_user_bookings(user_id=user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
