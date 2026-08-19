from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.schemas.facilities import FacilityAdd


async def test_get_hotels(ac):
    response = await ac.get(
        '/hotels',
        params = {
            'date_from': '2024-08-10',
            'date_to':  '2024-08-20'
            }
        )

    print(f'{response.json()}')
    assert response.status_code == 200



async def test_add_hotel(db):
    hotel_data = HotelAdd(title = 'Hotel 1', location = 'Сочи')
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()    
