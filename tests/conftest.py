import pytest
import json
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool

@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope='session', autouse=True)
async def load_mock_hotels(setup_database):
    async with DBManager(session_factory = async_session_maker_null_pool) as db:
        with open("tests/mock_hotels.json") as file:
            hotels = json.load(file)

        for hotel_data in hotels:
            hotel = HotelAdd(**hotel_data)
            await db.hotels.add(hotel)

        await db.commit()

@pytest.fixture(scope='session', autouse=True)
async def load_mock_rooms(setup_database):
    async with DBManager(session_factory = async_session_maker_null_pool) as db:
        with open("tests/mock_rooms.json") as file:
            rooms = json.load(file)

        for room_data in rooms:
            room = RoomAdd(**room_data)
            await db.rooms.add(room)

        await db.commit()                 

@pytest.fixture(scope="session", autouse=True)
async def register_user(load_mock_hotels):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test_something") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )        