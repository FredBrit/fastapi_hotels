
from datetime import date
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    await db.bookings.add(booking_data)

    booking_record = await db.bookings.get_one_or_none(user_id=booking_data.user_id, room_id=booking_data.room_id)
    assert booking_record
    print(f'Текущий price: {booking_record.price}')
    

    updated_booking_data = booking_data.model_copy(update={"price": 200})

    await db.bookings.edit(updated_booking_data, exclude_unset=True)

    new_booking_record = await db.bookings.get_one_or_none(user_id=booking_data.user_id, room_id=booking_data.room_id)
    assert new_booking_record.price == 200
    print(f'Новый price: {new_booking_record.price}')


    await db.bookings.delete(user_id=booking_data.user_id, room_id=booking_data.room_id)
    await db.commit()

    
    deleted_booking_record = await db.bookings.get_one_or_none(user_id=booking_data.user_id, room_id=booking_data.room_id)
    assert deleted_booking_record is None
    print(f'Запись удалена')