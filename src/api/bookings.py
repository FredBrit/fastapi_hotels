from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get('')
async def get_bookings(
    db: DBDep
):
    return await db.bookings.get_all()

@router.get('/me')
async def get_current_user_bookings(
    db: DBDep,
    user_id: UserIdDep
):
    return await db.bookings.get_all(user_id = user_id)



@router.post('')
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")

    room_price: int = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    try:
        booking = await db.bookings.add_booking(_booking_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await db.commit()
    return {"status": "OK", "data": booking}