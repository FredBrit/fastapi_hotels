from fastapi import Query, Body, APIRouter
from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.database import engine
from src.repos.hotels import HotelsRepository



router = APIRouter(prefix='/hotels', tags=['Отели'])





@router.get('')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description='Название отеля'),
    location: str | None = Query(None, description='Адрес отеля'),   
):

    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,  
            limit=per_page or 5, 
            offset=per_page * (pagination.page - 1)
            )
   

@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        await session.commit()
    return {'status': 'OK', 'data': hotel}        




@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status':'OK'}


@router.post('')
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        
        await session.commit()

    return {'status': 'OK', 'data': hotel}

@router.put('/{hotel_id}')
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_data, id=hotel_id)

        await session.commit()

    return {'status': 'OK', 'data': hotel}


@router.patch(
    '/{hotel_id}',
    summary = 'Частичное обновление отеля',
    description = 'Либо один из параметров, либо оба'

)
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)

        await session.commit()

    return {'status': 'OK', 'data': hotel} 