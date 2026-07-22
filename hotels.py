from fastapi import Query, APIRouter
from schemas.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep

router = APIRouter(prefix='/hotels', tags=['Отели'])


hotels=[
    {'id': 1, 'title': 'Sochi', 'name': 'South'},
    {'id': 2, 'title': 'Дубай', 'name': 'Sheih'},
    {'id': 3, 'title': 'Moscow', 'name': 'Adulter'},
    {'id': 4, 'title': 'Spb', 'name': 'Astoria'},
    {'id': 5, 'title': 'Kazan', 'name': 'Don'},
    {'id': 6, 'title': 'Киев', 'name': 'Kazak'},
    {'id': 7, 'title': 'Чернигов', 'name': 'Rodina'},
    {'id': 8, 'title': 'Владимир', 'name': 'Royal'},
    {'id': 9, 'title': 'Ярославль', 'name': 'Polisye'},
]



@router.get('')
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description='Айдишник отеля'),
    title: str | None = Query(None, description='Название отеля'),
):

    hotels_=[]
    for hotel in hotels:
        if id and hotel['id']!=id:
            continue
        if title and hotel['title']!=title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:       
        return hotels_[pagination.per_page*(pagination.page-1):][:pagination.per_page]
    return hotels_    

@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels=[hotel for hotel in hotels if hotel['id']!=hotel_id]
    return {'status':'OK'}


@router.post('')
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append(
        {
            'id': hotels[-1]['id']+1,
            'title': hotel_data.title,
            'name': hotel_data.name,
        }
    )
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