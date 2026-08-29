from fastapi import Query, Body, APIRouter, HTTPException
from fastapi_cache.decorator import cache
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.api.dependencies import PaginationDep, DBDep
from datetime import date
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundHTTPException
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(json_schema_extra={"example": "2026-08-01"}),
    date_to: date = Query(json_schema_extra={"example": "2026-08-12"}),
):

    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )

    return {'status': 'OK', 'data': hotels}


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    hotel = await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK", "data": hotel}


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Deluxe", "location": "Сочи, ул. Мира, д.6"},
            },
            "2": {
                "summary": "Дубайск",
                "value": {
                    "title": "Sheih Resort",
                    "location": "Дубайск, ул. Аль-Абдаллы, д.3",
                },
            },
        }
    ),
):

    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, db: DBDep, hotel_data: HotelAdd):

    hotel = await HotelService(db).put_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    
    return {"status": "OK", "data": hotel}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление отеля",
    description="Либо один из параметров, либо оба",
)
async def patch_hotel(
    hotel_id: int,
    db: DBDep,
    hotel_data: HotelPatch,
):

    hotel = await HotelService(db).patch_hotel(hotel_data=hotel_data, hotel_id=hotel_id)

    return {"status": "OK", "data": hotel}
