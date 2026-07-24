from fastapi import Query, Body, APIRouter
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.database import engine

from src.models.hotels import HotelsORM

from sqlalchemy import insert, select

router = APIRouter(prefix='/hotels', tags=['Отели'])





@router.get('')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description='Название отеля'),
    location: str | None = Query(None, description='Адрес отеля'),   
):

    per_page = pagination.per_page or 5

    async with async_session_maker() as session:

        query = select(HotelsORM)

        if title:
            query = query.where(HotelsORM.title.ilike(f"%{title.strip()}%"))

        if location:
            query = query.where(HotelsORM.location.ilike(f"%{location.strip()}%"))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )        

        result = await session.execute(query)
        
        hotels = result.scalars().all()
    
        return hotels    

@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels=[hotel for hotel in hotels if hotel['id']!=hotel_id]
    return {'status':'OK'}


@router.post('')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'OK'}

@router.put('/{hotel_id}')
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel['id']==hotel_id:
            hotel['title']=hotel_data.title
            hotel['name']=hotel_data.name
    return {'status': 'OK'}

@router.patch(
    '/{hotel_id}',
    summary = 'Частичное обновление отеля',
    description = 'Либо один из параметров, либо оба'

)
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    hotel=[hotel for hotel in hotels if hotel['id']==hotel_id][0]
    if hotel_data.title:
        hotel['title']=hotel_data.title
    if hotel_data.name:
        hotel['name']=hotel_data.name

    return {'status': 'OK', 'updated_hotel': hotel} 