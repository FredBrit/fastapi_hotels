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
    
  
    created_booking = await db.bookings.add(booking_data)
    await db.commit()
    
    print(f'Запись создана. Её ID: {created_booking.id}, Price: {created_booking.price}')
    

    updated_booking_data = booking_data.model_copy(update={"price": 200})

  
    await db.bookings.edit(updated_booking_data, exclude_unset=True, id=created_booking.id)
    await db.commit()

   
    new_booking_record = await db.bookings.get_one_or_none(id=created_booking.id)
    assert new_booking_record.price == 200
    print(f'Новый price: {new_booking_record.price}')

   
    await db.bookings.delete(id=created_booking.id)
    await db.commit()

    
    deleted_booking_record = await db.bookings.get_one_or_none(id=created_booking.id)
    assert deleted_booking_record is None
    print('Запись успешно удалена')