import pytest
import json
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.api.dependencies import get_db
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


@pytest.fixture(scope='function')
async def db() -> DBManager:
    async with DBManager(session_factory = async_session_maker_null_pool) as db:
        yield db



async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory = async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool        


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    async with DBManager(session_factory = async_session_maker_null_pool) as db_:
        with open("tests/mock_hotels.json") as file_hotels:
            hotels = json.load(file_hotels)

        with open("tests/mock_rooms.json") as file_rooms:
            rooms = json.load(file_rooms)    

        for hotel_data in hotels:
            hotel = HotelAdd(**hotel_data)
            await db_.hotels.add(hotel)

        for room_data in rooms:
            room = RoomAdd(**room_data)
            await db_.rooms.add(room)
    

        await db_.commit()  


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport = ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )