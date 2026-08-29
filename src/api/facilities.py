import json
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task
from src.api.dependencies import DBDep
from src.init import redis_manager
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удоства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
