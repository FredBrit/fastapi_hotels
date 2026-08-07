from fastapi import Query, Body, APIRouter
from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep, DBDep
from datetime import date




router = APIRouter(prefix='/hotels', tags=['Отели'])





@router.get('')
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description='Название отеля'),
    location: str | None = Query(None, description='Адрес отеля'),
    date_from: date = Query(json_schema_extra={"example": "2026-08-01"}), 
    date_to: date = Query(json_schema_extra={"example": "2026-08-12"})  
):

    per_page = pagination.per_page or 5

    
    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
        limit=per_page or 5, 
        offset=per_page * (pagination.page - 1)
        )




@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return {'status': 'OK', 'data': hotel}        




@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep):
    hotel = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status':'OK'}


@router.post('')
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    '1': {
        'summary': 'Сочи',
        'value': {
            'title': 'Deluxe',
            'location': 'Сочи, ул. Мира, д.6'
        },
    },

    '2': {
        'summary': 'Дубайск',
        'value': {
            'title': 'Sheih Resort',
            'location': 'Дубайск, ул. Аль-Абдаллы, д.3'
        },
    },
})
):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()        
    return {'status': 'OK', 'data': hotel}

@router.put('/{hotel_id}')
async def put_hotel(
    hotel_id: int,
    db: DBDep,
    hotel_data: HotelAdd
):

    hotel = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'OK', 'data': hotel}


@router.patch(
    '/{hotel_id}',
    summary = 'Частичное обновление отеля',
    description = 'Либо один из параметров, либо оба'

)
async def patch_hotel(
    hotel_id: int,
    db: DBDep,
    hotel_data: HotelPatch,
):
    
    hotel = await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {'status': 'OK', 'data': hotel} 