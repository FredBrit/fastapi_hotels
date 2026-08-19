import json
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task
from src.api.dependencies import DBDep
from src.init import redis_manager


router = APIRouter(prefix='/facilities', tags = ['Удоства'])


@router.get('')
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()
      




@router.post('')
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {'status': 'OK', 'data': facility}    