import pytest
import json
from tests.conftest import get_db_null_pool
from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager
from sqlalchemy import select, update, text
from src.schemas.rooms import RoomAdd


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-02", "2024-08-11", 200),
        (1, "2024-08-03", "2024-08-12", 200),
        (1, "2024-08-04", "2024-08-13", 200),
        (1, "2024-08-05", "2024-08-14", 200),
        (1, "2024-08-06", "2024-08-15", 409)
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()

@pytest.fixture(scope="module")
async def reset_bookings_and_rooms():
    """Полностью очищает бронирования и восстанавливает количество мест в комнатах"""
    async with async_session_maker_null_pool() as session:
        # 1. Очищаем таблицу бронирований
        await session.execute(text("TRUNCATE TABLE bookings RESTART IDENTITY CASCADE"))
        await session.execute(text("TRUNCATE TABLE rooms RESTART IDENTITY CASCADE"))
        await session.commit() 

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        with open("tests/mock_rooms.json") as file_rooms:
            rooms = json.load(file_rooms)   

        for room_data in rooms:
            room = RoomAdd(**room_data)
            await db_.rooms.add(room) 

        await db_.commit()        


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-02", "2024-08-11", 2),
        (1, "2024-08-03", "2024-08-12", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    reset_bookings_and_rooms,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booked_rooms
